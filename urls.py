from django.conf.urls.defaults import *
from loansProject.views import *

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
    (r'^dueInstallments/$', dueInstallments),
    (r'^allApplications/$', allApplications),
)
"""
    (r'^applyForLoan/$', applyForLoan),
    (r'^allLoans/$', allLoans),
    (r'^loanDetails/$', loanDetails),
    (r'^applicationDetails/$', applicationDetails),
    (r'^paymentHistory/$', paymentHistory),
    (r'^payNow/$', payNow),
    (r'^supporrt/$', support),
"""
