"""
Author: Talya Gross
database project
"""
import database
import pickle
import logging
import os

FILE = "database"


class FileDatabase(database.DataBase):
    def __init__(self):
        super().__init__()
        if not os.path.isfile(FILE):
            with open(FILE, "wb") as file:
                logging.debug("read file")
                pickle.dump(self.data_dict, file)

    def set_value(self, key, val):
        """
        setting the key value to val
        :param key: the key of the dictionary
        :param val: the value of the key
        :return:
        """
        flag = True
        try:
            with open(FILE, "rb") as file:
                logging.debug("opened file")
                self.data_dict = pickle.load(file)
            super().set_value(key, val)  # updating the object of the dictionary
            logging.debug("set value")
            with open(FILE, "wb") as file:
                logging.debug("read file")
                pickle.dump(self.data_dict, file)
        except OSError as err:
            print('received pickle exception - ' + str(err))
            flag = False
        finally:
            # self.data_dict.close()
            return flag

    def get_value(self, key):
        """
        :return: the dictionary after reading it to update
        """
        with open(FILE, "rb") as file:
            logging.debug("opened file")
            self.data_dict = pickle.load(file)
        return super().get_value(key)

    def delete_value(self, key):
        """
        deleting the key in the dictionary, and updating it without the deleted key
        :param key: the key of the dictionary
        :return: the updated dictionary without the key
        """
        with open(FILE, "rb") as file:
            logging.debug("opened file")
            self.data_dict = pickle.load(file)
        val = super().delete_value(key)
        logging.debug("deleted key and value")
        with open(FILE, "wb") as file:
            logging.debug("read file")
            pickle.dump(self.data_dict, file)
        return val


if __name__ == '__main__':
    logging.basicConfig(filename="fileDB.log", filemode="a")
