from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Usuario_autenticacao(models.Model):
    id_usuario_autenticacao = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=500, blank=True, null=True)
    sobrenome = models.CharField(max_length=500, blank=True, null=True)
    celular = models.CharField(max_length=500, blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    senha = models.CharField(max_length=500, blank=True, null=True)
    data_criacao = models.DateTimeField()
    ultima_edicao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuario_autenticacao'

class Usuario_configuracao(models.Model):
    id_usuario_configuracao = models.AutoField(primary_key=True)
    id_usuario_autenticacao = models.ForeignKey(Usuario_autenticacao, on_delete=models.CASCADE)
    endereco = models.JSONField(blank=True, null=True)
    nacionalidade = models.CharField(max_length=100, blank=True, null=True)
    cpf = models.CharField(max_length=50, unique=True, blank=True, null=True)
    genero = models.CharField(max_length=50, blank=True, null=True)
    nome_social = models.CharField(max_length=200, blank=True, null=True)
    data_nascimento = models.DateField(default=None, blank=True, null=True)

    class Meta:
        db_table = 'usuario_configuracao'

class Usuario_exame_arquivo(models.Model):
    id_exame_arquivo = models.AutoField(primary_key=True)
    id_usuario_autenticacao = models.IntegerField()
    laudo = models.CharField(max_length=500, blank=True, null=True)
    nome_exame = models.CharField(max_length=500, blank=True, null=True)
    nome_arquivo = models.CharField(max_length=500, blank=True, null=True)
    extensao = models.CharField(max_length=500, blank=True, null=True)
    profissional = models.CharField(max_length=500, blank=True, null=True)
    data_realizacao = models.CharField(max_length=500, blank=True, null=True)
    id_laboratorio_possui_usuario = models.IntegerField()
    status_exame = models.IntegerField() # 0 - Recusado / 1 - Pendente / 2 - Aprovado # Quando o proprio paciente adiciona um exame ele já fica como aprovado
    comentarios_recusa = models.CharField(max_length=500, default=None, blank=True, null=True)

    class Meta:
        db_table = 'usuario_exame_arquivo'

class UploadedFile(models.Model):
    file = models.FileField(upload_to='arquivos_exames/')
    uploaded_at = models.DateTimeField(auto_now_add=True)