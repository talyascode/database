"""
Author: Talya Gross
file database class
"""

# import
import threading
import multiprocessing
from fileDatabase import *


class SyncDatabase:
    def __init__(self, mode):
        """
            build function of the SyncDatabase class
        """
        # lock- only one can get, for writing
        # semaphore- only 10 can get, for reading

        # mode - True for processing, False for threading
        if mode:  # multi
            self.read = multiprocessing.Semaphore(10)
            self.write = multiprocessing.Lock()
        else:  # threading
            self.read = threading.Semaphore(10)
            self.write = threading.Lock()
        self.data = FileDatabase()

    def get_value(self, key):
        """
        acquiring the read semaphore, getting the value of the key and releasing the semaphore
        :param key: the key of the dictionary
        :return: the value for the key
        """
        # print(self.data.get_value("color"))
        self.read.acquire()  # waiting until available
        logging.debug("reading key")
        data = self.data.get_value(key)
        self.read.release()
        return data

    def delete_value(self, key):
        """
        acquiring all the 10 semaphores for reading and the lock for writing
        and then deleting the key from the dictionary. releasing all the semaphores and the lock
        :param key: the key of the dictionary
        :return: the deleted value / None if the key doesnt exists
        """
        self.get_acquires()   # waiting until available
        logging.debug("deleted key and value")
        data = self.data.delete_value(key)
        self.get_releases()
        return data

    def set_value(self, key, val):
        """
        acquiring all the 10 semaphores for reading and the lock for writing
        setting the key to val and releasing all the semaphores and the lock.
        :param key: the key of the dictionary
        :param val: the value of the key
        :return  true or false for success or failure
        """
        flag = True
        self.get_acquires()
        logging.info(flag)
        flag = self.data.set_value(key, val)
        self.get_releases()
        return flag  # true or false

    def get_acquires(self):
        """
        acquiring all the 10 semaphores for reading and the lock for writing
        """
        self.write.acquire()
        for i in range(10):
            self.read.acquire()

    def get_releases(self):
        """
        releasing all the semaphores and the lock
        """
        self.write.release()
        for i in range(10):
            self.read.release()

    def print_all(self):
        """
        acquiring the semaphore for reading and printing the dictionary
        """
        self.read.acquire()
        self.data.print_all()
        self.read.release()


if __name__ == '__main__':
    db = SyncDatabase(True)
    assert db.set_value('2', '4') == True
    assert db.get_value('2') == '4'
    assert db.delete_value('2') == '4'

