from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin
from frankly_test_app.views import *

admin.autodiscover()
urlpatterns = patterns('',
    
#     url(r'^finance/$', TemplateView.as_view(template_name="finance.html"), name='finance'),
#      url(r'^admin/', include(admin.site.urls)),
     url(r'^accounts/', include('registration.backends.simple.urls')),
     url(r'^hackers_news/$', hackers_news, name='hackers_news'),
#      url(r'', custom_login, name='custom_login'),
    
 )



   