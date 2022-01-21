from blog import app


@app.route('/')
@app.route('/home')
def home_page():
    return '<p>Hello World</p>'
