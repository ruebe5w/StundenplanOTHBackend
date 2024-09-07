from django.db import models

# Create your models here.

class Course(models.Model):
    name=models.CharField(max_length=100)
class Timetable(models.Model):
    name=models.CharField(max_length=100)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)

class Module(models.Model):
    tag = models.IntegerField()
    name = models.CharField(max_length=100)
    longname = models.CharField(max_length=200)
    dozent = models.CharField(max_length=100)
    raum = models.CharField(max_length=50)
    startBlock = models.IntegerField()
    endBlock = models.IntegerField()
    notes = models.CharField(max_length=500)
    timetable=models.ForeignKey(Timetable,on_delete=models.CASCADE)

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')