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
    business_partner = ForeignKeyField(BusinessPartner, backref='claims')
    subject = CharField()
    day = DateField()
    payment = CharField()
    amount = CharField()
    status = CharField()
    class Meta:
        database = db # This model uses the "people.db" database
db.create_tables([Claim], safe=True)

class Receipt(Model):
    business_partner = ForeignKeyField(BusinessPartner, backref='receipts')
    subject = CharField()
    day = DateField()
    amount = CharField()
    status = CharField()
    class Meta:
        database = db # This model uses the "people.db" database
db.create_tables([Receipt], safe=True)

class Quotation(Model):
    business_partner = ForeignKeyField(BusinessPartner, backref='quotation')
    subject = CharField()
    day = DateField()
    amount = CharField()
    status = CharField()
    class Meta:
        database = db # This model uses the "people.db" database
    db.create_tables([Quotation], safe=True)
    
class Inquiry(Model):
    name = CharField()
    furigana = CharField(
    mail = CharField()
    detail  = CharField()
    file = CharField()
    class Meta:
            database = db # This model uses the "people.db" database
    db.create_tables([Inquiry], safe=True)
    
