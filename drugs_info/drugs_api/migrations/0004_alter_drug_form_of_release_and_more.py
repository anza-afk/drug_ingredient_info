# Generated by Django 4.0.6 on 2022-10-31 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs_api', '0003_alter_drug_recipe_only'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='form_of_release',
            field=models.CharField(blank=True, max_length=2048, null=True, verbose_name='Лекарственная форма'),
        ),
        migrations.AlterField(
            model_name='drug',
            name='pharmacological_class',
            field=models.CharField(blank=True, max_length=2048, null=True, verbose_name='Фармакологическая группа'),
        ),
        migrations.AlterField(
            model_name='drug',
            name='recipe_only',
            field=models.BooleanField(null=True, verbose_name='Требуется рецепт'),
        ),
    ]
