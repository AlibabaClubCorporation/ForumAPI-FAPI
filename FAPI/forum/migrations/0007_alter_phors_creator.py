# Generated by Django 4.0.5 on 2022-07-12 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_themes_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phors',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phors', to='forum.usersofclient', verbose_name='Ссылка на создателя фора'),
        ),
    ]