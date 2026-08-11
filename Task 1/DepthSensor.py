import time
import random
import matplotlib

class DepthSensor:
    def __init__(self, extra_RandomFactor = 0):  #extra_randomfactor [0,1] was to verify how effective the denoising was
        self.depth = 0.0
        self.DEPTHS = []
        with open("SEDS Induction/Avionics/Task 1/Depth Data.csv", "r") as file:
            for line in file:
                if line.split(',')[0] == 'Point': continue
                self.DEPTHS.append(str(line.split(',')[1]))
        self.time = time.time()
        self.randomFactor = extra_RandomFactor

    def read_depth(self, delta_T = 0.1):  #Assuming each datapoint is 0.1 seconds apart, this function will read the next depth value from the list every time it is called. 
        TimeElapsed = time.time() - self.time #Time elapsed since class definition in SECONDS

        if TimeElapsed/delta_T >= len(self.DEPTHS): #End of Sample Data
            return None 
        #Mapping of point to Time
        PointIndex = int(TimeElapsed/delta_T) #Index of the point in the list of depths
        try: 
            return str (float(self.DEPTHS[PointIndex]) * (1 + ( (random.random()-0.5) * self.randomFactor) )) # addes randomness if random factor is greater than 0
        except: return self.DEPTHS[PointIndex]

    #DEBUGGING FUNCTION
    def GraphDepths(self):
        import matplotlib.pyplot as plt
        
        plt.plot(self.DEPTHS, marker='o', linestyle='-', color='b')
        plt.title("Depth vs Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Depth (m)")

        # DYNAMIC SCALING: Automatically calculates ideal, round-number steps 
        # and caps the total number of y-axis labels to a maximum of 6.
        from matplotlib.ticker import MaxNLocator
        plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
        
        plt.show()
