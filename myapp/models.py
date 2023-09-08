from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.

class work_types(models.Model):
    works = models.CharField(max_length=25)
    # Customuser = models.ForeignKey('customuser',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.works


class customuser(AbstractUser):
    is_worker = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    address = models.TextField(null=True)
    experience = models.CharField(max_length=25,null=True)
    photo = models.ImageField(upload_to='profile',null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=30,null=True)
    type_of_work = models.ForeignKey(work_types,on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=False)


class schedule(models.Model):
    Customuser = models.ForeignKey(customuser,on_delete=models.CASCADE,null=True)
    date_available = models.DateField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    type_of_work = models.ForeignKey(work_types,on_delete=models.CASCADE,null=True, related_name='schedules')

class appointment(models.Model):
    Customuser = models.ForeignKey(customuser,on_delete=models.CASCADE,null=True)
    Schedule = models.ForeignKey(schedule,on_delete=models.CASCADE,null=True)
    status = models.IntegerField(default=0)


# class payments(models.Model):
#     Customuser = models.ForeignKey(customuser,on_delete=models.CASCADE,null=True)
#     amount = models.IntegerField(default=False)
#     bill_date = models.DateField(null=True)
class Bill(models.Model):
    Customuser = models.ForeignKey(customuser,on_delete=models.CASCADE)
    amount = models.FloatField()
    bill_date = models.DateTimeField(default=timezone.now)
    paid_on = models.DateField(auto_now=True)
    status = models.IntegerField(default=0)


class card(models.Model):
    bill = models.ForeignKey(Bill,on_delete=models.CASCADE)
    card_no = models.CharField(max_length=30)
    card_cvv = models.CharField(max_length=30)
    expiry_date = models.CharField(max_length=200)

# class user_payment(models.Model):
#     amount_and_bill = models.ForeignKey(payments,on_delete=models.CASCADE,null=True)
#     payment_date = models.DateField()

class complaints(models.Model):
    Customuser = models.ForeignKey(customuser,on_delete=models.CASCADE)
    type_complaint = models.TextField(max_length=255)
    complaint_date = models.DateTimeField(default=timezone.now)
    reply_complaint = models.TextField(max_length=255, null=True)
    reply_date = models.DateTimeField(default=timezone.now)






