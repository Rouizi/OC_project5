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

        list_of_category = []
        # We wont to have this category in list_of_category
        category = ['Epicerie', 'Biscuits fourrés', 'Produits à tartiner', 'Biscuits et gâteaux',
                    'Desserts', 'Surgelés', 'Sauces', 'Conserves', 'Chocolats', 'Confitures et marmelades']

        for data_cat in data_categories:  # type(data_cat) = dict
            if data_cat['name'] in category:
                list_of_category.append(data_cat['name'])
            else:
                pass
        return list_of_category

    def get_product(self):
        list_of_category = self.get_category()
        dict_cat_prod = {}
        for i in range(10):
            for page in range(1,10):
                # exemple: requests.get('https://fr.openfoodfacts.org/categorie/Epicerie/1.json')
                r = requests.get(self.url_cat[0:-8] + '/' + list_of_category[i] + '/' + str(page) + '.json')
                r_json = r.json()
                data_products = r_json['products'] # type(tag_product) = list
                dict_prod = {}
                for prod_detail in data_products: # type(prod_detail) = dict
                    # According to the API of the web site some product may not have
                    # 'product_name', 'nutrition_grade_fr' or 'code' in their fiels so we make an if to filter all that
                    if ('product_name' in prod_detail and prod_detail['product_name'] != '' and
                        'nutrition_grade_fr' in prod_detail and prod_detail['nutrition_grade_fr'] != '' and
                        'code' in prod_detail and prod_detail['code'] != ''):
                            dict_prod[prod_detail['product_name']] = [prod_detail['nutrition_grade_fr'].upper(), prod_detail['code']]
                    else:
                        pass
                #If dictionary is empty we can't do dict[x].update(dict2) so we enter in the first case
                if i + 1 not in dict_cat_prod:
                    dict_cat_prod[i + 1] = dict_prod
                else:
                    dict_cat_prod[i + 1].update(dict_prod)
                if len(dict_cat_prod[i + 1]) > 40:
                    dict_cat_prod[i + 1] = dict(list(dict_cat_prod[i + 1].items())[0:40])
                    break
            print(len(dict_cat_prod[i + 1]))
            print(dict_cat_prod)
        return dict_cat_prod

    def get_substitut(self, bar_code):
        dict_nutri_score = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
        # for exemple self.url_prod = 'https://fr.openfoodfacts.org/api/v0/produit/4060800002242.json'
        r_prod = requests.get(self.url_prod + '/' + bar_code + '.json')
        r_prod_json = r_prod.json()
        data_prod = r_prod_json['product'] # type(data_prod) = dict
        nutri_score_prod = data_prod['nutrition_grade_fr']
        print(nutri_score_prod)
        # We can simply do list_of_categories = data_prod['categories_hierarchy'] and delete this 5 rows
        d = {len(data_prod['categories_hierarchy']): data_prod['categories_hierarchy'],
             len(data_prod['categories'].split(',')): data_prod['categories'].split(','),
             len(data_prod['categories_tags']): data_prod['categories_tags']
        }
        print(data_prod['categories'])
        print("data_prod['categories'].split(',') = ", data_prod['categories'].split(','))
        print("data_prod['categories_hierarchy'] = ", data_prod['categories_hierarchy'])
        print("data_prod['categories_tags'] = ", data_prod['categories_tags'])
        len_list = max(d.keys())
        list_of_categories = d[len_list]
        categories_dict = {}
        print('list_of_category', list_of_categories)
        for name_cat in list_of_categories:
            print(name_cat)
            # exemple: requests.get('https://fr.openfoodfacts.org/categorie/boissons-sans-alcool/1.json')
            r_cat = requests.get(self.url_cat[0:-8] + '/' + name_cat + '/1.json')
            r_cat_json = r_cat.json()
            nb_prod = r_cat_json['count']
            categories_dict[nb_prod] = name_cat
            print(categories_dict)
        min_nb_prod = min(categories_dict.keys())
        print(min_nb_prod)
        cat_with_min_prod = categories_dict[min_nb_prod]
        i = 1
        nutri_score = ''
        while not nutri_score:
            r = requests.get(self.url_cat[0:-8] + '/' + cat_with_min_prod + '/' + str(i) + '.json')
            r_json = r.json()
            data_products = r_json['products']
            if not data_products:
                print("Ce produit n'a pas de substitut de meilleur qualité")
                break
            dict_description = {}
            for prod_details in data_products:
                if 'nutrition_grade_fr' in prod_details and prod_details['nutrition_grade_fr'] != '':
                    n = prod_details['nutrition_grade_fr']
                    if dict_nutri_score[n] < dict_nutri_score[nutri_score_prod]:
                        nutri_score = n
                        if 'product_name' in prod_details:
                            product_name = prod_details['product_name']
                            dict_description['product_name'] = product_name
                            dict_description['nutri_score'] = nutri_score
                        if 'brands' in prod_details:
                            brand = prod_details['brands']
                            dict_description['brand'] = brand
                        if 'quantity' in prod_details:
                            quantity = prod_details['quantity']
                            dict_description['quantity'] = quantity
                        if 'ingredients_text' in prod_details:
                            ingredients = prod_details['ingredients_text']
                            dict_description['ingredients'] = ingredients
                        if 'stores' in prod_details:
                            stores = prod_details['stores']
                            dict_description['stores'] = stores
                        if 'url' in prod_details:
                            url = prod_details['url']
                            dict_description['url'] = url
                        print('dict_description = ', dict_description)
                        return dict_description

            i += 1


class Database:
    def __init__(self, user, password, name_db):
        self.user = user
        self.password = password
        self.name_db = name_db
        self.insert = True
        try:
            self.cnx = mysql.connector.connect(host='localhost',
                                          user=self.user,
                                          password=self.password,
                                          )
            self.cnx.get_warnings = True
            if self.cnx.is_connected():
                print('vous etes connecté')

        except mysql.connector.Error as e:
            print(e)


    def create_db(self):
        cursor = self.cnx.cursor()
        query_create = f"CREATE DATABASE IF NOT EXISTS {self.name_db}"
        query_use = f"USE {self.name_db}"

        try:
            print(f"Création de la base de données {self.name_db}...")
            cursor.execute(query_create)
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
                          "name TEXT NOT NULL, "
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
                           "name TEXT NOT NULL, "
                           "marque TEXT, "
                           "quantity VARCHAR(200), "
                           "ingredients TEXT, "
                           "nutri_score CHAR(1), "
                           "stores TEXT, "
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
            if cursor.fetchwarnings():
                self.insert = False

        except mysql.connector.Error as e:
            print(e)

    def insert_data(self):
        if self.insert:
            cursor = self.cnx.cursor()

            # INSERT LIST OF CATEGORY
            query_cat = "INSERT INTO Category (name) VALUES (%s)"
            list_of_category = OpenFoodFact('https://fr.openfoodfacts.org/categories&json=1', None).get_category()
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

            # INSERT LIST OF PRODUCTS
            query_product = ("INSERT INTO Product (name, nutri_score, bar_code, category_id) " 
                            "VALUES (%s, %s, %s, %s)")
            dict_cat_prod = OpenFoodFact('https://fr.openfoodfacts.org/categories&json=1', None).get_product()
            try:
                for cat_id, dict_prod in dict_cat_prod.items():
                    for prod, values in dict_prod.items():
                        # values contains nutri_score and bar_code
                        cursor.execute(query_product, (prod, values[0], values[1], cat_id))
                        self.cnx.commit()

            except mysql.connector.Error as e:
                print(e)

    def select_data(self, table):
        cursor = self.cnx.cursor()

        try:
            if table == 'Category':
                query_cat = "SELECT name FROM Category "
                cursor.execute(query_cat)

                i = 1
                dict_cat = {}
                for name in cursor:
                    print(i, '-', ''.join(name))
                    dict_cat[i] = ''.join(name)
                    i += 1
                print("\n")

                choice_cat = False
                while not choice_cat:
                    response = input('Sélectionnez une catégorie:')

                    try:
                        response = int(response)
                    except ValueError:
                        print("Vous n'avez pas saisi de nombre")
                        continue

                    if response not in dict_cat.keys():
                        print("Vous n'avez pas saisi un nombre valide")
                    else:
                        query_prod_from_cat = ("SELECT Product.name, Product.nutri_score FROM Category " 
                                            "INNER JOIN Product ON Product.category_id = Category.id " 
                                            "WHERE Category.name = %s ORDER BY name")
                        name_cat = dict_cat[response],
                        cursor.execute(query_prod_from_cat, name_cat)
                        dict_prod = {}
                        while True:
                            rows = cursor.fetchmany(size=100)
                            if not rows:
                                break
                            i = 1
                            for row in rows:
                                print(i, '-', ' => NUTRI_SCORE: '.join(row))
                                dict_prod[i] = row
                                i += 1
                        print(dict_prod)
                        print('\n')

                        choice_prod = False
                        while not choice_prod:
                            response2 = input("Sélectionnez un produit: ")

                            try:
                                response2 = int(response2)
                            except ValueError:
                                print("Vous n'avez pas saisi de nombre")
                                continue

                            if response2 not in dict_prod.keys():
                                print("Vous n'avez pas saisi un nombre valide")
                                continue
                            else:
                                name_prod = dict_prod[response2][0]
                                query_bar_code = "SELECT bar_code FROM Product WHERE name = %s"
                                cursor.execute(query_bar_code, (name_prod,))
                                bar_code = ''
                                for i in cursor:
                                    bar_code = ''.join(i)
                                dict_description = OpenFoodFact('https://fr.openfoodfacts.org/categories&json=1',
                                                'https://fr.openfoodfacts.org/api/v0/produit').get_substitut(bar_code)
                                print('nom du produit: ', name_prod)
                                print('NUTRI_SCORE du produit: ', dict_prod[response2][1])
                                for key, value in dict_description.items():
                                    if key == 'product_name':
                                        print('nom du substitut: ',dict_description['product_name'])
                                    if key == 'nutri_score':
                                        print('NUTRI_SCORE du substitut', dict_description['nutri_score'])
                                    if key == 'brands':
                                        print('marque(s) du substitut: ', dict_description['brands'])
                                    if key == 'quantity':
                                        print('quantité du substitut: ', dict_description['quantity'])
                                    if key == 'ingredients_text':
                                        print('ingrédients du substitut: ', dict_description['ingredients_text'])
                                    if key == 'stores':
                                        print('magasin(s) du substitut: ', dict_description['stores'])
                                    if key == 'url':
                                        print('url du substitut: ', dict_description['url'])


            elif table == 'Product':
                pass

            elif table == 'Substitut':
                pass


        except mysql.connector.Error as e:
            print(e)



