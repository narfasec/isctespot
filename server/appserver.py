from api.__init__ import create_app

if __name__ == '__main__':
    create_app = create_app()
    create_app.run(debug=True, host="0.0.0.0")