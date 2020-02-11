# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


from .forms import DocumentForm
from .forms import DocumentfolderForm
from .models import Document
from .models import Details
import hashlib


def home(request):
    user = request.user
    if user.is_authenticated:
        documents = Document.objects.filter(username=request.user)
        check = Details.objects.filter(username=request.user).exists()
        if not check:
            p = Details(username=user)
            p.save()
        details = Details.objects.get(username=request.user)
        return render(request, 'home.html', {'documents': documents, 'details': details})
    else:
        return redirect('login')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy(viewname='login')
    template_name = 'signup.html'


def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        filepath = form.data['filepath']
        #padlength = form.data['padlength']
        files = request.FILES.getlist('document')
        username = request.user
        for doc in files:
            na = doc.name
            hashf = hashlib.md5()
            blocksize = 65536
            for block in iter(lambda: doc.read(blocksize), b""):
                hashf.update(block)
            md5sum = str(hashf.hexdigest())
            check = Document.objects.filter(username=request.user, name=na, filepath=filepath).exists()
            if check:
                Document.objects.filter(username=request.user, name=na, filepath=filepath).delete()
            p = Document(name=na, filepath=filepath, document=doc, username=username, md5sum=md5sum)
            p.save()
        return redirect('home')
    else:
        user = request.user
        if user.is_authenticated:
            form = DocumentForm()
            return render(request, 'upload.html', {
            'form': form
            })
        else:
            return redirect('login')


def delete(request, id):
    user = request.user
    if user.is_authenticated:
        Document.objects.filter(username=request.user, id=id).delete()
        return redirect('home')
    else:
        return redirect('login')

def deadlocksetfalse(request):
    user = request.user
    if user.is_authenticated:
        Details.objects.filter(username=request.user).update(in_sync=False)
        return redirect('home')
    else:
        return redirect('login')


def deadlocksettrue(request):
    user = request.user
    if user.is_authenticated:
        Details.objects.filter(username=request.user).update(in_sync=True)
        return redirect('home')
    else:
        return redirect('login')


def upload_folder(request):
    if request.method == 'POST':
        form = DocumentfolderForm(request.POST, request.FILES)
        filepath = form.data['filepath']
        files = request.FILES.getlist('document')
        username = request.user
        for doc in files:
            na=doc.name
            p = Document(name=na, filepath=filepath, document=doc, username=username)
            p.save()
        return redirect('home')
    else:
        user = request.user
        if user.is_authenticated:
            form = DocumentfolderForm()
            return render(request, 'upload.html', {
            'form': form
            })
        else:
            return redirect('login')
