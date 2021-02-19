from django.db import models
from django.contrib.auth import get_user_model

# UserModel = ''
# # get_user_model()
from django.conf import settings




class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user.username[:10]},{self.title[:10]} - {self.created.strftime("%c")}'
    
    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Entries'