import logging
import math
from missions.mission import Mission

SICKS_FRONT = {2, 3}
SICKS_BACK = {0, 1}

class Goto(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.position = None
        self.last_position = None
        self.last_angle = None
        self.angle = None
        self.sicks = set()
        
    def go(self, msg):
        if msg.name == 'reset goto':
            self.last_position = (0, 0)
            self.last_angle = math.pi
            self.asserv.setPos(0, 0, math.pi)

        elif msg.board == "internal" and msg.name == 'goto':
            self.position = msg.position if self.robot.color == 1 else (msg.position[0], -msg.position[1])

            assert -math.pi <= self.angle <= math.pi
            self.angle = msg.angle if self.robot.color == 1 else -msg.angle

            # calcul de la façon dont on va s'orienter pour trouver les sicks utiles
            angle = math.atan2(self.position[1] - self.last_position[1], self.position[0] - self.last_position[0])
            self.nosick = SICKS_FRONT if abs(angle - self.last_angle) < math.pi / 2 else SICKS_BACK
            try:
                self.nosick.update(msg.nosick)
            except:
                pass

            self.asserv.motion_pos(self.position[0], self.position[1])
            self.state = "going"
        
        elif msg.board == "asserv" and msg.name == 'sick':
            self.sicks.add(msg.id)
            if self.state == 'going' and self.sicks > self.nosick:
                self.asserv.block()
                self.state = "waiting"

        elif self.state == 'going' and msg.board == "asserv" and msg.name == 'done':
            self.asserv.motion_angle(self.angle)
            self.state = 'turning'

        elif self.state == 'turning' and msg.board == 'asserv' and msg.name == 'done':
            self.state = "off"
            self.create_send_internal('goto done')
                
        elif msg.board == 'asserv' and msg.name == 'freepath':
            try:
                self.sicks.remove(msg.id)
            except KeyError:
                logging.warning("Freepath on an already free sick.")
            if not self.sicks and self.state == 'waiting':
                self.asserv.motion_pos(self.position[0], self.position[1])
                self.state = "going"
                
