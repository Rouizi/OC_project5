import mysql.connector
from classes import OpenFoodFact
from classes import Database

database = Database('root', 'Lalydydu1456', 'alimentation')
database.create_db()
database.create_tables()
database.insert_data()



def main():
    main_menu = True
    choice_cat = False

    while main_menu:

        print(45 * '-')
        print("1- Quel aliment souhaitez-vous remplcer ?\n"
              "2- Retrouver mes aliments substitués\n"
              "3- Quitter le programme")
        response1 = input(':')
        print(45 * '-')

        try:
            response1 = int(response1)
        except ValueError:
            print("vous n'avez pas saisi de nombre")
            continue

        if int(response1) == 1:

            seconday_menu = True
            while seconday_menu:
                print("a- Sélectionnez une catégorie\n"
                      "b- Sélectionnez un produit")

                response2 = input(':')
                print(45 * '-')
                if response2 == 'a':
                    choice_cat = True
                    choice_prod = True
                    dict_cat = database.select_cat()
                    for i, name_cat in dict_cat.items():
                        print(str(i) + '-', name_cat)

                elif response2 == 'b':
                    choice_prod = True
                    dict_prod = database.select_prod()
                    dict_prod_displayed = {}
                    l = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
                    for i, (name_prod, bar_code, nutri_score,) in dict_prod.items():
                        print(str(i) + '-', name_prod, '### NUTRI_SCORE:', nutri_score)
                        dict_prod_displayed[i] = [name_prod, bar_code, nutri_score]
                        if i in l:
                            lock = True
                            while lock:
                                print(45 * '-')
                                reponse = input("Afficher les 50 prochains produits o/n ?: ")
                                print(45 * '-')
                                if reponse != 'o' and reponse != 'n':
                                    print("Vous n'avez pas saisi de réponse valide")
                                    continue
                                else:
                                    lock = False

                            if reponse == 'o':
                                continue
                            elif reponse == 'n':
                                break
                    dict_prod = dict_prod_displayed

                else:
                    print("Vous n'avez pas saisi de réponse valide")
                    continue


                while choice_cat:
                    print(45 * '-')
                    cat_id = input('Sélectionnez une catégorie:')
                    print(45 * '-')

                    try:
                        cat_id = int(cat_id)
                    except ValueError:
                        print("Vous n'avez pas saisi de nombre")
                        continue

                    if cat_id not in dict_cat.keys():
                        print("Vous n'avez pas saisi un nombre valide")
                        continue
                    else:
                        dict_prod_from_cat = database.select_prod_from_cat(dict_cat, cat_id)
                        for i, (name_prod, bar_code, nutri_score) in dict_prod_from_cat.items():
                            print(str(i) + '-', name_prod, '### NUTRI_SCORE', nutri_score)

                        dict_prod = dict_prod_from_cat
                        choice_cat = False


                while choice_prod:
                    print(45 * '-')
                    prod_id = input("Sélectionnez un produit: ")
                    print(45 * '-')

                    try:
                        prod_id = int(prod_id)
                    except ValueError:
                        print("Vous n'avez pas saisi de nombre")
                        continue

                    if prod_id not in dict_prod.keys():
                        print("Vous n'avez pas saisi un nombre valide")
                        continue
                    else:
                        bar_code_prod = dict_prod[prod_id][1]
                        dict_description= OpenFoodFact('https://fr.openfoodfacts.org/categories&json=1',
                                    'https://fr.openfoodfacts.org/api/v0/produit').get_substitut(bar_code_prod)
                        name_prod = dict_prod[prod_id][0]

                        if dict_description:
                            if 'product_name' not in dict_description.keys():
                                dict_description['product_name'] = ''
                            if 'nutri_score' not in dict_description.keys():
                                dict_description['nutri_score'] = ''
                            if 'brands' not in dict_description.keys():
                                dict_description['brands'] = ''
                            if 'quantity' not in dict_description.keys():
                                dict_description['quantity'] = ''
                            if 'ingredients_text' not in dict_description.keys():
                                dict_description['ingredients_text'] = ''
                            if 'stores' not in dict_description.keys():
                                dict_description['stores'] = ''
                            if 'url' not in dict_description.keys():
                                dict_description['url'] = ''

                            print('nom du produit:', name_prod)
                            print('nutri_score du produit:', dict_prod[prod_id][2])
                            print('nom du substitut:', dict_description['product_name'])
                            print('nutri_score:', dict_description['nutri_score'])
                            print('marque(s):', dict_description['brands'])
                            print('quantité:', dict_description['quantity'])
                            print('ingrédients:', dict_description['ingredients_text'])
                            print('magasin(s):', dict_description['stores'])
                            print('url:', dict_description['url'])

                        else:
                            continue

                        choice = False
                        while not choice:
                            print(45 * '-')
                            print('1- Enregistrer substitut\n'
                                  '2- Sélectionner un autre produit\n'
                                  '3- Retourner au menu secondaire\n'
                                  '4- Retourner au menu principal')
                            response3 = input(': ')
                            print(45 * '-')

                            try:
                                response3 = int(response3)
                            except ValueError:
                                print("Vous n'avez pas saisi de réponse valide")
                                continue
                            if response3 not in (1, 2, 3, 4):
                                print("Vous n'avez pas saisi un nombre valide")

                            if response3 == 1:
                                try:
                                    database.save_substitut(bar_code_prod, dict_description)
                                except mysql.connector.Error:
                                    print("Vous avez déjà enregistrer ce substitut")
                                    continue
                            elif response3 == 2:
                                choice = True
                            elif response3 == 3:
                                choice = True
                                choice_prod = False
                            elif response3 == 4:
                                choice = True
                                choice_prod = False
                                seconday_menu = False

        elif int(response1) == 2:
            database.select_substitut()
        elif int(response1) == 3:
            print("A bientôt sur OpenFoodFacts")
            main_menu = False
        else:
            print("Vous n'avez pas saisi une réponse valide")



main()
database.cnx.cursor().close()
database.cnx.close()

"""
DROP TABLE Substitut, Product, Category;
"""