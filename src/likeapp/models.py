from django.db import models
from django.contrib.auth.models import User
from blogapp.models import Blog

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='likes', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=("user","blog")

    def __str__(self):
        return f'{self.user.username} likes {self.blog.title}'
