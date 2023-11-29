from django.db import models

# Create your models here.
class Developers(models.Model):
    name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=11)
    Email = models.CharField(unique=True,max_length=20)

    def __str__(self):
        return self.name


class project(models.Model):
    project_name = models.CharField(max_length=50)
    developers = models.ManyToManyField(Developers)


    
    @property
    def developer_name(self):
        return self.developer.id


class Manager(models.Model):
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    developer = models.ForeignKey(Developers, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.developer.name} - {self.salary}"

class Bank(models.Model):
    employee = models.CharField(max_length=20)
    employee_salary = models.DecimalField(max_digits=10, decimal_places=2)
