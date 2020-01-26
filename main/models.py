from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse


class Profile(models.Model):
    organization_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ein_number = models.IntegerField()
    name = models.CharField(max_length=250)
    about = models.TextField()


class HighlightedEvents(models.Model):
    event_name = models.CharField(max_length=50)
    organization = models.ForeignKey(to=Profile, related_name='events', on_delete=models.CASCADE)
    event_start_date = models.DateField()
    event_start_time = models.TimeField()
    event_end_date = models.DateField()
    event_end_time = models.TimeField()
    event_description = models.TextField()
    event_link = models.URLField()


class Donations(models.Model):
    amount = models.DecimalField(max_digits=5,decimal_places=2)
    organization = models.ForeignKey(to=User, related_name='events', on_delete=models.CASCADE)
    success = models.BooleanField(default=False)
    donation_timestamp = models.DateTimeField(default=timezone.now)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class News(models.Model):
    STATUS_CHOICES = {
        ('draft', 'Draft'),
        ('published', 'Published'),
    }
    organization = models.ForeignKey(to='Profile', on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=250)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    news_details = models.TextField()
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('template',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ])
