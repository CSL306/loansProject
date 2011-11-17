from django.db import models

# Create your models here.

LOAN_TYPES = (
  ("Personal - Home", "Personal - Home"),
  ("Personal - Car", "Personal - Car"),
  ("Corporate", "Corporate")
)

COMPLAINT_TYPES = (
  ("None of these", "None of these"),
  ("TYPE A", "TYPE A"),
  ("TYPE B", "TYPE B")
)

SECURITY_TYPES = (
  ("None", "None"),
  ("Vehicle", "Vehicle"),
  ("Car", "Car"),
  ("House", "House")
)

class Customer(models.Model):
  name = models.CharField(max_length=50)
  accountNumber = models.IntegerField()
  customerType = models.CharField(max_length=20)
  creditRating = models.IntegerField()

  def __unicode__(self):
    return u'%s %s' % (self.accountNumber, self.name)

class Loan(models.Model):
  name = models.CharField(max_length=50)
  isActive = models.BooleanField()
  principal = models.DecimalField(max_digits=15, decimal_places=2)
  originalMonths = models.IntegerField()
  interestCategory = models.CharField(max_length=10) # Fixed or Floating
  loanType = models.CharField(max_length=100, choices=LOAN_TYPES) # of the form "Personal - Car", etc
  dateTaken = models.DateTimeField(auto_now_add=True)
  security = models.CharField(max_length=100, choices=SECURITY_TYPES)
  customer = models.ForeignKey(Customer)

  def __unicode__(self):
    return u'%s' % (self.name)

class ActiveLoan(models.Model):
  loan = models.OneToOneField(Loan)
  expectedDateOfTermination = models.DateTimeField()
  elapsedMonths = models.IntegerField()
  monthlyInstallment = models.DecimalField(max_digits=15, decimal_places=2)
  interestRate = models.DecimalField(max_digits=6, decimal_places=2) # This is annual interest rate in percentage.
  prepaymentPenaltyRate = models.DecimalField(max_digits=6, decimal_places=2)
  outstandingLoanBalance = models.DecimalField(max_digits=15, decimal_places=2)
  nextInstallmentDueDate = models.DateTimeField()

  def computeMonthlyInstallment(self):
    monthlyInterestRate = self.interestRate/(100*12)
    return (self.principal * monthlyInterestRate * (1 + monthlyInterestRate)**(self.originalMonths))/((1 + monthlyInterestRate)**(self.originalMonths) - 1)

  def computeOutstandingLoanBalance(self):
    monthlyInterestRate = self.interestRate/(100*12)
    return self.principal * ((1+monthlyInterestRate)**(self.originalMonths) - (1 + monthlyInterestRate)**(self.elapsedMonths))/((1 + monthlyInterestRate)**(self.originalMonths) - 1)

  def save(self, *args, **kwargs):
    self.monthlyInstallment = self.computeMonthlyInstallment()
    self.outstandingLoanBalance = self.computeOutstandingLoanBalance()
    super(ActiveLoan, self).save(*args, **kwargs)

class CompletedLoan(models.Model):
  loan = models.OneToOneField(Loan)
  dateOfCompletion = models.DateTimeField(auto_now_add=True)
  totalAmountPaid = models.DecimalField(max_digits=15, decimal_places=2)
  averageInterestRate = models.DecimalField(max_digits=6, decimal_places=2)

class Payment(models.Model):
  amount = models.DecimalField(max_digits=15, decimal_places=2)
  loan = models.ForeignKey(Loan)
  paymentType = models.CharField(max_length=20) #prepayment/installment
  datePaid = models.DateTimeField(auto_now_add=True)
  merchantUsed = models.CharField(max_length=20)

class OverdueInstallment(models.Model):
  amount = models.DecimalField(max_digits=15, decimal_places=2)
  dueDate = models.DateTimeField()
  loan = models.ForeignKey(Loan)

  def __unicode__(self):
    return u'%s' % (self.loan)

class Application(models.Model):
  name = models.CharField(max_length=50)
  loanType = models.CharField(max_length=100, choices=LOAN_TYPES) # of the form "Personal - Car", etc
  amountAppliedFor = models.DecimalField(max_digits=15, decimal_places=2)
  dateApplied = models.DateTimeField(auto_now_add=True)
  security = models.CharField(max_length=100, choices=SECURITY_TYPES)
  customer = models.ForeignKey(Customer)
  amountAllotted = models.DecimalField(max_digits=15, decimal_places=2)
  interestCategory = models.CharField(max_length=10)
  interestRate = models.DecimalField(max_digits=6, decimal_places=2) # This is annual interest rate in percentage.
  dateOfAllotment = models.DateTimeField()
  loan = models.ForeignKey(Loan, blank=True, null=True)
  status = models.CharField(max_length=20) # Active, Allotted, Rejected, Cancelled
  isArchived = models.BooleanField()
  remark = models.TextField()

class SupportTicket(models.Model):
  loan = models.ForeignKey(Loan, blank=True, null=True)
  complaintType = models.CharField(max_length=20, choices=COMPLAINT_TYPES)
  complaintMessage = models.TextField()
  customer = models.ForeignKey(Customer)

#class Merchant(models.Model):


#class IdentityModule(models.Model):


#class AccountsModule(models.Model):


#class TransactionsModule(models.Model):
