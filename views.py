from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template
from loans.models import *
from django.shortcuts import render_to_response

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
      overdueInstallments.append({'amount':oi.amount,
                                  'dueDate':oi.dueDate,
                                  'loan':oi.loan_id})
    di = {'amount':activeLoan.monthlyInstallment,
          'dueDate':activeLoan.nextInstallmentDueDate,
          'loan':activeLoan.id}
    dueInstallments.append(di)

  def getDueDate(installment):
    return installment['dueDate']
  overdueInstallments = sorted(overdueInstallments, key=getDueDate)
  dueInstallments = sorted(dueInstallments, key=getDueDate)

  t = get_template('dueInstallments.html')
  c = Context({'overdueInstallments':overdueInstallments,
               'dueInstallments':dueInstallments})
  html = t.render(c)
  return HttpResponse(html)


def allApplications(request):
  # View for displaying all the loan applications a customer has made.
  # These applications include those which have been approved, rejected or are under consideration.

  # Authenticate Customer (TBD)
  # customerID =

  # Get a list of all Applications associated with that Customer.
  # Sort them in three categories.
  applicationList = Application.objects.filter(customer=2)

  processedApplications = []
  underProcessingApplications = []
  archivedApplications = []
  for application in applicationList:

    if application.isArchived == False:

      if application.status == "Active":
        underProcessingApplications.append({'id':application.id,
                                            'name':application.name,
                                            'loanType':application.loanType,
                                            'amountAppliedFor':application.amountAppliedFor,
                                            'dateApplied':application.dateApplied,
                                            'status':application.status,
                                            'remark':application.remark})
      elif application.status == "Allotted" or application.status == "Rejected":
        processedApplications.append({'id':application.id,
                                      'name':application.name,
                                      'loanType':application.loanType,
                                      'status':application.status,
                                      'amountAllotted':application.amountAllotted,
                                      'dateOfAllotment':application.dateOfAllotment,
                                      'interestCategory':application.interestCategory,
                                      'interestRate':application.interestRate})

    else:
      archivedApplications.append({'id':application.id,
                                   'name':application.name,
                                   'loanType':application.loanType,
                                   'status':application.status,
                                   'amountAllotted':application.amountAllotted,
                                   'dateOfAllotment':application.dateOfAllotment,
                                   'interestCategory':application.interestCategory,
                                   'interestRate':application.interestRate,
                                   'amountAppliedFor':application.amountAppliedFor,
                                   'dateApplied':application.dateApplied,
                                   'remark':application.remark})

  t = get_template('allApplications.html')
  c = Context({'processedApplications':processedApplications,
               'underProcessingApplications':underProcessingApplications,
               'archivedApplications':archivedApplications})
  html = t.render(c)
  return HttpResponse(html)


def cancelOrArchive(request, cancelOrArchive, applicationID):
  # Authenticate Customer (TBD)
  # customerID =
  if cancelOrArchive=="cancel":
    Application.objects.filter(id=applicationID).update(status="Cancelled", isArchived="True")
  elif cancelOrArchive=="archive":
    Application.objects.filter(id=applicationID).update(isArchived="True")
  return HttpResponseRedirect("/allApplications/")


def allLoans(request):
  
  # Authenticate Customer
  customerID=2
  actLoans=ActiveLoan.objects.filter(customer=customerID) 
  compLoans=CompletedLoan.objects.filter(customer=customerID)
  actDict = []
  compDict = []
  for loan in actLoans:
	  actDict.append({'id':loan.id,
	                  'name':loan.name,
                          'loanType':loan.loanType,
                          'principal':loan.principal,
                          'totalMonths':loan.originalMonths,
                          'dateTaken':loan.dateTaken,
			  'expTermination':loan.expectedDateOfTermination,
			  'outstandingAmount':loan.outstandingLoanBalance,
			  'monthsLeft':loan.elapsedMonths,
			  'interestCategory':loan.interestCategory,
			  'interestRate':loan.interestRate,
			  'monthlyInstallment':loan.monthlyInstallment,
			  'nextDueInstallment':loan.nextInstallmentDueDate,
			  'prepayPenalty':loan.prepaymentPenaltyRate,
			  'security':loan.security})
 
  for loan in compLoans:
	  compDict.append({'id':loan.id,
                           'name':loan.name,
			   'loanType':loan.loanType,
			   'principal':loan.principal,
			   'totalMonths':loan.originalMonths,
			   'dateTaken':loan.dateTaken,
			   'dateOfCompletion':loan.dateOfCompletion,
			   'totalAmountPaid':loan.totalAmountPaid,
			   'interestCategory':loan.interestCategory,
			   'interestRate':loan.averageInterestRate})

  return render_to_response('allLoans.html',locals())

def loanDetails(request,status,loanID):
  if status=="completed":
    loanlist=CompletedLoan.objects.filter(id=loanID)
    details = []
    for comploan in loanlist:
      details.append({'id':comploan.id,
                      'name':comploan.name,
                      'comploanType':loan.loanType,
                      'principal':comploan.principal,
                      'totalMonths':comploan.originalMonths,
                      'dateTaken':comploan.dateTaken,
                      'dateOfCompletion':comploan.dateOfCompletion,
                      'totalAmountPaid':comploan.totalAmountPaid,
                      'interestCategory':comploan.interestCategory,
                      'interestRate':comploan.averageInterestRate})
    """
    paymentList=Payment.objects.filter(loan=comploan.loan)
    paymentDetails=[]
    for payment in paymentList:
      paymentDetails.append({'amount':payment.amount,
                             'datePaid':payment.datePaid,
			     'type':payment.paymentType,
			     'merchant':payment.merchantUsed})
    """
    template='completedLoanDetails.html'

  elif status=="active":
    loanlist=ActiveLoan.objects.filter(id=loanID)
    details = []
    for actloan in loanlist:
      details.append({'id':actloan.id,
                      'name':actloan.name,
                      'loanType':actloan.loanType,
                      'principal':actloan.principal,
                      'totalMonths':actloan.originalMonths,
                      'dateTaken':actloan.dateTaken,
                      'expTermination':actloan.expectedDateOfTermination,
                      'outstandingAmount':actloan.outstandingLoanBalance,
                      'monthsLeft':actloan.elapsedMonths,
                      'interestCategory':actloan.interestCategory,
                      'interestRate':actloan.interestRate,
                      'monthlyInstallment':actloan.monthlyInstallment,
                      'nextDueInstallment':actloan.nextInstallmentDueDate,
                      'prepayPenalty':actloan.prepaymentPenaltyRate,
                      'security':actloan.security})
    """
    paymentList=Payment.objects.filter(loan=actloan.loan)
    paymentDetails=[]
    for payment in paymentList:
      paymentDetails.append({'amount':payment.amount,
                             'datePaid':payment.datePaid,
			     'type':payment.paymentType,
			     'merchant':payment.merchantUsed})
    """
    template='activeLoanDetails.html'

  return render_to_response(template,locals())


def payInstallment(request, loanID):
  return HttpResponse(loanID)

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

