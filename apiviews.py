from djangorestframework.views import ModelView, View;
from djangorestframework.mixins import ReadModelMixin, InstanceMixin
from djangorestframework.renderers import JSONRenderer;
from djangorestframework.serializer import Serializer;
from loans.models import *

import datetime;

class InstanceReadOnlyModelView(InstanceMixin, ReadModelMixin, ModelView):
  """A view which provides default operations for read against a model instance."""
  _suffix = 'Instance'


class PaymentsBetween(View):
  """
  This is an API function which takes customer id, start date (optional) and end date (optional) and returns a JSON object containing a list of all the payments made by the customer between start and end date.
  If start data is missing, it returns all payments made BEFORE the end date.
  If end date is missing, it returns all payments made AFTER start date.
  If both are missing, it returns all payments made by the customer.

  Format of URL: http://localhost:8000/api/paymentsBetween/<customer_id>/<start_date>/<end_date>
  <start_date>: s<date>
  <end_date>: e<date>
  <date>:ddmmyyyy

  <start_date> and <end_date> are optional

  Examples: http://localhost:8000/api/paymentsBetween/1
          : http://localhost:8000/api/paymentsBetween/1/s17112011
          : http://localhost:8000/api/paymentsBetween/1/e19112011
          : http://localhost:8000/api/paymentsBetween/1/s17112011/e19112011

  Note: Don't reverse the order of <start_date> and <end_date>
  """

  # start and end are in ddmmyyyy format
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
        paymentsList += Payment.objects.filter(loan = l)  #add the list of payments corresponding to every loan to paymentsList

    elif (start != None and end == None):
      for l in loansList:
        paymentsList += Payment.objects.filter(loan = l).exclude(datePaid__lt=start)  #excludes payments made BEFORE the start date

    elif (start == None and end != None):
      for l in loansList:
        paymentsList += Payment.objects.filter(loan = l).exclude(datePaid__gt=end)  #excludes payments made AFTER the end date

    else:
      for l in loansList:
        paymentsList += Payment.objects.filter(loan = l).exclude(datePaid__gt=end).exclude(datePaid__lt=start)  #excludes payments made before the start date and after the end date

    result=[]
    for payment in paymentsList:
      result.append(payment.serialize());  #serialize all the payment objects so that they can be converted to JSON

    return JSONRenderer(self).render(result)  #convert to JSON


class PaymentHistoryOfLoan(View):
  """
  This class takes a customer id and loan name and returns all the payments corresponding to that loan
  Format of URL: http://localhost:8000/api/paymentHistoryOfLoan/<customer_id>/<loan_name>

  Examples: http://localhost:8000/api/paymentHistoryOfLoan/1/NewTestLoan1
  """

  def get(self, request, lname, cust_id):

    l = Loan.objects.filter(customer=cust_id, name=lname)  #get all loans with the given customer id and name

    paymentsList = Payment.objects.filter(loan = l)  #get all the payments associated with that loan

    result = []
    for payment in paymentsList:
      result.append(payment.serialize())  #serialize all the payment objects

    return JSONRenderer(self).render(result)  #convert to JSON


class Defaulters(View):
  """
  This class defines customers with more than 2 overdue installments as defaulters and returns a list of all such customers.
  Format of URL: http://localhost:8000/api/defaulters
  """

  def get(self, request):

    overdue = OverdueInstallment.objects.all()  #get all the overdue installments
    users = []
    for ins in overdue:
      users.append(ins.loan.customer)  #for every overdue installment, get the associated loan and the customer associated with that loan

    defaulters = []
    for user in users:
      if (users.count(user) > 2):  #condition for being a defaulter
        defaulters.append(user)

    result = []
    for defaulter in defaulters:
      result.append(defaulter)  #serialize all the customer objects

    return JSONRenderer(self).render(result)  #convert to JSON


class PaymentHistoryAllLoans(View):
  """
  Format of URL: http://localhost:8000/api/paymentHistoryAllLoans/<customer_id>

  Example: http://localhost:8000/api/paymentHistoryAllLoans/1
  """

  def get(self, request, cust_id):
    # Get all the loans for the customer using the customer_id
    loansList = Loan.objects.filter(customer=cust_id)

    #the list to be returned
    paymentsList = []

    #loop over all the loans of the customer and get payments for every loan
    for l in loansList:
      paymentsList += Payment.objects.filter(loan = l)  #add the list of payments corresponding to every loan to paymentsList

    result = []
    for payment in paymentsList:
      result.append(payment.serialize())  #serialize

    return JSONRenderer(self).render(result)  #convert to JSON


class MonthlyInstallment(View):
  """
  This class gives all the monthly installments of all the loans of a given customer.
  Format of URL: http://localhost:8000/api/monthlyInstallment/<customer_id>

  Example: http://localhost:8000/api/monthlyInstallment/1
  """
  
  def get(self, request, cust_id):

    loansList = Loan.objects.filter(customer=cust_id, isActive=True)  #get active loan objects

    result = []
    for l in loansList:
      activeLoan = ActiveLoan.objects.filter(loan = l)  #for every loan, get the corresponding active loan
      result.append({'cust_id': l.customer.name, 'loanType': l.loanType, 'MonthlyInstallment': activeLoan[0].monthlyInstallment, 'DueDate': activeLoan[0].nextInstallmentDueDate,})  #serialize

    return JSONRenderer(self).render(result)  #convert to JSON
