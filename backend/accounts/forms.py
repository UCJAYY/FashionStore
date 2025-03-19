from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    
    # Explicitly define choice-based fields to ensure proper validation
    age_range = forms.ChoiceField(
        choices=CustomUser.AGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    gender = forms.ChoiceField(
        choices=CustomUser.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    clothing_size = forms.ChoiceField(
        choices=CustomUser.SIZE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    preferred_style = forms.ChoiceField(
        choices=CustomUser.STYLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    budget = forms.ChoiceField(
        choices=CustomUser.BUDGET_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    brand_preferences = forms.ChoiceField(
        choices=CustomUser.BRAND_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    body_type = forms.ChoiceField(
        choices=CustomUser.BODY_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    favorite_colors = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., Red, Blue, Green',
            'class': 'form-control'
        }),
        help_text="Separate colors with commas"
    )

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password1',
            'password2',
            'age_range',
            'gender',
            'clothing_size',
            'preferred_style',
            'budget',
            'favorite_colors',
            'brand_preferences',
            'body_type',
            'sustainability_preference'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove default password help text
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None