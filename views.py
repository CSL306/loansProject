from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from loans.models import *

def home(request):
  t = get_template('home.html') # Instead of t = Template('')
  c = Context(locals())
  html = t.render(c)
  return HttpResponse(html)

def dueInstallments(request):
  # View for displaying all the installments which are due.
  # These installments may belong to different loans.

  # Authenticate Customer (TBD)
  # customerID =

  # Get a list of all ActiveLoans associated with that Customer.
  activeLoanList = ActiveLoan.objects.filter(customer=2)

  # For each ActiveLoan get a list of all OverdueInstallment and merge these lists
  # Make a list of due installments using nextInstallmentDueDate for each ActiveLoan
  # Sort both these lists chronologically
  overdueInstallments = []
  dueInstallments = []
  for activeLoan in activeLoanList:
    ois = OverdueInstallment.objects.filter(loan=activeLoan)
    for oi in ois:
      overdueInstallments.append({'amount':oi.amount, 'dueDate':oi.dueDate, 'loan':oi.loan_id})
    di = {'amount':activeLoan.monthlyInstallment, 'dueDate':activeLoan.nextInstallmentDueDate, 'loan':activeLoan.id}
    dueInstallments.append(di)

  def getDueDate(installment):
    return installment['dueDate']
  overdueInstallments = sorted(overdueInstallments, key=getDueDate)
  dueInstallments = sorted(dueInstallments, key=getDueDate)

  t = get_template('dueInstallments.html')
  c = Context({'overdueInstallments':overdueInstallments, 'dueInstallments':dueInstallments})
  html = t.render(c)
  return HttpResponse(html)


def allApplications(request):
  # View for displaying all the loan applications a customer has made.
  # These applications include those which have been approved, rejected or are under consideration.

  # Authenticate Customer (TBD)
  # customerID =

  # Get a list of all Applications associated with that Customer.
  applicationList = Application.objects.filter(customer=2)

  processedApplications = []
  underProcessingApplications = []
  archivedApplications = []
  for application in applicationList:
    if application.isArchived == False:
      if application.status == "Active":
        underProcessingApplications.append({'name':application.name, 'loanType':application.loanType, 'amountAppliedFor':application.amountAppliedFor, 'dateApplied':application.dateApplied, 'status':application.status, 'remark':application.remark})
      elif application.status == "Allotted" or application.status == "Rejected":
        processedApplications.append({'name':application.name, 'loanType':application.loanType, 'status':application.status, 'amountAllotted':application.amountAllotted, 'dateOfAllotment':application.dateOfAllotment, 'interestCategory':application.interestCategory, 'interestRate':application.interestRate})
    else:
      archivedApplications.append({'name':application.name, 'loanType':application.loanType, 'status':application.status, 'amountAllotted':application.amountAllotted, 'dateOfAllotment':application.dateOfAllotment, 'interestCategory':application.interestCategory, 'interestRate':application.interestRate, 'amountAppliedFor':application.amountAppliedFor, 'dateApplied':application.dateApplied, 'remark':application.remark})

  t = get_template('allApplications.html')
  c = Context({'processedApplications':processedApplications, 'underProcessingApplications':underProcessingApplications, 'archivedApplications':archivedApplications})
  html = t.render(c)
  return HttpResponse(html)


"""
def applyForLoan(request):
  # View for applying for a new loan.

def allLoans(request):
  # View for displaying all the loans taken by the customer.
  # These loans also include loans which have been paid off.
  # Provide options for displaying them in different orders.
  # When a customer clicks on a loan, it takes them to a page which shows the details about that loan.

def loanDetails(reques):
  # View for displaying all the details about a single loan.

def applicationDetails(request):
  # View for displaying all the details about a single applicaiton.

def paymentHistory(request):
  # View for displaying the payment history.

def payNow(request):
  # View for paying an installment.

def support(request):
  # View for filing a support request.
"""
