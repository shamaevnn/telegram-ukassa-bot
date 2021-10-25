from django.urls import path
from .views import ProcessUkassaEvent


urlpatterns = [
    path('event/', ProcessUkassaEvent.as_view()),
]
