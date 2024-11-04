from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from datebase import BusinessPartner
from datebase import Claim
from peewee import *

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
  claim = Claim.select()
  return render_template("claim.html" , claim = claim)


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

@app.route("/business_partner")
def business_partner():
  business_partners = BusinessPartner.select()
  return render_template("business_partner.html", business_partners = business_partners)

@app.route("/business_partner_create")
def business_partner_create():
  return render_template("business_partner_create.html")


@app.route("/business_partner_edit")
def business_partner_edit():
  return render_template("business_partner_edit.html")

@app.route("/new_business_partner", methods=["POST"])
def new_business_partner():
  name = request.form.get("name")
  address = request.form.get("address")
  contact = request.form.get("contact")
  remarks = request.form.get("remarks")

  bp = BusinessPartner(name=name, address=address, contact=contact, remarks=remarks)
  bp.save()
  return redirect("/business_partner")

@app.route("/new_claim", methods=["POST"])
def new_claim():
  subject = request.form.get("subject")
  day = request.form.get("day")
  payment = request.form.get("payment")
  amount = request.form.get("amount")
  status = request.form.get("status")

  bp = Claim(subject=subject, day=day, payment=payment, amount=amount ,status=status)
  bp.save()
  return redirect("/claim")




app.run(host='0.0.0.0', port=5001)
