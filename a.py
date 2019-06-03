import mysql.connector

class OpenFoodFact:
    def __init__(self):
        pass

    def get_ccategory(self):
        pass
    def get_food(self):
        pass


class Database:
    def __init__(self, user, password, name_db):
        self.user = user
        self.password = password
        self.name_db = name_db
        try:
            self.cnx = mysql.connector.connect(host='localhost',
                                          user=self.user,
                                          password=self.password,
                                          )
            if self.cnx.is_connected():
                print('vous etes connecté')

        except mysql.connector.Error as e:
            print(e)


    def create_db(self):
        cursor = self.cnx.cursor()
        query = f"CREATE DATABASE {self.name_db}"

        try:
            print(f"Création de la base de données {self.name_db}")
            cursor.execute(query)
            self.cnx.commit()

        except:
            pass


    def tables(self):
        cursor = self.cnx.cursor()
        query = ("CREATE TABLE Category ("
                 "id ")


database = Database('root', 'Lalydydu1456','alimention')
database.create_db()

