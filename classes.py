import mysql.connector
import requests


class OpenFoodFact:
    def __init__(self):
        self.url = 'https://fr.openfoodfacts.org/categories&json=1'

    def get_category(self):
        r = requests.get(self.url) #'https://fr.openfoodfacts.org/categories&json=1'
        r_json = r.json()  # dict
        tag_category = r_json['tags']  # list

        list_of_category = []
        #We wont to have this category in list_of_category
        category = ['Plats préparés', 'Boissons chaudes', 'Produits à tartiner', 'Biscuits et gâteaux',
                    'Desserts', 'Surgelés', 'Sauces', 'Conserves', 'Chocolats', 'Confitures et marmelades']

        for data_cat in tag_category:  # data_cat ==> dict
            if data_cat['name'] in category:
                list_of_category.append(data_cat['name'])
            else:
                pass
        return list_of_category

    def get_food(self):
        list_of_category = self.get_category()
        dict_cat_prod = {}
        for i in range(2):
            for page in range(1,10):
                r = requests.get('https://fr.openfoodfacts.org/categorie/'+list_of_category[i]+'/'+str(page)+'.json') #'https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux/1'
                r_json = r.json()
                tag_product = r_json['products']
                list_of_product = []
                for product in tag_product:
                    # we make an if because some of product don't have 'product_name' in their field
                    # and others have 'product_name' but it is empty
                    if 'product_name' in product and product['product_name'] != '':
                        list_of_product.append(product['product_name'])
                    else:
                        pass
                if i+1 not in dict_cat_prod:
                    dict_cat_prod[i+1] = list_of_product
                else:
                    dict_cat_prod[i+1] += list_of_product
                if len(dict_cat_prod[i+1]) > 40:
                    dict_cat_prod[i + 1] = dict_cat_prod[i+1][0:40]
                    break
            print(len(dict_cat_prod[i+1]))
            print(dict_cat_prod)
        return dict_cat_prod

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
        #INSERT LIST OF CATEGORY
        query_cat = "INSERT INTO Category (name) VALUES (%s)"
        list_of_category = OpenFoodFact().get_category()
        print(list_of_category)
        list_of_tuple = []
        for name_of_cat in list_of_category:
            name = name_of_cat,
            list_of_tuple.append(name)
        try:
            cursor.executemany(query_cat, list_of_tuple)
            self.cnx.commit()

        except mysql.connector.Error as e:
            print(e)
        #INSERT LIST OF PRODUCTS
        query_product = ("INSERT INTO Product (name, category_id) " 
                        "VALUES (%s, %s)")
        dict_cat_prod = OpenFoodFact().get_food()
        try:
            for cat_id, list_prod in dict_cat_prod.items():
                for product in list_prod:
                    cursor.execute(query_product, (product, cat_id))
                    self.cnx.commit()
        except mysql.connector.Error as e:
            print(e)



database = Database('root', 'Lalydydu1456','alimentation')
database.create_db()
database.create_tables()
database.insert_data()


database.cnx.cursor().close()
database.cnx.close()
