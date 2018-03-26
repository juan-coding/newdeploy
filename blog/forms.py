from django import forms
from .models import Comment, Post


class EmailSharePostForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'upload', 'body', 'publish', 'status', 'tag']

