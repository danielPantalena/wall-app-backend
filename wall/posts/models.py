from django.utils.translation import gettext_lazy as _
from django.db.models import (
    Model,
    DateTimeField,
    CharField,
    TextField,
    BooleanField,
    ForeignKey,
    CASCADE
)


class Post(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    title = CharField(max_length=255)
    body = TextField()
    deleted = BooleanField(default=False)
    owner = ForeignKey('auth.User', related_name='Posts',on_delete=CASCADE)
    

    def __str__(self):
        return self.title
