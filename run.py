from blog import app
import os

if __name__ == '__main__':
    if not (host := os.environ.get('FLASK_HOST')):
        host = 'localhost'
    if not (port := os.environ.get('FLASK_PORT')):
        port = '5000'
    app.run(host, port)
