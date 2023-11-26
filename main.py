import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTreeWidget, QTreeWidgetItem
from views.add_view import AddApp
from views.main_view import MainFormApp
import logging

def main():
    app = QApplication(sys.argv)
    main_view = MainFormApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


