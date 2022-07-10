import uuid
from django.db import models
from django.contrib.auth.hashers import make_password


class Note(models.Model):
    
    secondary_id = models.UUIDField(default=uuid.uuid4, unique=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    password_to_edit = models.CharField(max_length=2000, null=True, blank=True)
    password_to_read = models.CharField(max_length=2000, null=True, blank=True)
    
    class Meta:
        ordering = ["-created"]
    
    def __str__(self):
        return str(self.id)
        
    #def save(self, *args, **kwargs):
        #self.password_to_edit =  make_password(self.password_to_edit)
        #self.password_to_read =  make_password(self.password_to_read)
          
        #super().save(*args, **kwargs)  
        
        