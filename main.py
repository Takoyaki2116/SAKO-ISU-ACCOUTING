from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
  return redirect('/top')


@app.route("/top")
def top():
  return render_template("top.html")


@app.route("/login")
def login():
  return render_template("login.html")


@app.route("/claim")
def claim():
  return render_template("claim.html")


@app.route("/claim_create")
def claim_create():
  return render_template("claim_create.html")


@app.route("/claim_edit")
def claim_edit():
  return render_template("claim_edit.html")


@app.route("/receipt")
def receipt():
  return render_template("receipt.html")


@app.route("/receipt_create")
def receipt_create():
  return render_template("receipt_create.html")


@app.route("/receipt_edit")
def receipt_edit():
  return render_template("receipt_edit.html")


@app.route("/quotation")
def quotation():
  return render_template("quotation.html")


@app.route("/quotation_create")
def quotation_create():
  return render_template("quotation_create.html")


@app.route("/quotation_edit")
def quotation_edit():
  return render_template("quotation_edit.html")


app.run(host='0.0.0.0', port=5001)
