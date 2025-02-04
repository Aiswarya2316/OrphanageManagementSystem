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
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(Stafreg, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    category = models.CharField(max_length=100, choices=[
        ('Food', 'Food'),
        ('Clothes', 'Clothes'),
        ('Books', 'Books'),
        ('Medicines', 'Medicines'),
        ('Other', 'Other')
    ])
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.quantity}"

class DailyActivity(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    activity_details = models.TextField()
    staff = models.ForeignKey(Stafreg, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.child.name} - {self.date}"


class Feedback(models.Model):
    donor = models.ForeignKey(DonorRegister, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Stafreg, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.donor.name if self.donor else self.staff.name} on {self.date_submitted}"


class MedicalRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    date = models.DateField()
    doctor_name = models.CharField(max_length=100)
    diagnosis = models.TextField()
    prescription = models.TextField()

    def __str__(self):
        return f"{self.child.name} - {self.date}"


class Wishlist(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Fulfilled', 'Fulfilled')], default='Pending')

    def __str__(self):
        return f"{self.child.name} - {self.item_name} ({self.status})"

