# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class  pokemon(models.Model):
    """Pokemon model
    """
    
    #Pokemon features
    #id = models.AutoField(primary_key=True)

    idApi= models.IntegerField()
    name = models.CharField(max_length=100, primary_key=True)
    height = models.FloatField()
    weight= models.FloatField()

    #stats
    speed= models.FloatField()
    specialDefense= models.FloatField()
    specialAttack = models.FloatField()
    defense= models.FloatField()
    attack= models.FloatField()
    hp =models.FloatField()

    #chain link 
    prevolution=models.CharField(max_length=100,null = True)
    evolution=models.CharField(max_length=100,null = True)
    

    #utils
    created = models.DateTimeField(auto_now_add=True)

    