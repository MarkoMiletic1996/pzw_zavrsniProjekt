from flask import Flask, redirect, url_for, render_template, request,abort,make_response
import sqlite3

app = Flask(__name__)

DATABASE = 'app.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.route("/")
@app.route("/home")
def index():
	return render_template("index.html")
	
	
@app.route("/slike")
def slike():
	return render_template("slike.html")
	
@app.route("/treneri")
def treneri():
	return render_template("treneri.html")
	

@app.route("/radnoVrijeme")
def radnoVrijeme():
	return render_template("radnoVrijeme.html")

@app.route("/addUser")
def addUser():
	return render_template("login.html")

@app.route("/login")
def login():
	username = request.args.get('username')
	email = request.args.get('email')
	visina = request.args.get('visina')
	tezina = request.args.get('tezina')
	godine = request.args.get('godine')
	db = connect_db()
	sql = "insert into users (username, email, visina, tezina, godine) values (?,?,?,?,?)"
	db.execute(sql, [username, email, visina, tezina, godine])
	db.commit()
	db.close()
	return render_template("login.html", username=username, email=email, visina=visina, tezina=tezina, godine=godine)


@app.route("/userList")
def userList():
	db = connect_db()
	cur = db.execute("select id, username, email, visina, tezina, godine from  users")
	entries = [dict(id=row[0], username=row[1], email=row[2], visina=row[3], tezina=row[4], godine=row[5]) for row in
			   cur.fetchall()]
	print(entries)
	db.close()
	return render_template('userList.html', entries=entries)


# edit profile (update or delete)
@app.route('/editUser')
def editUser():
	id = request.args.get('id')
	db = connect_db()
	cur = db.execute("select id, username, email, visina, tezina, godine from users where id=?", [id])
	rv = cur.fetchall()
	cur.close()
	users = rv[0]
	print(rv[0])
	db.close()
	return render_template('userListUpdate.html', users=users)

@app.route('/updateUser')
def updateUser():
	id = request.args.get('id')
	username = request.args.get('username')
	email = request.args.get('email')
	print(">>>>>>>>>>>>>", username + email)
	visina = request.args.get('visina')
	tezina = request.args.get('tezina')
	godine = request.args.get('godine')
	db = connect_db()
	sql = "update users set username=?, email=?, visina=?, tezina=?, godine=? where id=?"
	db.execute(sql, [username, email, visina, tezina, godine, id])
	db.commit()
	db.close()
	return index()

@app.route('/deleteUser')
def deleteUser():
	id = request.args.get('id')
	db = connect_db()
	sql = "delete from users where id=?"
	db.execute(sql, [id])
	db.commit()
	db.close()
	return render_template('index.html')


if __name__ == "__main__":
	app.run(debug=True)