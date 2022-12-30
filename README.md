Bank by Nick Deupree
Readme aided by ChatGPT
A program that allows users to track their finances.

Part 1
This part of the code includes the necessary imports and global variables, as well as functions for handling the key, logging, balance, and transactions.

The load_key function reads the key from the file "key.key".

The clearLogs function clears the contents of the file "logs.dat".

The getBalance function gets the balance from the file "bal.dat" and creates the file if it does not exist. If the file is empty, the balance is set to 0.00.

The writeBalance function writes the balance to the file "bal.dat" and updates the balance label in the user interface.

The add function adds money to the balance and writes it to the file "bank.dat". It also updates the text widget in the user interface and clears the amount and description entries.

The delete function subtracts money from the balance and writes it to the file "bank.dat". It also updates the text widget in the user interface and clears the amount and description entries.

The updateText function reads the contents of the file "bank.dat", decrypts the messages using the key, and updates the text widget in the user interface.

Part 2

This part of the Bank program includes the main window and its user interface. The user interface includes a sidebar with controls for changing the allowance amount and day of the week, as well as a dropdown menu for selecting the appearance mode. It also includes a text widget for displaying transaction history, a balance label, and entries and buttons for adding and deleting money. There is also a button for clearing the transaction history and balance.

The sidebarCollapseCommand function collapses or expands the sidebar when the collapse button is clicked.

The allowanceAmountButtonCommand function changes the allowance amount when the "Change Amount" button is clicked.

The allowanceDayOfTheWeekDropDownCommand function changes the allowance day of the week when a new option is selected from the dropdown menu.

The modeDropDownCommand function changes the appearance mode when a new option is selected from the dropdown menu.

The clearButtonCommand function clears the transaction history and balance when the "Clear Files" button is clicked.

The addMoneyButtonCommand function adds money to the balance and transaction history when the "Add Money" button is clicked.

The deleteMoneyButtonCommand function subtracts money from the balance and adds it to the transaction history when the "Delete Money" button is clicked.

The quitButtonCommand function quits the program when the "Quit" button is clicked



Regenerate response