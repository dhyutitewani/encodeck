from django.db import models
from django.conf import settings


class EncryptedFile(models.Model):
    filename = models.CharField(max_length=255)
    encrypted_data = models.BinaryField()
    iv = models.BinaryField() 
    aes_key = models.BinaryField()  
    uploaded_at = models.DateTimeField(auto_now_add=True)
    key_file = models.FileField(upload_to='keys/', null=True, blank=True)
    output_file = models.FileField(upload_to='encrypted_files/', null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="encrypted_files"
    )

    def __str__(self):
        return f"EncryptedFile {self.filename} by {self.user.first_name if self.user else 'Anonymous'}"
