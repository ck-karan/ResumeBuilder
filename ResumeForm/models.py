from django.db import models
from django.db.models import expressions

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length = 254)
    address = models.TextField(max_length=2000)
    linkedin = models.CharField(max_length=100)
    objective = models.TextField(max_length=2000)
    ssc = models.FloatField()
    ssc_univ = models.CharField(max_length=100)
    hsc = models.FloatField()
    hsc_univ = models.CharField(max_length=100)
    grad = models.CharField(max_length=100, null=True)
    gradp = models.FloatField(null=True)
    grad_univ = models.CharField(max_length=100, null=True)
    postgrad = models.FloatField(null=True)
    postgrad_univ = models.CharField(max_length=100, null=True)
    exp = models.TextField(max_length=2000)
    skills = models.TextField(max_length=2000)
    projects = models.TextField(max_length=2000)
