from django.conf.urls.defaults import *
from loansProject.views import *
from loansProject.resources import *
from djangorestframework.views import *
from loansProject.apiviews import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    
    # URL mappings for API calls
    (r'^api/paymentsBetween/(?P<cust_id>\d+)/$', PaymentsBetween.as_view()),
    (r'^api/paymentsBetween/(?P<cust_id>\d+)/s(?P<start>\d{8})/$', PaymentsBetween.as_view()),
    (r'^api/paymentsBetween/(?P<cust_id>\d+)/e(?P<end>\d{8})/$', PaymentsBetween.as_view()),
    (r'^api/paymentsBetween/(?P<cust_id>\d+)/s(?P<start>\d{8})/e(?P<end>\d{8})/$', PaymentsBetween.as_view()),

    (r'^api/paymentHistoryOfLoan/(?P<cust_id>\d+)/(?P<lname>[a-zA-Z0-9]+)/$', PaymentHistoryOfLoan.as_view()),

    (r'^api/defaulters/$', Defaulters.as_view()),

    (r'^api/paymentHistoryAllLoans/(?P<cust_id>\d+)/$', PaymentHistoryAllLoans.as_view()),

    (r'^api/monthlyInstallment/(?P<cust_id>\d+)/$', MonthlyInstallment.as_view()),

    (r'^api/Loan/$', ListModelView.as_view(resource=LoanResource)),
    (r'^api/Loan/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=LoanResource)),

    (r'^api/Customer/$', ListModelView.as_view(resource=CustomerResource)),
    (r'^api/Customer/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=CustomerResource)),

    (r'^api/ActiveLoan/$', ListModelView.as_view(resource=ActiveLoanResource)),
    (r'^api/ActiveLoan/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=ActiveLoanResource)),

    (r'^api/CompletedLoan/$', ListModelView.as_view(resource=CompletedLoanResource)),
    (r'^api/CompletedLoan/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=CompletedLoanResource)),

    (r'^api/Payment/$', ListModelView.as_view(resource=PaymentResource)),
    (r'^api/Payment/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=PaymentResource)),

    (r'^api/OverdueInstallment/$', ListModelView.as_view(resource=OverdueInstallmentResource)),
    (r'^api/OverdueInstallment/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=OverdueInstallmentResource)),

    (r'^api/Application/$', ListModelView.as_view(resource=ApplicationResource)),
    (r'^api/Application/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=ApplicationResource)),

    (r'^api/SupportTicket/$', ListModelView.as_view(resource=SupportTicketResource)),
    (r'^api/SupportTicket/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=SupportTicketResource)),

    # URL mappings for page views
    (r'^home/$', home),
    (r'^dueInstallments/$', dueInstallments),
    (r'^allApplications/$', allApplications),
    (r'^allPayments/$', allPayments),
    (r'^cancelOrArchive/(archive)/(\d+)/$', cancelOrArchive),
    (r'^cancelOrArchive/(cancel)/(\d+)/$', cancelOrArchive),
    (r'^allLoans/$',allLoans),
    (r'^loanDetails/(\d+)/$',loanDetails),
    (r'^payInstallment/(\d+)/$', payInstallment),
    (r'^payInstallmentThanks/$', payInstallmentThanks),
    (r'^payPrepayment/(\d+)/$', payPrepayment),
    (r'^payPrepaymentThanks/$', payPrepaymentThanks),
    (r'^newApplication/$', newApplication),
    (r'^newApplicationThanks/$', newApplicationThanks),
    (r'^support/$', support),
    (r'^supportThanks/$', supportThanks),    
)

urlpatterns += patterns('django.views.static',
                        (r'^allApplications/(?P<path>.*)$','serve', {'document_root': 'staticMedia',}),
                        (r'^allLoans/(?P<path>.*)$','serve', {'document_root': 'staticMedia',}),
                        (r'^loanDetails/(\d+)/(?P<path>.*)$','serve', {'document_root': 'staticMedia',}),
                        (r'^dueInstallments/(?P<path>.*)$','serve', {'document_root': 'staticMedia',}),
                        (r'^allPayments/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}),
                        (r'^base/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}),
                        (r'^payInstallment/(\d+)/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}), 
                        (r'^payInstallmentThanks/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}),                          
                        (r'^payPrepayment/(\d+)/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}),
                        (r'^payPrepaymentThanks/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}),
                        (r'^newApplication/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}),
                        (r'^newApplicationThanks/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}),
                        (r'^support/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}),                        
                        (r'^supportThanks/(?P<path>.*)$', 'serve', {'document_root': 'staticMedia',}),
                        )
