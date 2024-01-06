from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, null=False)
    slug = models.CharField(max_length=255, unique=True, null=True)
    description = models.TextField(null=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name