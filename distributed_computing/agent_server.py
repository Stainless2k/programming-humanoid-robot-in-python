'''In this file you need to implement remote procedure call (RPC) server

* There are different RPC libraries for python, such as xmlrpclib, json-rpc. You are free to choose.
* The following functions have to be implemented and exported:
 * get_angle
 * set_angle
 * get_posture
 * execute_keyframes
 * get_transform
 * set_transform
* You can test RPC server with ipython before implementing agent_client.py
'''

# add PYTHONPATH
import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'kinematics'))
sys.path.append('../')
from inverse_kinematics import InverseKinematicsAgent
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
from keyframes import *

class ServerAgent(InverseKinematicsAgent):
    '''ServerAgent provides RPC service
    '''
    # YOUR CODE HERE
    def __init__(self):
        '''starts the server'''
        print "init"
        super(ServerAgent, self).__init__()
        self.server = SimpleXMLRPCServer(("localhost", 8080), allow_none=True)
        self.server.register_instance(self)
        self.thread = threading.Thread(target = self.server.serve_forever)
        self.thread.start()
        print "init done"


    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        return self.perception.joint[joint_name]

    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        # YOUR CODE HERE
        self.perception.joint[joint_name] = angle
        print joint_name, " set to ", self.perception.joint[joint_name]

    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        return self.posture

    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        #set start time to -1 so angle_interpolation computes relative time needed for bezier
        print self.keyframes
        self.sTime == -1
        self.keyframes = keyframes
        print self.keyframes

    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        return self.transforms[name]


    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE

if __name__ == '__main__':
    agent = ServerAgent()
    agent.run()
