from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import re
from django.urls import reverse


class PublishedManger(models.Manager):
    def get_queryset(self):
        return super(PublishedManger, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    upload = models.FileField(upload_to='uploads', null=True, blank=True)
    slug = models.SlugField(max_length=200, unique_for_date='publish', blank=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    tag = models.CharField(max_length=50, default='')

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManger()

    # generate slug automatically
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def tag_list(self):
        tag_list = re.split(", ", self.tag)
        return tag_list

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    # def __str__(self):
    #     return 'Comment by {} on {}'.format(self.name, self.post)







