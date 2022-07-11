from django.shortcuts import render, get_object_or_404
from django.urls import reverse 
from django.shortcuts import redirect 
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages

from .models import Note
from .forms import NoteForm, NoteEditForm


def index(request):
    if request.method == "POST":
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            password_to_read = note_form.cleaned_data.get("password_to_read")
            password_to_edit = note_form.cleaned_data.get("password_to_edit")
            if password_to_read:
                request.session["password_to_read"] = password_to_read 
            if password_to_edit:
                request.session["password_to_edit"] = password_to_edit
            return redirect(reverse('notes:note_detail', kwargs={'secondary_id': note.secondary_id}))
        return render(request, 'notes/index.html', {'note_form': note_form})
    note_form = NoteForm()
    return render(request, 'notes/index.html', {'note_form': note_form})
    

def note_detail(request, secondary_id):
    note = get_object_or_404(Note, secondary_id=secondary_id)
    if not note.password_to_read:
        return render(request, 'notes/detail.html', {'note': note})
    else:
        password_to_read = request.session.get('password_to_read')
        if password_to_read:
            if check_password(password_to_read, note.password_to_read):
                return render(request, 'notes/detail.html', {'note': note})
            else:
                messages.error(request, "Password is incorrect.")
                return redirect(reverse('notes:enter_password_to_read', kwargs={'secondary_id': note.secondary_id}))
        else:
            return redirect(reverse('notes:enter_password_to_read', kwargs={'secondary_id': note.secondary_id}))
            
            
def enter_password_to_read(request, secondary_id):
    if request.method == "POST":
        password_to_read = request.POST.get('password_to_read')
        if password_to_read:
            request.session['password_to_read'] = password_to_read
            return redirect(reverse('notes:note_detail', kwargs={'secondary_id': secondary_id}))
        messages.error(request, "Password can't be empty.")
        return render(request, 'notes/enter_password_to_read.html')
    return render(request, 'notes/enter_password_to_read.html')
    
    
def note_edit(request, secondary_id):
    note = get_object_or_404(Note, secondary_id=secondary_id)
    if not note.password_to_edit:
        messages.info(request, "No password was given when creating the note, this note cannot be edited.")
        return render(request, 'notes/detail.html', {'note': note})
    password_to_edit = request.session.get('password_to_edit')
    if not password_to_edit:
        return redirect(reverse('notes:enter_password_to_edit', kwargs={'secondary_id': note.secondary_id}))
    if check_password(password_to_edit, note.password_to_edit):
        if request.method == "POST":
            note_form = NoteEditForm(request.POST, instance=note)
            if note_form.is_valid():
                note_form.save()
                password_to_read = note_form.cleaned_data.get("password_to_read")
                if password_to_read:
                    request.session["password_to_read"] = password_to_read
                messages.success(request, "Note edited successfully.")
                return redirect(reverse('notes:note_detail', kwargs={'secondary_id': note.secondary_id}))
            return render(request, 'notes/index.html', {'note_form': note_form})
        note_form = NoteEditForm(instance=note)
        return render(request, 'notes/edit.html', {'note_form': note_form})
    else:
        messages.error(request, "Password is incorrect.")
        return redirect(reverse('notes:enter_password_to_edit', kwargs={'secondary_id': note.secondary_id}))
 
 
def enter_password_to_edit(request, secondary_id):
    if request.method == "POST":
        password_to_edit = request.POST.get('password_to_edit')
        if password_to_edit:
            request.session['password_to_edit'] = password_to_edit
            return redirect(reverse('notes:note_edit', kwargs={'secondary_id': secondary_id}))
        messages.error(request, "Password can't be empty.")
        return render(request, 'notes/enter_password_to_edit.html')
    return render(request, 'notes/enter_password_to_edit.html')
    