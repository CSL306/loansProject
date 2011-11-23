from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import *
from externalapis import *
from loans.models import *
from djangorestframework.views import View;
import datetime;

def getCustomerId(request):
  return 1
  #sessionId = request.session.get("id","none")
  #if (sessionId != "none"):
    #return IdentityModule.getCustomerId(sessionId)
  #else:
    #return HttpResponseRedirect("/home")


def home(request):
  """Home page for a unsigned user."""

  return render_to_response('home.html',locals())


def dueInstallments(request):
  """View for displaying all due and/or overdue installments for all loans of a customer."""

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
  """
     View for displaying all the loan applications a customer has made.
     These applications include those which have been approved, rejected or are under consideration.
  """

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

def allPayments(request):
	
	# Get customer id and verify is the session is active
	customer_id = getCustomerId(request)
	
	# Get all the loans for the customer using the customer_id
	loansList = Loan.objects.filter(customer=customer_id)
	
	#the list to be returned
	paymentsList = []
	
	#loop over all the loans of the customer and get payments for every loan
	for l in loansList:
			paymentsList += Payment.objects.filter(loan = l)	#add the list of payments corresponding to every loan to paymentsList
			
	#the following function is defined for use with the sorted method
	def getdatePaid(payment):
		return payment.datePaid
		
	#sort the payments reverse chronologically
	paymentsList = sorted(paymentsList, key=getdatePaid, reverse=True)
	return render_to_response('allPayments.html', locals())

def cancelOrArchive(request, cancelOrArchive, applicationID):
  """View for cancelling or archiving an application. Redirects back to allApplications. """

  customerID = getCustomerId(request)
  if cancelOrArchive=="cancel":
    Application.objects.filter(id=applicationID).update(status="Cancelled", isArchived="True")
  elif cancelOrArchive=="archive":
    Application.objects.filter(id=applicationID).update(isArchived="True")
  return HttpResponseRedirect("/allApplications/")


def allLoans(request):
  """Show all loans for a customer."""

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
  """Display the loan details for a loanId"""

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
  """View for paying an installment"""

  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  activeLoan = ActiveLoan.objects.get(loan__id=loanId)
  dueDate = activeLoan.nextInstallmentDueDate
  installment = activeLoan.monthlyInstallment
  outstandingLoanBalance = activeLoan.outstandingLoanBalance
  return render_to_response('payInstallment.html', locals())


def payInstallmentThanks(request, loanId):
  """
     Updates the database with the payment details etc.
     Redirects to thank you page after the payment of an installment.
  """

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
    activeLoan.outstandingLoanBalance = activeLoan.computeOutstandingLoanBalance()
    activeLoan.save()


def newApplication(request):
  """Files a new application."""

  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

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
  """Thank you page after a new application request."""

  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  return render_to_response('newApplicationThanks.html')


def payPrepayment(request, loanId):
  """Prepay an amount for a loan."""

  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  activeLoan = ActiveLoan.objects.get(loan_id=loanId)
  loanName = activeLoan.loan.name
  outstandingAmount = activeLoan.outstandingLoanBalance
  if request.method == 'POST':
      form = PrepaymentForm(loanId, request.POST)
      if form.is_valid():
          cd = form.cleaned_data
          amount = cd.prepayAmount/(1+(activeLoan.prepaymentPenaltyRate/100))
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
  """Thank you page after the payment of an installment."""

  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  return render_to_response('payPrepaymentThanks.html', local())


def support(request):
  """View for filing a support request."""

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
  """Thank you page after a support request submission."""

  # Get the customerId and verify if the session is active.
  customerId = getCustomerId(request)

  return render_to_response('supportThanks.html', locals())
<<<<<<< HEAD

#The following classes are to provide an API using the djangorestframework

class PaymentsBetween(View):

	"""Format of URL: http://localhost:8000/api/paymentsBetween/<customer_id>/<start_date>/<end_date>
		<start_date>: s<date>
		<end_date>: e<date>
		<date>:ddmmyyyy
		
		<start_date> and <end_date> are optional
		
		Examples: http://localhost:8000/api/paymentsBetween/1
		        : http://localhost:8000/api/paymentsBetween/1/s17112011
		        : http://localhost:8000/api/paymentsBetween/1/e19112011
		        : http://localhost:8000/api/paymentsBetween/1/s17112011/e19112011
		        
		Note: Don't reverse the order of <start_date> and <end_date>"""
		        
	  
	#This is an API function which takes customer id, start date (optional) and end date (optional) and returns a JSON object containing a list of all the payments made by the customer between start and end date. If start data is missing, it returns all payments made BEFORE the end date. If end date is missing, it returns all payments made AFTER start date. If both are missing, it returns all payments made by the customer.

	#start and end are in ddmmyyyy format
	def get(self, request, cust_id, start=None, end=None):
		# Get all the loans for the customer using the customer_id
		loansList = Loan.objects.filter(customer=cust_id)
		
		#parse the url to get start date and end date
		def parse(datearg):
			return datetime.date(int(datearg)%10000, (int(datearg)/10000)%100, (int(datearg)/1000000))
		
		if (start != None):
			start = parse(start)
		
		if (end != None):
			end = parse(end)
		
		paymentsList = []
	
		#loop over all the loans of the customer and get payments for every loan
		if (start == None and end == None):
			for l in loansList:
				paymentsList += Payment.objects.filter(loan = l)	#add the list of payments corresponding to every loan to paymentsList
				
		elif (start != None and end == None):
			for l in loansList:
				paymentsList += Payment.objects.filter(loan = l).exclude(datePaid__lt=start)	#excludes payments made BEFORE the start date
			
		elif (start == None and end != None):
			for l in loansList:
				paymentsList += Payment.objects.filter(loan = l).exclude(datePaid__gt=end)	#excludes payments made AFTER the end date
		
		else:
			for l in loansList:
				paymentsList += Payment.objects.filter(loan = l).exclude(datePaid__gt=end).exclude(datePaid__lt=start)	#excludes payments made before the start date and after the end date
				
		result=[]
		for payment in paymentsList:
			result.append(payment.serialize());	#serialize all the payment objects so that they can be converted to JSON
			
		return result
	
	
class PaymentHistoryOfLoan(View):

	"""Format of URL: http://localhost:8000/api/paymentHistoryOfLoan/<customer_id>/<loan_name>
	
		 Examples: http://localhost:8000/api/paymentHistoryOfLoan/1/NewTestLoan1"""
	#This class takes a customer id and loan name and returns all the payments corresponding to that loan
	def get(self, request, lname, cust_id):
	
		l = Loan.objects.filter(customer=cust_id, name=lname)	#get all loans with the given customer id and name
		
		paymentsList = Payment.objects.filter(loan = l)	#get all the payments associated with that loan
		
		result = []
		for payment in paymentsList:
			result.append(payment.serialize())	#serialize all the payment objects
			
		return result
		
class Defaulters(View):

	"""Format of URL: http://localhost:8000/api/defaulters"""
	
	#this class defines customers with more than 2 overdue installments as defaulters and returns a list of all such customers
	
	def get(self, request):
		
		overdue = OverdueInstallment.objects.all()	#get all the overdue installments
		users = []
		for ins in overdue:
			users.append(ins.loan.customer)	#for every overdue installment, get the associated loan and the customer associated with that loan
		
		defaulters = []
		for user in users:
			if (users.count(user) > 2):	#condition for being a defaulter
				defaulters.append(user)
			
		result = []
		for defaulter in defaulters:
			result.append(defaulter)	#serialize all the customer objects
			
		return result


class PaymentHistoryAllLoans(View):
	
	"""Format of URL: http://localhost:8000/api/paymentHistoryAllLoans/<customer_id>
		
			Example: http://localhost:8000/api/paymentHistoryAllLoans/1"""
	
	def get(self, request, cust_id):
		# Get all the loans for the customer using the customer_id
		loansList = Loan.objects.filter(customer=cust_id)
	
		#the list to be returned
		paymentsList = []
	
		#loop over all the loans of the customer and get payments for every loan
		for l in loansList:
			paymentsList += Payment.objects.filter(loan = l)	#add the list of payments corresponding to every loan to paymentsList
 
		result = []
		for payment in paymentsList:
			result.append(payment.serialize())	#serialize
  	
		return result	
  	
class MonthlyInstallment(View):

	"""Format of URL: http://localhost:8000/api/monthlyInstallment/<customer_id>
	
		Example: http://localhost:8000/api/monthlyInstallment/1"""
	#This class gives all the monthly installments of all the loans of a given customer
	def get(self, request, cust_id):
	
		loansList = Loan.objects.filter(customer=cust_id, isActive=True)	#get active loan objects
		
		result = []
		for l in loansList:
			activeLoan = ActiveLoan.objects.filter(loan = l)	#for every loan, get the corresponding active loan
			result.append({'cust_id': l.customer.name, 'loanType': l.loanType, 'MonthlyInstallment': activeLoan[0].monthlyInstallment, 'DueDate': activeLoan[0].nextInstallmentDueDate,})	#serialize
			
		return result



=======
>>>>>>> origin
