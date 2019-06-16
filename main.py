import mysql.connector
from classes import OpenFoodFact
from classes import Database

access_to_db = False
while not access_to_db:
    database = Database('alimentation')
    access_denied = database.create_db()
    if access_denied:
        print(access_denied)
        print("Use another user")
        continue
    else:
        database.create_tables()
        database.insert_data()
        break



def main():
    main_menu = True
    choice_cat = False

    while main_menu:

        print(45 * '-')
        print("1- What food do you want to replace ?\n"
              "2- Find my substituted foods\n"
              "3- Quit the program")
        response1 = input(': ')
        print(45 * '-')

        try:
            response1 = int(response1)
        except ValueError:
            print("You have not entered a number")
            continue

        if int(response1) == 1:
            seconday_menu = True
            while seconday_menu:
                print(45* '-')
                print("a- Select a category\n"
                      "b- Select a product")

                response2 = input(': ')
                print(45 * '-')
                if response2 == 'a':
                    choice_cat = True
                    choice_prod = True
                    dict_cat = database.select_cat()
                    # Displays all the categories
                    for i, name_cat in dict_cat.items():
                        print(str(i) + '-', name_cat)

                elif response2 == 'b':
                    choice_prod = True
                    dict_prod = database.select_prod()
                    dict_prod_displayed = {}
                    l = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

                    # We display 50 products and we enter in the while loop to ask the user if he want to display
                    # the next 50 products
                    for i, (name_prod, bar_code, nutri_score,) in dict_prod.items():
                        print(str(i) + '-', name_prod, '### NUTRI_SCORE:', nutri_score)
                        dict_prod_displayed[i] = [name_prod, bar_code, nutri_score]

                        if i == 500:
                            break
                        if i in l:
                            lock = True
                            while lock:
                                print(45 * '-')
                                response = input("Display the next 50 products y/n: ")
                                print(45 * '-')
                                if response != 'y' and response != 'n':
                                    print("You did not enter a valid response")
                                    continue
                                else:
                                    lock = False

                            if response == 'y':
                                continue
                            elif response == 'n':
                                break
                    dict_prod = dict_prod_displayed

                else:
                    print("You did not enter a valid response")
                    continue

                while choice_cat:
                    print(45 * '-')
                    cat_id = input('Select a category from the list: ')
                    print(45 * '-')

                    try:
                        cat_id = int(cat_id)
                    except ValueError:
                        print("You have not entered a number")
                        continue
                    # We check if the user enter a valid number of category
                    if cat_id not in dict_cat.keys():
                        print("You have not entered a valid number")
                        continue
                    else:
                        dict_prod_from_cat = database.select_prod_from_cat(dict_cat, cat_id)
                        for i, (name_prod, bar_code, nutri_score) in dict_prod_from_cat.items():
                            print(str(i) + '-', name_prod, '### NUTRI_SCORE', nutri_score)

                        dict_prod = dict_prod_from_cat
                        choice_cat = False


                while choice_prod:
                    print(45 * '-')
                    num_prod = input("Select a product from the list: ")
                    print(45 * '-')

                    try:
                        num_prod = int(num_prod)
                    except ValueError:
                        print("You have not entered a number")
                        continue

                    # We check if the user enter a valid number of products
                    if num_prod not in dict_prod.keys():
                        print("You have not entered a valid number")
                        continue
                    else:
                        bar_code_prod = dict_prod[num_prod][1]
                        dict_description= OpenFoodFact('https://fr.openfoodfacts.org/categories&json=1',
                                    'https://fr.openfoodfacts.org/api/v0/produit').get_substitute(bar_code_prod)
                        name_prod = dict_prod[num_prod][0]

                        # We check if we have a substitute
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

                            print('Product name:', name_prod)
                            print('nutri_score of the product:', dict_prod[num_prod][2])
                            print('substitute name:', dict_description['product_name'])
                            print('nutri_score:', dict_description['nutri_score'])
                            print('brand(s):', dict_description['brands'])
                            print('quantity:', dict_description['quantity'])
                            print('ingredients:', dict_description['ingredients_text'])
                            print('store(s):', dict_description['stores'])
                            print('url:', dict_description['url'])

                        else:
                            continue

                        choice = False
                        while not choice:
                            print(45 * '-')
                            print('1- Save substitute\n'
                                  '2- Select another product\n'
                                  '3- Return to the secondary menu\n'
                                  '4- Return to the main menu')
                            response3 = input(': ')
                            print(45 * '-')

                            try:
                                response3 = int(response3)
                            except ValueError:
                                print("You have not entered a valid answer")
                                continue

                            if response3 not in (1, 2, 3, 4):
                                print("You have not entered a valid number")
                                continue
                            if response3 == 1:
                                try:
                                    database.save_substitute(bar_code_prod, dict_description)
                                except mysql.connector.Error:
                                    print("You already have registered this substitute")
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
            list_of_data = database.select_substitute()
            for substitute in list_of_data:
                print('substitute name:', substitute[0])
                print('nutri_score:', substitute[1])
                print('brand(s):', substitute[2])
                print('quantity:', substitute[3])
                print('ingredients:', substitute[4])
                print('store(s):', substitute[5])
                print('url:', substitute[6])
                print(50 * '-')
        elif int(response1) == 3:
            print("See you soon on OpenFoodFacts")
            main_menu = False
        else:
            print("You have not entered a valid answer")
            continue



main()
database.cnx.cursor().close()
database.cnx.close()

"""
DROP TABLE Substitute, Product, Category;
"""