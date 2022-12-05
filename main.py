import threading
import multiprocessing
from syncDatabase import SyncDatabase
import logging
MODE = True  # True for processing, False for threading


def main():
    def get(key, db):
        for i in range(0, 10000):
            assert("blue" == db.get_value(key))
        print(db.get_value(key))

    def sett(db):
        print(sync_database.set_value("shape", "circle"))
        print(sync_database.set_value("shap", "circl"))

    def delete(db):
        print(sync_database.delete_value("shape"))
        print(sync_database.delete_value("color"))


    logging.basicConfig(filename="fileDB.log", filemode="a", level=logging.DEBUG)
    sync_database = SyncDatabase(MODE)
    print(sync_database.set_value("color", "blue"))  # returns fail or success
    print(sync_database.set_value("shape", "circle"))  # returns fail or success
    print(sync_database.set_value("area", "24"))  # returns fail or success
    # print(sync_database.get_value("color"))  # returns the value for the key, None if the key doesn't exists
    # print(sync_database.delete_value("circle"))  # deletes the value for key and returns it, if doesnt exists return none

    if not MODE:  # threading
        g = threading.Thread(target=get, args=["color", sync_database])
        g.start()

        s = threading.Thread(target=sett, args=[sync_database])
        s.start()

        d = threading.Thread(target=delete, args=[sync_database])
        d.start()

        if "24" == sync_database.get_value("area") and "circle" == sync_database.get_value("shape") and "circl" == sync_database.get_value("shap"):
            print()
    else:  # multi processing
        g = multiprocessing.Process(target=get, args=("color", sync_database))
        g.start()

        s = multiprocessing.Process(target=sett, args=(sync_database,))
        s.start()

        d = multiprocessing.Process(target=delete, args=(sync_database,))
        d.start()


if __name__ == '__main__':
    main()
