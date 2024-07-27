from django.db import models
from django.contrib.auth.models import User


class Influencer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to="profile_pics/")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class VideoRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    name = models.CharField(max_length=110)
    email = models.EmailField()
    message = models.TextField()
    status = models.CharField(max_length=20,
                              default="pending",
                              choices=[
                                  ("Pending", "Pending"), ("Completed", "Completed")]
                              )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Payment(models.Model):
    request = models.ForeignKey(VideoRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="pending",
                              choices=[
                                  ("Pending", "Pending"), ("Completed", "Completed")]
                              )
    transaction_id = models.CharField(max_length=100, unique=True)
