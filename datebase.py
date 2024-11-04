from peewee import *

db = SqliteDatabase('SAKO_ISU.db')

class BusinessPartner(Model):
    name = CharField()
    address = CharField()
    contact = CharField()
    remarks = CharField()

    class Meta:
        database = db # This model uses the "people.db" database.
db.connect()
db.create_tables([BusinessPartner], safe=True)

class Claim(Model):
    subject = CharField()
    day = DateField()
    payment = CharField()
    amount = CharField()
    status = CharField()
    class Meta:
        database = db # This model uses the "people.db" database
db.create_tables([Claim], safe=True)