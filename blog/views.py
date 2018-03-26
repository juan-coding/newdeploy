from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
import re
from .forms import CommentForm, PostForm
from django.db.models import Q
from django.utils import timezone

months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]


def post_create(request):
    sent = False
    context = {
        'sent': sent,
        'form': '',
        'post': '',
        'sub_title': 'Add a new post'
    }
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.publish = timezone.now()
            post.save()
            # return redirect('blog:post_detail',
            #                 # year=post.publish.year,
            #                 # month=post.publish.month,
            #                 # day=post.publish.day,
            #                 # slug=post.slug)
            sent = True
            context.update({
                'sent': sent,
                'form': form,
                'post': post,
            })

    else:
        form = PostForm()

    context.update({
        'sent': sent,
        'form': form,
    })
    return render(request, 'blog/post/post_create.html', context)


def post_edit(request, year, month, day, slug):
    sent = False
    context = {
        'sent': sent,
        'form': '',
        'post': '',
        'sub_title': 'Update a post'
    }
    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug,
                             status='published')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.publish = timezone.now()
            post.save()
            return redirect('blog:post_detail',
                            year=post.publish.year,
                            month=post.publish.month,
                            day=post.publish.day,
                            slug=post.slug)
        context.update({
            'sent': sent,
            'form': form,
            'post': post,
            'sub_title': "Update post '{}'".format(post.title)
        })
        sent = True
    else:
        form = PostForm()
    context.update({
        'sent': sent,
        'form': form,
    })
    return render(request, 'blog/post/post_edit.html', context)


# this 'posts' variable will be used inside the functions
posts = Post.objects.all().filter(status='published')


def tag_archive_data(posts):
    """create a list for tag and its counts"""
    count_list = []
    count = {}
    for post in posts:
        # tag = post.tag
        tag_list = re.split(", ", post.tag)
        for tag in tag_list:
            if tag not in count:
                count[tag] = 1
            else:
                count[tag] += 1
    for k, v in sorted(count.items(), reverse=True):
        count_list.append({'tag': k, 'count': v})
    return count_list


def year_archive_data(posts):
    """create a list for year and the posts count"""
    count_list = []
    ycount_dic = {}
    mcount_dic= {}
    for post in posts:
        year = post.publish.year
        if year not in ycount_dic:
            ycount_dic[year] = 1
            mcount_dic[year] = {}
        else:
            ycount_dic[year] += 1
        month = post.publish.month
        if month not in mcount_dic[year]:
            mcount_dic[year][month] = 1
        else:
            mcount_dic[year][month] += 1

    for year, ycount in sorted(ycount_dic.items(), reverse=True):
        count_list.append({'ycount': True,
                           'year': year,
                           'count': ycount})
        for month, mcount in sorted(mcount_dic[year].items(), reverse=True):
            count_list.append({'ycount': False,
                               'year': year,
                               'd_month': month,
                              'c_month': months[month],
                              'count': mcount})
        # count_list.append({'year_month': k, 'count': v})
    return count_list


def context_data():
    """combine tag_count and year_archive_count data into one single function"""
    tag_count = tag_archive_data(posts)
    year_count = year_archive_data(posts)
    context = {'posts': posts,
               'tag_count': tag_count,
               'year_count': year_count,
               'body_title': ""}
    return context


def post_list(request):
    context = context_data()
    queryset_list = posts
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(body__icontains=query)
        ).distinct() # distinct() to prevent duplicate search results popping up
        body_title = "Search results for: " + query
    else:
        body_title = "All posts"
    paginator = Paginator(queryset_list, 7)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    post_list = paginator.get_page(page)
    context.update({'posts': post_list, 'body_title': body_title})
    return render(request, 'blog/post/list.html', context)


def post_year_archive(request, year):
    context = context_data()
    post_list = Post.objects.all().filter(publish__year=year)
    # post_list = get_object_or_404(Post, publish__year=year, status='published')
    # get_object_or_404 used to return a single post
    context.update({'posts': post_list, 'body_title': 'Posts for {}'.format(year)})
    return render(request, 'blog/post/list.html', context)


def post_month_archive(request, year, month):
    context = context_data()
    post_list = Post.objects.all().filter(publish__year=year).filter(publish__month=month)
    context.update({'posts': post_list, 'body_title': 'Posts for {} {}'.format(months[int(month)], year)})
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, slug):
    context = context_data()
    post_list=[]
    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug,
                             status='published')
    post_list.append(post)
    context.update({"posts": post_list})
    # return render(request, 'blog/post/detail.html', data)

    # process comment data
    comments = post.comments.filter(active=True)
    comment_count = comments.count()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    # create similar posts according to tag
    post_tag = post.tag_list()
    similar_posts = []
    for tag in post_tag:
        posts_with_same_tag = Post.objects.all().filter(status='published', tag=tag).exclude(id=post.id)
        for post_with_same_tag in posts_with_same_tag:
            similar_posts.append(post_with_same_tag)
    similar_posts_count = len(similar_posts)
    context.update({'form': comment_form,
                    'comments': comments,
                    'comment_count': comment_count,
                    'similar_posts': similar_posts,
                    'similar_posts_count': similar_posts_count})
    return render(request, 'blog/post/detail.html', context)


def tag_view(request, tag):
    context = context_data()
    tag_posts = []
    for post in posts:
        tag_list = re.split(", ", post.tag)
        if tag in tag_list:
            tag_posts.append(post)

    # tag_posts = Post.objects.all().filter(tag=tag)
    # tag_posts = get_object_or_404(Post, tag=tag)
    paginator = Paginator(tag_posts, 5)
    page = request.GET.get('page')
    tag_posts = paginator.get_page(page)
    context.update({"posts": tag_posts, 'body_title': 'Posts tagged with "{}"'.format(tag)})
    return render(request, 'blog/post/list.html', context)
    # return render(request, 'blog/tag_view.html', {"posts": tag_posts,
    #                                               'tag_count': sidebardata['tag_count'],
    #                                               'year_count': sidebardata['year_count']})


# def share_post(request, post_id):
#     # get_object_or_404 return a single post, so use it in this function
#     post = get_object_or_404(Post,
#                              id=post_id,
#                              status='published')
#     sent = False
#
#     if request.method == 'POST':
#         form = EmailSharePostForm(request.POST)
#         if form.is_valid():
#             from django.urls import reverse
#             post_url = request.build_absolute_uri(reverse('post_detail', args=(post.publish.year, post.publish.month,
#                                                                                post.publish.day, post.slug)))
#             cd = form.cleaned_data
#             name = cd['name']
#             from_email = cd['email']
#             to_email = cd['to']
#             comment = cd['comment']
#             subject = '{} ({}) recommends you reading "{}"'.format(name, from_email, post.title)
#             message = "Read '{}' at {}. {}'s comments: {}".format(post.title, post_url, name, comment)
#             send_mail(subject, message, from_email, [to_email])
#             sent = True
#     else:
#         form = EmailSharePostForm()
#     return render(request, 'blog/share/index.html', {'post': post,
#                                                      'form': form,
#                                                      'sent': sent})
