from django.conf.urls import url
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    url(r'^(?P<id>\d+)/add-comment/$', add_comment,name="comment-create"),
    url(r'^create/$', PostCreateView.as_view(),name="post-create"),
    url(r'^(?P<pk>\d+)/$',PostDetail.as_view(), name="post-detail"),
    url(r'^$', HomeView.as_view(template_name = 'home.html'),name="home"),
   
    
]