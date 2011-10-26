from django.db import models

# Create your models here.

class Customers(models.Model):
  name = models.CharField(max_length=50)

class Loans(models.Model):
  category = models.CharField(max_length=10)
  principal = models.DecimalField(max_digits=15, decimal_places=2)
  interestRate = models.DecimalField(max_digits=6, decimal_places=2)
  amountPaid = models.DecimalField(max_digits=15, decimal_places=2)
  dateTaken = models.DateTimeField(auto_now_add=True)
  customer = models.ForeignKey(Customers)

class FloatingLoans(Loans):
  minDate = models.DateTimeField()
  maxDate = models.DateTimeField()

class FixedLoans(Loans):
  lastInstallmentDate = models.DateTimeField()

class Installments(models.Model):
  amount = models.DecimalField(max_digits=15, decimal_places=2)
  loan = models.ForeignKey(Loans)

class PaidInstallments(Installments):
  datePaid = models.DateTimeField()
  merchantUsed = models.CharField(max_length=20)

class DueInstallments(Installments):
  startDate =  models.DateTimeField()
  endDate = models.DateTimeField()

class Applications(models.Model):
  customer = models.ForeignKey(Customers)
  loan = models.ForeignKey(Loans)
  dateApplied = models.DateTimeField(auto_now_add=True)
  details = models.TextField()
  status = models.CharField(max_length=20)
  remark = models.TextField()

class SupportTickets(models.Model):
  loan = models.ForeignKey(Loans)
  complaintType = models.CharField(max_length=20)
  complaintMessage = models.TextField()

#class Merchants(models.Model):


#class IdentityModule(models.Model):


#class AccountsModule(models.Model):


#class TransactionsModule(models.Model):

