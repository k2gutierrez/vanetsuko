from urllib.error import HTTPError
from flask import Flask, render_template, request, redirect, url_for, session, Response
import pyrebase
import os
from datetime import date
from math import pi

from requests import RequestException

app = Flask(__name__)

app.secret_key = os.urandom(24)

firebaseConfig = {
    'apiKey': "AIzaSyDm_ixM4ucAE7ApU7zEl9coPoAQGoLMoFM",
    'authDomain': "vanetsuko-26cea.firebaseapp.com",
    'databaseURL': 'https://vanetsuko-26cea-default-rtdb.firebaseio.com/',
    'projectId': "vanetsuko-26cea",
    'storageBucket': "vanetsuko-26cea.appspot.com",
    'messagingSenderId': "321227997578",
    'appId': "1:321227997578:web:26c76b2e9e4f5b38dd4873"
}

#Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
#authentication
auth = firebase.auth()
#Storage
storage = firebase.storage()
#Database
db=firebase.database()

#########################################################################################
@app.route('/', methods= ['POST', 'GET'])
def home():

    nombre = ''
    mensaje = ''
    seleccion = ''
    message = ''
    info = {}

    if request.method == "POST":
        nombre = str(request.form.get('nombre'))
        mensaje = str(request.form.get('mensaje'))
        seleccion = str(request.form.get('flexRadioDefault'))
        info = {
            'nombre': nombre,
            'mensaje': mensaje,
            'eleccion': seleccion
        }
        if nombre == '' or mensaje == '':
            message = 'Debes llenar los campos para poder mandar mensaje'
            return render_template('home.html', message=message, nombre=nombre, mensaje=mensaje, seleccion=seleccion, info=info)
        elif nombre != '' and mensaje != '' and seleccion == 'no':
            db.child('no asisten').push(info)
            return redirect(url_for('.noasisten'))
        elif nombre != '' and mensaje != '' and seleccion == 'si':
            db.child('asisten').push(info)
            return redirect(url_for('.asisten'))

    return render_template('home.html', message=message, nombre=nombre, mensaje=mensaje, seleccion=seleccion, info=info)

#########################################################################################

@app.route('/asisten', methods= ['POST', 'GET'])
def asisten():

    t = 0

    all = db.child('asisten').get()
    if all.val() is None:
        t = 0
        return render_template('asisten.html', all=all, t=t)
    elif all.val() is not None:
        t = 1
        return render_template('asisten.html', all=all, t=t)

    return render_template('asisten.html', all=all, t=t)
    
#########################################################################################

@app.route('/noasisten', methods= ['POST', 'GET'])
def noasisten():

    t = 0

    all = db.child('no asisten').get()
    if all.val() is None:
        t = 0
        return render_template('noasisten.html', all=all, t=t)
    elif all.val() is not None:
        t = 1
        return render_template('noasisten.html', all=all, t=t)

    return render_template('noasisten.html', all=all, t=t)
    
#########################################################################################

if __name__ == "__main__":
    app.run(threaded=True, debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))