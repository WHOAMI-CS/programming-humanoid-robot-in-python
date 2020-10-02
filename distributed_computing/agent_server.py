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
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import pickle
import numpy as np
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'kinematics'))

from inverse_kinematics import InverseKinematicsAgent
from recognize_posture import PostureRecognitionAgent


class ServerAgent(InverseKinematicsAgent):
    '''ServerAgent provides RPC service
    '''
    # YOUR CODE HERE
    def __init__(self):
        super(ServerAgent, self).__init__()
        server = SimpleXMLRPCServer(("localhost", 3000), logRequests = True, allow_none=True)
        server.register_instance(self)
        print "Started"
        thread = threading.Thread(target=server.serve_forever)
        thread.start()


    def recognize_posture(self):
        posture = 'unknown'
        perception = self.perception
        classes = ['Left', 'StandInit', 'Crouch', 'Belly', 'Sit', 'Frog', 'Right',
                   'Stand', 'Knee',
                   'Back', 'HeadBack']
        ROBOT_POSE_CLF = '../joint_control/robot_pose.pkl'
        joints = ['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'RHipYawPitch',
                  'RHipRoll', 'RHipPitch', 'RKneePitch']
        data_for_clf = [perception.joint[joint] for joint in joints]
        [data_for_clf.append(perc) for perc in perception.imu]
        data_for_clf = np.asarray(data_for_clf)
        clf2 = pickle.load(open(ROBOT_POSE_CLF))
        posture = clf2.predict([data_for_clf])
        return classes[int(posture)]

    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        print "ANGLE"
        return self.perception.joint[joint_name]
    
    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        # YOUR CODE HERE
        self.target_joints[joint_name] = angle
        return True


    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        return self.recognize_posture()


    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        # self.keyframes = keyframes
        self.sTime = -1
        target_joints = self.angle_interpolation(keyframes, self.perception)
        while (target_joints!= {}):
            self.target_joints.update(target_joints)
            target_joints = self.angle_interpolation(keyframes, self.perception)
        return True


    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        print(self.transforms[name])
        # str(self.transforms[name])

        return str(self.transforms[name])


    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        mat = np.matrix(transform.replace("[", "").replace("]", ";")[:-2])
        joint_angles = self.inverse_kinematics(effector_name, mat)
        self.target_joints.update(joint_angles)
        return True

if __name__ == '__main__':
    agent = ServerAgent()
    agent.run()

