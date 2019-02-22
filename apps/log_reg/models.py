from __future__ import unicode_literals
from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):

    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if len(postData['fname']) < 2:
            errors["fname"] = "First name should be more than 2 characters long"
        if len(postData['lname']) < 2:
            errors["lname"] = "Last name should be more than 2 characters long"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Email needs to be a valid email"
        if User.objects.filter(email=postData['email']).count() >= 1:
            errors["email"] = "Not a unique email"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be more than 2 characters long"
        if postData['cpassword'] != postData['password']:
            errors["cpassword"] = "Passwords needs to match"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["login_email"] = "Email needs to be a valid email"
        else:
            if User.objects.filter(email=postData['email']).count() < 1:
                errors["duplicate_email"] = "Not a user"
        if len(postData['password']) < 1:
            errors["login_password"] = "Password should be more than 2 characters long"

        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()