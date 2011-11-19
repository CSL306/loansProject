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
                                            'remark':application.remark,
                                            'cancelLink':"/cancelOrArchive/cancel/"+str(application.id),})
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
                                      'dateApplied':application.dateApplied,
                                      'archiveLink':"/cancelOrArchive/archive/"+str(application.id),})

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

  loanList=Loan.objects.filter(customer=customerID)
  actDict = []
  compDict = []

  for loan in loanList:
    if loan.isActive:
      actDict.append({'id':loan.id,
                      'name':loan.name,
                      'loanType':loan.loanType,
                      'principal':loan.principal,
                      'totalMonths':loan.originalMonths,
                      'dateTaken':loan.dateTaken,
                      'expectedDateOfTermination':loan.activeloan.expectedDateOfTermination,
                      'outstandingLoanBalance':loan.activeloan.outstandingLoanBalance,
                      'monthsLeft':loan.originalMonths - loan.activeloan.elapsedMonths,
                      'interestCategory':loan.interestCategory,
                      'interestRate':loan.activeloan.interestRate,
                      'monthlyInstallment':loan.activeloan.monthlyInstallment,
                      'nextInstallmentDueDate':loan.activeloan.nextInstallmentDueDate,
                      'prepaymentPenaltyRate':loan.activeloan.prepaymentPenaltyRate,
                      'security':loan.security,
                      'detailLink':"../loanDetails/"+str(loan.id),
      })
    else:
      compDict.append({'id':loan.id,
                       'name':loan.name,
                       'loanType':loan.loanType,
                       'principal':loan.principal,
                       'totalMonths':loan.originalMonths,
                       'dateTaken':loan.dateTaken,
                       'dateOfCompletion':loan.completedloan.dateOfCompletion,
                       'totalAmountPaid':loan.completedloan.totalAmountPaid,
                       'interestCategory':loan.interestCategory,
                       'averageInterestRate':loan.completedloan.averageInterestRate,
                       'detailLink':"../loanDetails/"+str(loan.id),
      })

  return render_to_response('allLoans.html',locals())


def loanDetails(request,loanId):
  # Display the loan details for a loanId
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  loan = Loan.objects.get(id=loanId)

  # Retrieve the payment list for a loan
  paymentList = Payment.objects.filter(loan=loanId)
  paymentDetails = []
  for payment in paymentList:
    paymentDetails.append({'amount':payment.amount,
                           'datePaid':payment.datePaid,
                           'type':payment.paymentType,
                           'merchant':payment.merchantUsed,
    })

  if (loan.isActive):
    activeLoan = loan.activeloan
    details = {'id':activeLoan.id,
               'name':activeLoan.loan.name,
               'loanType':activeLoan.loan.loanType,
               'principal':activeLoan.loan.principal,
               'totalMonths':activeLoan.loan.originalMonths,
               'dateTaken':activeLoan.loan.dateTaken,
               'expTermination':activeLoan.expectedDateOfTermination,
               'outstandingAmount':activeLoan.outstandingLoanBalance,
               'monthsLeft':activeLoan.elapsedMonths,
               'interestCategory':activeLoan.loan.interestCategory,
               'interestRate':activeLoan.interestRate,
               'monthlyInstallment':activeLoan.monthlyInstallment,
               'nextDueInstallment':activeLoan.nextInstallmentDueDate,
               'prepayPenalty':activeLoan.prepaymentPenaltyRate,
               'security':activeLoan.loan.security,
    }
    return render_to_response('activeLoanDetails.html', locals())
  else:
    completedLoan = loan.completedloan
    details = {'id':completedLoan.loan.id,
               'name':completedLoan.loan.name,
               'loanType':completedLoan.loan.loanType,
               'principal':completedLoan.loan.principal,
               'totalMonths':completedLoan.loan.originalMonths,
               'dateTaken':completedLoan.loan.dateTaken,
               'dateOfCompletion':completedLoan.dateOfCompletion,
               'totalAmountPaid':completedLoan.totalAmountPaid,
               'interestCategory':completedLoan.loan.interestCategory,
               'interestRate':completedLoan.averageInterestRate,
    }
    return render_to_response('completedLoanDetails.html', locals())


def payInstallment(request, loanId):
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  # View for paying an installment
  activeLoan = ActiveLoan.objects.get(loan__id=loanId)
  dueDate = activeLoan.nextInstallmentDueDate
  installment = activeLoan.monthlyInstallment
  outstandingLoanBalance = activeLoan.outstandingLoanBalance
  return render_to_response('payInstallment.html', locals())


def payInstallmentThanks(request, loanId):
  # Thank you page after the payment of an installment.
  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  activeLoan = ActiveLoan.objects.get(loan__id=loanId)

  # Adds the payment to Payment model
  payment = Payment(amount=activeLoan.monthlyInstallment, loan=activeLoan.loan, paymentType="installment", merchantUsed="none")
  payment.save()

  # Updates the activeLoan or makes it a completed loan if this was the last installment.
  if activeLoan.elapsedMonths + 1 == activeLoan.loan.originalMonths:
    paymentList = Payment.objects.filter(loan__id=loanId)
    totalAmountPaid = 0
    for payment in paymentList:
      totalAmountPaid += payment.amount
    averageInterestRate = activeLoan.interestRate
    completedLoan = CompletedLoan(loan=activeLoan.loan, totalAmountPaid=totalAmountPaid, averageInterestRate=averageInterestRate)
    completedLoan.save()
    activeLoan.loan.isActive = False
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
      form = PrepaymentForm(loanId, request.POST)
      if form.is_valid():
          cd = form.cleaned_data
          amount = cd.prepayAmount
          activeloan.outstandingLoanBalance = activeloan.outstandingLoanBalance - amount
          activeloan.save()
          # Adds the payment to Payment model
          payment = Payment(amount=amount, loan=activeLoan.loan, paymentType="prepayment", merchantUsed="none")
          payment.save()

          return HttpResponseRedirect('/payPrepayment/thanks/')
  else:
      form = PrepaymentForm(loanId, initial = {'prepayAmount': outstandingAmount/2})
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
      form = SupportForm(customerId, request.POST)
      if form.is_valid():
          cd = form.cleaned_data
          ticket = SupportTicket(loan=cd.loan, complaintType=cd.complaintType, complaintMessage=cd.message)
          ticket.save()
          return HttpResponseRedirect('/support/thanks/')
  else:
      form = SupportForm(customerId, initial={'message': 'Please enter your message here.'})
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
