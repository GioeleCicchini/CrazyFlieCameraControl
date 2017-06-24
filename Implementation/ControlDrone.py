import cflib
from cflib.crazyflie import Crazyflie
from PID import PID
import math



Pr = 0.1
Ir = 0.02
Dr = 4

Pp = 0.005
Ip = 0.01
Dp = 5

Pt = 1
It = 0
Dt = 6


setPointY = 240
setPointX = 320


class ControlDrone:

#link_uri nel costruttore
    def __init__(self,link_uri):
        """ Initialize and run the example with the specified link_uri """


        self._cf = Crazyflie()

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)
        self._cf.open_link(link_uri)
        print('Connecting to %s' % link_uri)


        self.heading = 0

        self.PIDRoll = PID()
        self.PIDPitch = PID()
        self.PIDTrottle = PID()



        self.PIDRoll.setKp(Pr)
        self.PIDPitch.setKp(Pp)
        self.PIDTrottle.setKp(Pt)
        self.PIDRoll.setKd(Dr)
        self.PIDPitch.setKd(Dp)
        self.PIDTrottle.setKd(Dt)
        self.PIDRoll.setKi(Ir)
        self.PIDPitch.setKi(Ip)
        self.PIDTrottle.setKi(It)


        self.PIDRoll.setPoint(setPointX)
        self.PIDPitch.setPoint(setPointY)






    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""

        # Start a separate thread to do the motor test.
        # Do not hijack the calling thread!

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)

    def _inizialize_drone(self):
        self._cf.commander.send_setpoint(0, 0, 0, 0)

    def _control_drone(self, PositionX,PositionY):

        errorPitch = self.PIDPitch.update(PositionY)
        errorRoll = self.PIDRoll.update(PositionX)

        desiredRoll = errorRoll * math.cos((self.heading * math.pi) / 180) + errorPitch * math.sin((self.heading * math.pi) / 180) * (1 / 9.81)
        desiredPitch = errorPitch * math.cos((self.heading * math.pi) / 180) + errorRoll * math.sin((self.heading * math.pi) / 180) * (1 / 9.81);


        print (desiredRoll,desiredPitch)
        self._cf.commander.send_setpoint(desiredRoll,-desiredPitch,0,43000)
        return desiredRoll,desiredPitch




    def _cut_motor(self):
        self._cf.commander.send_setpoint(0, 0, 0, 0)