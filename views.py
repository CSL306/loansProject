from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import *
from externalapis import *
from loans.models import *

def getCustomerId(request):
  return 1
  #sessionId = request.session.get("id","none")
  #if (sessionId != "none"):
    #return IdentityModule.getCustomerId(sessionId)
  #else:
    #return HttpResponseRedirect("/home")


def home(request):
  # Home page for a unsigned user.
  return render_to_response('home.html',locals())


def dueInstallments(request):
  # View for displaying all due installments for all loans of a customer.

  # Get the customerId and verify if the session is active.
  customerID = getCustomerId(request)

  # Get a list of all ActiveLoans associated with that Customer.
  activeLoanList = Loan.objects.filter(customer=customerID, isActive=True)

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
    di = {'amount':activeLoan.activeloan.monthlyInstallment,
          'dueDate':activeLoan.activeloan.nextInstallmentDueDate,
          'loan':activeLoan.activeloan.id}
    dueInstallments.append(di)

  def getDueDate(installment):
    return installment['dueDate']

  overdueInstallments = sorted(overdueInstallments, key=getDueDate)
  dueInstallments = sorted(dueInstallments, key=getDueDate)

  return render_to_response('dueInstallments.html', locals())


def allApplications(request):
  # View for displaying all the loan applications a customer has made.
  # These applications include those which have been approved, rejected or are under consideration.

  # Get the customerId and verify if the session is active.
  customerID = getCustomerId(request)

  # Get a list of all Applications associated with that Customer.
  # Sort them in three categories.
  applicationList = Application.objects.filter(customer=customerID)

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
                                      'interestRate':application.interestRate,
                                      'amountAppliedFor':application.amountAppliedFor,
                                      'dateApplied':application.dateApplied,})


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

  return render_to_response('allApplications.html', locals())


def cancelOrArchive(request, cancelOrArchive, applicationID):
  customerID = getCustomerId(request)
  if cancelOrArchive=="cancel":
    Application.objects.filter(id=applicationID).update(status="Cancelled", isArchived="True")
  elif cancelOrArchive=="archive":
    Application.objects.filter(id=applicationID).update(isArchived="True")
  return HttpResponseRedirect("/allApplications/")


def allLoans(request):
  # Show all loans for a customer.
  # Get the customerId and verify if the session is active.
  customerID = getCustomerId(request)

  actLoans=ActiveLoan.objects.filter(customer=customerID)
  compLoans=CompletedLoan.objects.filter(customer=customerID)
  actDict = []
  compDict = []

  for actLoan in actLoans:
    actDict.append({'id':actLoan.loan.id,
                    'name':actLoan.loan.name,
                    'loanType':actLoan.loan.loanType,
                    'principal':actLoan.loan.principal,
                    'totalMonths':actLoan.loan.originalMonths,
                    'dateTaken':actLoan.loan.dateTaken,
                    'expTermination':actLoan.expectedDateOfTermination,
                    'outstandingAmount':actLoan.outstandingLoanBalance,
                    'monthsLeft':actLoan.loan.originalMonths - actLoan.elapsedMonths,
                    'interestCategory':actLoan.loan.interestCategory,
                    'interestRate':actLoan.interestRate,
                    'monthlyInstallment':actLoan.monthlyInstallment,
                    'nextDueInstallment':actLoan.nextInstallmentDueDate,
                    'prepayPenalty':actLoan.prepaymentPenaltyRate,
                    'security':actLoan.security})

  for compLoan in compLoans:
    compDict.append({'id':compLoan.loan.id,
                     'name':compLoan.loan.name,
                     'loanType':compLoan.loan.loanType,
                     'principal':compLoan.loan.principal,
                     'totalMonths':compLoan.loan.originalMonths,
                     'dateTaken':compLoan.loan.dateTaken,
                     'dateOfCompletion':compLoan.dateOfCompletion,
                     'totalAmountPaid':compLoan.totalAmountPaid,
                     'interestCategory':compLoan.loan.interestCategory,
                     'interestRate':compLoan.averageInterestRate})

  return render_to_response('allLoans.html',locals())


def loanDetails(request,loanId):
  # Display the loan details for a loanId
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  loan = Loan.objects.get(id=loanId)

  # Retrieve the payment list for a loan
  paymentList = Payment.objects.filter(loan=id)
  paymentDetails = []
  for payment in paymentList:
    paymentDetails.append({'amount':payment.amount,
                            'datePaid':payment.datePaid,
                            'type':payment.paymentType,
                            'merchant':payment.merchantUsed})

  if (loan.isactive):
    activeLoan = loan.activeLoan
    details = {'id':actloan.id,
                    'name':actloan.loan.name,
                    'loanType':actloan.loan.loanType,
                    'principal':actloan.loan.principal,
                    'totalMonths':actloan.loan.originalMonths,
                    'dateTaken':actloan.loan.dateTaken,
                    'expTermination':actloan.expectedDateOfTermination,
                    'outstandingAmount':actloan.outstandingLoanBalance,
                    'monthsLeft':actloan.elapsedMonths,
                    'interestCategory':actloan.loan.interestCategory,
                    'interestRate':actloan.interestRate,
                    'monthlyInstallment':actloan.monthlyInstallment,
                    'nextDueInstallment':actloan.nextInstallmentDueDate,
                    'prepayPenalty':actloan.prepaymentPenaltyRate,
                    'security':actloan.loan.security}
    return render_to_response('activeLoanDetails.html', locals())
  else:
    completedLoan = loan.completedLoan
    details = {'id':completedLoan.loan.id,
                      'name':completedLoan.loan.name,
                      'loanType':completedLoan.loan.loanType,
                      'principal':completedLoan.loan.principal,
                      'totalMonths':completedLoan.loan.originalMonths,
                      'dateTaken':completedLoan.loan.dateTaken,
                      'dateOfCompletion':completedLoan.dateOfCompletion,
                      'totalAmountPaid':completedLoan.totalAmountPaid,
                      'interestCategory':completedLoan.loan.interestCategory,
                      'interestRate':completedLoan.averageInterestRate}
    return render_to_response('completedLoanDetails.html', locals())


def payInstallment(request, loanId):
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  # View for paying an installment
  activeLoan = ActiveLoan.objects.filter(loan_id=loanId)
  dueDate = activeLoan.nextInstallmentDueDate
  installment = activeLoan.monthlyInstallment
  outstandingLoanBalance = activeLoan.outstandingLoanBalance
  return render_to_response('payInstallment.html', locals())


def payInstallmentThanks(request, loanId):
  # Thank you page after the payment of an installment.
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  activeLoan = ActiveLoan.objects.get(loan_id=loanId)

  # Adds the payment to Payment model
  payment = Payment(amount=activeLoan.monthlyInstallment, loan=activeLoan.loan, paymentType="installment", merchantUsed="none")
  payment.save()

  # Updates the activeLoan or makes it a completed loan if this was the last installment.
  if activeLoan.elapsedMonths + 1 == activeLoan.originalMonths:
    paymentList = Payment.objects.filter(loan_id=activeLoanId)
    totalAmountPaid = 0
    for payment in paymentList:
      totalAmountPaid += payment.amount
    averageInterestRate = activeLoan.interestRate
    completedLoan = CompletedLoan(loan=activeLoan.loan, totalAmountPaid=totalAmountPaid, averageInterestRate=averageInterestRate)
    completedLoan.save()
    activeLoan.loan.isactive = False
    activeLoan.delete()
  else:
    activeLoan.elapsedMonths += 1
    activeLoan.save()


def newApplication(request):
  # Files a new application.
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  # View for applying for a new loan.
  if request.method == 'POST':
      form = ApplicationForm(request.POST)
      if form.is_valid():
          cd = form.cleaned_data
          application = Application(name=cd.loanName, amountAppliedFor=cd.loanAmount, loanType=cd.loanCategory, security=cd.security)
          application.save()
          return HttpResponseRedirect('/newApplication/thanks/')
  else:
      form = ApplicationForm()
  return render_to_response('newApplication.html', locals())


def newApplicationThanks(request):
  # Thank you page after a new application request.
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  return render_to_response('newApplicationThanks.html')


def payPrepayment(request, loanId):
  # Prepay an amount for a loan.
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  activeLoan = ActiveLoan.objects.get(loan_id=loanId)
  loanName = activeLoan.loan.name
  outstandingAmount = activeLoan.outstandingLoanBalance
  if request.method == 'POST':
      form = PrepaymentForm(request.POST)
      if form.is_valid():
          cd = form.cleaned_data
          amount = cd.prepayAmount
          #TODO update details for the active loan
          return HttpResponseRedirect('/payPrepayment/thanks/')
  else:
      form = PrepaymentForm(initial = {'prepayAmount': outstandingAmount/2})
  return render_to_response('payPrepayment.html', locals())


def payPrepaymentThanks(request):
  # Thank you page after the payment of an installment.
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  return render_to_response('payPrepaymentThanks.html', local())


def support(request):
  # View for filing a support request.
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  if request.method == 'POST':
      form = SupportForm(request.POST)
      if form.is_valid():
          cd = form.cleaned_data
          ticket = SupportTicket(loan=Loan.objects.get(id=cd.loanId), complaintType=cd.complaintType, complaintMessage=cd.message)
          ticket.save()
          return HttpResponseRedirect('/support/thanks/')
  else:
      form = SupportForm(
          initial={'message': 'Please enter your message here.'}
      )
  return render_to_response('support.html', locals())


def supportThanks(request):
  # Thank you page after a support request submission.
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  return render_to_response('supportThanks.html', locals())


"""
def paymentHistory(request):
  # View for displaying the payment history.


def payInstallment(request):
  # View for paying an installment.
"""
