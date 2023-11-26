import os
import sys
import config as cf
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTreeWidget, QTreeWidgetItem, QMainWindow, QStyle, QInputDialog, QMessageBox
from controller.main_ui_controller import mainUIController
from PyQt5.QtGui import QIcon


class MainFormApp(QWidget):
    tree: QTreeWidget = None
    add_new_button: QPushButton = None

    full_path: str = ""
    path_line_edit: QLineEdit = None
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
        '''
        this's main window. update 27/11 only 1 window
        we don't need to use addView()
         _______________
        | top-layout   |
        ----------------
        | add | refresh|
        _______________
        |  tree view  |
        ---------------
        '''
        layout_top = self.layout_top()
        '''part top include /path_label and path_line_edit and open_folder_button/  '''
        path_label = QLabel('Path:')
        layout_top.addWidget(path_label)
        self.path_line_edit = self.path_line_input()
        layout_top.addWidget(self.path_line_edit)
        open_folder_button = self.button_show_folder()
        layout_top.addWidget(open_folder_button)

        '''part middle include /add_button and refresh_button/'''
        layout_middle = self.layout_middle()
        self.add_new_button = self.button_add()
        layout_middle.addWidget(self.add_new_button)
        refreshButton = self.button_refresh()
        layout_middle.addWidget(refreshButton)

        '''part tree view include /self.tree/'''
        layout_treeview = QHBoxLayout()
        self.tree = self.tree_widget()
        layout_treeview.addWidget(self.tree)

        '''Main layout'''
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_top)
        main_layout.addLayout(layout_middle)
        main_layout.addLayout(layout_treeview)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # self.window_curent()
        self.setLayout(main_layout)
        self.show()

    def layout_top(self) -> QHBoxLayout:
        lout = QHBoxLayout()
        return lout

    def layout_middle(self) -> QHBoxLayout:
        lout = QHBoxLayout()
        lout.setContentsMargins(0, 10, 0, 0)
        return lout

    def tree_widget(self) -> QTreeWidget:
        from views.tree_widget import CustomTreeWidget
        tree = CustomTreeWidget()
        tree.setHeaderHidden(True)
        tree.setContentsMargins(0, 10, 0, 0)

        # enable add button when user select any one folder
        tree.itemSelectionChanged.connect(self.onSelectionChanged)

        # Lấy biểu tượng thư mục mặc định
        folder_icon = QApplication.style().standardIcon(QStyle.SP_DirIcon)
        ddriver_item = QTreeWidgetItem(tree, [cf._path_treeWidget.split('\\')[-1]])
        ddriver_item.setIcon(0, folder_icon)  # set icon folder
        self.controller.populate_tree_with_folder_contents(ddriver_item, cf._path_treeWidget, folder_icon)
        # clickListener
        tree.itemClicked.connect(self.on_item_tree_widget_clicked)
        return tree

    def on_item_tree_widget_clicked(self, item: QTreeWidgetItem) -> None:
        """
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
        self.path_line_edit.setText(self.full_path)
    def button_show_folder(self) -> QPushButton:
        btn = QPushButton('Show folder')
        btn.clicked.connect(lambda: self.controller.handle_btn_showfolder(self.full_path))
        print("hiccc")
        return btn
    def button_add(self) -> QPushButton:
        btn = QPushButton('Add New', self)
        btn.clicked.connect(lambda: self.controller.add_new_folder(self))
        btn.setEnabled(False) #only enable when path_line_edit not None
        return btn

    # def on_add_action_completed(self, success: str) -> None:
    #     """
    #     27/11 : new requirement! don't need to use this function
    #     """
    #     if success:
    #         print("Hành động hoàn thành mà không có lỗi.")
    #     else:
    #         print("Đã có lỗi xảy ra.")

    def button_refresh(self) -> QPushButton:
        btn = QPushButton('Refresh')
        btn.clicked.connect(lambda: self.controller.handle_btn_refresh(this=self))
        return btn



    def path_line_input(self) -> QLineEdit:
        pathLineEdit = QLineEdit('FTP://MODEL/ICPN/MPN/LocationOnPCB/Project&checksum/machineID/checksum.txt')
        return pathLineEdit



    def onSelectionChanged(self) -> None:
        '''If selected_item is None (path_line_edit is None) disable add_new_button '''
        try:
            selected_item = self.tree.currentItem()
            self.add_new_button.setEnabled(selected_item is not None)
        except Exception as e:
            print(e)


def main():
    app = QApplication(sys.argv)
    ex = MainFormApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

    # print(cf._path_treeWidget.split('\\')[0])
