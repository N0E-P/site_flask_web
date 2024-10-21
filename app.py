from flask import Flask, abort, render_template, request
import os, json

TEMPLATES = "templates"

app = Flask(__name__, template_folder=TEMPLATES)

@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/animaux")
def animaux():
    with open("animaux.json") as f:
        animaux_data = json.load(f)
    return render_template("animaux.html", animaux=animaux_data)

@app.route("/animaux/<int:id>")
def presentation(id):
    with open("animaux.json") as f:
        animaux_data = json.load(f)
    animal = animaux_data[id]
    return render_template("presentation.html", animal=animal)


@app.route('/animaux/<code>/achat/', methods = ["GET", "POST"])
def achat(code):
    if request.method == "GET":
        return render_template("achat.html", code=code)
    else:
        #Récupérer les données du formulaire
        form = request.form
        print(form)
        print(form["name"])
        print(form["livraison"])
        with open("animaux.json") as f:
            animaux_data = json.load(f)
        animal = animaux_data[int(code)]

        #Ecrire que le vélo n'est plus disponible dans le fichier json
        animaux_data[int(code)]["in_stock"] = animaux_data[int(code)]["in_stock"] - 1
        with open("animaux.json", "w") as f:
            json.dump(animaux_data, f)

        return render_template("bravo.html", nom=form["name"] , livraison=form["livraison"], animal=animal)