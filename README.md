# OC_project5


The startup Pur Beurre noticed that their users wanted to change their diet but did not know where to start. Replace Nutella with hazelnut paste, yes, but which one? And in which store to buy it? Their idea is to create a program that would interact with the Open Food Facts database to retrieve food, compare it and offer the user a healthier substitute for the food that makes him want.


## Description of the user path
The user is on the terminal. The terminal shows him the following choices:

1 - Which food do you want to replace?<br/>
2 - Find my substituted foods.

The user selects 1. The program asks the user the following questions and the user selects the answers:

  - Select the category. [Several proposals associated with a number. The user enters the corresponding digit and presses enter]<br/>
  - Select the food. [Several proposals associated with a number. The user enters the digit corresponding to the chosen food and presses      enter]<br/>
  - The program offers a substitute, its description, a store where to buy it (if any) and a link to the Open Food Facts page about that food.<br/>
  - The user then has the possibility to save the result in the database.
  
If the user selects 2, the program displays the result of the searches already done thus avoiding to redo a search in the database.

## Features

- Food search in the Open Food Facts database.
- The user interacts with the program in the terminal, but if you want to develop a graphical interface you can,
- If the user enters a character that is not a digit, the program must repeat the question,
- The search must be done on a MySQL basis.


## Steps
#### 1 - Organize your work

Cut your program into user stories and then into tasks and subtasks. Create an agile table and assign deadlines.

Before coding, initialize a Github repo and make your first push.

Then start writing the documentation. Yes, first! I propose a work methodology quite recognized in the world of development: the "Doc Driven Development" or "Readme Driven Development". Just create a text file called Readme.txt.

<aside data-claire-semantic = "information">
You can use the Markdown syntax if you already know it. To do this, simply call your Readme.md document.


When you start a new feature, write the documentation first. What do you want your program to do? How will the developer understand the code? Then code what you need for your program to "validate" the Readme.


#### 2 - Build the database
Before you start the different features of your Readme, start by asking yourself about the information you need and draw the schema of the database. What information will you record? What data will you manipulate?

Then interest youself in external data. The Open Food Facts database has an API (experimental at the moment) that allows you to retrieve the desired data in JSON format. You can consult the documentation of this API.

Create the database: tables and foreign keys.

Then write a Python script that will insert the collected data from the API into your database.

<aside data-claire-semantic = "warning">
The users of the Pur Beurre startup are French and are probably doing their shopping in France. It is not necessary to import the entire database, especially since it is so large that it would slow down your program considerably (and make your users run away).



#### 3 - Build the program
List the features of your program to ask about the responsibilities of each class. Then build the desired architecture.

#### 4 - Interact with the database
You have the database and you have the classes. Bravo! Now, allow your user to interact with the database.

Start by working on the answer question system (input, field validation). Then focus on the search: which SQL queries? In which table (s)?

Finally, find how to save the data generated by the program for the user to find them.


## Deliverables
- Physical model of data (or relational model) and using the computer tool of your choice (no freehand drawing!).
- Script for creating your database
- Source code published on Github
- Table Trello, Taiga or Pivotal Tracker.
- Text document explaining the approach chosen, the difficulties encountered and the solutions found and including the link to your source code on Github. In particular, develop the choice of algorithm and the project methodology chosen. Explain also the difficulties encountered and the solutions found. The document must be in pdf format and not exceed 2 A4 pages. It can be written in either English or French, but take into consideration that spelling and grammar mistakes will be evaluated!
## Constraints
- Your code will be written in English: variables, function names, comments, documentation, ...
- Your project will be versioned and published on Github so that your mentor can leave comments.
## Importante note

For certain products the program offers a not very convincing substitute, this is due to the fact that to find a substitute the program will look for the categories in which the product belongs and then try to find a substitute for the category that contains the least product.

So if we take, for example, the product "Kiri à la crème de lait (12 Portions)" (https://fr.openfoodfacts.org/produit/3073780258098/kiri-a-la-creme-de-lait-12-portions) the program will look for a substitute in the "Gouter" category (https://fr-en.openfoodfacts.org/category/gouter) so it could offer us "Grany cereal chocolate" as a substitute, which is not really a substitute. 

For the product "Kiri à la crème de lait (12 Portions)" he will not offer us "Grany cereals chocolate" since he does not have a better nutri_score but I gave an example to know that it can happen for other products
## At the launch of the program

To be able to use the program you must either connect with the user "root" (administrator having all rights) or create a new user and give him all the rights on the database 'alimentation'.

If you choose to create a new user to use the program, do like this:

Connect to mysql with "root" and then type this query:

CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON alimentation.* TO 'username'@'localhost';

If you need some help contact me on: cinorouizi@hotmail.fr or on facebook search: Yacine Rouizi.
