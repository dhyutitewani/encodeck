from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField()


class DecryptFileForm(forms.Form):
    encrypted_file = forms.FileField(label='Encrypted File')
    key_file = forms.FileField(label='Key File')