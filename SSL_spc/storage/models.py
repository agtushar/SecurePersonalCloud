from django.db import models

class userFile(models.Model):
    filename = models.CharField(max_length=200)
    content = models.BinaryField();
    def __str__(self):
        return self.filename

class MyUser(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    password = models.CharField(max_length=200)
    files = models.ManyToManyField(userFile)
    def __str__(self):
        print(self.username)
        return self.username
