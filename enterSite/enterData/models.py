from django.db import models


class Account(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)  # хм

    def __str__(self):
        return self.username

    def serialize_data(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}
