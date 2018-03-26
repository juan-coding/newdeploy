from django import forms


# class EmailCommentForm(forms.Form):
#     your_name = forms.CharField(label='Your name', max_length=100, required=True)
#     your_email = forms.CharField(label="Your email", max_length=100, required=True)
#     your_comment = forms.CharField(label="Your comment", max_length=100, widget=forms.Textarea,required=True)
#

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
    sender_name = forms.CharField(max_length=100)
    sender_email = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
