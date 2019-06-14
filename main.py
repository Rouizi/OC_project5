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
                database.select_data('Category')
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