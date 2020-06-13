from django.db import models

# Create your models here.
class donor(models.Model):
	name = models.CharField(max_length = 64)
	phone_number = models.IntegerField()