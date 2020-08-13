import datetime
import crypto

class DataBase:
    def __init__(self, filename, efilename):
        self.filename = filename
        self.efilename = efilename
        self.users = None
        self.file = None
        self.efile = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.efile = open(self.efilename, "r")
        self.users = {}

        for line in self.file:
            email, password, name, created = line.strip().split(";")
            self.users[email] = (password, name, created)

        self.file.close()
        self.efile.close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            print("Email exists already")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")
        with open(self.efilename, "w") as g:
            for user in self.users:
                g.write(crypto.encrypt(user.encode()) + ";" + crypto.encrypt(self.users[user][0].encode()) + ";" + crypto.encrypt(self.users[user][1].encode()) + ";" + crypto.encrypt(self.users[user][2].encode()) + "\n")
        f.close()
        g.close()

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]