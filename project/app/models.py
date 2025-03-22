from django.db import models
from django.contrib.auth.models import User


class DonorRegister(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField()
    phone = models.IntegerField()
    password = models.TextField()
    location= models.TextField()
    confirm_password=models.TextField()

    def __str__(self):
        return self.name

class Stafreg(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField()
    phone = models.IntegerField()
    password = models.TextField()
    location= models.TextField()
    confirm_password=models.TextField()

    def __str__(self):
        return self.name
    


class adminreg(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField()
    phone = models.IntegerField()
    password = models.TextField()

    def __str__(self):
        return self.name

class Child(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    medical_history = models.TextField()
    education_status = models.CharField(max_length=200)
    admission_date = models.DateField(auto_now_add=True)
    guardian_name = models.CharField(max_length=100, null=True, blank=True)
    guardian_contact = models.CharField(max_length=15, null=True, blank=True)
    staf = models.ForeignKey(Stafreg, on_delete=models.CASCADE)  # 🔹 Link to staff
    
    def __str__(self):
        return self.name
    

class Donation(models.Model):
    donor = models.ForeignKey(DonorRegister, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    donation_type = models.CharField(max_length=100, choices=[
        ('Money', 'Money'),
        ('Clothes', 'Clothes'),
        ('Food', 'Food'),
        ('Books', 'Books'),
        ('Others', 'Others')
    ])
    description = models.TextField()
    donation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.name} - {self.donation_type} - {self.amount}"


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    staff = models.ForeignKey(Stafreg, on_delete=models.CASCADE)  # 🔹 Event Created by Staff
    children = models.ManyToManyField(Child, related_name="events")  # 🔹 Children Participating

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    def __str__(self):
        return f"{self.name} - {self.subject}"
