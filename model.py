import database
class Model():
    def __init__(self):
        self.db = database.create_connection()
