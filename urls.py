from django.conf.urls.defaults import *
from loansProject.views import *
from loansProject.resources import *
from djangorestframework.views import *
from djangorestframework.renderers import JSONRenderer;


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
    (r'^api/paymentsBetween/(?P<cust_id>\d+)/$', PaymentsBetween.as_view()),
		(r'^api/paymentsBetween/(?P<cust_id>\d+)/s(?P<start>\d{8})/$', PaymentsBetween.as_view()),
		(r'^api/paymentsBetween/(?P<cust_id>\d+)/e(?P<end>\d{8})/$', PaymentsBetween.as_view()),
		(r'^api/paymentsBetween/(?P<cust_id>\d+)/s(?P<start>\d{8})/e(?P<end>\d{8})/$', PaymentsBetween.as_view()),
		(r'^api/paymentHistoryOfLoan/(?P<cust_id>\d+)/(?P<lname>[a-zA-Z0-9]+)/$', PaymentHistoryOfLoan.as_view()),
		(r'^api/defaulters/$', Defaulters.as_view()),
		(r'^api/paymentHistoryAllLoans/(?P<cust_id>\d+)/$', PaymentHistoryAllLoans.as_view()),
		(r'^api/monthlyInstallment/(?P<cust_id>\d+)/$', MonthlyInstallment.as_view()),
	
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
