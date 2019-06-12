from classes import OpenFoodFact
from classes import Database


def main():
    database = Database('root', 'Lalydydu1456', 'alimentation')
    database.create_db()
    database.create_tables()
    database.insert_data()



    main_menu = True
    while main_menu:

        print("1- Quel aliment souhaitez-vous remplcer ?\n"
              "2- Retrouver mes aliments substitués")
        response1 = input('\n:')

        try:
            response1 = int(response1)
        except ValueError:
            print("vous n'avez pas saisi de nombre")
            continue

        if int(response1) == 1:

            print("a- Sélectionnez la catégorie\n"
                  "b- Sélectionnez un produit")
            print("\n")
            response2 = input(':')

            if response2 == 'a':
                database.select_data('Category')
            elif response2 == 'b':
                pass
            else:
                print("Vous n'avez pas saisi de réponse valide")
                continue

        elif int(response1) == 2:
            pass
        else:
            print("Vous n'avez pas saisi une réponse valide")

        database.cnx.cursor().close()
        database.cnx.close()



main()


"""
DROP TABLE Substitut, Product, Category;
"""