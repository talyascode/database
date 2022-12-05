"""
Author: Talya Gross
database project
"""
# import
import threading
import multiprocessing
from syncDatabase import SyncDatabase
import logging

# constant
MODE = False  # True for multi processing, False for threading


def get(key, val, db):
    """
    the function gets the value for the key and checks that it wasnt changed
    :param key: the key of the dictionary
    :param val: the value of the key
    :param db: the database object
    """
    for i in range(0, 10000):
        assert val == db.get_value(key)
    # db.print_all()


def sett(db):
    """
    the function sets values for keys and deletes them
    :param db: the database object
    """
    for i in range(200, 300):
        assert True == db.set_value(str(i), "t")
    for i in range(200, 300):  # deleting the keys that i set
        assert "t" == db.delete_value(str(i))
    # db.print_all()


def delete(db):
    """
    the function creates and deletes keys in the dictionary
    :param db: the database object
    """
    for i in range(100, 200):
        db.set_value(str(i), "c")
        assert "c" == db.delete_value(str(i))
    # db.print_all()


def main():
    """
    the main function, according to the current mode, the function creates a database object and checks that
    you can read and write to the data( through the set, delete and get functions) -
    without any errors or lack of synchronization.
    """
    jobs = []
    logging.basicConfig(filename="fileDB.log", filemode="a", level=logging.DEBUG)
    sync_database = SyncDatabase(MODE)
    print(sync_database.print_all())
    for i in range(0, 100):
        sync_database.set_value(str(i), "c")
    print(sync_database.set_value("color", "blue"))
    original_data = sync_database
    print(sync_database.print_all())

    # get-  returns the value for the key, None if the key doesn't exists
    # delete- deletes the value for key and returns it, if doesnt exists return none
    # set- setting the key to val returns fail or success

    if not MODE:  # threading
        # get
        g = threading.Thread(target=get, args=["color", "blue", sync_database])
        g.start()
        jobs.append(g)

        # set
        s = threading.Thread(target=sett, args=[sync_database])
        s.start()
        jobs.append(s)

        # delete
        d = threading.Thread(target=delete, args=[sync_database])
        d.start()
        jobs.append(d)

    else:  # multi processing
        # get
        g = multiprocessing.Process(target=get, args=("color", "blue", sync_database))
        g.start()
        jobs.append(g)

        # set
        s = multiprocessing.Process(target=sett, args=(sync_database,))
        s.start()
        jobs.append(s)

        # delete
        d = multiprocessing.Process(target=delete, args=(sync_database,))
        d.start()
        jobs.append(d)

    for job in jobs:  # join- waiting for the threads to finish
        job.join()

    if original_data == sync_database:
        print(" the data didnt change!")
        print(sync_database.print_all())
    else:
        print("the data has changed... ")


if __name__ == '__main__':
    main()
