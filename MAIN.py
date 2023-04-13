from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root*4"
app.config["MYSQL_DB"] = "sk_database"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


@app.route("/")
def home():
    con = mysql.connection.cursor()
    query = "SELECT * FROM students"
    con.execute(query)
    result = con.fetchall()
    return render_template("home.html", datas=result)


@app.route("/InsertUser", methods=['GET', 'POST'])
def InsertUser():
    if request.method == 'POST':
        name = request.form["NAME"]
        age = request.form["AGE"]
        subject = request.form["SUBJECT"]
        city = request.form["CITY"]
        con = mysql.connection.cursor()
        query = "INSERT INTO students (NAME,AGE,SUBJECT,CITY) VALUES (%s,%s,%s,%s)"
        con.execute(query, (name, age, subject, city))
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    return render_template("InsertUser.html")


@app.route("/EditUser/<string:Id>", methods=['POST', "GET"])
def EditUser(Id):
    con = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form["NAME"]
        age = request.form["AGE"]
        subject = request.form["SUBJECT"]
        city = request.form["CITY"]
        query = "UPDATE students SET NAME=%s,AGE=%s,SUBJECT=%s,CITY=%s WHERE ID=%s"
        con.execute(query, [name, age, subject, city, Id])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    con = mysql.connection.cursor()
    query = "SELECT * FROM students WHERE ID=%s"
    con.execute(query, [Id])
    result = con.fetchone()
    return render_template("EditUser.html", datas=result)


@app.route("/DeleteUser/<string:Id>", methods=['POST', 'GET'])
def DeleteUser(Id):
    con = mysql.connection.cursor()
    query = "DELETE FROM students WHERE ID=%s"
    con.execute(query, (Id,))
    mysql.connection.commit()
    con.close()
    return redirect(url_for("home"))


@app.route("/clear", methods=['POST', 'GET'])
def clear():
    con = mysql.connection.cursor()
    query = "TRUNCATE TABLE students"
    con.execute(query)
    mysql.connection.commit()
    con.close()
    return redirect(url_for("home"))


if (__name__ == '__main__'):
    app.secret_key = "Key"
    app.run(debug=True)
