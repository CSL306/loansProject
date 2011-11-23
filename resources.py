from djangorestframework.resources import *
from loans.models import *

from djangorestframework.renderers import JSONRenderer

class LoanResource(ModelResource):
    model = Loan

class CustomerResource(ModelResource):
    model = Customer

class ActiveLoanResource(ModelResource):
    model = ActiveLoan

class CompletedLoanResource(ModelResource):
    model = CompletedLoan

class PaymentResource(ModelResource):
    model = Payment

class OverdueInstallmentResource(ModelResource):
    model = OverdueInstallment

class ApplicationResource(ModelResource):
    model = Application

class SupportTicketResource(ModelResource):
    model = SupportTicket
    

