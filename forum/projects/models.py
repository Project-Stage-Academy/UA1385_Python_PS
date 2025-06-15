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
        InvestorProfile,
        through='ProjectInvestor'
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    progress = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title} ({self.startup.title})"

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'
        db_table = 'projects'

        indexes = [
            models.Index(fields=['startup']),
            models.Index(fields=['progress'])
        ]

class ProjectInvestor(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    investor = models.ForeignKey('investors.InvestorProfile', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.investor} -> {self.project.title}"

    class Meta:
        db_table = 'project_investors'
        indexes = [
            models.Index(fields=['investor']),
        ]
        unique_together = ('project', 'investor')