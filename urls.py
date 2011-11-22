from django.conf.urls.defaults import *
from loansProject.views import *
from loansProject.resources import *
from djangorestframework.views import *


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

    (r'^api/Loan/$', ListModelView.as_view(resource=LoanResource)),
    (r'^api/Loan/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=LoanResource)),

    (r'^api/Customer/$', ListModelView.as_view(resource=CustomerResource)),
    (r'^api/Customer/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=CustomerResource)),

    (r'^api/ActiveLoan/$', ListModelView.as_view(resource=ActiveLoanResource)),
    (r'^api/ActiveLoan/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=ActiveLoanResource)),

    (r'^api/CompletedLoan/$', ListModelView.as_view(resource=CompletedLoanResource)),
    (r'^api/CompletedLoan/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=CompletedLoanResource)),

    (r'^api/Payment/$', ListModelView.as_view(resource=PaymentResource)),
    (r'^api/Payment/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=PaymentResource)),

    (r'^api/OverdueInstallment/$', ListModelView.as_view(resource=OverdueInstallmentResource)),
    (r'^api/OverdueInstallment/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=OverdueInstallmentResource)),

    (r'^api/Application/$', ListModelView.as_view(resource=ApplicationResource)),
    (r'^api/Application/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=ApplicationResource)),

    (r'^api/SupportTicket/$', ListModelView.as_view(resource=SupportTicketResource)),
    (r'^api/SupportTicket/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=SupportTicketResource)),

    (r'^home/$', home),
    (r'^dueInstallments/$', dueInstallments),
    (r'^allApplications/$', allApplications),
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
                        (r'^dueInstallments/(?P<path>.*)$','serve', {'document_root': 'staticMedia',}), )

"""
    (r'^applyForLoan/$', applyForLoan),
    (r'^applicationDetails/$', applicationDetails),
    (r'^paymentHistory/$', paymentHistory),
    (r'^supporrt/$', support),
"""
