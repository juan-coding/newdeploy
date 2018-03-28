from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound


def cv_view(request):
    fs = FileSystemStorage()
    filename = 'CV_Juan Li_webDev.pdf'
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')