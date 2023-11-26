import traceback
from datetime import datetime
import os


def log_exception(ex) -> None:
    """
    This function was created to manage exception by saving them to a log file day by day!
    """
    log_filename:str = 'log' + datetime.now().strftime('%d%m%Y') + '.txt'

    with open(log_filename, 'a') as log_file:
        log_file.write('---\n')
        log_file.write('Timestamp: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')

        log_file.write('Exception: ' + str(ex) + '\n')
        traceback.print_exc(file=log_file)  # Ghi stack trace

        log_file.write('\n')

    print(f"An exception was logged in {log_filename}")
def log_activities() -> None:
    """
        This function was created to manage user activities by saving them to a log file day by day!
        - > in Fact : to manage software changes!
    """

def log_fail(fail_content:str) -> None:
    """
        This function was created to manage activities by saving them to a log file day by day!
        """
    log_filename: str = 'log' + datetime.now().strftime('%d%m%Y') + '.txt'

    with open(log_filename, 'a') as log_file:
        log_file.write('---\n')
        log_file.write('Timestamp: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')

        log_file.write('Fail Activity: ' + str(fail_content) + '\n')
        traceback.print_exc(file=log_file)

        log_file.write('\n')

    print(f"An fail activity was logged in {log_filename}")

