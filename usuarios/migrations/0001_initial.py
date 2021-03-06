# Generated by Django 3.0.3 on 2020-07-08 03:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.FileField(blank=True, null=True, upload_to='avatar')),
                ('slack_id', models.TextField(blank=True, max_length=250, null=True)),
                ('recibir_correos', models.BooleanField(default=False)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'usuarios_perfiles',
            },
        ),
    ]
