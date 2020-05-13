# Generated by Django 3.0.3 on 2020-03-24 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0005_auto_20200302_0159'),
        ('kanban', '0009_asignacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='proyecto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='proyectos.Proyecto'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tarea',
            name='lista_kanban',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kanban.ListaKanban'),
        ),
    ]