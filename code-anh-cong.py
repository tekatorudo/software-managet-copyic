import sys
from PyQt5.QtCore import *
import serial
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
import cv2
import ctypes
import subprocess
import pysftp
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol
import time
import os
from datetime import datetime
from pathlib import Path
from threading import Thread

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("createacc.ui", self)
        self.Scan.clicked.connect(self.ScanSN)
        self.ScanQR.clicked.connect(self.Scan_QR)
        self.Send.clicked.connect(self.ErorCode)
        self.SN.setText('')
        self.Error.setCurrentIndex(0)
        dataCOM = open('SetCOM.txt', 'r').read().split()
        try:
            self.pump = serial.Serial(port=dataCOM[5], baudrate=9600, timeout=50)
        except:
            Mbox('Warning', 'Không thể kết nối cổng COM!', 0)

    def ScanSN(self):
        self.SN.setText('')
        self.Error.setCurrentIndex(0)
        data1 = open('SetCamera.txt', 'r').read()
        a = data1.find('CameraLED')
        b = a + 11
        c = b - 1
        data3 = (data1[c:b])
        data3 = int(data3)
        cap = cv2.VideoCapture(data3, cv2.CAP_DSHOW)
        while True:
            _, img = cap.read()
            barcodeData = None
            barcode = pyzbar.decode(img, symbols=[ZBarSymbol.QRCODE])
            for barcode in barcode:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(img, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 3)
            cv2.imshow('Camera', img)
            cv2.waitKey(1)

            if barcodeData != None:
                barcodeData = (str(barcodeData)).split('.')
                sn = barcodeData[1]
                self.SN.setAlignment(Qt.AlignCenter)
                self.SN.setStyleSheet(
                    'font: 12pt "MS Shell Dlg 2 Bold";color:rgb(0, 0,0)')
                FB = self.SendSFC(sn.ljust(35) + 'END')
                if FB.find('PASS') != -1:
                    self.status.setText("Testing")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 255, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                    self.SN.setText(sn)
                    Thread(target=self.showtime).start()
                else:
                    Thread(target=self.showtime).start()
                    self.status.setText("Sai luu trinh")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                break
        cv2.destroyAllWindows()


    def Scan_QR(self):
        data1 = open('SetCamera.txt', 'r').read()
        a = data1.find('CameraLED')
        b = a + 11
        c = b - 1
        data3 = (data1[c:b])
        data3 = int(data3)
        cap = cv2.VideoCapture(data3, cv2.CAP_DSHOW)
        while True:
            _, img = cap.read()
            barcodeData = None
            barcode = pyzbar.decode(img, symbols=[ZBarSymbol.QRCODE])
            for barcode in barcode:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(img, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 3)
            cv2.imshow('Camera', img)
            cv2.waitKey(1)

            if barcodeData != None:
                Mbox('QR', str(barcodeData), 0)
                break
        cv2.destroyAllWindows()

    def SendSFC(self, data):
        data += '\r\n'
        self.pump.write(data.encode())
        respose = (self.pump.readline().decode())
        return respose
    def showtime(self):
        for i in range(0, 5000):
            app.processEvents()
            self.timetest.display(i)
            time.sleep(1)
            if self.status.text() != 'Testing':
                break
            if i > 1200:
                self.status.setText("Qua Thoi Gian")
                self.status.setAlignment(Qt.AlignCenter)
                self.status.setStyleSheet(
                    'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                self.save_log_fail()
                break

    def TimeToSystem(self, idataTime={}):
        iurl = "https://10.228.110.91/e-alt-api/v1/test/testtimetracking/post"
        cmd = 'testtimetosystem.exe "' + str(idataTime) + '" "' + iurl + '"'
        buffer = ''
        pp = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, creationflags=0x08000000)
        for line in iter(pp.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            buffer += res
            print(res)
            if not line:
                break
        pp.stdout.close()
        pp.wait()
    def save_log_pass(self):
        folder_time = datetime.now().strftime("%d-%m-%Y")
        file_time = datetime.now().strftime("%I%M%S%p")
        drive_letter = r'D:/LogFile/' + folder_time + r'/' + '393.00'
        if not os.path.exists(drive_letter):
            Path(drive_letter).mkdir(parents=True, exist_ok=True)
        name_of_file = self.SN.text() + " PASS " + file_time
        completeName2 = os.path.join(drive_letter, name_of_file + ".txt")
        file1 = open(completeName2, "w")
        file1.write(self.Error.currentText() + '\n' + 'Total Time Ttest: ' + str(self.timetest.value()))
        file1.close()
    def save_log_fail(self):
        folder_time = datetime.now().strftime("%d-%m-%Y")
        file_time = datetime.now().strftime("%I%M%S%p")
        drive_letter = r'D:/LogFile/' + folder_time + r'/' + '393.00'
        if not os.path.exists(drive_letter):
            Path(drive_letter).mkdir(parents=True, exist_ok=True)
        name_of_file = self.SN.text() + " FAIL" + file_time
        completeName2 = os.path.join(drive_letter, name_of_file + ".txt")
        file1 = open(completeName2, "w")
        file1.write(self.Error.currentText() + '\n' + 'Total Time Ttest: ' + str(self.timetest.value()) + 's')
        file1.close()
    def Send_logfile_sftp(self):
        hostname = '10.228.28.37'
        sftp_port = 22
        sftp_username = 'TEB01'
        sftp_password = 'foxconn168!!'
        folder_time = datetime.now().strftime("%d-%m-%Y")
        patfile = '10.228.28.37/Logs'
        pathfile = '10.228.28.37/Logs/OBA'
        pathfile2 = '10.228.28.37/Logs/OBA/U46P393.00'
        pathfile3 = pathfile2 + "TCA400COMPC1"
        pathfile4 = pathfile3 + folder_time
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys=None
        with pysftp.Connection (host = hostname,port = sftp_port,username = sftp_username,password = sftp_password,cnopts=cnopts) as sftp:
            try:
                if not os.path.exists(patfile):
                    sftp.makedirs(pathfile)
            except:
                print('Warning!!!', 'Can not creat file' + patfile)
            try:
                if not os.path.exists(pathfile):
                    sftp.makedirs(pathfile)
            except:
                print('Warning!!!', 'Can not creat file: ' + pathfile )
            try:
                if not os.path.exists(pathfile2):
                    sftp.makedirs(pathfile2)
            except:
                print('Warning!!!', 'Can not creat file: ' + pathfile2 )
            try:
                if not os.path.exists(pathfile3):
                    sftp.makedirs(pathfile3)
            except:
                print('Warning!!!', 'Can not creat file: ' + pathfile3 )
            try:
                if not os.path.exists(pathfile4):
                    sftp.makedirs(pathfile4)
            except:
                print('Warning!!!', 'Can not creat file: ' + pathfile4 )
    def ErorCode(self):
        sn = self.SN.text()
        Computername = open('ComputerName.txt', 'r').read().split()
        if sn == '':
            self.status.setText("Chưa Scan SN!")
            self.status.setAlignment(Qt.AlignCenter)
            self.status.setStyleSheet(
                'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
        elif self.Error.currentText() == '':
            self.status.setText("Chưa Chon Ma Loi!")
            self.status.setAlignment(Qt.AlignCenter)
            self.status.setStyleSheet(
                'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
        else:
            if self.Error.currentText() == 'Cổng Micro-USB':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FMIUSB')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FMIUSB",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Chức năng USB Serial Console Port':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FUSBCS')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FUSBCS",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Nút Reset và Reboot':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FBUTRS')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FBUTRS",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Nút Home':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FBUTHM')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FBUTHM",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Chức năng LTE':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FCNLTE')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FCNLTE",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Thông Tin Sản Phẩm':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FINFOR')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FINFOR",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'PSU +/-':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FPSU+-')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FPSU+-",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Battery +/-':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FBATRY')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FBATRY",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Battery Infor':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FBATIF')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FBATIF",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Wi-Fi 2.4G':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FWF2GB')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FWF2GB",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Wi-Fi 5G':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FWF5GB')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FWF5GB",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Cellular check':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FCELAR')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FCELAR",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Video check':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FVIDEO')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FVIDEO",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Bluetooth check':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FBLTOO')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FBLTOO",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Pixels and Touch Sreen':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FPXTOS')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FPXTOS",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'TP Terminal':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FTPTER')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FTPTER",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Backlight':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FBKLIT')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FBKLIT",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'LED':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FCKLED')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FCKLED",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Tamper / Siren':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FTAMSI')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FTAMSI",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Microphone':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FMICPH')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FMICPH",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Zigbee':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FZIGBE')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FZIGBE",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'LCM Display':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FLCMDL')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FLCMDL",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'Completion & Removing USB Flash Drive':
                FB = self.SendSFC(sn.ljust(47) + Computername[0] + 'FCRUSB')
                if FB.find('PASS') != -1:
                    self.save_log_fail()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "FAIL",
                        "ErrorCode": "FCRUSB",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("FAIL")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            elif self.Error.currentText() == 'All Funtion PASS':
                FB = self.SendSFC(sn.ljust(47) + Computername[0])
                if FB.find('PASS') != -1:
                    self.save_log_pass()
                    idataTime = {
                        "ModelName": "U46P393.00",
                        "Route": "OBA_FUNCTION",
                        "Station": Computername[0],
                        "Sn": sn,
                        "Result": "PASS",
                        "ErrorCode": "",
                        "TotalTime": str(self.timetest.value()),
                    }
                    self.TimeToSystem(idataTime)
                    self.status.setText("PASS")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(0, 255, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
                else:
                    self.status.setText("Kiem tra SFC!")
                    self.status.setAlignment(Qt.AlignCenter)
                    self.status.setStyleSheet(
                        'background-color:rgb(255, 0, 0);font: 36pt "Calibri Bold";color:rgb(0, 0,0)')
            self.SN.setText('')
            self.Error.setCurrentIndex(0)





def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

app = QApplication(sys.argv)
login = LoginScreen()
login.Send_logfile_sftp()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login)
widget.setFixedHeight(421)
widget.setFixedWidth(671)
widget.show()
try:
    sys.exit(app.exec_())
except:
    CREATE_NO_WINDOW = 0x08000000
    subprocess.call('taskkill /F /IM Program TCA400 OBA Online Version 1.0.exe', creationflags=CREATE_NO_WINDOW)

