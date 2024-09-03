import http.server, socketserver, webbrowser, flask, threading
import wsgiref  
from threading import Thread
from flask import Flask, send_from_directory, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    # Sirve el archivo HTML de la carpeta actual
    return send_from_directory('.', 'index.html')

def abrir_navegador():
    # Abre la página en el navegador predeterminado
    webbrowser.open('http://localhost:5000/')

# Inicia el servidor Flask en un hilo separado
threading.Timer(interval=1, function=abrir_navegador)
app.run(host='0.0.0.0', port=5000, debug=True)