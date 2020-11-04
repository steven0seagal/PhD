from django.db import models

# Create your models here.

class FFASDatabase(models.Model):

    input_file = models.CharField(max_length=200)
    analysis_name = models.CharField(max_length=200)
    user_id = models.IntegerField()
    profile_out = models.CharField(max_length=200)
    PDB_out = models.CharField(max_length=200)
    SCOP_out = models.CharField(max_length=200)
    PFAM_out = models.CharField(max_length=200)
    Hsapiens = models.CharField(max_length=200)
    COG_out = models.CharField(max_length=200)

    def __str__(self):
        return self.analysis_name