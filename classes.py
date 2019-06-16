import mysql.connector
import requests


class OpenFoodFact:
    def __init__(self, url_cat, url_prod):
        self.url_cat = url_cat
        self.url_prod = url_prod


    def get_category(self):
        r = requests.get(self.url_cat) # self.url_cat = 'https://fr.openfoodfacts.org/categories&json=1'
        r_json = r.json()  # type(r_json) = dict
        data_categories = r_json['tags']  # type(tag_category) = list

        list_of_categories = []
        # We wont to have this category in list_of_category
        categories = ['Confiseries', 'Biscuits fourrés', 'Produits à tartiner', 'Céréales et dérivés',
                    'Desserts', 'Surgelés', 'Sauces', 'Conserves', 'Chocolats', 'Confitures et marmelades']

        for data_category in data_categories:  # type(data_cat) = dict
            if data_category['name'] in categories:
                list_of_categories.append(data_category['name'])
        return list_of_categories

    def get_product(self):
        list_of_categories = self.get_category()
        list_of_name_prod = []
        dict_cat_prod = {}
        for i in range(10):
            for page in range(1,20):
                # exemple: requests.get('https://fr.openfoodfacts.org/categorie/Confiseries/1.json')
                r = requests.get(self.url_cat[0:-8] + '/' + list_of_categories[i] + '/' + str(page) + '.json')
                r_json = r.json()
                data_products = r_json['products'] # type(data_products) = list
                dict_prod = {}
                for prod_detail in data_products: # type(prod_detail) = dict
                    # According to the API of the web site some product may not have
                    # 'product_name', 'nutrition_grade_fr' or 'code' in their fiels so we make an if to filter all that
                    if ('product_name' in prod_detail and prod_detail['product_name'] != '' and
                        'nutrition_grade_fr' in prod_detail and prod_detail['nutrition_grade_fr'] != '' and
                        'code' in prod_detail and prod_detail['code'] != ''
                        and prod_detail['product_name'].lower() not in list_of_name_prod):
                        list_of_name_prod.append(prod_detail['product_name'].lower())
                        dict_prod[prod_detail['product_name']] = [prod_detail['nutrition_grade_fr'].upper(), prod_detail['code']]

                #If dictionary is empty we can't do dict[x].update(dict2) so we enter in the first case
                if i + 1 not in dict_cat_prod:
                    dict_cat_prod[i + 1] = dict_prod
                else:
                    dict_cat_prod[i + 1].update(dict_prod)
                if len(dict_cat_prod[i + 1]) > 50:
                    # We take only 50 products per category
                    dict_cat_prod[i + 1] = dict(list(dict_cat_prod[i + 1].items())[0:50])
                    break
            print(f"Récupération des produits de la catégorie: {list_of_categories[i]}")
        return dict_cat_prod

    def get_substitut(self, bar_code):
        dict_nutri_score = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
        # for exemple self.url_prod = 'https://fr.openfoodfacts.org/api/v0/produit/4060800002242.json'
        r_prod = requests.get(self.url_prod + '/' + bar_code + '.json')
        r_prod_json = r_prod.json()
        data_prod = r_prod_json['product'] # type(data_prod) = dict
        nutri_score_prod = data_prod['nutrition_grade_fr']
        # We can simply do: list_of_categories = data_prod['categories_hierarchy'], and delete this 5 rows
        d = {len(data_prod['categories_hierarchy']): data_prod['categories_hierarchy'],
             len(data_prod['categories'].split(',')): data_prod['categories'].split(','),
             len(data_prod['categories_tags']): data_prod['categories_tags']
        }
        len_list = max(d.keys())
        # We take the field hwo contains tho most categories
        list_of_categories = d[len_list]
        categories_dict = {}
        for name_cat in list_of_categories:
            # exemple: requests.get('https://fr.openfoodfacts.org/categorie/boissons-sans-alcool/1.json')
            r_cat = requests.get(self.url_cat[0:-8] + '/' + name_cat + '/1.json')
            r_cat_json = r_cat.json()
            nb_prod = r_cat_json['count']
            categories_dict[nb_prod] = name_cat
        min_nb_prod = min(categories_dict.keys())
        cat_with_min_prod = categories_dict[min_nb_prod]
        i = 1
        nutri_score = ''
        # We search on the category that contains the least products
        while not nutri_score:
            r = requests.get(self.url_cat[0:-8] + '/' + cat_with_min_prod + '/' + str(i) + '.json')
            r_json = r.json()
            data_products = r_json['products']
            dict_description = {}
            # We research on only 10 pages so as not to take too much time to find a substitute
            if i > 10:
                print("Ce produit n'a pas de substitut de meilleur qualité")
                return dict_description
            # If the category contains less then 10 pages ( ex: 6p), so beyond the 6th pages data_products = []
            if not data_products:
                print("Ce produit n'a pas de substitut de meilleur qualité")
                return dict_description

            for prod_details in data_products:
                if 'nutrition_grade_fr' in prod_details and prod_details['nutrition_grade_fr'] != '':
                    n = prod_details['nutrition_grade_fr']
                    # If the nutri_score of the substitute is better than that of the product so we take this substitute
                    if dict_nutri_score[n] < dict_nutri_score[nutri_score_prod]:
                        nutri_score = n.upper()
                        if 'product_name' in prod_details:
                            dict_description['product_name'] = prod_details['product_name']
                            dict_description['nutri_score'] = nutri_score
                        if 'brands' in prod_details:
                            dict_description['brands'] = prod_details['brands']
                        if 'quantity' in prod_details:
                            dict_description['quantity'] = prod_details['quantity']
                        if 'ingredients_text' in prod_details:
                            dict_description['ingredients_text'] = prod_details['ingredients_text']
                        if 'stores' in prod_details:
                            dict_description['stores'] = prod_details['stores']
                        if 'url' in prod_details:
                            dict_description['url'] = prod_details['url']
                        return dict_description

            i += 1


class Database:
    def __init__(self, user, password, name_db):
        self.user = user
        self.password = password
        self.name_db = name_db
        self.insert = True
        self.is_connected = False
        try:
            self.cnx = mysql.connector.connect(host='localhost',
                                          user=self.user,
                                          password=self.password,
                                          )
            self.cnx.get_warnings = True
            if self.cnx.is_connected():
                print(f'vous etes connecté en tant que {self.user}')
                self.is_connected = True

        except mysql.connector.Error as e:
            print(e)


    def create_db(self):
        # We will not try to create DB if we are not connected (wrong password or user ...)
        if self.is_connected:
            cursor = self.cnx.cursor()
            query_create = f"CREATE DATABASE IF NOT EXISTS {self.name_db}"
            query_use = f"USE {self.name_db}"

            try:
                cursor.execute(query_create)
                # If DB exists we will have a warning so we skip this step
                if not cursor.fetchwarnings():
                    print(f"Création de la base de données {self.name_db}...")
                cursor.execute(query_use)


            except mysql.connector.Error as e:
                print(e)

    def create_tables(self):
        cursor = self.cnx.cursor()
        query_category = ("CREATE TABLE IF NOT EXISTS Category ("
                 "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT, "
                 "name VARCHAR(100) NOT NULL, "
                 "PRIMARY KEY (id)"
                 ")"
                 "ENGINE=InnoDB"
                 )
        query_product = ("CREATE TABLE IF NOT EXISTS Product ("
                          "id INT UNSIGNED NOT NULL AUTO_INCREMENT, "
                          "name VARCHAR(255) NOT NULL, "
                          "nutri_score CHAR(1), "
                          "bar_code CHAR(13) NOT NULL, "
                          "category_id SMALLINT UNSIGNED NOT NULL, "
                          "PRIMARY KEY (id), "
                          "CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Category(id)"
                          ")"
                          "ENGINE=InnoDB"
                          )

        query_substitut = ("CREATE TABLE IF NOT EXISTS Substitut ("
                           "id INT UNSIGNED NOT NULL AUTO_INCREMENT, "
                           "product_id INT UNSIGNED NOT NULL, "
                           "name VARCHAR(255) NOT NULL, "
                           "brand TEXT, "
                           "quantity VARCHAR(200), "
                           "ingredients TEXT, "
                           "nutri_score CHAR(1), "
                           "stores TEXT, "
                           "url VARCHAR(255), "
                           "PRIMARY KEY (id), "
                           "CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Product(id), "
                           "UNIQUE INDEX ind_uni_url (url)"
                           ")"
                           "ENGINE=InnoDB"
                           )
        try:
            if self.is_connected:
                cursor.execute(query_category)
                cursor.execute(query_product)
                cursor.execute(query_substitut)
                if cursor.fetchwarnings():
                    # If table already exists we turn "self.insert" into false to not insert data again
                    self.insert = False


        except mysql.connector.Error as e:
            print(e)

    def insert_data(self):
        # If we are not connected due to wrong password or for another reason, we will have an exception if we try
        # to insert data so we make an if to avoid that
        if self.is_connected and self.insert:
            cursor = self.cnx.cursor()

            # INSERT LIST OF CATEGORY
            query_cat = "INSERT INTO Category (name) VALUES (%s)"
            list_of_categories = OpenFoodFact('https://fr.openfoodfacts.org/categories&json=1', None).get_category()
            print(f'Récupération des catégories: {list_of_categories}')
            list_of_tuple = []
            for name_of_cat in list_of_categories:
                name = name_of_cat,
                list_of_tuple.append(name)
            try:
                cursor.executemany(query_cat, list_of_tuple)
                self.cnx.commit()

            except mysql.connector.Error as e:
                print(e)

            # INSERT LIST OF PRODUCTS
            query_product = ("INSERT INTO Product (name, nutri_score, bar_code, category_id) " 
                            "VALUES (%s, %s, %s, %s)")
            dict_cat_prod = OpenFoodFact('https://fr.openfoodfacts.org/categories&json=1', None).get_product()
            try:
                for cat_id, dict_prod in dict_cat_prod.items():
                    for prod, values in dict_prod.items():
                        # values is a list that contains nutri_score and bar_code
                        cursor.execute(query_product, (prod, values[0], values[1], cat_id))
                self.cnx.commit()

            except mysql.connector.Error as e:
                print(e)

    def select_cat(self):
        cursor = self.cnx.cursor()

        query_cat = "SELECT name FROM Category "
        cursor.execute(query_cat)

        i = 1
        dict_cat = {}
        for name in cursor:

            dict_cat[i] = ''.join(name)
            i += 1
        return dict_cat


    def select_prod_from_cat(self, dict_cat, response):
        cursor = self.cnx.cursor()

        query_prod_from_cat = ("SELECT Product.name, Product.nutri_score, Product.bar_code FROM Category " 
                            "INNER JOIN Product ON Product.category_id = Category.id " 
                            "WHERE Category.name = %s ORDER BY name")
        name_cat = dict_cat[response],
        cursor.execute(query_prod_from_cat, name_cat)
        dict_prod_from_cat = {}
        while True:
            rows = cursor.fetchmany(size=100)
            if not rows:
                break
            i = 1
            for name_prod, nutri_score, bar_code in rows:
                dict_prod_from_cat[i] = [name_prod, bar_code, nutri_score]
                i += 1
        return dict_prod_from_cat

    def select_prod(self):
        cursor = self.cnx.cursor()
        query_prod = "SELECT name, nutri_score, bar_code FROM Product ORDER BY name"
        cursor.execute(query_prod)
        rows = cursor.fetchmany(size=500)
        i = 0
        dict_prod = {}
        for name_prod, nutri_score, bar_code in rows:
            i += 1
            dict_prod[i] = [name_prod, bar_code, nutri_score]
        return dict_prod

    def select_substitut(self):
        cursor = self.cnx.cursor()
        query_subst = "SELECT name, nutri_score, brand, quantity, ingredients, stores, url FROM Substitut"
        cursor.execute(query_subst)
        for i in cursor:
            print('nom du substitut:', i[0])
            print('nutri_score:', i[1])
            print('marque(s):', i[2])
            print('quantity:', i[3])
            print('ingredients:', i[4])
            print('stores:', i[5])
            print('url:', i[6])
            print(50 * '-')


    def save_substitut(self, bar_code_prod, dict_description):
        cursor = self.cnx.cursor()

        query_id = "SELECT id FROM Product WHERE bar_code = %s"
        arg = bar_code_prod
        cursor.execute(query_id, (arg,))
        id = 0
        for i in cursor:
            id = i[0]
        query_insert_sub = ("INSERT INTO Substitut (product_id, name, brand, "
                            "quantity, ingredients, nutri_score, stores, url) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        args = (id, dict_description['product_name'], dict_description['brands'],
                dict_description['quantity'], dict_description['ingredients_text'],
                dict_description['nutri_score'], dict_description['stores'],
                dict_description['url'])
        cursor.execute(query_insert_sub, args)
        self.cnx.commit()
        print("Substitut enregistrer")




"""
        elif table == 'Product':
            pass

        elif table == 'Substitut':
            pass"""












