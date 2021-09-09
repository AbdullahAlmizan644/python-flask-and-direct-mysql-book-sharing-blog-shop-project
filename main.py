from os import stat_result
from flask import Flask,render_template,request
from flask_mysqldb import MySQL
from werkzeug.utils import redirect

app=Flask(__name__)


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']=""
app.config["MYSQL_DB"] ="mydatabase"

mysql=MySQL(app)

@app.route("/",methods=["GET","POST"])
def index():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM stories")
    stories=cur.fetchall()
    return render_template("index.html",stories=stories)



@app.route("/add_story",methods=["GET","POST"])
def add_story():
    if request.method=="POST":
        name=request.form["name"]
        story=request.form["story"]
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO stories(name,story) VALUES (%s,%s)",(name,story))
        cur.connection.commit()
        return redirect("/")
    return render_template("add_story.html")



@app.route("/update/<int:sno>",methods=["GET","POST"])
def update(sno):
    cur=mysql.connection.cursor()
    cur.execute("""SELECT * FROM stories WHERE sno = %s""", (sno,))
    stories=cur.fetchone()
    print(stories)
    if request.method=="POST":
        name=request.form["name"]
        story=request.form["story"]
        cur=mysql.connection.cursor()
        cur.execute("UPDATE stories SET name=%s, story=%s WHERE sno=%s",(name,story,sno))
        mysql.connection.commit()
        return redirect("/")

    return render_template("update.html",stories=stories)

@app.route("/delete/<int:sno>",methods=["GET"])
def delete(sno):
    cur=mysql.connection.cursor()
    cur.execute(""" DELETE FROM stories where sno=%s""",(sno,))
    mysql.connection.commit()
    return redirect("/")

@app.route("/search",methods=["GET","POST"])
def search():
    if request.method=="POST":
        search_name=request.form.get("search")
        cur=mysql.connection.cursor()
        cur.execute(f"SELECT * FROM stories WHERE name LIKE '%{search_name}%'")
        s_result=cur.fetchall()
        for i in s_result:
            print(i[0],i[1],i[2])
        if s_result==():
            return '<script>alert("No Result Matched")</script>'

        return render_template("search.html",s_result=s_result)



if __name__=='__main__':
    app.run(debug=True)
