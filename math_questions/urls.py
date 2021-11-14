from django.urls import path

from . import views

urlpatterns = [
    # ex: /math_questions/content_list/
    path('content_list/', views.questions, name='questions'),
    path('label_list/', views.labels, name="labels")
]
