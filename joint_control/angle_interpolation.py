'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import *


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])
        self.sTime = -1

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE
        (names, times, keys) = keyframes
        # print names[0], times[0], keys[0]
        if(self.sTime == -1):
            self.sTime = perception.time
        time = perception.time - self.sTime
        for j, joint_name in enumerate(names):
            if joint_name not in self.joint_names:
                continue
            tJoint = times[j]
            kJoint = keys[j]
            for t in range(len(tJoint)):
                if time > tJoint[-1]:  # when time > last item in the joints
                    target_joints[joint_name] = perception.joint[joint_name]
                    continue
                if time < tJoint[t]:
                    if t == 0:
                        t0, P_0, P_1 = 0, 0, 0
                        T_3 = tJoint[0]
                        P_2 = kJoint[0][1][2]
                        P_3 = kJoint[0][0]
                        i = time / T_3
                    elif time >= tJoint[t-1]:
                        t0, T_3 = tJoint[t-1], tJoint[t]
                        P_0, P_3 = kJoint[t-1][0], kJoint[t][0]
                        P_1 = P_0 + kJoint[t-1][2][2]
                        P_2 = P_3 + kJoint[t][1][2]
                        i = (time - t0)/(T_3 - t0)
                    target_joints[joint_name] = (
                        (1-i)**3)*P_0 + 3*((1-i)**2)*i*P_1 + 3*(1-i)*(i**2)*P_2 + (i**3)*P_3
                    break
        # print target_joints
        return target_joints

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
