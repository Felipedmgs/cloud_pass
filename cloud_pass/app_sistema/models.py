# app_sistema/models.py
from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings

# Gere uma chave e adicione ao seu settings.py
# key = Fernet.generate_key().decode()
# settings.FERNET_KEY = key

class Credential(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    system = models.CharField(max_length=100)
    module = models.CharField(max_length=100)
    encrypted_password = models.TextField()
    login  = models.CharField(max_length=100, default='default_login')
   
    def save(self, *args, **kwargs):
        f = Fernet(settings.FERNET_KEY.encode())  # Cria uma instância do Fernet com a chave secreta
        self.encrypted_password = f.encrypt(self.encrypted_password.encode()).decode()  # Criptografa a senha
        super().save(*args, **kwargs)

    def get_decrypted_password(self):
        f = Fernet(settings.FERNET_KEY.encode())
        return f.decrypt(self.encrypted_password.encode()).decode()  # Descriptografa a senha
