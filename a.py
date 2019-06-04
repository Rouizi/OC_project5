import mysql.connector
import requests


class OpenFoodFact:
    def __init__(self):
        pass

    def get_ccategory(self):
        r = requests.get('https://fr.openfoodfacts.org/categories')
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
        #query = f"CREATE DATABASE {self.name_db}"
        query_use = f"USE {self.name_db}"

        try:
            print(f"Création de la base de données {self.name_db}")
            #cursor.execute(query)
            cursor.execute(query_use)

        except mysql.connector.Error as e:
            print(e)


    def create_tables(self):
        cursor = self.cnx.cursor()
        query_category = ("CREATE TABLE Category ("
                 "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT, "
                 "name VARCHAR(100) NOT NULL, "
                 "PRIMARY KEY (id)"
                 ")"
                 "ENGINE=InnoDB"
                 )
        query_products = ("CREATE TABLE Product ("
                          "id INT UNSIGNED NOT NULL AUTO_INCREMENT, "
                          "name VARCHAR(100) NOT NULL, "
                          "category_id SMALLINT UNSIGNED NOT NULL, "
                          "PRIMARY KEY (id), "
                          "CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Category(id)"
                          ")"
                          "ENGINE=InnoDB"
                          )

        query_substituts = ("CREATE TABLE Substitut ("
                           "id INT UNSIGNED NOT NULL AUTO_INCREMENT, "
                           "product_id INT UNSIGNED NOT NULL, "
                           "name VARCHAR(100) NOT NULL, "
                           "marque VARCHAR(100), "
                           "quantite VARCHAR(20), "
                           "ingredients TEXT, "
                           "nutri_score CHAR(1), "
                           "magasin VARCHAR(100), "
                           "url TEXT NOT NULL, "
                           "PRIMARY KEY (id), "
                           "CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Product(id)"
                           ")"
                           "ENGINE=InnoDB"
                           )
        try:
            cursor.execute(query_category)
            cursor.execute(query_products)
            cursor.execute(query_substituts)

        except mysql.connector.Error as e:
            print(e)

    def insert_data(self):
        pass

database = Database('root', 'Lalydydu1456','alimentation')
database.create_db()
database.create_tables()

