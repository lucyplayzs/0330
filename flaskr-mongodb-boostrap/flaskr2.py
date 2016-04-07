# -*- coding: utf-8 -*-
# all the imports
import os

from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash
from contextlib import closing
import pymongo
from pymongo import MongoClient
#create our little application
app=Flask(__name__)


app.config.update(dict(
    DATABASE="text",
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='czs',
    PASSWORD='123456'
    ))

print app.config['DATABASE']


def connect_db():
    client = MongoClient("localhost", 27017)
    db = client.test
    return db


@app.before_request
def before_request():
    g.db=connect_db()
@app.route('/')

def first_page():
    entries=[dict(title=row['title'],text=row['text'])for row in g.db.posts.find()]
    return render_template('layout.html',entries=entries)
@app.route('/show')


def show_entries():
    entries=[dict(title=row['title'],text=row['text'])for row in g.db.posts.find()]
    return render_template('show_entries.html',entries=entries)
@app.route('/add',methods=['POST'])


def add_entry():
    if not session.get('logged_in'):
        abort(401)
    post = {"title":request.form['title'],"text":request.form['text']}
    g.db.posts.insert(post)

    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/delete',methods=['POST'])
def delete_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('delete from entries (title,text) values(?,?)',[request.form['title'],request.form['text']])
    g.db.commit()
    flash('A entry was successfully delete')
    return redirect(url_for('show_entries')) 


@app.route('/login',methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        if request.form['username']!=app.config['USERNAME']:
            error='Invalid username'
        elif request.form['password']!=app.config['PASSWORD']:
            error='Invalid password'
        else:
            session['logged_in']=True
            flash('You were logged_in')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('first_page'))
if __name__=='__main__':
    app.run()