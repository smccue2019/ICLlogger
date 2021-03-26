#!/usr/bin/env python3 

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication
import socket, signal, sys, configparser
from sjm_pkg.ICLloggerUI import Ui_MainWindow
from sjm_pkg.moxaComms import Moxacomms

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
        #self.querystr.append(0x0D) # put <CR> here
        #self.querystr.append(0x0A) # put <LF> here

        print(str(self.querystr))
        self.simulate = False   # Normal operation is False.
        #self.mydl = DataLogger()
        
        self.disp_systime_timer = QTimer()
        self.disp_systime_timer.timeout.connect(self.at_disp_systime_timeout)
        self.disp_systime_timer.start(1000)        

        self.query_timer = QTimer()
        self.query_timer.timeout.connect(self.on_query_timer_timeout)

        self.last_good_response_timer = QTimer()  # increment counter per 1 sec
        self.last_good_response_timer.timeout.connect(self.on_good_response_timeout)
        self.do_init()
        self.s = Moxacomms(self.moxa_ip, self.moxa_port)
        self.s.new_icl_record.connect(self.on_new_icl_record)
        self.s.lost_moxa_comms.connect(self.on_comms_lost)
        
        self.mydl = DataLogger()

    def on_query_timer_timeout(self):
        if not self.simulate:
            self.s.transmit_msg(self.querystr)
            self.query_counter += 1
            self.ui.query_count_lbl.setText(str(self.query_counter))
        else:
            nowtime = QTime()
            msg = "#WT??.+" + str(nowtime.second()) + " +" + str(nowtime.minute()) 

    def on_new_icl_record(self, msg):
        #print(msg)
        self.ui.response_display.setText(msg)
        preamble, self.tip_temp, self.housing_temp = msg.split('+')

        try:
            test = num(self.tip_temp)
            tip_is_ok = True
        except ValueError:
            self.tip_temp = "---"

        try:
            test = num(self.housing_temp)
            housing_is_ok = True
        except ValueError:
            self.housing_temp = "---"

        if housing_is_ok and tip_is_ok:
            self.last_good_response_timer.stop()
            self.last_good_response_timer.start(1000)
            self.good_response_seconds = 0
            
        self.ui.tip_temp_label.setText(self.tip_temp)
        self.ui.housing_temp_label.setText(self.housing_temp)
        self.mydl.writeRecord(self.tip_temp + "\t" + self.housing_temp)
       
    def on_comms_lost(self, comm_msg):
        self.ui.query_count_lbl.setStyleSheet("QLabel {background: rgb(100, 0, 0)}")
        self.ui.comms_status.setText(comm_msg)
        self.on_stop_button()

    def at_disp_systime_timeout(self):
        self.now_f = mysystimef1();
        self.ui.TimeDisplay.setText(self.now_f)

    def on_good_response_timeout(self):
        # Count the seconds since last good responses from probes
        self.good_response_seconds += 1
        self.last_good_response_timer.start(1000)
        disp_str=("Last: " + str(self.good_response_seconds))
        self.ui.last_good_duration.setText(disp_str)
                
    def on_start_button(self):
        if self.initiated == False:
            self.initiated = True
            self.query_counter=0
            self.ui.startButton.setEnabled(False)
            self.ui.stopButton.setEnabled(True)
            self.query_timer.start(self.query_period)
            self.ui.query_count_lbl.setStyleSheet("QLabel {background: rgb(0, 155, 0)}")

            if not self.simulate:
                self.s.open_comms()

            self.mydl.start_logging()
        
    def on_stop_button(self):
        if self.initiated == True:
            self.initiated = False
            self.ui.startButton.setEnabled(True)
            self.ui.stopButton.setEnabled(False)
            self.query_timer.stop()

            self.mydl.stop_logging()
            self.ui.query_count_lbl.setStyleSheet("QLabel {background: rgb(255, 255, 255)}")
            
    def on_quit_button(self):
        self.mydl.stop_logging()
        self.query_timer.stop()
        QCoreApplication.exit()
        
    def do_init(self):
        self.initiated = False
        self.good_response_seconds = 0
        
        incfg = configparser.ConfigParser()
        incfg.read("ICLlogger.ini")

        self.moxa_ip = incfg.get('ICL','moxa_ip')
        #self.moxa_ip = bytes(self.moxa_ip, 'utf-8')
        self.moxa_port = int(incfg.get('ICL','moxa_port'))
        self.query_period = int(incfg.get('ICL','query_period'))
        
class DataLogger(QObject):

    def __init__(self):
        super(DataLogger, self).__init__()
        self.logfileh_does_exist = False

    def start_logging(self):
        nowstr = mysystimef2()
        self.logfilename = nowstr+'.ICT'
        self.logfileh = QFile(self.logfilename)
        self.logfileh.open(QFile.WriteOnly)
        self.logfileh_does_exist = True
        self.logstream = QTextStream(self.logfileh)
        self.logstream << "Date Time\tTip degC\tHousing degC\n"
        
    def writeRecord(self, record2log):
        self.logstream << mysystimef1() << "\t" << record2log << "\n"

    def stop_logging(self):
        if self.logfileh_does_exist:
            self.logfileh.close()
        
def mysystimef1():
    now = QDateTime.currentDateTime()
    systime = now.toString("yyyy/MM/dd hh:mm:ss")
    return systime

def mysystimef2():
    now = QDateTime.currentDateTime()
    systime = now.toString("yyyyMMddhhmmss")
    return systime

def num(s):
    try:
        return int(s)
    except ValueError as e:
        return float(s)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    icl=ICLlogger()
    icl.show()
        
    sys.exit(app.exec_())
