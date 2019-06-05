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


##Steps
### 1 - Organize your work

Cut your program into user stories and then into tasks and subtasks. Create an agile table and assign deadlines.

Before coding, initialize a Github repo and make your first push.

Then start writing the documentation. Yes, first! I propose a work methodology quite recognized in the world of development: the "Doc Driven Development" or "Readme Driven Development". Just create a text file called Readme.txt.

<aside data-claire-semantic = "information">
You can use the Markdown syntax if you already know it. To do this, simply call your Readme.md document.

</ Aside>
When you start a new feature, write the documentation first. What do you want your program to do? How will the developer understand the code? Then code what you need for your program to "validate" the Readme.
