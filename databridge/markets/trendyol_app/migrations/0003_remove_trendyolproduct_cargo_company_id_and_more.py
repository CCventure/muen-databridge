# Generated by Django 5.1.8 on 2025-04-04 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("trendyol_app", "0002_rename_product_trendyolproduct"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trendyolproduct",
            name="cargo_company_id",
        ),
        migrations.RemoveField(
            model_name="trendyolproduct",
            name="dimensional_weight",
        ),
    ]
