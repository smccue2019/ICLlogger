#!/usr/bin/env python3

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtNetwork
import sys,re, threading

class UDPreceiver(QDialog):

    new_winch = pyqtSignal(str, str, str, name = 'new_winch')

    def __init__(self, listen_port, parent=None):
        super(UDPreceiver, self).__init__(parent)

        self.ListenPort = listen_port

        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.udpSocket.bind(QtNetwork.QHostAddress.Any, self.ListenPort)
        self.udpSocket.readyRead.connect(self.processPendingDatagrams)

    def processPendingDatagrams(self):
        while self.udpSocket.hasPendingDatagrams():
            udp_bytearr, host, port = \
               self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())

            udpstr = udp_bytearr.decode("utf-8")
            #print(udpstr)
            u = datagram2packetID(udpstr)
            id_string = u.identify_datagram()
            if id_string == 'WINCH':
                self.parse_winch(udpstr)
            else:
                # Other packets don't matter
                pass

    def parse_winch(self,winchpkt):
        winchpkt.rstrip('\n')
        (date,time,id,tens,blank1,payout1,blank2,payrate,blank3,payout2) = winchpkt.split(",")
        cable_out = payout1
        self.new_winch.emit(tens, cable_out, payrate)
        return (date, time, tens, cable_out, payrate)


class datagram2packetID():

    def __init__(self, datagram):

        self.datagram = datagram
        # Terrible criterion- just have something in place for now.
        # Do something better if we ever use this beyond AT42-19
        self.wre = re.compile('^2019')

    def identify_datagram(self):

        if (self.datagram):
            return('WINCH')
        else:
            return None
