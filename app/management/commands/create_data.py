import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand

from ...models import Category, Product

class Command(BaseCommand):
    help = "Command to insert test data to the database"

    def handle(self, *args, **kwargs):
        category_data = pd.read_csv("app/management/commands/categories.csv", sep=";").replace({np.nan: None})
        product_data = pd.read_csv("app/management/commands/products.csv", sep=";").replace({np.nan: None})

        for _, category_row in category_data.iterrows():
            row = category_row.to_dict()
            Category.objects.get_or_create(**row)

        for _, product_row in product_data.iterrows():
            row = product_row.to_dict()
            row["category"] = Category.objects.get(name=row["category"])
            Product.objects.get_or_create(**row)