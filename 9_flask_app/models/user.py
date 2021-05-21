import json


class User:
    def __init__(self, login=None, hash_password=None, salt=None, registration_date=None):
        self.login = login
        self.hash_password = hash_password
        self.salt = salt
        self.registration_date = registration_date

    def to_json(self):
        data = {
            "login": self.login,
            "hash_password": self.hash_password,
            "salt": self.salt,
            "date_registration": self.registration_date
        }
        return json.dumps(data, ensure_ascii=False)

    def get_tuple(self):
        return self.login, self.hash_password, self.salt, self.registration_date
