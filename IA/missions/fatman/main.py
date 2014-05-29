#/usr/bin/python

from missions.mission import Mission
import math

class Test(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)

    def go(self, msg):
        # look at this beautiful hack !
        if msg.board == 'asserv' and msg.name == 'blocked':
            msg.name = 'goto done'
            msg.board = 'internal'


        if msg.board == 'asserv' and msg.name == 'start':
            self.robot.color = msg.color
            self.create_timer(3, 'timer start')
            self.create_timer(92, 'funny action')
            self.state = 'waiting for start'
        elif msg.name == 'timer start' and self.state == 'waiting for start':
            self.create_send_internal('reset goto')
            self.create_send_internal('goto', position=(0.7, 0.05), angle=math.pi)
            self.state = 'sortie'
        elif self.state == 'sortie' and msg.board == 'internal' and msg.name == 'goto done':
            self.state = 'prendre premier feu'
            self.asserv.catch_arm(1 + self.robot.color)
        elif self.state == 'prendre premier feu' and msg.name == 'caught':
            self.state = 'demi tour 1'
            self.create_send_internal('goto', position=(0.95, 0.05), angle=0)
        elif self.state == 'demi tour 1' and msg.name == 'goto done':
            self.state = 'fruits 1'
            self.create_send_internal('goto', position=(1.45, 0.04), angle=0)
        elif self.state == 'fruits 1' and msg.name == 'goto done':
            self.state = 'devant deuxième feu'
            self.create_send_internal('goto', position=(1.5, 0.52), angle=math.pi)
        elif self.state == 'devant deuxième feu' and msg.name == 'goto done':
            self.state = 'prendre deuxième feu'
            self.asserv.catch_arm(1 + (1 - self.robot.color))
        elif self.state == 'prendre deuxième feu' and msg.name == 'caught':
            self.state = 'pose feux'
            self.create_send_internal('goto', position=(1.64, 0.15), angle=0.7)
        elif self.state == 'pose feux' and msg.name == 'goto done':
            self.state = 'pose feu 1'
            self.asserv.pull_arm(1 + (1 - self.robot.color))
        elif self.state == 'pose feu 1' and msg.name == 'laid':
            self.state = 'demi tour feu 2'
            self.create_send_internal('goto', position=(1.56, 0.07), angle=0.8-math.pi)
        elif self.state == 'demi tour feu 2' and msg.name == 'goto done':
            self.asserv.pull_arm(1 + self.robot.color)
            self.state = 'pose feu 2'
        elif self.state == 'pose feu 2' and msg.name == 'laid':
            self.state = 'fruits 2 avant'
            self.create_send_internal('goto', position=(1.68, 0.30), angle=math.pi/2)
        elif self.state == 'fruits 2 avant' and msg.name == 'goto done':
            self.state = 'fruits 2'
            self.create_send_internal('goto', position=(1.68, 1.135), angle=math.pi/2)
        elif self.state == 'fruits 2' and msg.name == 'goto done':
            self.state = 'prendre troisième feu'
            self.asserv.catch_arm(1 + (1 - self.robot.color))
        elif self.state == 'prendre troisième feu' and msg.name == 'caught':
            self.state = 'après troisième feu'
            self.create_send_internal('goto', position=(1.6, 1.3), angle=-math.pi/2)
        elif self.state == 'après troisième feu' and msg.name == 'goto done':
            self.state = 'avant quatrième feu'
            self.create_send_internal('goto', position=(1.68, 1.54), angle=-math.pi/2)
        elif self.state == 'avant quatrième feu' and msg.name == 'goto done':
            self.state = 'prendre quatrième feu'
            self.asserv.catch_arm(1 + self.robot.color)
        elif self.state == 'prendre quatrième feu' and msg.name == 'caught':
            self.state = 'vers foyer du milieu'
            self.create_send_internal('goto', position=(1.2, 1.53), angle=-0.8)
        elif self.state == 'vers foyer du milieu' and msg.name == 'goto done':
            self.state = 'pose feu 3'
            self.asserv.pull_arm(1 + self.robot.color)
        elif self.state == 'pose feu 3' and msg.name == 'laid':
            self.state = 'après pose feu 3'
            self.create_send_internal('goto', position=(1.4, 1.25), angle=math.pi)
        elif self.state == 'après pose feu 3' and msg.name == 'goto done':
            self.state = 'avant pose feu 4'
            self.create_send_internal('goto', position=(1.18, 1.06), angle=-2.36)
        elif self.state == 'avant pose feu 4' and msg.name == 'goto done':
            self.state = 'pose feu 4'
            self.asserv.pull_arm(1 + (1 - self.robot.color))
        elif self.state == 'pose feu 4' and msg.name == 'laid':
            self.state = 'avant fruits 3'
            self.create_send_internal('goto', position=(1.68, 1.7), angle=math.pi/2)
        elif self.state == 'avant fruits 3' and msg.name == 'goto done':
            self.state = 'fruits 3'
            self.create_send_internal('goto', position=(1.68, 2), angle=math.pi/2)
        elif self.state == 'fruits 3' and msg.name == 'goto done':
            self.state = 'mammouth ennemi'
            self.create_send_internal('goto', position=(0.25, 2), angle=math.pi)
        elif self.state == 'mammouth ennemi' and msg.name == 'goto done':
            self.state = 'convoyer'
            self.asserv.convoyer()
        elif self.state == 'convoyer' and msg.name == 'done':
            self.state = 'filet'
            self.create_send_internal('filet')

