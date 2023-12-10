import os
import sys

from PyQt5.QtCore import Qt

import config as cf
from PyQt5.QtWidgets import QTreeWidget, QMenu, QInputDialog, QMessageBox, QTreeWidgetItem
from controller.main_ui_controller import mainUIController


class CustomTreeWidget(QTreeWidget):
    controller: mainUIController = mainUIController()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.folder_colors = {}  # Dùng để lưu trạng thái màu sắc của các thư mục

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        rename_action = menu.addAction("🧾 Rename Folder")
        highlight_action = menu.addAction("🟢 Highlight Parent Folder")

        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == rename_action:
            self.renameFolder()
        elif action == highlight_action:
            self.highlightParentFolder()

    def renameFolder(self):
        selected_item = self.currentItem()
        if selected_item:  # if path to folder is visible
            old_name = selected_item.text(0)
            new_name, ok = QInputDialog.getText(self, 'Rename Folder', 'Enter new folder name:', text=old_name)
            if ok and new_name and new_name != old_name:
                print("ok and new_name: ", ok, new_name)
                try:
                    current_path = self.controller.get_full_path(selected_item)
                    new_path = os.path.join(os.path.dirname(current_path), new_name)

                    os.rename(current_path, new_path)
                    selected_item.setText(0, new_name)
                except OSError as e:
                    print("Error", f"Cannot rename folder: {e}")
            else:
                print("if ok and new_name and new_name != old_name:")
        else:
            print("hiccc:")

    def highlightParentFolder(self):
        selected_item = self.currentItem()
        if selected_item and not selected_item.childCount():
            parent_item = selected_item.parent()  # Lấy thư mục cha
            if parent_item:
                parent_item.setBackground(0, Qt.darkGreen)  # Đặt màu nền của thư mục cha là màu xanh
                self.folder_colors[parent_item.text(0)] = Qt.darkGreen  # Lưu trạng thái màu sắc vào cấu trúc dữ liệu

    def restoreFolderColors(self):
        # Code để khôi phục trạng thái màu sắc từ dữ liệu đã lưu
        for folder_name, color in self.folder_colors.items():
            items = self.findItems(folder_name, Qt.MatchExactly | Qt.MatchRecursive)
            if items:
                for item in items:
                    item.setBackground(0, color)