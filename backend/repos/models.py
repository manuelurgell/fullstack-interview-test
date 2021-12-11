from django.db import models


class PR(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('merged', 'Merged')
    )

    base = models.CharField(max_length=70)
    compare = models.CharField(max_length=70)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='open'
    )
    author_name = models.CharField(max_length=200)
    author_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
