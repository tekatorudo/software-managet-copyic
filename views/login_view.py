import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox, QCheckBox


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login Form')

        layout = QVBoxLayout()

        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.remember_checkbox = QCheckBox('Remember Password', self)
        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)

        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_edit)
        layout.addWidget(self.remember_checkbox)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        from service.SQL.cursor import Conn
        # Thực hiện truy vấn
        cursor = Conn().cursor
        username = self.username_edit.text()
        password = self.password_edit.text()


        query = f"SELECT * FROM LOGIN_COPYIC WHERE [USER_NAME] = ? AND [PASSWORD] = ?"
        cursor.execute(query, (username, password))
        row = cursor.fetchall()

        print(row, type(row))

        if row:
            QMessageBox.information(self, 'Login', 'Login successful!')

            self.close()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')


        # Đóng kết nối
        Conn().conn().close()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        login_action = QAction('Login', self)
        login_action.triggered.connect(self.show_login_form)
        file_menu.addAction(login_action)

        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self.logout)
        logout_action.setEnabled(False)  # Disabled by default
        file_menu.addAction(logout_action)

        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        self.login_form = LoginForm()
        self.logout_action = logout_action

    def show_login_form(self):
        self.login_form.show()

    def logout(self):
        # Add your logout logic here
        self.login_form.username_edit.clear()
        self.login_form.password_edit.clear()
        self.login_form.remember_checkbox.setChecked(False)
        self.logout_action.setEnabled(False)  # Disable logout action after logout

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())