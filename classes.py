import mysql.connector
import requests


class OpenFoodFact:
    def __init__(self, url):
        self.url = url

    def get_category(self):
        r = requests.get(self.url) #'https://fr.openfoodfacts.org/categories&json=1'
        r_json = r.json()  # dict
        tag_category = r_json['tags']  # list

        i = 0
        name = []
        while i < 10:
            for data_cat in tag_category:  # tag_category ==> dict
                if i == 10:
                    break
                else:
                    cat_name = ' '.join(data_cat['id'][3:].split('-'))
                    name.append(cat_name)
                i += 1
        return name

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
        query_product = ("CREATE TABLE Product ("
                          "id INT UNSIGNED NOT NULL AUTO_INCREMENT, "
                          "name VARCHAR(100) NOT NULL, "
                          "category_id SMALLINT UNSIGNED NOT NULL, "
                          "PRIMARY KEY (id), "
                          "CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Category(id)"
                          ")"
                          "ENGINE=InnoDB"
                          )

        query_substitut = ("CREATE TABLE Substitut ("
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
            cursor.execute(query_product)
            cursor.execute(query_substitut)

        except mysql.connector.Error as e:
            print(e)

    def insert_data(self):
        cursor = self.cnx.cursor()
        query_insert = "INSERT INTO Category (name) VALUES (%s)"
        name = OpenFoodFact('https://fr.openfoodfacts.org/categories&json=1').get_category()
        name_list= []
        for i in name:
            name_in_tuple = i,
            name_list.append(name_in_tuple)
        print(name_list)
        try:
            cursor.executemany(query_insert, name_list)
            self.cnx.commit()

        except mysql.connector.Error as e:
            print(e)


database = Database('root', 'Lalydydu1456','alimentation')
database.create_db()
#database.create_tables()
database.insert_data()

database.cnx.cursor().close()
database.cnx.close()
