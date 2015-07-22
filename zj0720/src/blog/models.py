#coding=UTF-8
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Manager(models.Model):
    name=models.CharField(max_length=30)
    
    def __unicode__(self) :
        return self.name
class House(models.Model):
    name=models.CharField(max_length=30)
    date=models.DateTimeField()
    price=models.IntegerField()
    
    def __unicode__(self) :
        return self.name
    
    
class Group(models.Model):
    name=models.CharField(max_length=30)
    manager=models.ManyToManyField(Manager)
    house=models.ManyToManyField(House)
    
    #ManyToOne models.ForeignKey(Author)
    def __unicode__(self):
        return self.name
