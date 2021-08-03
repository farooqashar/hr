from flask import Flask, render_template, request, redirect, url_for,flash
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import literal_column
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

app = Flask(__name__)

class Employees(Base):
   __tablename__ = 'crud'
   id = Column(Integer, primary_key =  True)
   name = Column(String)
   email = Column(String)
   phone = Column(String)

engine = create_engine("postgresql://postgres:password@localhost:5457/crud")
Session = sessionmaker(bind=engine)

session = Session()

app.secret_key = "Secret Key"

@app.route("/")
def index():

    all_data = session.query(Employees).all()
    return render_template("index.html", employees = all_data)

@app.route("/insert", methods= ["POST"])
def insert():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        query_str = "INSERT INTO crud (name, email, phone) VALUES ('" + name + "', '" + email + "', '" + phone + "');"

        session.execute(query_str)
        session.commit()

        flash("Employee has been successfully added!")
        return redirect(url_for("index"))


@app.route("/update", methods = ["GET","POST"])
def update():

    if request.method == "POST":

        id = request.form.get("id")
        relevant_data = session.query(Employees).get(id)

        relevant_data.name = request.form["name"]
        relevant_data.email = request.form["email"]
        relevant_data.phone = request.form["phone"]

        session.commit()
        flash("Employee information has been successfully updated!")

        return redirect(url_for("index"))

@app.route("/delete/<id>/", methods = ["GET","POST"])
def delete(id):
    relevant_data = session.query(Employees).get(id)
    session.delete(relevant_data)
    session.commit()
    flash("Employee has been successfully deleted!")
    
    return redirect(url_for("index"))




if __name__ == "__main__":
    app.run(debug=False)
