#!/usr/bin/env python3 

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication
import socket, signal, sys, configparser
from sjm_pkg.ICLloggerUI import Ui_MainWindow

signal.signal(signal.SIGINT, signal.SIG_DFL)

class ICLlogger(QMainWindow):
    
    def __init__(self, parent=None):
        super(ICLlogger, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.quitButton.clicked.connect(self.on_quit_button)
        self.ui.stopButton.clicked.connect(self.on_stop_button)
        self.ui.startButton.clicked.connect(self.on_start_button)
        self.ui.stopButton.setEnabled(False)
        
        # String to trigger a reading is #WT. <CR> <LF> per Hugh P.
        self.querystr = bytearray(b'#WT.')
        self.querystr.append(0x0D) # put <CR> here
        self.querystr.append(0x0A) # put <LF> here

        self.simulate = True
        self.mydl = DataLogger()
        
        self.disp_systime_timer = QTimer()
        self.disp_systime_timer.timeout.connect(self.at_disp_systime_timeout)
        self.disp_systime_timer.start(1000)        

        self.query_timer = QTimer()
        self.query_timer.timeout.connect(self.on_query_timer_timeout)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.do_init()

#        self.new_icl-record.connect(self.on_new_icl-record)

    def on_query_timer_timeout(self):
        if not self.simulate:
            self.s.sendall(self.querystr)
            msg, ancdata, flags, addr = self.s.recvmsg(64)
        else:
            nowtime = QTime()
            msg = "#WT??.+" + str(nowtime.second()) + " +" + str(nowtime.minute()) 
        preamble, self.tip_temp, self.housing_temp = msg.split('+')
        self.ui.tip_temp_label.setText(self.tip_temp)
        self.ui.housing_temp_label.setText(self.housing_temp)
        self.mydl.writeRecord(self.tip_temp + "\t" + self.housing_temp)
       
    def at_disp_systime_timeout(self):
        self.now_f = mysystimef1();
        self.ui.TimeDisplay.setText(self.now_f)

    def on_start_button(self):
        if self.initiated == False:
            self.initiated = True
            self.ui.startButton.setEnabled(False)
            self.ui.stopButton.setEnabled(True)
            self.query_timer.start(self.query_period)

            if not self.simulate:
                self.s.connect((self.moxa_ip, self.moxa_port))

            self.mydl.start_logging()
        
    def on_stop_button(self):
        if self.initiated == True:
            self.initiated = False
            self.ui.startButton.setEnabled(True)
            self.ui.stopButton.setEnabled(False)
            self.query_timer.stop()

            self.mydl.stop_logging()
        
    def on_quit_button(self):
        self.mydl.stop_logging()
        self.query_timer.stop()
        QCoreApplication.exit()

    def do_init(self):
        self.initiated = False
        incfg = configparser.ConfigParser()
        incfg.read("ICLlogger.ini")

        self.moxa_ip = incfg.get('ICL','moxa_ip')
        self.moxa_ip = bytes(self.moxa_ip, 'utf-8')
        self.moxa_port = int(incfg.get('ICL','moxa_port'))
        self.query_period = int(incfg.get('ICL','query_period'))
        
class DataLogger(QObject):

    def __init__(self):
        super(DataLogger, self).__init__()


    def start_logging(self):
        nowstr = mysystimef2()
        self.logfilename = nowstr+'.ICT'
        self.logfileh = QFile(self.logfilename)
        self.logfileh.open(QFile.WriteOnly)
        self.logstream = QTextStream(self.logfileh)

    def writeRecord(self, record2log):
        self.logstream << mysystimef1() << "\t" << record2log << "\n"

    def stop_logging(self):
        self.logfileh.close()
        
        
def mysystimef1():
    now = QDateTime.currentDateTime()
    systime = now.toString("yyyy/MM/dd hh:mm:ss")
    return systime

def mysystimef2():
    now = QDateTime.currentDateTime()
    systime = now.toString("yyyyMMddhhmmss")
    return systime

if __name__ == "__main__":

    app = QApplication(sys.argv)

    icl=ICLlogger()
    icl.show()
        
    sys.exit(app.exec_())
