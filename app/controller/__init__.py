from flask import request, render_template, abort
from app.model.user import User
from app import app

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(error):
    return render_template('403.html'), 403

def auth_required(func):

    def wraper(*args, **argv):
        uid = request.args.get('uid', 0)
        if uid:
            usr = User.find(uid)
            if usr:
                request.user = usr
                return func(*args, **argv)
        abort(403)
    return wraper