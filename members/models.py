from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='members/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.position}"
