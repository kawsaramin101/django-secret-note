from django.urls import path

from .views import (index, note_detail, note_edit,
enter_password_to_read, enter_password_to_edit)


app_name = 'notes'

urlpatterns = [
    path('', index, name="index"),
    path('note/<str:id>/', note_detail, name="note_detail"),
    path('edit/<str:id>/', note_edit, name="note_edit"),
    
    path('enter/password_to_read/<str:id>/', enter_password_to_read, name="enter_password_to_read"),
    path('enter/password_to_edit/<str:id>/', enter_password_to_edit, name="enter_password_to_edit"),
]
