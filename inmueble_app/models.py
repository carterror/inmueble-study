from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Max
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(max_length=250)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Inmueble(models.Model):
    address = models.CharField(max_length=250)
    pais = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    imagen = models.CharField(max_length=900)
    active = models.BooleanField(default=True)
    avg_califications = models.FloatField(default=0)
    num_califications = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='inmuebles')

    def __str__(self):
        return self.address


class Comment(models.Model):
    qualification = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    texto = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.qualification) + " " + self.inmueble.address
