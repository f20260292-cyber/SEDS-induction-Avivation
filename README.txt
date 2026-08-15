TASK 1:

    First I felt like using the depth data file to create a virutal sensor. 

        I created a sensor class that behaved like a virtual sensor. It has a read_depth function that returns the current depth of the ocean beneth. 
        I made the assumtion that the depth data file has each datapoint seperated by 0.1 seconds (arbitarily). And the sensor class keeps track of 
        the time when it was intiated and at any moment in time, it will know how much time has passed and will choose to return the correct depth 
        as per the depth data file.
        The sensor handles reaching end of depth data by returning a None value
        For having a slightly more varied test, I also added the option to add extra randomness to the data with the scaling factor extra_randomFactor
        
    Next I created the SensorTest.py file to check if the virtual sensor was behaving correctly

    Task.py is the final file that exectues the Task 1

        It samples the sensor data every 100 miliseconds (0.1s was what I had chosen arbitarily as mentioned before, thats why). Any data from the
        sensor is first checked to ensure that it is a number, else that datapoint is skipped, before that it is also checked if it is None, in that
        case we know that we have reached the end of the Depth Data.csv. Outliers are also skipped (>3times the median of last data). 
        This sampled data is then recorded in RawDepth list along with a similar list recording the time of sampling. Another list called depth is
        also created which contains the noise corrected version of RawDepth. After atleast 7 datapoints are recorded, each datapoint in depth
        becomes the average its 3 neighbours RawDepth (as in +-3 from that index is averaged). And from this point, the current data is no longer the 
        RawSensor data, but rather a prediction done by looking at the previous data. (I went overboard at this part, so it is hard to explain the code
        in english, I have left comments in my code which is probaly a faster way to understand it)

        I planned on plotting everything using matplotlib and as always I asked an llm to do it -_-. I inluded features that made sense like 
        scaling based on the moving median data rather than average or max as the sensor data does contain random outliers. [it was mentioned
        that I removed the outliers previously, but this is where I implemented it]

TASK 2:

    Just implemented the features as dictated 