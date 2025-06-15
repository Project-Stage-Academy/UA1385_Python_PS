from django.db import models
from users.models import User

class StartupProfile(models.Model):
    startup_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    industry = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'startup'
        verbose_name_plural = 'startups'
        db_table = 'startups'

class Subscription(models.Model):
    investor = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name="subscriptions")
    
    startup = models.ForeignKey(StartupProfile,
                                 on_delete=models.CASCADE,
                                 related_name="subscribers")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.investor.email} -> {self.startup.title}'

    class Meta:
        unique_together = ('investor', 'startup')