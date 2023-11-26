import os
import sys
import config as cf
from PyQt5.QtWidgets import QTreeWidget, QMenu, QInputDialog, QMessageBox, QTreeWidgetItem
from controller.main_ui_controller import mainUIController


class CustomTreeWidget(QTreeWidget):
    controller: mainUIController = mainUIController()

    def __init__(self, parent=None):
        super().__init__(parent)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        renameAction = menu.addAction("🧾 Rename Folder")
        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == renameAction:
            self.renameFolder()

    def renameFolder(self):
        selected_item = self.currentItem()
        if selected_item:
            print("selected_item: ",selected_item)
            old_name = selected_item.text(0)
            new_name, ok = QInputDialog.getText(self, 'Rename Folder', 'Enter new folder name:', text=old_name)
            if ok and new_name and new_name != old_name:
                print("ok and new_name: ", ok ,new_name)
                try:
                    current_path = self.controller.get_full_path(selected_item)
                    print(current_path)
                    new_path = os.path.join(os.path.dirname(current_path), new_name)

                    os.rename(current_path, new_path)
                    selected_item.setText(0, new_name)
                except OSError as e:
                    # QMessageBox.critical(self, "Error", f"Cannot rename folder: {e}")
                    print( "Error", f"Cannot rename folder: {e}")
            else:
                print("if ok and new_name and new_name != old_name:")
        else:
            print("hiccc:")

