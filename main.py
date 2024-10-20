from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_cors import CORS
from config import DevelopmentConfig
from io import BytesIO

import models
import base64

import matplotlib.pyplot as ptl
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
app.config.from_object(DevelopmentConfig)

#DECORADORES O RUTAS
@app.route('/api', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)


