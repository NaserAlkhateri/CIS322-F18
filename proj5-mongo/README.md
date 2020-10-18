Author: Naser Alkhateri
Email: nalkhate@uoregon.edu 
Description:
In this project we added the submit and display buttons to our ACP time calculator.
Implementation of recieving the submitted data are in the function new which takes the control distance and opening and closing times and save them so todo.html which is basically the display page iterates and displays in a table'ish format.
File needs credential.ini for docker to build.
Use this command line to run: bash run.sh
Error handling:
If submit  with no input will throw an error redirect to 404.html 
If requested display with no prior submisstion will also throw an error. /n