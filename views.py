from flask import render_template, request

from app import app

@app.route('/')
def homepage():
    name = request.args.get('name')
    if not name:
        name = '<unknown>'
    # Pass name into the template context
    return render_template('homepage.html', name=name)