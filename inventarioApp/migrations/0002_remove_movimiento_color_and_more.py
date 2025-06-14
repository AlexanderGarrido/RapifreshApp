# Generated by Django 5.0.1 on 2025-06-04 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarioApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimiento',
            name='color',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='precio_anterior',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='precio_nuevo',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='talla',
        ),
        migrations.RemoveField(
            model_name='productos',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='productos',
            name='precio',
        ),
        migrations.RemoveField(
            model_name='productos',
            name='talla',
        ),
        migrations.AddField(
            model_name='movimiento',
            name='proveedor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='productos',
            name='proveedor',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productos',
            name='categoria',
            field=models.CharField(choices=[('Indumentaria', 'Indumentaria'), ('Herramientas', 'Herramientas'), ('Cajas', 'Cajas'), ('Film', 'Film'), ('Bolsa', 'Bolsa')], default='Indumentaria', max_length=50),
        ),
    ]
