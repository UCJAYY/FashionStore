from django.urls import path
from .views import itemsdisplay_view, add_fashion_item, delete_item, my_recommendations

urlpatterns = [
    path('', itemsdisplay_view, name='itemsdisplay'),
    path('add/', add_fashion_item, name='add_fashion_item'),
    path('delete/<int:item_id>/', delete_item, name='delete_item'),
    path('recommendations/', my_recommendations, name='my_recommendations'),
]
