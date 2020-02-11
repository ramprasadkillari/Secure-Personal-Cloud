from db_file_storage.form_widgets import DBClearableFileInput
from django import forms
from .models import Document


class DocumentfolderForm(forms.ModelForm):
    document = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'webkitdirectory': True, 'directory': True}))

    class Meta:
        model = Document
        exclude = ['username','name']
        widgets = {
            'document': DBClearableFileInput
        }


class DocumentForm(forms.ModelForm):
    document = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Document
        exclude = ['username', 'name', 'enc_scheme', 'md5sum']
        widgets = {
            'document': DBClearableFileInput
        }

