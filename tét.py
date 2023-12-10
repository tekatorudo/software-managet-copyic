# from PyQt4.QtGui import QApplication, QLabel
# from PySide2.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QApplication, QLabel


class model():
    def __init__(self, name: str, age: int, address: str, mark_i: int, mark_ii: int, mark_avg: float):
        super().__init__()
        self.name = name
        self.age = age
        self.address = address
        self.mark_i = mark_i
        self.mark_ii = mark_ii
        self.mark_avg = mark_avg

    a = [
        {"model": "95.9034986", "PN": "95.34.54567", "MPN": 'AOOFSS.34.324', "LocationPCB": 'S0',
         "Binfile": 'binfile test.txt', "Machine": 'DA1000', "checksum": 'test.txt', "project": 'test2.txt'},
        {"model": "95.9034986", "PN": "95.34.54567", "MPN": 'AOOFSS.34.324', "LocationPCB": 'S0',
         "Binfile": 'binfile test.txt', "Machine": 'DP-800', "checksum": 'test.txt', "project": 'test2.txt'},

        {"model": "95.9034986", "PN": "95.34.54567", "MPN": 'AOOFSS.34.324', "LocationPCB": 'U2',
         "Binfile": 'binfile test.txt', "Machine": 'DA1000', "checksum": 'test.txt', "project": 'test2.txt'},
        {"model": "95.9034986", "PN": "95.34.54567", "MPN": 'AOOFSS.34.324', "LocationPCB": 'U2',
         "Binfile": 'binfile test.txt', "Machine": 'DP-800', "checksum": 'test.txt', "project": 'test2.txt'},

        {"model": "95.9034986", "PN": "95.34.54567", "MPN": 'MKASDDW32.123', "LocationPCB": 'S10',
         "Binfile": 'binfile test.txt', "Machine": 'DA1000', "checksum": 'test.txt', "project": 'test2.txt'},
        {"model": "95.9034986", "PN": "95.34.54567", "MPN": 'MKASDDW32.123', "LocationPCB": 'U2',
         "Binfile": 'binfile test.txt', "Machine": 'DA1000', "checksum": 'test.txt', "project": 'test2.txt'},

    ]
