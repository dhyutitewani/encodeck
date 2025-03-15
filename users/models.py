from django.db import models

    
class Users(models.Model):
    first_name=models.CharField(max_length=120)
    last_name=models.CharField(max_length=120)
    email=models.CharField(max_length=120)

    def __str__(self):
        last_4_digits=self.last_name
        return "{}_{}".format(self.first_name, last_4_digits)
