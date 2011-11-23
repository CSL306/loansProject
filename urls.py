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

    (r'^api/paymentsBetween/(?P<cust_id>\d+)/$', PaymentsBetween.as_view()),
    (r'^api/paymentsBetween/(?P<cust_id>\d+)/s(?P<start>\d{8})/$', PaymentsBetween.as_view()),
    (r'^api/paymentsBetween/(?P<cust_id>\d+)/e(?P<end>\d{8})/$', PaymentsBetween.as_view()),
    (r'^api/paymentsBetween/(?P<cust_id>\d+)/s(?P<start>\d{8})/e(?P<end>\d{8})/$', PaymentsBetween.as_view()),

		(r'^api/loansTakenBetween/(?P<cust_id>\d+)/$', LoansTakenBetween.as_view()),
    (r'^api/loansTakenBetween/(?P<cust_id>\d+)/s(?P<start>\d{8})/$', LoansTakenBetween.as_view()),
    (r'^api/loansTakenBetween/(?P<cust_id>\d+)/e(?P<end>\d{8})/$', LoansTakenBetween.as_view()),
    (r'^api/loansTakenBetween/(?P<cust_id>\d+)/s(?P<start>\d{8})/e(?P<end>\d{8})/$', LoansTakenBetween.as_view()),
    
    (r'^api/loansWithOverdueInstallments/$', LoansWithOverdueInstallments.as_view()),
    (r'^api/loansWithOverdueInstallments/(?P<cust_id>\d+)/$', LoansWithOverdueInstallments.as_view()),
    
    (r'^api/loanHistory/(?P<cust_id>\d+)/$', LoanHistory.as_view()),
    
    (r'^api/paymentHistoryOfLoan/(?P<cust_id>\d+)/(?P<lname>[a-zA-Z0-9]+)/$', PaymentHistoryOfLoan.as_view()),

    (r'^api/defaulters/$', Defaulters.as_view()),

    (r'^api/paymentHistoryAllLoans/(?P<cust_id>\d+)/$', PaymentHistoryAllLoans.as_view()),

    (r'^api/monthlyInstallment/(?P<cust_id>\d+)/$', MonthlyInstallment.as_view()),

    (r'^api/loan/$', ListModelView.as_view(resource=LoanResource)),
    (r'^api/loan/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=LoanResource)),

    (r'^api/customer/$', ListModelView.as_view(resource=CustomerResource)),
    (r'^api/customer/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=CustomerResource)),

    (r'^api/activeLoan/$', ListModelView.as_view(resource=ActiveLoanResource)),
    (r'^api/activeLoan/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=ActiveLoanResource)),

    (r'^api/completedLoan/$', ListModelView.as_view(resource=CompletedLoanResource)),
    (r'^api/completedLoan/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=CompletedLoanResource)),

    (r'^api/payment/$', ListModelView.as_view(resource=PaymentResource)),
    (r'^api/payment/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=PaymentResource)),

    (r'^api/overdueInstallment/$', ListModelView.as_view(resource=OverdueInstallmentResource)),
    (r'^api/overdueInstallment/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=OverdueInstallmentResource)),

    (r'^api/application/$', ListModelView.as_view(resource=ApplicationResource)),
    (r'^api/application/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=ApplicationResource)),

    (r'^api/supportTicket/$', ListModelView.as_view(resource=SupportTicketResource)),
    (r'^api/supportTicket/(?P<pk>[^/]+)/$', InstanceReadOnlyModelView.as_view(resource=SupportTicketResource)),

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


#    (r'^applyForLoan/$', applyForLoan),
#    (r'^applicationDetails/$', applicationDetails),
#    (r'^paymentHistory/$', paymentHistory),
#    (r'^supporrt/$', support),
