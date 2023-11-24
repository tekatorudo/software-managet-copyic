import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QFormLayout, QMainWindow, QFileDialog, QMessageBox, QDialog)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from views.main_view import MainFormApp
from controller.add_ui_controller import addUIController
import config as cf
from PyQt5.QtCore import pyqtSignal


class AddApp(MainFormApp,QDialog):
    model_path: QLineEdit = None
    pn_path: QLineEdit = None
    mpn_path: QLineEdit = None
    location_on_pcb_path: QLineEdit = None
    bin_file_path: QLineEdit = None
    project_checksums_path: QLineEdit = None
    controller: addUIController = addUIController()
    default_folder_path =  cf._path_treeWidget


    def __init__(self):
        super().__init__()
        self.add_init()


    def main_init(self) -> None:
        pass

    def window_curent(self) -> None:
        super().window_curent()
        self.setFixedSize(600, 250)


    def add_init(self):
        form_select_folder_layout = QFormLayout()

        # Các label và QLineEdit của bạn
        self.model_path = self.create_line_edit("Model")
        self.pn_path = self.create_line_edit("IC P/N")
        self.mpn_path = self.create_line_edit("MPN")
        self.location_on_pcb_path = self.create_line_edit("Location on PCB")
        self.bin_file_path = self.create_line_edit("Bin File")
        self.project_checksums_path = self.create_line_edit("Project & Checksum")
        # add roww to form_select_folder_layout
        form_select_folder_layout.addRow("Model", self.model_path)
        form_select_folder_layout.addRow("IC P/N", self.pn_path)
        form_select_folder_layout.addRow("MPN", self.mpn_path)
        form_select_folder_layout.addRow("Location on PCB", self.location_on_pcb_path)
        form_select_folder_layout.addRow("Bin File", self.bin_file_path)
        form_select_folder_layout.addRow("Project&Checksum", self.project_checksums_path)

        # Khởi tạo các QLineEdit với trạng thái kích hoạt cụ thể
        self.model_path.setEnabled(True)  # Cho phép người dùng chọn 'Model' ngay lập tức
        self.pn_path.setEnabled(False)  # Các trường còn lại sẽ không kích hoạt
        self.mpn_path.setEnabled(False)
        self.location_on_pcb_path.setEnabled(False)
        self.bin_file_path.setEnabled(False)
        self.project_checksums_path.setEnabled(False)


        # Main layout setup
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(form_select_folder_layout)
        mainLayout.setContentsMargins(20, 20, 20, 20)

        # Set the layout and window title
        self.setLayout(mainLayout)
        # Show the application window
        self.show()

    def layoutv_all_path(self) -> QVBoxLayout:
        lout = QVBoxLayout()
        return lout

    def layouth_path(self) -> QHBoxLayout:
        lout = QHBoxLayout()
        return lout

    def create_line_edit(self, label_text):
        line_edit = QLineEdit(self)
        line_edit.mousePressEvent = lambda event, le=line_edit: self.on_line_edit_clicked(event, le, label_text)
        return line_edit

    def on_line_edit_clicked(self, event, line_edit, label_text):
        # dialog only open when QLineEdit is active
        if line_edit.isEnabled():
            self.select_folder(event, line_edit)

    def select_folder(self, event, line_edit):
        # Đặt folder mặc định là ổ D, hoặc sử dụng folder đã chọn cuối cùng
        folder_path = QFileDialog.getExistingDirectory(self, f'Select {line_edit.placeholderText()}',
                                                       self.default_folder_path)
        if folder_path:
            line_edit.setText(folder_path)
            # Cập nhật default_folder_path để lần mở tiếp theo sẽ bắt đầu từ đây
            self.default_folder_path = folder_path
            self.enable_next_line_edit(line_edit)

    def enable_next_line_edit(self, current_line_edit):
        # Cập nhật trạng thái kích hoạt của các QLineEdit dựa trên người dùng đã chọn
        order = [self.model_path, self.pn_path, self.mpn_path, self.location_on_pcb_path, self.bin_file_path,
                 self.project_checksums_path]
        current_index = order.index(current_line_edit)
        for i in range(current_index + 1, len(order)):
            order[i].setEnabled(False)  # Disable tất cả các QLineEdit bên dưới
            order[i].clear()  # Xóa text hiện tại

        # Enable QLineEdit tiếp theo
        if current_index + 1 < len(order):
            order[current_index + 1].setEnabled(True)





        # ...

    def some_function_that_closes_add_app(self):
        # event when user click close this View
        print("? close ")
        self.accept()
def main():
    app = QApplication(sys.argv)
    ex = AddApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
