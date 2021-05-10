#!/usr/bin/env python3
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QTextStream
from PyQt5.QtWidgets import QDialog
from PyQt5.QtNetwork import QHostAddress, QUdpSocket, QAbstractSocket

class Udp_rebroadcaster(QDialog):

    def __init__(self, broadcast_dest, dest_port1, dest_port2=None, parent=None):
        super(Udp_rebroadcaster, self).__init__(parent)

        # broadcast to make available to sealog, dlog1, and RaspPIs
        self.broadcast_ip = QHostAddress()
        self.broadcast_ip.setAddress(broadcast_dest)
        self.dest_port1 = int(dest_port1)
        
        if dest_port2 is None:
            self.dest_count=1
            print("Rebroadcasting to " + broadcast_dest + "port " + str(dest_port1))
        else:
            self.dest_count=2
            self.dest_port2 = int(dest_port2)
            print("Rebroadcasting to " + broadcast_dest + "port " + str(dest_port1))
            print("Rebroadcasting to " + broadcast_dest + "port " + str(dest_port2))

    def open_outsocks(self):
        # For Jason ops destination is full broadcast to make available
        # to sealog host, dlog1, and RaspPi metadata displays.

        self.sock_b1 = QUdpSocket()
        self.sock_b1.bind(self.broadcast_ip, self.dest_port1)
        
        if self.dest_count == 2:
            self.sock_b2 = QUdpSocket()
            self.sock_b2.bind(self.broadcast_ip, self.dest_port2)
            
    def send_datagram(self, out_msg):
            
        outBA = bytearray(out_msg, 'utf-8')
        
        print("Sending msg " + outBA.decode('utf-8') + " to " + self.broadcast_ip.toString() + " port " + str(self.dest_port1))
        
        res1 = self.sock_b1.writeDatagram(outBA, self.broadcast_ip, self.dest_port1)
        if res1 < 0:
           print("Problem broadcasting ICL datagram to " + str(self.dest_port1))
            
        if self.dest_count == 2:
            print("Sending msg " + outBA.decode('utf-8') + " to " + self.broadcast_ip.toString() + " port " + str(self.dest_port2))
        
            res2 = self.sock_b2.writeDatagram(outBA, self.broadcast_ip, self.dest_port2)
