#app.py
import os #to check for the files
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", defaults={'path': ''})#catches the path and pass it to the path argument
@app.route("/<path:path>")
def hello(path):
    #the typed url will be passed in this function and
    #will go through certain checks and then will be looked for
    #in the templates directory, if found it will load.
    fileDir = "templates/" + path #the path directory for the files
    if path == "": #when nothing is passed
        return "Welcome to the homepage",200    
    if path.endswith(('.css' , '.html')):
        if '//' in path or '..' in path or '~' in path:
            return error_403()
        elif path.startswith('//'):
            return error_403()
        elif os.path.isfile(fileDir):
           return render_template(path), 200
        else:
            return error_404()
    else:
        return error_401()

#error returners
def error_401():
    return("Doesn't follow the typical format")
def error_403():
    return render_template("403.html"), 403
def error_404():
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
