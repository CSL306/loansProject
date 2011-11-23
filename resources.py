from djangorestframework.resources import *
from loans.models import *

class LoanResource(ModelResource):
  """
  This class enumerates ALL the loan objects

  Format of URL: http://localhost:8000/api/loan
  """
  model = Loan

class CustomerResource(ModelResource):
  """
  This class enumerates ALL the customer objects

  Format of URL: http://localhost:8000/api/customer
  """
  model = Customer

class ActiveLoanResource(ModelResource):
  """
  This class enumerates ALL the active loan objects

  Format of URL: http://localhost:8000/api/activeLoan
  """
  model = ActiveLoan

class CompletedLoanResource(ModelResource):
  """
  This class enumerates ALL the completed loan objects

  Format of URL: http://localhost:8000/api/completedLoan
  """
  model = CompletedLoan

class PaymentResource(ModelResource):
  """
  This class enumerates ALL the payment objects

  Format of URL: http://localhost:8000/api/payment
  """
  model = Payment

class OverdueInstallmentResource(ModelResource):
  """
  This class enumerates ALL the overdue installment objects

  Format of URL: http://localhost:8000/api/overdueInstallment
  """
  model = OverdueInstallment

class ApplicationResource(ModelResource):
  """
  This class enumerates ALL the application objects

  Format of URL: http://localhost:8000/api/application
  """
  model = Application

class SupportTicketResource(ModelResource):
  """
  This class enumerates ALL the support ticket objects

  Format of URL: http://localhost:8000/api/supportTicket
  """
  model = SupportTicket
