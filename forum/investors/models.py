from django.db import models
from users.models import User

class InvestorProfile(models.Model):
    investor_id = models.AutoField(primary_key=True)  
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)


    class Meta:
        verbose_name = 'investor'
        verbose_name_plural = 'investors'
        db_table = 'investors'