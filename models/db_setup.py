from flask_mysqldb import MySQL

# Class to encapsulate MySQL initialization
class Database:
    def __init__(self, app):
        """
        Initialize the MySQL database with the app configuration.
        """
        self.mysql = MySQL(app)

    def get_connection(self):
        """
        Return the MySQL connection instance.
        """
        return self.mysql
