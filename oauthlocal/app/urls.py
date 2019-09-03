from django.urls import path
from .views import (top_view,
                    callback_view)

urlpatterns = [
    path('', top_view, name='top'),
    path('callback', callback_view, name='callback')
]
