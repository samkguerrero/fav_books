from django.db import models
from apps.log_reg.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=45)
    desc = models.TextField()
    one_user_who_uploaded_this_book = models.ForeignKey(User, related_name="books_uploaded")
    users_who_like_this_book = models.ManyToManyField(User, related_name="books_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)