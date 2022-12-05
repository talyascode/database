"""
Author: Talya Gross
database project

"""
import logging


class DataBase:
    def __init__(self):
        """
        the constructor function
        """
        self.data_dict = {}

    def set_value(self, key, val):
        """
        setting the value of key to val
        :param key: the key of the dictionary
        :param val: the value of the key
        """
        # if key doesnt exist-> creates new key and val, if key exists-> the value will be changed to val
        logging.debug("setting" + key + "to value:" + val)
        self.data_dict.update({key: val})
        return True

    def get_value(self, key):
        """
        :param key: the key of the dictionary
        :return: the value of the key
        """
        logging.debug("return" + key)
        if key in self.data_dict.keys():
            return self.data_dict[key]
        return None

    def delete_value(self, key):
        """
        deletes the key from the dictionary
        :param key: the key of the dictionary
        :return: the updated dictionary without the key
        """
        logging.debug("return dict after deleting:" + key)
        return self.data_dict.pop(key, None)


if __name__ == '__main__':
    logging.basicConfig(filename="database.log", filemode="a")
