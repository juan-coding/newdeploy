from django.shortcuts import render
# from django.http import HttpResponse
from contact.forms import ContactForm
from django.core.mail import send_mail


def index(request):

    sent = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender_name = form.cleaned_data["sender_name"]
            sender_email = form.cleaned_data["sender_email"]
            cc_myself = form.cleaned_data["cc_myself"]

            recipients = ['juanli.work@gmail.com']
            if cc_myself:
                recipients.append(sender_email)

            message = "This message was sent by {} with email: {}".format(sender_name, sender_email) + '\n' +\
                      'Message:' + '\n' + message
            send_mail(subject, message, sender_email, recipients)
            sent = True
            # return HttpResponse('/THANKS FOR YOUR MESSAGE!/')
    else:
        form = ContactForm()

    return render(request, "contact/index.html",
                  {"form": form,
                   "sent": sent})



