import mysql.connector
from classes import OpenFoodFact
from classes import Database

database = Database('root', 'Lalydydu1456', 'alimentation')
database.create_db()
database.create_tables()
database.insert_data()

def main():
    main_menu = True
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

            print("a- Sélectionnez une catégorie\n"
                  "b- Sélectionnez un produit")

            response2 = input(':')
            print(45 * '-')
            if response2 == 'a':
                dict_cat = database.select_cat()
                for i, name_cat in dict_cat.items():
                    print(str(i) + '-', name_cat)

                choice_cat = False
                while not choice_cat:
                    print(45 * '-')
                    response3 = input('Sélectionnez une catégorie:')
                    print(45 * '-')

                    try:
                        response3 = int(response3)
                    except ValueError:
                        print("Vous n'avez pas saisi de nombre")
                        continue

                    if response3 not in dict_cat.keys():
                        print("Vous n'avez pas saisi un nombre valide")
                        continue
                    else:
                        dict_prod = database.select_prod_from_cat(dict_cat, response3)
                        for i, (name_prod, bar_code, nutri_score) in dict_prod.items():
                            print(str(i) + '-', name_prod, '### NUTRI_SCORE', nutri_score)

                    choice_prod = False
                    while not choice_prod:
                        print(45 * '-')
                        response4 = input("Sélectionnez un produit: ")
                        print(45 * '-')

                        try:
                            response4 = int(response4)
                        except ValueError:
                            print("Vous n'avez pas saisi de nombre")
                            continue

                        if response4 not in dict_prod.keys():
                            print("Vous n'avez pas saisi un nombre valide")
                            continue
                        else:
                            bar_code_prod = dict_prod[response4][1]
                            dict_description= OpenFoodFact('https://fr.openfoodfacts.org/categories&json=1',
                                        'https://fr.openfoodfacts.org/api/v0/produit').get_substitut(bar_code_prod)
                            name_prod = dict_prod[response4][0]

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
                                print('nutri_score du produit:', dict_prod[response4][2])
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
                                      '3- Sélectioner une autre catégorie\n'
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
                                        database.save_substitut(bar_code_prod, dict_description, name_prod)
                                    except mysql.connector.Error:
                                        print("Vous avez déjà enregistrer ce substitut")
                                        continue

            elif response2 == 'b':
                pass
            else:
                print("Vous n'avez pas saisi de réponse valide")
                continue

        elif int(response1) == 2:
            pass
        elif int(response1) == 3:
            pass
        else:
            print("Vous n'avez pas saisi une réponse valide")



main()
database.cnx.cursor().close()
database.cnx.close()

"""
DROP TABLE Substitut, Product, Category;
"""