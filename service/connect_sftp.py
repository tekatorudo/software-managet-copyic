from typing import Optional
import pysftp
import config as cf

def sftp_connection(**kwargs) -> Optional[pysftp.Connection]:
    """
    :param kwargs: include(host,port,username,password)
    :return: pysftp.Connection type | None type
    """
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try:
        sftp = pysftp.Connection(host=kwargs.get("host"),
                                 port=kwargs.get("port"),
                                 username=kwargs.get("username"),
                                 password=kwargs.get("password"),
                                 cnopts=cnopts)
        return sftp
    except Exception as e:
        print(f"Could not establish SFTP connection: {e}")
        return None


if __name__ == '__main__':
    sftp_conn = sftp_connection(host=cf._HOST_NAME, port=cf._SFTP_PORT,username=cf._SFTP_USERNAME,password=cf._SFTP_PASSWORD)
    if sftp_conn:
        print(sftp_conn)


