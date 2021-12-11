from django.urls import path

from . import views

urlpatterns = [
    # ex: /math_questions/content_list/
    path('content_list', views.questions, name='questions'),
    path('label_list', views.labels, name="labels"),
    path('cleaned_result', views.cleaned_data, name='cleaned data'),
    path('clean_data', views.clean, name='clean data'),
    path('data_summary', views.data_summary, name='data summary'),
    path('read_vector', views.read_vector, name='get formula vector'),

    path('manual_tag', views.tag, name='manual tag'),
    path('manual_check', views.check_same_label, name='manual check')
]
