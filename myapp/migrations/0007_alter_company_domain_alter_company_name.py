# Generated by Django 5.0.7 on 2024-09-02 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_company_year_founded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='domain',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
