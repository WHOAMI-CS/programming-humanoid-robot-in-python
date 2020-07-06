'''In this exercise you need to implement inverse kinematics for NAO's legs
* Tasks:
    1. solve inverse kinematics for NAO's legs by using analytical or numerical method.
       You may need documentation of NAO's leg:
       http://doc.aldebaran.com/2-1/family/nao_h21/joints_h21.html
       http://doc.aldebaran.com/2-1/family/nao_h21/links_h21.html
    2. use the results of inverse kinematics to control NAO's legs (in InverseKinematicsAgent.set_transforms)
       and test your inverse kinematics implementation.
'''

from forward_kinematics import ForwardKinematicsAgent
from numpy.matlib import identity
import numpy as np
from math import atan2, sqrt



class InverseKinematicsAgent(ForwardKinematicsAgent):

    def inverse_kinematics(self, effector_name, transform):
        '''solve the inverse kinematics
        :param str effector_name: name of end effector, e.g. LLeg, RLeg
        :param transform: 4x4 transform matrix
        :return: list of joint angles
        '''
        joint_angles = []

        # YOUR CODE HERE

        lambda_ = 0.001

        current_joint = {}
        for name in self.chains[effector_name]:
            current_joint[name] = self.perception.joint[name]

        target = self.from_trans(transform)

        for i in range(1000):
            self.forward_kinematics(current_joint)
            T = [0] * len(self.chains[effector_name])
            for j, name in enumerate(self.chains[effector_name]):
                T[j] = self.transforms[name]
            Te = np.array([self.from_trans(T[-1])])
            error = target - Te
            T = np.array([self.from_trans(j) for j in T[0:]])
            J = Te - T
            J_t = J.T
            J_t[-1, :] = 1
            JJT = np.dot(J, J.T)
            d_theta = lambda_ * np.dot(np.dot(J.T, np.linalg.pinv(JJT)), error.T)
            print d_theta
            for name in self.chains[effector_name]:
                current_joint[name] = current_joint[name] + np.asarray(d_theta.T)[0][1]
            if np.linalg.norm(d_theta) < lambda_:
                break
            return current_joint
        joint_angles = current_joint
        return joint_angles

    def from_trans(self, T):
        x, y, z = T[0, 3], T[1, 3], T[2, 3]
        theta_x = atan2(T[2,1], T[2, 2])
        theta_y = atan2(-T[2,0], sqrt(T[2,1]**2 + T[2, 2]**2))
        theta_z = atan2(T[1,0], T[0,0])
        return np.array([x, y, z, theta_x, theta_y, theta_z])



    def set_transforms(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        joint_angles = self.inverse_kinematics(effector_name, transform)
        self.target_joints.update(joint_angles)

if __name__ == '__main__':
    agent = InverseKinematicsAgent()
    # test inverse kinematics
    T = identity(4)
    T[-1, 1] = 0.05
    T[-1, 2] = 0.26
    agent.set_transforms('LLeg', T)
    agent.run()