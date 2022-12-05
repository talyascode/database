import threading
import multiprocessing
from syncDatabase import SyncDatabase
import logging

MODE = False  # True for processing, False for threading


def get(key, db):
    for i in range(0, 10000):
        assert ("blue" == db.get_value(key))
    db.print_all()


def sett(db):
    for i in range(100, 200):
        assert (True == db.set_value(str(i), "t"))
    db.print_all()


def delete(db):
    for i in range(0, 100):
        # db.set_value(str(i), "c")
        assert "c" == db.delete_value(str(i))
    db.print_all()


def main():
    logging.basicConfig(filename="fileDB.log", filemode="a", level=logging.DEBUG)
    sync_database = SyncDatabase(MODE)
    print(sync_database.print_all())
    for i in range(0, 100):
        sync_database.set_value(str(i), "c")
    print(sync_database.set_value("color", "blue"))
    print(sync_database.print_all())

    # get-  returns the value for the key, None if the key doesn't exists
    # delete # deletes the value for key and returns it, if doesnt exists return none
    # set- returns fail or success

    if not MODE:  # threading
        g = threading.Thread(target=get, args=["color", sync_database])
        g.start()

        s = threading.Thread(target=sett, args=[sync_database])
        s.start()

        d = threading.Thread(target=delete, args=[sync_database])
        d.start()

    else:  # multi processing
        g = multiprocessing.Process(target=get, args=("color", sync_database))
        g.start()

        s = multiprocessing.Process(target=sett, args=(sync_database,))
        s.start()

        d = multiprocessing.Process(target=delete, args=(sync_database,))
        d.start()


if __name__ == '__main__':
    main()
