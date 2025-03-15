from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

from .algorithms import aes
from .models import EncryptedFile
from .forms import FileUploadForm, DecryptFileForm

def index(request):
    form = FileUploadForm()
    return render(request, "cryptography/index.html", {'form': form})


@login_required
def dashboard(request):
    encrypted_files = EncryptedFile.objects.filter(user=request.user)    
    return render(request, 'cryptography/dashboard.html', {'encrypted_files': encrypted_files})


def encrypter(request):
    encrypted_file = None

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            encrypted_data, aes_key = aes.encrypt_file(uploaded_file)
            
            output_filename = f"{uploaded_file.name.split('.')[0]}_AES.enc"
            key_filename = f"{uploaded_file.name.split('.')[0]}_key"

            if request.user.is_authenticated:
                encrypted_file = EncryptedFile(
                    filename=uploaded_file.name,
                    encrypted_data=encrypted_data[16:],  
                    iv=encrypted_data[:16],  
                    aes_key=aes_key,  
                    user=request.user
                )
                encrypted_file.save()
                
                encrypted_file.output_file.save(output_filename, ContentFile(encrypted_data))
                encrypted_file.key_file.save(key_filename, ContentFile(aes_key))
            else:
                encrypted_file = EncryptedFile(
                    filename=uploaded_file.name,
                    encrypted_data=encrypted_data[16:],  
                    iv=encrypted_data[:16],  
                    aes_key=aes_key,  
                )
                encrypted_file.output_file.save(output_filename, ContentFile(encrypted_data))
                encrypted_file.key_file.save(key_filename, ContentFile(aes_key))

            return render(request, 'cryptography/encrypter.html', {'form': form, 'encrypted_file': encrypted_file})
    else:
        form = FileUploadForm()

    return render(request, 'cryptography/encrypter.html', {'form': form})


def decrypter(request, file_id=None):
    decrypted_data = None

    if request.method == 'GET' and file_id is not None:
        encrypted_file = get_object_or_404(EncryptedFile, id=file_id)
        key_file = encrypted_file.key_file

        try:
            encrypted_file_data = encrypted_file.output_file.read()
            key_data = key_file.read()

            decrypted_data = aes.decrypt_file(encrypted_file_data, key_data)

            original_filename = encrypted_file.filename.rsplit('.', 1)[0]
            output_filename = f"decrypted_{original_filename}.txt"

            response = HttpResponse(decrypted_data, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
            return response

        except Exception as e:
            error_message = f"Decryption failed: {str(e)}"
            return render(request, "cryptography/dashboard.html", {'error': error_message})

    if request.method == 'POST':
        form = DecryptFileForm(request.POST, request.FILES)
        if form.is_valid():
            encrypted_file = request.FILES['encrypted_file']
            key_file = request.FILES['key_file']
            
            try:
                encrypted_file_data = encrypted_file.read()
                
                key_data = key_file.read()
                
                decrypted_data = aes.decrypt_file(encrypted_file_data, key_data)

                original_filename = encrypted_file.name.rsplit('.', 1)[0]
                output_filename = f"decrypted_{original_filename}.txt"
                
                response = HttpResponse(decrypted_data, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
                return response

            except Exception as e:
                error_message = f"Decryption failed: {str(e)}"
                return render(request, "cryptography/decrypter.html", {'form': form, 'error': error_message})

    else:
        form = DecryptFileForm()

    return render(request, "cryptography/decrypter.html", {'form': form})


def download_file(request, file_id, file_type):
    encrypted_file = get_object_or_404(EncryptedFile, id=file_id)

    base_filename = encrypted_file.filename.rsplit('.', 1)[0]

    if file_type == 'encrypted':
        file_content = encrypted_file.output_file.read()
        filename = f"{base_filename}_aes.enc"
    elif file_type == 'key':
        file_content = encrypted_file.key_file.read()
        filename = f"{base_filename}_key"
    else:
        return HttpResponse("Invalid file type", status=400)

    response = HttpResponse(file_content, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def delete_file(request, file_id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to delete files.")
        return HttpResponseRedirect(reverse('login'))

    encrypted_file = get_object_or_404(EncryptedFile, id=file_id, user=request.user)
    encrypted_file.delete()

    messages.success(request, f"The file {encrypted_file.filename} has been deleted.")
    return HttpResponseRedirect(reverse('dashboard'))
