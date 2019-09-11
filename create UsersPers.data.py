import pickle

Users = {}
Users["None"] = "None"
pickle.dump(Users, open("UsersPers.data", "wb"))