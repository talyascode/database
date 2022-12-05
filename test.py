import pickle

with open("database", "rb") as file:
    #logging.debug("opened file")
    data_dict = pickle.load(file)
    print(data_dict)
