from django.conf.urls.defaults import *
from loansProject.views import home

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^loansProject/', include('loansProject.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^home/$', home),
)
"""
    (r'^applyForLoan/$', applyForLoan),
    (r'^dueInstallments/$', dueInstallments),
    (r'^allLoans/$', allLoans),
    (r'^loanDetails/$', loanDetails),
    (r'^allApplications/$', allApplications),
    (r'^applicationDetails/$', applicationDetails),
    (r'^paymentHistory/$', paymentHistory),
    (r'^payNow/$', payNow),
    (r'^supporrt/$', support),
"""
