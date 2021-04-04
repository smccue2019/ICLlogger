#!/usr/bin/env python3

from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QTextStream
from PyQt5.QtWidgets import QDialog
from PyQt5.QtNetwork import QHostAddress, QTcpSocket, QAbstractSocket
import sys,re, threading

class Moxacomms(QDialog):

    new_icl_record = pyqtSignal(str, name = 'new_icl_record')
    lost_moxa_comms = pyqtSignal(str, name = 'lost_moxa_comms')

    def __init__(self, moxa_ip, moxa_port, parent=None):
        super(Moxacomms, self).__init__(parent)

        #print("Moxa IP: " + moxa_ip + " Moxa port: " + str(moxa_port))
        self.moxa_ip = QHostAddress()
        self.moxa_ip.setAddress(str(moxa_ip))
        self.moxa_port = int(moxa_port)

    def open_comms(self):

        self.sock = QTcpSocket()
        self.sock.error.connect(self.on_tcp_error)
        self.sock.readyRead.connect(self.__receive)

        try:
            self.sock.connectToHost(self.moxa_ip, self.moxa_port)
            if not self.sock.waitForConnected(1000):
                print("Error Communicating with moxa at" + self.moxa_ip + ":" + self.moxa_port)
        except:
            print(self.sock.SocketError())

    def close_comms(self):
        self.sock.close()
        
    def transmit_msg(self, msg):
        out_msg = bytearray()

        self.cr = 0x0d
        self.nl = 0x0a
        out_msg.extend(msg)
        #out_msg.append(0x0d)
        out_msg.append(0x0a)
        #print("Send:" + str(out_msg))

        self.sock.write(out_msg)
        self.sock.flush()

        QTimer.singleShot(500, self.check_response)

    def check_response(self):
        if self.sock.bytesAvailable() > 0:
            self.__receive()
        
    def __receive(self):

        # Initially written to respond to a readyRead, but expanded in
        # order to test whether the ICL records are too small.
        instream = QTextStream(self.sock)
        iclpkt = ()

        iclpkt = instream.readAll() 
        print(iclpkt)
        self.new_icl_record.emit(iclpkt)

    def on_tcp_error(self, connect_error):

        if connect_error == QAbstractSocket.RemoteHostClosedError:
            print("ERROR: Remote host closed")
            self.lost_moxa_comms.emit("Remote host closed")
        elif connect_error == QAbstractSocket.HostNotFoundError:
            print("ERROR: Host was not found")
            self.lost_moxa_comms.emit("Remote host not found")
        elif connect_error == QAbstractSocket.ConnectionRefusedError:
            print("ERROR: The connection was refused by the peer")
            self.lost_moxa_comms.emit("Connection refused")
        else:
            print("The following error occurred: %l" % self.sock.errorString())
