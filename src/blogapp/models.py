from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Blog(models.Model):
    title=models.TextField(max_length=100)
    description=models.TextField(max_length=255)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images/',null=True)
    creator =models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    class Meta:
        db_table="blogs"
