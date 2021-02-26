#!/usr/bin/env python3

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtNetwork
import sys,re, threading

class UDPcomms(QDialog):

    new_icl_record = pyqtSignal(str, str, name = 'new_icl_record')

    def __init__(self, listen_port, parent=None):
        super(UDPreceiver, self).__init__(parent)

        self.ListenPort = listen_port

        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.udpSocket.bind(QtNetwork.QHostAddress.Any, self.ListenPort)
        self.udpSocket.readyRead.connect(self.processPendingDatagrams)

    def transmit_msg(self, msg):
        out_msg = bytearray()

        self.cr = 0x0d
        self.nl = 0x0a
        buffer="%s" % (msg)
        out_msg.append(0x0d)
        out_msg.append(0x0a)

        self.udpSocket(out_msg)

        
    def processPendingDatagrams(self):
        while self.udpSocket.hasPendingDatagrams():
            udp_bytearr, host, port = \
               self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())

            udpstr = udp_bytearr.decode("utf-8")
            #print(udpstr)
            u = datagram2packetID(udpstr)
            id_string = u.identify_datagram()
            if id_string == 'ICL':
                self.parse_icl(udpstr)
            else:
                # Other packets don't matter
                pass

    def parse_icl(self,iclpkt):
        iclpkt.rstrip('\n')
        (preamble, tip_temp, housing_temp) = iclpkt.split(" ")
        self.new_icl_record.emit(tip_temp, housing_temp)
        #        return (date, time, tens, cable_out, payrate)
        return

class datagram2packetID():

    def __init__(self, datagram):

        self.datagram = datagram
        self.ire = re.compile('^#W??T')

    def identify_datagram(self):

        if (self.ire.match(self.datagram)):
            return('ICL')
        else:
            return None
