#/usr/bin/python

from missions.mission import Mission
import logging
from math import pi
from mathutils.types import Vertex
from mathutils.geometry import angle

class Baroud(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.pos = 0
        self.moumouth = Vertex(0.73, 1)
        
    def go(self, msg):
        if (self.state == 'off' and msg.board == 'internal' and msg.name == 'beginBaroud'):
            self.state = 'on'
            if Mission.data['color'] == 'rouge':
                self.moumouth = Vertex(-0.73, 1) 
            self.create_send_internal('forward', target=0.735, axe='y')

        elif (self.state == 'on' and msg.board == 'internal' and msg.name == 'forward_done'):
            self.asserv.getPos()
            
        elif (self.state == 'on' and msg.board == 'asserv' and msg.name == 'pos'):
            self.state = 'allyourbasearebelongtous'
            self.pos = Vertex(msg.x, msg.y)
            angle_tir = pi/2 - angle(self.pos, self.moumouth)
            self.create_send_internal('turn', target=angle_tir)
        
        elif (self.state == 'allyourbasearebelongtous' and msg.board == 'internal' and msg.name == 'turn_done'):
            self.asserv.launchBalls(0)
            
        elif (self.state == 'allyourbasearebelongtous' and msg.board == 'asserv' and msg.name == 'doneLaunch'):
            self.asserv.stop()
            self.asserv.stopLaunch()
            self.state = 'off'
            self.create_send_internal('endBaroud')