from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from hello.boss import Boss
from .models import Greeting
from .models import Document
from .forms import DocumentForm
import time

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            b = Boss()
            b.graph_spectrogram(newdoc.docfile.url)
            # Redirect to the document list after POST
            return render(request, "audio.html", {'document': newdoc})
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()


    # Render list page with the documents and the form
    return render(request, "upload.html", {'documents': documents, 'form': form })

def record(request):
    if request.method == 'POST':
        newdoc = Document(docfile = request.FILES['audio'])
        newdoc.save()

    return render(request, "record.html", {})

def audio(request):
    return render(request, "audio.html", {})

def aboutUs(request):
    return render(request, "about-us.html", {})
