from flask import Flask

app = Flask(__name__)
app.debug = True  # Enable debug mode directly

@app.route("/")
def home():
    return "Hello, Flask with PyCharm!"

if __name__ == "__main__":
    app.run()  # No need for debug=True, it's already set
