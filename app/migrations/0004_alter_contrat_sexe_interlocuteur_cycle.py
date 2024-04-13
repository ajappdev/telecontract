# Generated by Django 4.2.11 on 2024-04-12 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_contrat_created_at_contrat_date_contrat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrat',
            name='sexe_interlocuteur',
            field=models.CharField(blank=True, choices=[('M.', 'M.'), ('Mme.', 'Mme.')], default='', max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('statut', models.CharField(blank=True, choices=[('En cours', 'En cours'), ('Payé', 'Payé'), ('Achevé', 'Achevé')], default='', max_length=200, null=True)),
                ('contrat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.contrat')),
            ],
        ),
    ]
