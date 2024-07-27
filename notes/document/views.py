from django.shortcuts import render, redirect
from .models import Note
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
 
 
# create editor page
@login_required(login_url='/login/')
def editor(request):
    docid = int(request.GET.get('docid', 0))
    notes = Note.objects.all()
 
    if request.method == 'POST':
        docid = int(request.POST.get('docid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')
 
        if docid > 0:
            note = Note.objects.get(pk=docid)
            note.title = title
            note.content = content
            note.save()
 
            return redirect('/?docid=%i' % docid)
        else:
            note = Note.objects.create(title=title, content=content)
 
            return redirect('/?docid=%i' % note.id)
 
    if docid > 0:
        note = Note.objects.get(pk=docid)
    else:
        note = ''
 
    context = {
        'docid': docid,
        'notes': notes,
        'note': note
    }
 
    return render(request, 'editor.html', context)
 
# create delete notes page
 
 
@login_required(login_url='/login/')
def delete_note(request, docid):
    note = Note.objects.get(pk=docid)
    note.delete()
 
    return redirect('/?docid=0')
 
 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/login/')
def editor(request):
    docid = int(request.GET.get('docid', 0))
    
    if request.method == 'POST':
        docid = int(request.POST.get('docid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')

        if docid > 0:
            note = get_object_or_404(Note, pk=docid, user=request.user)
            note.title = title
            note.content = content
            note.save()
            messages.success(request, "Note updated successfully.")
        else:
            Note.objects.create(title=title, content=content, user=request.user)
            messages.success(request, "Note created successfully.")
        
        return redirect('/?docid=%i' % docid)

    if docid > 0:
        note = get_object_or_404(Note, pk=docid, user=request.user)
    else:
        note = None

    notes = Note.objects.filter(user=request.user)
    
    context = {
        'docid': docid,
        'notes': notes,
        'note': note
    }
    return render(request, 'editor.html', context)

@login_required(login_url='/login/')
def delete_note(request, docid):
    note = get_object_or_404(Note, pk=docid, user=request.user)
    note.delete()
    messages.success(request, "Note deleted successfully.")
    return redirect('/?docid=0')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = authenticate(username=username, password=password)
        if user_obj is not None:
            login(request, user_obj)
            return redirect('editor')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, "login.html")

def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is taken")
            return redirect('register')
        user_obj = User.objects.create(username=username)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, "Account created")
        return redirect('login')
    return render(request, "register.html")

def custom_logout(request):
    logout(request)
    return redirect('login')