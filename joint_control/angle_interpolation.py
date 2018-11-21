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
        #print(perception.time)
        # need relative time instead of

        if self.sTime == -1:
            self.sTime = perception.time

        rTime = perception.time - self.sTime

        names, times, keys = keyframes

        for n in range(len(names)):

            name = names[n]
            time = times[n]
            key = keys[n]

            #why is there a non joint name in there (LHAND)????
            if name not in self.joint_names:
                continue

            for j in range(len(time) - 1):
                #check if were before the first Keyframe
                if rTime < time[0]:
                    #print('first frame')
                    #p0 is current angle (or maybe 0??) because we dont have a keyframe yet
                    p0 = perception.joint[name]
                    # no frame no biezier point
                    p1 = p0
                    p3 = key[0][0]
                    p2 = p3 + (key[j][2][1] * key[j][2][2])
                    #normalize time, because berzier just takes i[0,1]
                    i = (rTime - 0.0) / (time[1] - 0.0)
                #check between wich frames current time is (maybe do this before hand instead of abusing a for loop but len(time) < 10 usually)
                elif time[j] < rTime < time[j+1]:
                    #print('some frame')
                    p0 = key[j][0]
                    p1 = p0 + (key[j][2][1] * key[j][2][2])
                    p3 = key[j + 1][0]
                    p2 = p3 + (key[j+1][1][1] * key[j+1][1][2])
                    #normalize time, because berzier just takes i[0,1]
                    i = (rTime - time[j]) / (time[j+1] - time[j])
                #do nothing if we have no keyframes left
                else:
                    #print('no frame')
                    continue
                    
                #biezier formular from wikipedia
                #p0 first point: angle from keyframe
                #p1 second bezier handle from first point: p0 + offset (offset=dAngle*dTime of said handle)
                #p2 second point: angle from next keyframe
                #p3 first bezier point of second point: p3 + offset
                target_joints[name] = (1 - i) ** 3 * p0 + 3 * (1 - i) ** 2 * i * p1 + 3 * (1 - i) * i ** 2 * p2 + i ** 3 * p3

        return target_joints

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
