from system_monitor import app
from flask import render_template


# These don't actually work for some reason, even when the decorators 
# take an Exception instead of an error code... hmmm...

@app.errorhandler(404)
def error_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_internal(error):
    db.session.rollback()
    return render_template('500.html'), 500



