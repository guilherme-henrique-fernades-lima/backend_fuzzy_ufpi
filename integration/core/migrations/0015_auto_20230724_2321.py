# Generated by Django 3.2.4 on 2023-07-25 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_emprestimoitem_tp_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprestimo',
            name='bairro',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='cep',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='cidade',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='complLogr',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='cpf',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='estado',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='logradouro',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='numLogr',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='telefone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
