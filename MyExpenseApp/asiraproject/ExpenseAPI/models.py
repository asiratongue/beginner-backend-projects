from django.db import models


    
class Expense(models.Model):

    userID = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    expense = models.CharField(max_length=100)
    createdat = models.DateTimeField("User Created At", auto_now_add=True)

    def __str__(self):
        return self.name


#this is like sqlalchemy where your database models are defined and also where you can add class methods.