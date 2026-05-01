from django.db import models
from django.contrib.auth.models import User

# Student Profile
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    skills = models.TextField()
    education = models.CharField(max_length=200)
    college = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return self.user.username


# Internship
class Internship(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    required_skills = models.TextField()
    description = models.TextField()
    deadline = models.DateField()

    def __str__(self):
        return self.title


# Application
class Application(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('applied', 'Applied'),
            ('shortlisted', 'Shortlisted'),
            ('rejected', 'Rejected')
        ],
        default='applied'
    )

    def __str__(self):
        return f"{self.student.username} - {self.internship.title}"