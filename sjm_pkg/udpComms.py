#!/usr/bin/env python3
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QTextStream
from PyQt5.QtWidgets import QDialog
from PyQt5.QtNetwork import QHostAddress, QUdpSocket, QAbstractSocket

class Udp_rebroadcaster(QDialog):

    def __init__(self, broadcast_dest, dest_port, parent=None):
        super(Udp_rebroadcaster, self).__init__(parent)

        # broadcast to make available to sealog, dlog1, and RaspPIs
        self.broadcast_ip = QHostAddress()
        self.broadcast_ip.setAddress(broadcast_dest)
                                  
        self.dest_port = int(dest_port)
        print("Rebroadcasting to " + broadcast_dest + "port " + str(dest_port))

    def open_outsocks(self):
        # For Jason ops destinations are the sealog host and dlog1 host
        self.sock_broadcast = QUdpSocket()
        self.sock_broadcast.bind(self.broadcast_ip, self.dest_port)

    def send_datagram(self, out_msg):
            
        outBA = bytearray(out_msg, 'utf-8')
        
        res = self.sock_broadcast.writeDatagram(outBA, self.broadcast_ip, self.dest_port)
        if res < 0:
           print("Problem broadcasting ICL datagram")
            

            
