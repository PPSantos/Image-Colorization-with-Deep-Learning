from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('stats', views.stats_view, name='stats'),

    # AJAX endpoints
    path('ajax/submit', views.ajax_submit_test, name='ajax-submit-test'),
]
