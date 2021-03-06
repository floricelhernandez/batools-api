# Generated by Django 3.0.3 on 2020-07-08 03:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyectos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaKanban',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(max_length=35)),
                ('col_pila_sin_priorizar', models.BooleanField(default=False)),
                ('col_finalizado', models.BooleanField(default=False)),
                ('color', models.TextField(max_length=8)),
                ('orden', models.PositiveSmallIntegerField(default=1)),
                ('fijar_en_kanban', models.BooleanField(default=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('estatus', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='proyectos.Estatus')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proyectos.Sprint')),
            ],
            options={
                'db_table': 'listas_kanban',
            },
        ),
        migrations.CreateModel(
            name='Prioridad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(max_length=25)),
                ('descripcion', models.TextField(max_length=50)),
                ('clave', models.TextField(default='ninguno', max_length=25)),
                ('orden', models.SmallIntegerField(default=1)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'prioridades',
            },
        ),
        migrations.CreateModel(
            name='TipoTarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(max_length=25)),
                ('clave', models.TextField(default='kanban', max_length=25)),
            ],
            options={
                'db_table': 'tipos_tarea',
            },
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.PositiveSmallIntegerField(default=1)),
                ('no_tarea', models.IntegerField(default=1)),
                ('nombre', models.TextField(max_length=150)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('vencimiento', models.DateField(blank=True, null=True)),
                ('inicio', models.DateTimeField(blank=True, null=True)),
                ('fin', models.DateTimeField(blank=True, null=True)),
                ('fijar_en_kanban', models.BooleanField(default=True)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('estatus', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='proyectos.Estatus')),
                ('lista_kanban', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kanban.ListaKanban')),
                ('prioridad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kanban.Prioridad')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proyectos.Proyecto')),
                ('tipo_tarea', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='kanban.TipoTarea')),
            ],
            options={
                'db_table': 'tareas',
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField(max_length=500)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comentarios', to='kanban.Tarea')),
            ],
            options={
                'db_table': 'tareas_comentarios',
            },
        ),
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kanban.Tarea')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participante_asignado', to=settings.AUTH_USER_MODEL)),
                ('usuario_asigna', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tareas_asignaciones',
            },
        ),
        migrations.CreateModel(
            name='Adjunto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField(blank=True, max_length=200, null=True)),
                ('nombre_archivo', models.TextField(blank=True, max_length=200, null=True)),
                ('ruta', models.TextField(blank=True, max_length=1000, null=True)),
                ('archivo', models.FileField(upload_to='')),
                ('tipo', models.TextField(blank=True, max_length=25, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adjuntos', to='kanban.Tarea')),
            ],
            options={
                'db_table': 'tareas_adjuntos',
            },
        ),
    ]
