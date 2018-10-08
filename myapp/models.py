from django.db import models

class Credential(models.Model):

   name = models.CharField(max_length = 50)
   password = models.CharField(max_length = 50)

   class Meta:
      db_table = "credential"  
      ordering = ('name',) 

class Document(models.Model):
    filename = models.CharField(max_length = 50)
    document = models.BinaryField(null=True)
    real_user = models.ManyToManyField(Credential)
    shared_user = models.ManyToManyField(Credential) 

    class Meta:
        db_table = "document"
        ordering = ('filename',) 
