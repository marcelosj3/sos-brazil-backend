from django.db import models


# Create your models here.
class Ongs(models.Model):
    name= models.CharField(max_length= 100, null= True, unique= True)
    description= models.CharField(max_length= 255, null= True, unique= True)
    cnpj= models.CharField(max_length= 14, null= True, unique= True)
    site_address= models.CharField(max_length= 255)
    logo= models.CharField(max_length= 255, null= True)
    created_at= models.DateField(auto_now= True) 
