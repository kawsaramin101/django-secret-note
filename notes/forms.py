from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.hashers import make_password

from .models import Note

class NoteForm(forms.ModelForm):
    password_to_edit = forms.CharField(required=False, max_length=32, min_length=4, help_text='Include this if you want to edit this note.', widget=PasswordInput())
    #password_to_read = forms.CharField(required=False, max_length=32, min_length=4, help_text='Include this if you want to password protect your note.', widget=PasswordInput())
    
    class Meta:
        model = Note 
        fields = ['body', 'password_to_edit']#, 'password_to_read']
        
        #widgets = {
            #'password_to_edit': PasswordInput(),
            #'password_to_read': PasswordInput()
        #}
        
    def save(self, commit=True, *args, **kwargs):
        instance = super(NoteForm, self).save(commit=False)
        password_to_edit = self.cleaned_data.get('password_to_edit') 
        #password_to_read = self.cleaned_data.get('password_to_read')
        #if password_to_read:
            #instance.password_to_read = make_password(password_to_read) 
        if password_to_edit:
            instance.password_to_edit = make_password(password_to_edit)
        instance.save()
        return instance
          
          
class NoteEditForm(forms.ModelForm):
     
    class Meta:
        model = Note 
        fields = ['body']