import pickle

Users = {}
Users["None"] = "None"
pickle.dump(Users, open("UsersAPIs.data", "wb"))