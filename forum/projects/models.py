from django.db import models
from startups.models import StartupProfile
from investors.models import InvestorProfile

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    
    startup = models.ForeignKey(
        StartupProfile,
        on_delete=models.CASCADE,
        db_column='startup_id'
    )
    
    investor = models.ManyToManyField(
        InvestorProfile
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    progress = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'
        db_table = 'projects'