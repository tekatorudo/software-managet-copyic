import shutil

from PyQt5.QtCore import pyqtSignal
from modules import log_exception
import config as cf
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTreeWidget, QTreeWidgetItem, QMainWindow, QStyle, QMessageBox, QInputDialog, QFileDialog
from PyQt5.QtGui import QIcon


class mainUIController:
    dialog_closed_signal = pyqtSignal()
    name_button: str = "All Files (*)"

    def __init__(self):
        self.controller = None
        self.folder_is_valid: bool = None
        self.lst_model: list = []

    def handle_btn_add(self, this, callback=None) -> None:
        '''
        :params : type of "this" it's "MainFormApp()"
        using class AddApp() is child modal
        When this AddApp() closed! It had sent a signal to MainFormApp
        27/11 : do not use 🚫
        '''
        this.dll()
        try:
            from views.add_view import AddApp
            dialog = AddApp()
            dialog.dialog_closed_signal.connect(self.dialogClosed)
            dialog.exec_()
            if callback:
                callback("êcc")
        except Exception as e:
            print(e)
            if callback:
                callback("ádasdasd")

    def handle_btn_refresh(self, this) -> None:
        """
        :params : type of "this" it's "MainFormApp()"
        """
        # Xử lý sự kiện click ở đây
        print('handle_btn_refresh was clicked!')
        if this:
            self.refresh_tree_view(this)

    def handle_btn_showfolder(self, this, folder_path: str):
        """
        :param folder_path: when click to "button_show_folder", the system will go to that "folder_path"
        """

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Chỉ cho phép đọc file, không cho phép ghi

        fileDialog = QFileDialog(this)
        fileDialog.setOptions(options)
        fileDialog.setFileMode(QFileDialog.ExistingFiles)
        fileDialog.setNameFilter("All Files (*)")

        if fileDialog.exec_():
            selectedFiles = fileDialog.selectedFiles()
            if selectedFiles:
                # Lấy ra danh sách các file được chọn
                for file_path in selectedFiles:
                    # Xử lý file_path ở đây
                    # Ở đây, chúng ta chỉ in ra tên file đã chọn
                    print(f'Selected File: {file_path}')

                    # Lưu file vào đường dẫn D:\LDPlayer\test\
                    destination_folder = r'D:\LDPlayer\test'
                    file_name = os.path.basename(file_path)
                    destination_path = os.path.join(destination_folder, file_name)

                    # Kiểm tra nếu file đã tồn tại trong thư mục đích, xoá nó đi trước
                    if os.path.exists(destination_path):
                        os.remove(destination_path)

                    # Di chuyển file đến thư mục đích
                    shutil.move(file_path, destination_path)

        else:
            print('Dialog was canceled.')

    # if os.path.exists(folder_path):
    #     if os.path.isfile(folder_path):
    #         # if path is file path
    #         folder_path = os.path.dirname(folder_path)
    #     else:
    #         # if path is folder path
    #         folder_path = folder_path
    #     os.system(f'explorer "{folder_path}"')
    # else:
    #     return 0

    def populate_tree_with_folder_contents(self, parentItem: QTreeWidgetItem, path: str, folderIcon: QIcon) -> None:
        """
        :return: folder + file for treeView in main UI
        """
        try:
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                # print(full_path)
                counter = full_path.count("\\")
                if os.path.isdir(full_path):
                    try:
                        sub_item = QTreeWidgetItem(parentItem, [entry])
                        sub_item.setIcon(0, folderIcon)
                        self.populate_tree_with_folder_contents(sub_item, full_path, folderIcon)
                    except Exception as e:
                        print("PermissionError 116", e)
                        log_exception.log_exception(e)
                        pass
                else:
                    QTreeWidgetItem(parentItem, [entry])
                    if counter > 3:
                        self.excute_test(full_path)
        except Exception as e:
            log_exception.log_exception(e)
            print("PermissionError 121", e)

    def excute_test(self, path: str) -> None:
        from modules.model.model_test import model

        val: list[str] = path.split("\\")[2:]
        if len(val) < 3: return
        self.lst_model.append(val)


    def refresh_tree_view(self, this) -> None:
        """
        :params : type of "this" it's "MainFormApp()"
        """
        this.tree.clear()  # Delete all content current on tree view
        folder_icon = QApplication.style().standardIcon(QStyle.SP_DirIcon)
        d_drive_item = QTreeWidgetItem(this.tree, [cf._path_treeWidget.split('\\')[-1]])
        d_drive_item.setIcon(0, folder_icon)

        # Tải lại nội dung vào TreeView từ đường dẫn mục gốc
        this.controller.populate_tree_with_folder_contents(d_drive_item, cf._path_treeWidget, folder_icon)

    def get_full_path(self, item: QTreeWidgetItem) -> str:
        path = ""
        while item is not None:
            if path:
                path = os.path.join(item.text(0), path)
            else:
                path = item.text(0)
            item = item.parent()
        return os.path.join(cf._path_treeWidget.split('\\')[0] + "\\", path)

    def add_new_folder(self, this) -> None:
        """
        :params : type of "this" it's "MainFormApp()"
        """
        selected_item = this.tree.currentItem()
        if selected_item:
            # show QInputDialog to typing a new name folder
            folder_name, ok = QInputDialog.getText(this, 'New Folder', 'Enter folder name:')
            if ok and folder_name:
                parent_path = self.get_full_path(selected_item)
                new_folder_path = os.path.join(parent_path, folder_name)
                if not os.path.exists(new_folder_path):
                    try:
                        os.mkdir(new_folder_path)  # Tạo folder mới
                    except Exception as e:
                        log_exception.log_exception(e)
                        print("Error", f"Cannot create folder: {e}")
                        return

                    # Cập nhật TreeView
                    folder_icon = QApplication.style().standardIcon(QStyle.SP_DirIcon)
                    new_folder_item = QTreeWidgetItem(selected_item, [folder_name])
                    new_folder_item.setIcon(0, folder_icon)

                    # Gọi lại hàm để nạp nội dung vào folder mới
                    self.populate_tree_with_folder_contents(new_folder_item, new_folder_path, folder_icon)
                    selected_item.setExpanded(True)  # Mở rộng item cha để hiển thị item mới
                else:
                    print("add_new_folder : have no path! check again")
                    log_exception.log_fail("mainUIController > add_new_folder() >> Have no path!")
            else:
                print("add_new_folder:  UI QInputDialog error! ")
                log_exception.log_fail("mainUIController > add_new_folder() >> UI QInputDialog error!")

    def dialogClosed(self):
        print('AddApp(QDialog) đã tắt')
