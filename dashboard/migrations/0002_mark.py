# Generated by Django 5.0.4 on 2024-05-20 13:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.PositiveIntegerField()),
                ('comment', models.TextField(blank=True, default='')),
                ('marked_at', models.DateTimeField(auto_now_add=True)),
                ('remarked_at', models.DateTimeField(auto_now=True)),
                ('criterion', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.criterion')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to=settings.AUTH_USER_MODEL)),
                ('marked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.submission')),
            ],
            options={
                'unique_together': {('submission', 'employee')},
            },
        ),
    ]
