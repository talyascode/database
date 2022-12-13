"""
Author: Talya Gross
file database class
"""
# import
import database
import pickle
import logging

FILE = "database"


class FileDatabase(database.DataBase):
    def __init__(self):
        """
            build function of the FileDatabase class
        """
        super().__init__()
        with open(FILE, "wb") as file:
            logging.debug("read file")
            pickle.dump(self.data_dict, file)

    def set_value(self, key, val):
        """
        reading the data, setting the key to val in the file and database object.
        :param key: the key of the dictionary
        :param val: the value of the key
        :return: true or false for success or failure
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
            return flag

    def get_value(self, key):
        """
        reading the dictionary file
        :param key: the key of the dictionary
        :return: the value for the key
        """
        with open(FILE, "rb") as file:
            logging.debug("opened file")
            self.data_dict = pickle.load(file)
        return super().get_value(key)

    def delete_value(self, key):
        """
        reading the file, deleting the value in the database object and file
        and updating it without the deleted key in the file
        :param key: the key of the dictionary
        :return: the deleted value / None if the key doesnt exists
        """
        with open(FILE, "rb") as file:
            logging.debug("opened file")
            self.data_dict = pickle.load(file)
        val = super().delete_value(key)
        logging.debug("deleted value")
        with open(FILE, "wb") as file:
            logging.debug("read file")
            pickle.dump(self.data_dict, file)
        return val

    def print_all(self):
        """
        printing the dictionary
        """
        with open(FILE, "rb") as file:
            logging.debug("opened file")
            self.data_dict = pickle.load(file)
        print(self.data_dict)


if __name__ == '__main__':

    db = FileDatabase()
    assert db.set_value('2', '4') == True
    assert db.get_value('2') == '4'
    assert db.delete_value('2') == '4'

