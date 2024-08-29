from mongoengine import Document, StringField

class FirstName(Document):
    name = StringField(required=True, unique=True)

    def __str__(self):
        return self.name