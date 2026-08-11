from DepthSensor import DepthSensor

def PrintRealTimeDepths():
    Sensor = DepthSensor()
    while 1:
        depth = Sensor.read_depth()
        if depth is None:
            break
        print(depth)
# PrintRealTimeDepths()
Sensor = DepthSensor()
Sensor.GraphDepths()