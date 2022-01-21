from blog import app
from blog import db
from flask import render_template, redirect, url_for, flash, request


@app.route('/info')
def info_page():
    return render_template('info.html')


@app.route('/')
@app.route('/feed')
def feed_page():
    return render_template('feed.html')
