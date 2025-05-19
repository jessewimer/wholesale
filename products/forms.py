# Form to display products to the admin user
from django import forms
from .models import Product
from stores.models import Store

class ProductForm(forms.Form):
    # store_choices = [
    #     ('1', 'All Stores'),
    #     [(store.store_number, store.name) for store in Store.objects.all()]
    # ]
    store_choices = [
        ('1', 'All Stores'),
    ] + [(store.store_number, store.name) for store in Store.objects.all()]

    store_selection = forms.ChoiceField(
        choices=store_choices,
        label='Select a Store'
    )

    store_selection = forms.ChoiceField(
        choices=store_choices,
        label='Select a Store'
    )

    category_choices = [
        ('all', 'All Categories'),
        ('vegetables', 'Vegetables'),
        ('herbs', 'Herbs'),
        ('flowers', 'Flowers'),
    ]

    category_selection = forms.ChoiceField(
        #required=False,
        choices=category_choices,
        label='Select a Category'
    )

    veg_type_choices = [
        ('all', 'All Crops'),
        ('bean', 'Bean'),
        ('beet', 'Beet'),
        ('carrot', 'Carrot'),
        ('tomato', 'Tomato'),
        ('cucumber', 'Cucumber'),
        ('lettuce', 'Lettuce'),
        ('pepper', 'Pepper'),
        ('squash', 'Squash'),
        ('corn', 'Corn'),
        ('melon', 'Melon'),
        ('broccoli', 'Broccoli'),
        ('greens', 'Greens'),
        ('kale', 'Kale'),
        ('cabbage', 'Cabbage'),
        ('cauliflower', 'Cauliflower'),
        ('pea', 'Pea'),
        ('radish', 'Radish'),
        ('spinach', 'Spinach'),
        ('onion', 'Onion'),
        ('amaranth', 'Amaranth'),
        ('aster', 'Aster'),
        ('bachelor’s button', 'Bachelor’s Button'),
        ('basket flower', 'Basket Flower'),
        ('borage', 'Borage'),
        ('burdock', 'Burdock'),
        ('calendula', 'Calendula'),
        ('cardoon', 'Cardoon'),
        ('celeriac', 'Celeriac'),
        ('celosia', 'Celosia'),
        ('cerinthe', 'Cerinthe'),
        ('chard', 'Chard'),
        ('cosmos', 'Cosmos'),
        ('foxglove', 'Foxglove'),
        #add/remove other groups as needs
    ]

    veg_type_selection = forms.ChoiceField(
        choices=veg_type_choices,
        label='Select a Veg Type'
    )

    selected_varieties = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, seed_availabilities=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Get all the available product varieties from the database
        all_varieties_and_item_nums = Product.objects.values_list('variety', 'item_number', 'category', 'veg_type').distinct()

        # Added this ......
        all_varieties_and_item_nums = sorted(
            all_varieties_and_item_nums,
            key=lambda x: (x[2], x[3], x[0])  # Sort by category, veg_type, and variety
        )


        self.variety_info_list = [
            {'variety': variety, 'item_number': item_number, 'category': category, 'veg_type': veg_type}
            for variety, item_number, category, veg_type in all_varieties_and_item_nums
        ]

        # Use the provided seed_availabilities if available, otherwise use an empty list
        if seed_availabilities:
            seed_availabilities = [int(item_number) for item_number, is_available in seed_availabilities.items() if is_available]
        else:
            seed_availabilities = []

        choices = [
            (variety, item_number, category, veg_type) for variety, item_number, category, veg_type in all_varieties_and_item_nums
        ]

        # Set the form choices
        self.fields['selected_varieties'].choices = choices

        if seed_availabilities:

            # Get the corresponding varieties for the available item_numbers
            # initial_varieties = [variety for variety, item_number, category, veg_type in all_varieties_and_item_nums if item_number in seed_availabilities]

            # Set the initial value for the selected_varieties field
            self.fields['selected_varieties'].initial = seed_availabilities


