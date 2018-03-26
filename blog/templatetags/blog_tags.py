from django import template
from blog.models import Post
from django.db.models  import Count

register = template.Library()

# just for practice
# @register.filter(name='cut')
# def cut(value, arg):
#     return value.replace(arg, "")


# simple_tag processes data and returns a stream
@register.simple_tag
def total_posts():
    return Post.objects.all().filter(status='published').count()


# inclusion_tag processes the data and returns a rendered template
@register.inclusion_tag('blog/includes/recent_posts.html')
def recent_posts(count=6):
    posts = Post.published.order_by('-publish')[:count]
    return {
        'recent_posts': posts
    }


# assignment_tag processes the data and sets a variable in context
@register.inclusion_tag('blog/includes/most_commented_posts.html')
def most_commented_posts(count=6):
    posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return{
        'most_commented_posts': posts
    }
