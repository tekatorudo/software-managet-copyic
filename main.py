import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTreeWidget, QTreeWidgetItem


class ExampleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Top layout with labels and buttons
        topLayout = QHBoxLayout()

        departmentLabel = QLabel('Department: PE')
        topLayout.addWidget(departmentLabel)

        nThLabel = QLabel('N.T.H - V1050366')
        topLayout.addStretch(1)
        topLayout.addWidget(nThLabel)

        # Middle layout with path
        midLayout = QHBoxLayout()

        pathLabel = QLabel('Path:')
        midLayout.addWidget(pathLabel)

        pathLineEdit = QLineEdit('FTP://MODEL/ICPN/MPN/LocationOnPCB/Project&checksum/machineID/checksum.txt')
        midLayout.addWidget(pathLineEdit)

        # Bottom layout with buttons and tree
        bottomLayout = QHBoxLayout()

        addNewButton = QPushButton('Add New')
        bottomLayout.addWidget(addNewButton)

        refreshButton = QPushButton('Refresh')
        bottomLayout.addWidget(refreshButton)

        # Tree widget
        tree = QTreeWidget()
        tree.setHeaderHidden(True)

        # Adding items to the tree widget
        root = QTreeWidgetItem(tree, ["USER"])
        americaItem = QTreeWidgetItem(root, ["America"])
        usaItem = QTreeWidgetItem(americaItem, ["USA"])
        usaItem.addChild(QTreeWidgetItem(["Providence"]))
        usaItem.addChild(QTreeWidgetItem(["Brown University", "CS Department"]))

        europeItem = QTreeWidgetItem(root, ["EUROPE"])
        greeceItem = QTreeWidgetItem(europeItem, ["Greece"])
        greeceItem.addChild(QTreeWidgetItem(["Athens"]))
        greeceItem.addChild(QTreeWidgetItem(["Thessaloniki"]))

        italyItem = QTreeWidgetItem(europeItem, ["Italy"])
        italyItem.addChild(QTreeWidgetItem(["Milan"]))
        italyItem.addChild(QTreeWidgetItem(["Rome"]))
        italyItem.addChild(QTreeWidgetItem(["Turin"]))

        bottomLayout.addWidget(tree)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(midLayout)
        mainLayout.addLayout(bottomLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle('PyQt5 GUI')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = ExampleApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
