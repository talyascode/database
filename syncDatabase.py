# db object create
# sync_database = sync(db, true) / true for threading or multi


# lock- only one can get, for writing
# semaphore- only 10 can get, for reading

# state processing / state threading
import threading
import multiprocessing
from fileDatabase import *


# process = multiprocessing(target=get_value)
# process.start()


class SyncDatabase:
    def __init__(self, mode):
        # mode - True for processing, False for threading
        if mode:  # multi
            self.read = multiprocessing.Semaphore(10)
            self.write = multiprocessing.Lock()
        else:  # threading
            self.read = threading.Semaphore(10)
            self.write = threading.Lock()
        self.data = FileDatabase()

    def get_value(self, key):
        # print(self.data.get_value("color"))
        self.read.acquire()  # waiting until available
        logging.debug("reading key")
        data = self.data.get_value(key)
        self.read.release()
        return data

    def delete_value(self, key):
        self.get_acquires()   # waiting until available
        logging.debug("deleted key and value")
        data = self.data.delete_value(key)
        self.get_releases()
        return data

    def set_value(self, key, val):
        flag = True
        self.get_acquires()  # getting all the 10 semaphores for reading so no one will read while writing
        logging.info(flag)
        flag = self.data.set_value(key, val)
        self.get_releases()
        return flag  # true or false

    def get_acquires(self):
        self.write.acquire()
        for i in range(10):
            self.read.acquire()

    def get_releases(self):
        for i in range(10):
            self.read.release()
        self.write.release()

    def print_all(self):
        self.read.acquire()
        self.data.print_all()
        self.read.release()


if __name__ == '__main__':
    logging.basicConfig(filename="syncDatabase.log", filemode="a")
