import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from ...models import Category, Product, Image, UserProfile

class Command(BaseCommand):
    help = "Command to insert test data to the database"

    def handle(self, *args, **kwargs):
        category_data = pd.read_csv("app/management/commands/data/categories.csv", sep=";").replace({np.nan: None})
        product_data = pd.read_csv("app/management/commands/data/products.csv", sep=";").replace({np.nan: None})
        image_data = pd.read_csv("app/management/commands/data/images.csv", sep=";").replace({np.nan: None})
        product_image_data = pd.read_csv("app/management/commands/data/product_images.csv", sep=";").replace({np.nan: None})
        user_data = pd.read_csv("app/management/commands/data/users.csv", sep=";").replace({np.nan: ""})

        for _, category_row in category_data.iterrows():
            row = category_row.to_dict()
            Category.objects.get_or_create(**row)

        for _, product_row in product_data.iterrows():
            row = product_row.to_dict()
            Product.objects.get_or_create(**row)

        for _, image_row in image_data.iterrows():
            row = image_row.to_dict()
            Image.objects.get_or_create(**row)

        for _, product_image_row in product_image_data.iterrows():
            row = product_image_row.to_dict()
            product = Product.objects.get(pk=row["product_id"])
            image = Image.objects.get(pk=row["image_id"])
            product.images.add(image)
            product.save()

        for _, user_row in user_data.iterrows():
            row = user_row.to_dict()
            user = User.objects.create_user(**row)
            UserProfile.objects.get_or_create(user=user)
