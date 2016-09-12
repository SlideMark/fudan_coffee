from flask import render_template
from app import app

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_need_auth(error):
    return render_template('403.html'), 403