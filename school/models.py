from django.db import models

# Create your models here.

class school(models.Model):
	school_name = models.CharField(max_length = 64)
	location = models.CharField(max_length=64)
	requirements = models.CharField(max_length=100)

