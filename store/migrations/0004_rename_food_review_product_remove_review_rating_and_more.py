# Generated by Django 4.2.3 on 2023-09-01 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0003_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='food',
            new_name='product',
        ),
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]