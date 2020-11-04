# Generated by Django 2.1.7 on 2019-05-27 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchdb_coocurence', '0006_coocurence_data_base'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColapsedOnLegionellaStrains',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene1', models.CharField(max_length=20)),
                ('gene2', models.CharField(max_length=20)),
                ('together', models.IntegerField()),
                ('first_only', models.IntegerField()),
                ('second_only', models.IntegerField()),
                ('neither', models.IntegerField()),
                ('pvalue', models.DecimalField(decimal_places=100, max_digits=500)),
                ('data_base', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ColapsedOnLegionellaStrainWithingSpecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene1', models.CharField(max_length=20)),
                ('gene2', models.CharField(max_length=20)),
                ('together', models.IntegerField()),
                ('first_only', models.IntegerField()),
                ('second_only', models.IntegerField()),
                ('neither', models.IntegerField()),
                ('pvalue', models.DecimalField(decimal_places=100, max_digits=500)),
                ('data_base', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ColapsedOnSpeciesLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene1', models.CharField(max_length=20)),
                ('gene2', models.CharField(max_length=20)),
                ('together', models.IntegerField()),
                ('first_only', models.IntegerField()),
                ('second_only', models.IntegerField()),
                ('neither', models.IntegerField()),
                ('pvalue', models.DecimalField(decimal_places=100, max_digits=500)),
                ('data_base', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
