from app import create_app

app = create_app()

if __name__ == '__main__':
    # Set debug to True for development, change to False for production
    app.run(debug=True, port=5001)
