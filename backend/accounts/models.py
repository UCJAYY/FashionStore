from django.db import models

# Create your models here.
# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

AGE_CHOICES = [
    ('under_18', 'Under 18'),
    ('18_24', '18-24'),
    ('25_34', '25-34'),
    ('35_44', '35-44'),
    ('45_54', '45-54'),
    ('55_64', '55-64'),
    ('65_plus', '65+'),
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('non_binary', 'Non-binary'),
    ('prefer_not_to_say', 'Prefer not to say'),
]

BODY_TYPE_CHOICES = [
    ('hourglass', 'Hourglass'),
    ('pear', 'Pear'),
    ('athletic', 'Athletic'),
    ('rectangle', 'Rectangle'),
    ('petite', 'Petite'),
]

BUDGET_CHOICES = [
    ('0_50', '$0 - $50'),
    ('50_100', '$50 - $100'),
    ('100_200', '$100 - $200'),
    ('200_plus', '$200+'),
]

SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large')
    ]

STYLE_CHOICES = [
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('bohemian', 'Bohemian'),
        ('sporty', 'Sporty'),
        ('business', 'Business')
    ]
BRAND_CHOICES = [
    ('zara', 'Zara'),
    ('hm', 'H&M'),
    ('ecochic', 'EcoChic'),
    ('urbanstyle', 'UrbanStyle'),
    ('luxuryline', 'LuxuryLine')
]

class CustomUser(AbstractUser):
    # Remove the username field and use email as the primary identifier.
    username = None

    email = models.EmailField(unique=True, blank=False)
    AGE_CHOICES = AGE_CHOICES
    GENDER_CHOICES = GENDER_CHOICES
    SIZE_CHOICES = SIZE_CHOICES
    STYLE_CHOICES = STYLE_CHOICES
    BUDGET_CHOICES = BUDGET_CHOICES
    BRAND_CHOICES = BRAND_CHOICES
    BODY_TYPE_CHOICES = BODY_TYPE_CHOICES

    # Required user details for tailored recommendations
    age_range = models.CharField(
        max_length=10,
        choices=AGE_CHOICES,
        blank=False,
        null=False,
        help_text="Select your age range."
    )
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=False,
        null=False,
        help_text="Select your gender."
    )
   
# Update in models.py


    clothing_size = models.CharField(
        max_length=2,
        choices=SIZE_CHOICES,
        blank=False
    )
    # Add to models.py


    preferred_style = models.CharField(
        max_length=20,
        choices=STYLE_CHOICES,
        blank=False
    )
    budget = models.CharField(
        max_length=50,
        choices=BUDGET_CHOICES,
        blank=False,
        null=False,
        help_text="Select your typical budget range for fashion items."
    )
    favorite_colors = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Your favorite colors, separated by commas."
    )

    # Change in models.py
    brand_preferences = models.CharField(
        max_length=200,
        blank=False,
        help_text="Comma-separated list of brands"
    )
    
    body_type = models.CharField(
        max_length=50,
        choices=BODY_TYPE_CHOICES,
        blank=False,
        null=False,
        help_text="Select your body type from the available options."
    )
    # Although booleans are automatically assigned a default, this field can capture a user's eco-friendly preference.
    sustainability_preference = models.BooleanField(
        default=False,
        help_text="Check if you prefer eco-friendly fashion options."
    )
  

    # Use email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS are prompted when creating a superuser.
    # Note: The password field is automatically required.
    REQUIRED_FIELDS = [
        'age_range', 'gender',
        'clothing_size', 'preferred_style', 'budget', 'favorite_colors', 
        'brand_preferences', 'body_type'
    ]

    def __str__(self):
        return self.email
