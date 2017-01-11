#!/usr/bin/env python
# Import required Python code.
import rospy
import json
import actionlib
from std_msgs.msg import *

# Node example class.
class MasterNode():
    # Must have __init__(self) function for a class, similar to a C++ class constructor.
    def __init__(self):
        self.trip_is_finished = False
        self.no_failure = True
        dataloaderListener()
    def callbackDataLoader(self,data):
        dataParsed = json.loads(data)
        tripid = dataParsed.id
        startLocation = dataParsed.start #z = floornumber, x, y
        endLocation = dataParsed.dest#x,y,floor,rotation(float)
        while self.no_failure and not self.trip_is_finished:
            no_failure = move_coordinator_client([endLocation.x,endLocation.y,endLocation.z,0])
            next_trip = json.loads(nextTripClient())
            lastLocation = endLocation
            endLocation = next_trip.dest
            if lastLocation==endLocation:#might fail if does not evaluate correctly
                trip_is_finished = True

    def dataloaderListener():
        #init
        rospy.Subscriber('initialization', String, callbackDataLoader)

    def move_coordinator_client(goal):
        # Creates the SimpleActionClient, passing the type of the action
        # (moveCoordinatorAction) to the constructor.
        client = actionlib.SimpleActionClient('movement_coordinator_server',Float32MultiArray)
        # Waits until the action server has started up and started
        # listening for goals.
        client.wait_for_server()
        # Sends the goal to the action server.
        client.send_goal(goal)
        # Waits for the server to finish performing the action.
        client.wait_for_result()

        return client.get_result().no_error

    def nextTripClient():
        rospy.wait_for_service('complete_trip')
        try:
            complete_trip = rospy.ServiceProxy('complete_trip', CompleteTrip)
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        return complete_trip

# Main function.
if __name__ == '__main__':
    m_node = MasterNode()
    try:

    except Exception as e:
        raise
