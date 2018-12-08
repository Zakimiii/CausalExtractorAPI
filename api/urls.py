from rest_framework import routers
from django.urls import path, re_path
from api import views

app_name = 'api'
urlpatterns = [
    #crawles
    re_path(r'v1/crawles/(?P<text>[\S-]+)/(?P<limit>[\d-]+)/(?P<per_limit>[\d-]+)/$', views.run_crawle, name='run_crawle'),

    # goals
    re_path(r'v1/users/(?P<user_id>[\d-]+)/goals/(?P<text>[\S-]+)/$', views.goal_extraction, name='goal_extraction'),
    re_path(r'v1/goals/(?P<text>[\S-]+)/$', views.goal_extraction_no_user, name='goal_extraction_no_user'),

    # causals
    re_path(r'v1/causals/(?P<text>[\S-]+)/$', views.causal_extraction_no_user, name='causal_extraction_no_user'),
    re_path(r'v1/users/(?P<user_id>[\d-]+)/causals/(?P<text>[\S-]+)/$', views.goal_extraction, name='causal_extraction'),
    re_path(r'v1/users/(?P<user_id>[\d-]+)/causals/(?P<text>[\S-]+)/$', views.goal_extraction, name='causal_extraction_from_crawle'),

    #equals
    re_path(r'v1/equals/(?P<text>[\S-]+)/$', views.equal_extraction_no_user, name='equal_extraction_no_user'),
    re_path(r'v1/users/(?P<user_id>[\d-]+)/equals/(?P<text>[\S-]+)/$', views.equal_extraction, name='equal_extraction'),
]
