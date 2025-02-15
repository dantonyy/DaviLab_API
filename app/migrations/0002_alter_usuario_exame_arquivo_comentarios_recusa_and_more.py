# Generated by Django 4.2.7 on 2023-11-06 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario_exame_arquivo',
            name='comentarios_recusa',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='usuario_exame_arquivo',
            name='data_realizacao',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='usuario_exame_arquivo',
            name='extensao',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='usuario_exame_arquivo',
            name='laudo',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='usuario_exame_arquivo',
            name='nome_arquivo',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='usuario_exame_arquivo',
            name='nome_exame',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='usuario_exame_arquivo',
            name='profissional',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
