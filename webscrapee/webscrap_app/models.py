from django.db import models
from webscrap_app.Get_Current_Date import get_current_date

class leet_code_det(models.Model):
    logo = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    Username = models.CharField(max_length=40)
    rank =models.CharField(max_length=40)
    prob_sol =models.CharField(max_length=40)
    easy =models.CharField(max_length=40)
    medium =models.CharField(max_length=40)
    hard =models.CharField(max_length=40)
    date = models.CharField(max_length=20, editable=False)  # Custom date format, not auto_now_add
    days = models.IntegerField()
    
    class Meta:
        ordering = ['-date']
    
    def save(self, *args, **kwargs):
        if not self.id: 
            self.date = get_current_date()
        super().save(*args, **kwargs)


class Code_chef_det(models.Model):
    url = models.CharField(max_length=100)
    Username = models.CharField(max_length=50)
    Division =models.CharField(max_length=40)
    rating =models.CharField(max_length=40)
    star =models.CharField(max_length=40)
    H_Rating =models.CharField(max_length=40)
    global_rank =models.CharField(max_length=40)
    country_rank =models.CharField(max_length=40)
    date = models.CharField(max_length=20, editable=False)  # Custom date format, not auto_now_add
    days = models.IntegerField()

    
    class Meta:
        ordering = ['-date']
    def save(self, *args, **kwargs):
        if not self.id:  # Only set the date if the object is being created
            self.date = get_current_date()
        super().save(*args, **kwargs)
