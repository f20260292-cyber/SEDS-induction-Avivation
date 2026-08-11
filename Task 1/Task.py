
from math import inf

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import MaxNLocator
import statistics

from DepthSensor import DepthSensor  
import time


class RealTimeDepthPlotter:
    def __init__(self):
        # Initialize empty lists to store incoming real-time data
        self.times = []
        self.depths = []
        self.RawDepths = []
        
        # Set up the figure and axis
        self.fig, self.ax = plt.subplots()
        
        # Initialize an empty line plot object that we will update dynamically
        self.line, = self.ax.plot([], [], marker='.', color='b')
        
        # Style the plot basics
        self.ax.set_title("Real-Time Depth vs Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Depth (m)")
        
        # Clean up labels dynamically using our MaxNLocator
        self.ax.yaxis.set_major_locator(MaxNLocator(nbins=5, integer=True))
        # Optional: Invert y-axis for realistic depth visualization
        self.ax.invert_yaxis()
        self.y_upperBound = -inf

        self.Sensor = DepthSensor(extra_RandomFactor=0)  # Initialize the depth sensor to read real-time data
        self.start_time = time.time()  # Record the start time for elapsed time calculations

        #For adaptive denoising
        self.OldPredictedD = []
        self.currentVel = 0

        #DEBUG
        self.accumulatedError = 0

    def get_new_data(self):
        # (x,y) = (time elapsed since start, depth reading from sensor)
        return (time.time() - self.start_time, self.Sensor.read_depth())

    def update_graph(self, frame):
        """Main Update Loop"""
        # 1. Fetch new data point
        t, d = self.get_new_data()

        if d is None:
            print("Reached end of sample data.")
            print(f'DEBUG: Total error was {self.accumulatedError}')
            try:
                return self.line
            except:
                return
                
                
        #Handling invalid Sensor output
        try:
            d = float(d)  # Convert depth to float for plotting
        except (TypeError, ValueError):
            print("Invalid depth reading received:", d)
            return self.line,  # If depth is None or invalid, skip updating

        
        if d > self.y_upperBound and d < 0:
            self.times.append(t)
            self.RawDepths.append(d)  # Store raw depth reading
            #Apply Adaptive Denoising 
            PredictedD = self.AdaptiveDenoising()
            self.depths.append(PredictedD)  # Store depth reading for plotting
            
        else: print(f"Depth reading {d} is out of expected bounds. Skipping this point.")

        
        
        # 2. Update the line data without re-drawing the whole canvas
        self.line.set_data(self.times, self.depths)
        
        # 3. Dynamically adjust x and y axis limits to fit the growing data
        self.ax.set_xlim(max(0, t-30), t+1)

        self.y_upperBound = statistics.median(self.depths[-50:])*3  # Use last 50 points for median
        self.ax.set_ylim(0, self.y_upperBound)  # Adjust y-axis limit based on median depth
            

        # Recompute limits for data bounds cleanly
        self.ax.relim()
        self.ax.autoscale_view(scalex=False, scaley=True) # Lock X, auto-scale Y

        
        
        return self.line,

    def AdaptiveDenoising(self):
        """Applies a simple moving average filter to the depth data for noise reduction."""

        if len(self.RawDepths) < 7:
            return self.RawDepths[-1]  # Not enough data to apply filter, return last depth

        
        self.depths[-4] = (self.RawDepths[-2] + self.RawDepths[-3] + self.RawDepths[-4] + self.RawDepths[-5] + self.RawDepths[-6]) / 5  # Simple moving average of last 5 points
        # The rest of the program assumes this moving average to be the true value of depth at that point, the rawdata is just an estimate 

        if len(self.OldPredictedD) == 4:
            prevErrors = self.OldPredictedD[-4] - self.depths[-4]
            self.accumulatedError += prevErrors
            self.OldPredictedD.pop(0) #Remembering the predicted error for the last 4 values; poping the oldest one after use
        else:
            prevErrors = 0

        delta_D = (self.RawDepths[-4] - self.RawDepths[-5])
        delta_T_old = (self.times[-4] - self.times[-5])
        delta_T_new = (self.times[-1] - self.times[-4])
        self.currentVel = self.currentVel*0.9 + (delta_D / delta_T_new)*0.1
        PredictedD = self.currentVel * delta_T_old + self.depths[-4]  # Simple linear prediction based on last two points

        self.OldPredictedD.append(PredictedD)

        
        
        return PredictedD - prevErrors

    def start(self):
        """Starts the animation loop."""
        # interval=500 -> graph updates every 500 ms
        # blit=True optimizes rendering performance drastically
        self.ani = FuncAnimation(self.fig, self.update_graph, interval=100, blit=False)
        plt.show()

# To run the live plot:
if __name__ == "__main__":
    plotter = RealTimeDepthPlotter()
    plotter.start()
