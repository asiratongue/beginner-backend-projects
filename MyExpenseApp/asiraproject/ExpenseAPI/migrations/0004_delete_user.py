# Generated by Django 5.1.2 on 2024-10-29 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpenseAPI', '0003_alter_expense_userid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
