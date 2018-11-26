'''In this exercise you need to use the learned classifier to recognize current posture of robot

* Tasks:
    1. load learned classifier in `PostureRecognitionAgent.__init__`
    2. recognize current posture in `PostureRecognitionAgent.recognize_posture`

* Hints:
    Let the robot execute different keyframes, and recognize these postures.

'''


from angle_interpolation import AngleInterpolationAgent
from keyframes import hello
import pickle as p
import numpy as np

class PostureRecognitionAgent(AngleInterpolationAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(PostureRecognitionAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.posture = 'unknown'
        self.posture_classifier = p.load(open("robot_pose.pkl"))  # LOAD YOUR CLASSIFIER

    def think(self, perception):
        self.posture = self.recognize_posture(perception)
        return super(PostureRecognitionAgent, self).think(perception)

    def recognize_posture(self, perception):
        posture = 'unknown'
        curr = []
        # YOUR CODE HERE

        curr.append(perception.joint['LHipYawPitch'])
        curr.append(perception.joint['LHipRoll'])
        curr.append(perception.joint['LHipPitch'])
        curr.append(perception.joint['LKneePitch'])
        curr.append(perception.joint['RHipYawPitch'])
        curr.append(perception.joint['RHipRoll'])
        curr.append(perception.joint['RHipPitch'])
        curr.append(perception.joint['RKneePitch'])
        curr.append(perception.imu[0])
        curr.append(perception.imu[1])

        predict = self.posture_classifier.predict(np.array(curr).reshape(1, -1))

        poses = {
        0: 'Back',
        1: 'Belly',
        2: 'Crouch',
        3: 'Frog',
        4: 'HeadBack',
        5: 'Knee',
        6: 'Left',
        7: 'Right',
        8: 'Sit',
        9: 'Stand',
        10: 'StandInit'
        }

        posture = poses[predict[0]]

        return posture

if __name__ == '__main__':
    agent = PostureRecognitionAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
