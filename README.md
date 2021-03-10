# Py-wordman

## About
This project is a Password Manager made using python. This program allows you to generate new passwords, and save, view, update and delete your account/password pairs.

## How to Setup
If you have python 3.8.7 already installed, there is no need to follow this first step. To check your python version, simply open your command prompt and type "python -V"

Setting up is simple. First, go to the [Python website link here](https://www.python.org/ftp/python/3.8.7/python-3.8.7-amd64.exe) which will start your python download. When the installer begins, **tick the checkbox that says "Add to Path"**, and then press continue and go through the rest of the installer. 

After the installer is complete, you have now installed python and you are ready to run python programs. Return to this page and press the green button near the top that says Code, press it, and then press Download Zip. 

With the zip file downloaded, simply extract it using your method of choice, putting them in a folder of your choice (remember to keep all files in the same folder). 

Go to the folder where you have the files, and click the bar near the top of your file explorer, where your file path is shown (Something like "This PC > Desktop > MyFolder) as shown in this image ![](https://cdn.discordapp.com/attachments/783070812596731938/807350708667809813/unknown.png). When you click this bar, remove all the text, type cmd and press enter. This will open your command prompt. 

In your command prompt now, type "pip install -r requirements.txt". This will install the required packages. When that is completed, this program is now ready to use. 

From here just double click the main.py file to run it. Easy. I hope this comes in handy. If you have any queries or problems, feel free to email me at isaiahahmadsama@gmail.com with them. Enjoy.


## Features
### Main Menu
The main menu is where you can select 1 of 6 options based on the corresponding number.

### Generate a new password
This is option 1. This function will generate a password of a length that you specify, and will then copy it to your clipboard. After generating, I recommend using the "Save a new Password" function to save your generated password.

### Save a new Password
This is option 2. Allow you to add in the account that you desire and use that as your access to the password. For example. Say I wanted to save the password to like my steam account. For the name I would put Isamabevibin@gmail.com, then for the password I'd put my password of Isamazawarudo21. It will then save it, and it will be able to be accessed again from option 3

### View a password
Option 3 is view. This shows you a list of all that you have registered so far, and allows you to pick the name of the one whose password you wish to view.

### Update a password
Option 4, the update function, allows you to edit the password of an existing "account", say you changed it or had a typo or something. Does not change the account_name itself however, only the value which is the password

### Delete a password
Option 5, allows you to delete a registered account/password pair.

### Exit
Option 6, closes the program.
