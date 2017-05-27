from flask import render_template, request

from app import app

@app.route('/')
def homepage():
    name = request.args.get('name')
    number = request.args.get('number')
    # Pass name into the template context
    return render_template('homepage.html', name=name, number=number)