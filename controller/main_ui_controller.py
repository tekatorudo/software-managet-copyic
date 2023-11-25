import config as cf
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTreeWidget, QTreeWidgetItem, QMainWindow, QStyle, QMessageBox
from PyQt5.QtGui import QIcon

class mainUIController:

    def __init__(self):
        self.folder_is_valid:bool = None


    def handle_btn_add(self,callback=None) -> None:
        try:
            from views.add_view import AddApp
            self.add_app = AddApp()
            self.add_app.show()
            if callback:
                callback("êcc")
        except Exception as e:
            print(e)
            if callback:
                callback("ádasdasd")

    def handle_btn_refresh(self) -> None:
        # Xử lý sự kiện click ở đây
        print('handle_btn_refresh was clicked!')

    def handle_btn_showfolder(self,folder_path: str):
        """
        :param folder_path: when click to "button_show_folder", the system will go to that "folder_path"
        """
        if os.path.exists(folder_path):
            if os.path.isfile(folder_path):
                # if path is file path
                folder_path = os.path.dirname(folder_path)
            else:
                # if path is folder path
                folder_path = folder_path
            os.system(f'explorer "{folder_path}"')
        else:
            return 0





    def populate_tree_with_folder_contents(self, parentItem: QTreeWidgetItem, path: str, folderIcon: QIcon):
        """
        :return: folder + file for treeView in main UI
        """
        try:
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    try:
                        subItem = QTreeWidgetItem(parentItem, [entry])
                        subItem.setIcon(0, folderIcon)
                        self.populate_tree_with_folder_contents(subItem, full_path, folderIcon)

                    except PermissionError as e:
                        print("PermissionError 116", e)
                        pass
                else:
                    QTreeWidgetItem(parentItem, [entry])
        except PermissionError:
            print("PermissionError 121", e)

    # def set_button_state(self):
    #     if os.path.exists(self.full_path):
    #         # Nếu đường dẫn tồn tại, cho phép nút "Open Folder" hoạt động
    #         self.findChild(QPushButton, 'Open Folder').setEnabled(True)
    #     else:
    #         # Nếu đường dẫn không tồn tại, tắt nút "Open Folder"
    #         self.findChild(QPushButton, 'Open Folder').setEnabled(False)