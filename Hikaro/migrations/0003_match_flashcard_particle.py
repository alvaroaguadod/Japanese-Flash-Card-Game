# Generated by Django 4.1.5 on 2023-03-02 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hikaro', '0002_remove_flashcard_answer_remove_flashcard_question_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, default=None, max_length=200)),
                ('username', models.CharField(max_length=50, verbose_name='username')),
            ],
        ),
        migrations.AddField(
            model_name='flashcard',
            name='particle',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]