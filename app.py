# -*- coding: utf-8 -*-
from __future__ import division, print_function
from scripts import tabledef
from scripts import forms
from scripts import helpers
import json
import sys
import os
import time
import glob
import re
import numpy as np
import json
import run_qa
import tensorflow as tf

# Flask utils
from flask import Flask, flash, redirect, url_for, render_template, request, session, jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only

print('Model loaded')

# Heroku
#from flask_heroku import Heroku
#heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    y=''
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    y = 'olduser' 
                    session["y"]=y 
                    return json.dumps({'status': 'Login successful'}) 
                return json.dumps({'status': 'Invalid user/pass'}) 
            return json.dumps({'status': 'Both fields required'})   
        return render_template('login.html', form=form)
    user = helpers.get_user()
    #return render_template('home.html', user=user) 
    if session.get("y",None)=='olduser':
        session["y"]='done'   
        return render_template('index.html')
    return render_template('charge.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    #helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['password'] = password
                    session['username'] = username
                    session['email'] = email
                    return json.dumps({'status': 'Make Payment'})    
                return json.dumps({'status': 'Username taken'})    
            return json.dumps({'status': 'User/Pass required'})    
        return render_template('login.html', form=form)   
    return redirect(url_for('login'))
    #return render_template('charge.html')

# -------- Charge ---------------------------------------------------------- #
@app.route('/charge', methods=['GET', 'POST'])
def charge():
    if session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = session.get("username",None)
            password = session.get("password",None)
            email = session.get("email",None)
            coupon = request.form['coupon'].lower()
            if coupon == 'ctsfree':
                paymentflag = 'Y'
                helpers.add_user(username, password, email, paymentflag)
                return render_template('payss.html')
            return json.dumps({'status': 'Payment not successfull'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# -------- relogin ---------------------------------------------------------- #
@app.route('/relogin', methods=['GET', 'POST'])
def relogin():
    session['logged_in'] = False
    return redirect(url_for('login'))




# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


# -------- Get Answer Home page ---------------------------------------------------------- #
@app.route('/getanswer', methods=['GET', 'POST'])
def getanswer():
    if request.method == 'POST':
        return render_template('qa.html')    

# -------- Get the Answer ---------------------------------------------------------- #

@app.route('/answer', methods=['POST'])
def answer():
    question = request.form['question']
    # Convert data to squad json format
    x = {
            "version": "BioASQ6b", 
            "data": [
                {
                    "title": "BioASQ6b", 
                    "paragraphs": [ 
                        {
                            "context": question, 
                            "qas": [
                                {
                                    "question": question, 
                                    "id": "56c073fcef6e394741000020_000"
                                }
                            ]
                        }
                    ]
                }
            ]       
        }
    y = json.dumps(x)
    fo= open("./BIOASQ_DIR/Question.json", "w")
    fo.writelines(y)
    fo.close()
    run_qa.main()
    with open("./tmp/QA_output/predictions.json") as f:
        answer_mod = json.load(f)
    f.close()
    for k in answer_mod:
        answer = answer_mod[k]

    return render_template('answ.html',question=question, answer=answer)

# ======== Main ============================================================== #
if __name__ == "__main__":
    #app.run(debug=True, use_reloader=True)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
