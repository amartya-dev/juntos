from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


class Profile(models.Model):
    organization_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ein_number = models.CharField(max_length=10)
    name = models.CharField(max_length=250)
    about = RichTextField()
    organization_slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('template',
                       args=[
                           self.slug
                       ])


class HighlightedEvents(models.Model):
    event_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    organization = models.ForeignKey(to=User, related_name='events', on_delete=models.CASCADE)
    event_start_date = models.DateField()
    event_start_time = models.TimeField()
    event_end_date = models.DateField()
    event_end_time = models.TimeField()
    event_description = RichTextUploadingField()
    event_link = models.URLField()

    def __str__(self):
        return self.event_name

    def get_absolute_url(self):
        return reverse('template',
                       args=[
                           self.slug
                       ])


class Donations(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    organization = models.ForeignKey(to=User, related_name='donations', on_delete=models.CASCADE)
    success = models.BooleanField(default=False)
    donation_timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "For : {} amount : {}".format(self.organization.name, self.amount)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class News(models.Model):
    STATUS_CHOICES = {
        ('draft', 'Draft'),
        ('published', 'Published'),
    }
    organization = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    news_details = RichTextUploadingField()
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
