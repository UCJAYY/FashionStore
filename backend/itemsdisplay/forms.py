# itemsdisplay/forms.py
from django import forms
from .models import FashionItem

# Define choices for dropdown fields
AGE_RANGE_CHOICES = [
    ("", "Age Range"),
    ("18-24", "18-24"),
    ("25-34", "25-34"),
    ("35-44", "35-44"),
    ("45+", "45+"),
]

PROFESSION_CHOICES = [
    ("", "Profession"),
    ("Student", "Student"),
    ("Professional", "Professional"),
    ("Entrepreneur", "Entrepreneur"),
    ("Creative", "Creative"),
    ("Retired", "Retired"),
]

SIZE_CHOICES = [
    ("", "Size"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
]

GENDER_CHOICES = [
    ("", "Gender"),
    ("Male", "Male"),
    ("Female", "Female"),
    ("Unisex", "Unisex"),
]

BRAND_CHOICES = [
    ("", "Brand"),
    ("Zara", "Zara"),
    ("H&M", "H&M"),
    ("EcoChic", "EcoChic"),
    ("UrbanStyle", "UrbanStyle"),
    ("LuxuryLine", "LuxuryLine"),
]

BODY_TYPE_CHOICES = [
    ("", "Body Type"),
    ("Hourglass", "Hourglass"),
    ("Pear", "Pear"),
    ("Athletic", "Athletic"),
    ("Rectangle", "Rectangle"),
    ("Petite", "Petite"),
]

OCCASION_CHOICES = [
    ("", "Select Occasions"),
    ("Work", "Work"),
    ("Casual", "Casual"),
    ("Party", "Party"),
    ("Weddings", "Weddings"),
]

class FashionItemForm(forms.ModelForm):
    age_range = forms.ChoiceField(choices=AGE_RANGE_CHOICES, required=False)
    profession = forms.ChoiceField(choices=PROFESSION_CHOICES, required=False)
    size = forms.ChoiceField(choices=SIZE_CHOICES, required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    brand = forms.ChoiceField(choices=BRAND_CHOICES, required=False)
    body_type = forms.ChoiceField(choices=BODY_TYPE_CHOICES, required=False)
    occasion = forms.ChoiceField(choices=OCCASION_CHOICES, required=False)

    class Meta:
        model = FashionItem
        fields = [
            'name', 'description', 'price', 'image',
            'age_range', 'profession', 'size', 'gender',
            'brand', 'body_type', 'occasion'
        ]
