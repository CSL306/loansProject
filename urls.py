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
    (r'^allPayments/$', allPayments),
    (r'^cancelOrArchive/(archive)/(\d+)/$', cancelOrArchive),
    (r'^cancelOrArchive/(cancel)/(\d+)/$', cancelOrArchive),
    (r'^allLoans/$',allLoans),
    (r'^loanDetails/(\d+)/$',loanDetails),
    (r'^payInstallment/(\d+)/$', payInstallment),
)

urlpatterns += patterns('django.views.static',
                        (r'^allApplications/(?P<path>.*)$','serve', {'document_root': 'staticMedia',}),
                        (r'^allLoans/(?P<path>.*)$','serve', {'document_root': 'staticMedia',}),
                        (r'^loanDetails/(\d+)/(?P<path>.*)$','serve', {'document_root': 'staticMedia',}),
                        (r'^dueInstallments/(?P<path>.*)$','serve', {'document_root': 'staticMedia',}), 
                        (r'^allPayments/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}),
                        (r'^base/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}),)

"""
    (r'^applyForLoan/$', applyForLoan),
    (r'^applicationDetails/$', applicationDetails),
    (r'^paymentHistory/$', paymentHistory),
    (r'^supporrt/$', support),
"""
