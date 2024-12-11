from django.db import models


class ProjectSettings(models.Model):
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    smtp_server = models.CharField(max_length=255, null=True, blank=True)
    smtp_port = models.PositiveIntegerField(null=True, blank=True)
    smtp_username = models.CharField(max_length=255, null=True, blank=True)
    smtp_password = models.CharField(max_length=255, null=True, blank=True)
    smtp_use_tls = models.BooleanField(default=False)
    smtp_use_ssl = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if ProjectSettings.objects.exists() and not self.pk:
            raise ValueError("Only one ProjectSettings instance is allowed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return "Project Settings"
