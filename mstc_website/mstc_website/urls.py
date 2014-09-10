from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from Publish import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mstc_website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^djangoadmin/', include(admin.site.urls)),
    url(r'^admin$',views.admin),
    url(r'^logout/$',views.logout),
    url(r'^$',views.home),
    url(r'^addDynamics$',views.addDynamics),
    url(r'^dynlist$',views.dynlist),
    url(r'^dynlist/detail/$',views.dyndetail),
    url(r'^join/$',views.join),
)
