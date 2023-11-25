import os
import sys
import config as cf
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTreeWidget, QTreeWidgetItem, QMainWindow, QStyle
from controller.main_ui_controller import mainUIController
from PyQt5.QtGui import QIcon


class MainFormApp(QWidget):
    tree: QTreeWidget = None
    full_path: str = ""
    pathLineEdit: QLineEdit = None
    controller: mainUIController = mainUIController()

    def __init__(self):
        super().__init__()
        self.main_init()
        self.window_curent()

    def window_curent(self) -> None:
        window = QMainWindow()
        department: str = "Department: PE"
        id_employee: str = "N.T.H - V1050366"
        self.setWindowTitle(f'Software Management {department} - {id_employee}')
        self.setFixedSize(600, 450)

    def main_init(self):
        # phan tren
        layout_top = self.layout_top()

        pathLabel = QLabel('Path:')
        layout_top.addWidget(pathLabel)
        self.pathLineEdit = self.path_line_input()
        layout_top.addWidget(self.pathLineEdit)
        folderButton = self.button_show_folder()
        layout_top.addWidget(folderButton)

        # phan giua
        layout_middle = self.layout_middle()
        addNewButton = self.button_add()
        layout_middle.addWidget(addNewButton)
        refreshButton = self.button_refresh()
        layout_middle.addWidget(refreshButton)

        # phan tree view
        layout_treeview = QHBoxLayout()
        self.tree = self.tree_widget()
        layout_treeview.addWidget(self.tree)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout_top)
        mainLayout.addLayout(layout_middle)
        mainLayout.addLayout(layout_treeview)
        mainLayout.setContentsMargins(20, 20, 20, 20)

        # self.window_curent()
        self.setLayout(mainLayout)
        self.show()

    def layout_top(self) -> QHBoxLayout:
        lout = QHBoxLayout()
        return lout

    def layout_middle(self) -> QHBoxLayout:
        lout = QHBoxLayout()
        lout.setContentsMargins(0, 10, 0, 0)
        return lout

    def tree_widget(self) -> QTreeWidget:
        tree = QTreeWidget()
        tree.setHeaderHidden(True)
        tree.setContentsMargins(0, 10, 0, 0)

        # Lấy biểu tượng thư mục mặc định
        folderIcon = QApplication.style().standardIcon(QStyle.SP_DirIcon)
        # Tạo mục gốc cho ổ D
        dDriveItem = QTreeWidgetItem(tree, [cf._path_treeWidget.split('\\')[-1]])
        dDriveItem.setIcon(0, folderIcon)  # Đặt biểu tượng cho mục gốc
        self.controller.populate_tree_with_folder_contents(dDriveItem, cf._path_treeWidget, folderIcon)
        # clickListener
        tree.itemClicked.connect(self.onItemTreeWidgetClicked)
        return tree

    def onItemTreeWidgetClicked(self, item: QTreeWidgetItem) -> None:
        """
        :param item: No need to include
        this function only working in this class! I have no idea :(️
        """
        path = ""  # Reset self.path before set a new path
        while item is not None:  # if self.path not None, add "\"
            if path:
                path = os.path.join(item.text(0), path)
            else:
                path = item.text(0)
            item = item.parent()

        self.full_path = os.path.join(cf._path_treeWidget.split('\\')[0] + "\\", path)
        self.pathLineEdit.setText(self.full_path)

    def button_add(self) -> QPushButton:
        btn = QPushButton('Add New')
        btn.clicked.connect(lambda: self.controller.handle_btn_add(self.on_add_action_completed))
        return btn

    def on_add_action_completed(self, success: str):
        if success:
            print("Hành động hoàn thành mà không có lỗi.")
        else:
            print("Đã có lỗi xảy ra.")

    def button_refresh(self) -> QPushButton:
        btn = QPushButton('Refresh')
        btn.clicked.connect(self.controller.handle_btn_refresh)
        return btn

    def button_show_folder(self) -> QPushButton:
        btn = QPushButton('Show folder')
        btn.clicked.connect(lambda: self.controller.handle_btn_showfolder(self.full_path))

        print("hiccc")
        return btn

    def path_line_input(self) -> QLineEdit:
        pathLineEdit = QLineEdit('FTP://MODEL/ICPN/MPN/LocationOnPCB/Project&checksum/machineID/checksum.txt')
        return pathLineEdit

def main():
    app = QApplication(sys.argv)
    ex = MainFormApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

    # print(cf._path_treeWidget.split('\\')[0])
