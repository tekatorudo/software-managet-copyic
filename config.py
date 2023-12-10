from datetime import datetime

_HOST_NAME = '10.228.28.37'
_SFTP_PORT = 22
_SFTP_USERNAME = 'TEB01'
_SFTP_PASSWORD = 'foxconn168!!'
FOLDER_TIME = datetime.now().strftime("%d-%m-%Y")

# _path_treeWidget = r"D:\com hồng (rs232)"
_path_treeWidget = r"D:\SWmanagement"

ENGINE_ALCHEMY = "mssql+pyodbc://sa:123@ADMIN-PC/PC?driver=SQL+Server"
SERVER = 'ADMIN-PC'
DATABASE = 'USER_MANAGE'
USERNAME_ADMIN = 'sa'
PASSWORD_ADMIN = '123'
CONN_STRING = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME_ADMIN};PWD={PASSWORD_ADMIN}'
