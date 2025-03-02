from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sidebar-style-2")
def sidebar_style_2():
    return render_template("sidebar-style-2.html")

@app.route("/forms")
def forms():
    return render_template("forms/forms.html")

@app.route("/tables")
def datatables():
    return render_template("tables/datatables.html")

@app.route("/datatables")
def tables():
    return render_template("tables/tables.html")

@app.route("/charts")
def charts():
    return render_template("charts/charts.html")

@app.route("/sparkline")
def sparkline():
    return render_template("charts/sparkline.html")

if __name__ == "__main__":
    app.run(debug=True)

