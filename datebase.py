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