from django.db import models

# Create your models here.
class opportunity(models.Model):
    CaseID = models.IntegerField(primary_key=True)
    CaseName = models.CharField(max_length=255)
    Representative = models.CharField(max_length=64)
    CustomerName =  models.CharField(max_length=128)
    ExpectedOrderDate = models.DateField()
    ExpectedRevenueDate = models.DateField()
    OccurDate = models.DateField()
    CreatedDate = models.DateField()
    Creator  = models.CharField(max_length=64)
    UpdatedDate = models.DateField()
    Updater = models.CharField(max_length=64)
    Category = models.CharField(max_length=64)
#def __str__(self):
#    return self.CaseID
class Meta:
    ordering = ['CaseID']
#   verbose_name = 'opportunity'
#   verbose_name_plural = 'opportunities'
    db_table = 'opportunity'
