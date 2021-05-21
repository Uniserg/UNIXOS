from service.routes import *

if __name__ == "__main__":
    app.run(host='localhost',
            port=10000,
            ssl_context=('ssl/cert.pem', 'ssl/key.pem'))
