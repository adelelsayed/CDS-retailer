from django.conf.urls import url
from django.views.generic import RedirectView
from alerter import views

app_name = 'alerter'

urlpatterns = [

   url(r'^main/$',
    views.TheView.as_view({'post': 'view'}), name = 'main'),

    url(r'docview/$',views.TheView.as_view({'get':'browse'}),name = 'docView'),



]

#(?P<message>[ a-zA-Z0-9_|-]+)/'