from django.db import models
from django.db.models import signals
from django.db.models.signals import post_save

LOAN_TYPES = (
  ("Personal - Home", "Personal - Home"),
  ("Personal - Car", "Personal - Car"),
  ("Personal - Education", "Personal - Education"),
  ("Corporate", "Corporate"),
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
  """Each customer of the bank is an instance of this class."""
  name = models.CharField(max_length=50)
  accountNumber = models.IntegerField()
  customerType = models.CharField(max_length=20) # Personal or Corporate
  creditRating = models.IntegerField()

  def __unicode__(self):
    return u'%s %s' % (self.accountNumber, self.name)

  def serialize(self):
    result = {'name': str(self.name), 'accountNumber': str(self.accountNumber), 'customerType': str(self.customerType), 'creditRating': str(self.creditRating),}
    return result


class Loan(models.Model):
  """Each loan a customer take is an instance of this class. A customer can be associated with one or more loans."""
  name = models.CharField(max_length=50)
  isActive = models.BooleanField()
  principal = models.DecimalField(max_digits=15, decimal_places=2)
  originalMonths = models.IntegerField() # The total time period of the loan
  interestCategory = models.CharField(max_length=10) # Fixed or Floating
  loanType = models.CharField(max_length=100, choices=LOAN_TYPES)
  dateTaken = models.DateTimeField(auto_now_add=True)
  security = models.CharField(max_length=100, choices=SECURITY_TYPES)
  customer = models.ForeignKey(Customer)

  def serialize(self):
    result = {'name':str(self.name), 'isActive':str(self.isActive), 'principal':str(self.principal), 'originalMonths':str(self.originalMonths), 'interestCategory':str(self.interestCategory), 'loanType':str(self.loanType), 'dateTaken':str(self.dateTaken), 'security':str(self.security),}
    return result

  def __unicode__(self):
    return u'%s' % (self.name)


class ActiveLoan(models.Model):
  """Each ActiveLoan is an instance of this class."""
  loan = models.OneToOneField(Loan)
  expectedDateOfTermination = models.DateTimeField()
  elapsedMonths = models.IntegerField()
  monthlyInstallment = models.DecimalField(max_digits=15, decimal_places=2)
  interestRate = models.DecimalField(max_digits=6, decimal_places=2) # This is the annual interest rate in percentage.
  prepaymentPenaltyRate = models.DecimalField(max_digits=6, decimal_places=2)
  outstandingLoanBalance = models.DecimalField(max_digits=15, decimal_places=2)
  nextInstallmentDueDate = models.DateTimeField()

  def computeMonthlyInstallment(self):
    """Returns the monthly installment based on the current outstanding loan balance, monthly interest rate and remaining months."""
    monthlyInterestRate = self.interestRate/(100*12)
    remainingMonths = self.loan.originalMonths - self.elapsedMonths
    return (self.outstandingLoanBalance*monthlyInterestRate * (1+monthlyInterestRate)**(remainingMonths)) / ((1+monthlyInterestRate)**(remainingMonths) - 1)

  def computeOutstandingLoanBalance(self):
    """
    Returns the balance outstanding after elapsedMonths have passed (assuming all installments were paid on time.)
    Notes on usage: Call this function once after paying every installment (when you increase elapsedMonths). Set outstandingLoanBalance using the value returned by this function. After that use that variable to query the outstanding loan balance.
    """
    monthlyInterestRate = self.interestRate/(100*12)
    remainingMonths = self.loan.originalMonths - self.elapsedMonths
    if self.elapsedMonths != 0:
      return self.outstandingLoanBalance * ((1+monthlyInterestRate)**(remainingMonths+1) - (1 + monthlyInterestRate))/((1 + monthlyInterestRate)**(remainingMonths+1) - 1)
    else:
      return self.loan.principal

  def save(self, *args, **kwargs):
    """Updates monthlyInstallment and saves the entry"""
    self.monthlyInstallment = self.computeMonthlyInstallment()
    super(ActiveLoan, self).save(*args, **kwargs)

def firstSaveHandler(sender, instance, created, *args, **kwargs):
  """
  This function is used to set the outstanding loan balance and elapsed months when the loan object is created.
  Argument Explanation:
  sender - The model class. (ActiveLoan)
  instance - The actual instance being saved.
  created - Boolean; True if a new record was created.
  """
  if created:
    instance.outstandingLoanBalance = instance.loan.principal
    instance.elapsedMonths = 0
    instance.save()

post_save.connect(firstSaveHandler, sender=ActiveLoan)


class CompletedLoan(models.Model):
  """Record for every completed loan."""
  loan = models.OneToOneField(Loan)
  dateOfCompletion = models.DateTimeField(auto_now_add=True)
  totalAmountPaid = models.DecimalField(max_digits=15, decimal_places=2)
  averageInterestRate = models.DecimalField(max_digits=6, decimal_places=2)


class Payment(models.Model):
  """Record storing every transaction"""
  amount = models.DecimalField(max_digits=15, decimal_places=2)
  loan = models.ForeignKey(Loan)
  paymentType = models.CharField(max_length=20) # Prepayment or Installment
  datePaid = models.DateTimeField(auto_now_add=True)
  merchantUsed = models.CharField(max_length=20)

  def serialize(self):
    result = {'amount': str(self.amount), 'loan': str(self.loan), 'paymentType': str(self.paymentType), 'datePaid': str(self.datePaid), 'merchantUsed': str(self.merchantUsed),}

    return result;


class OverdueInstallment(models.Model):
  """This class stores all the installments which have passed their due dates and haven't been paid yet"""
  amount = models.DecimalField(max_digits=15, decimal_places=2)
  dueDate = models.DateTimeField()
  loan = models.ForeignKey(Loan)

  def __unicode__(self):
    return u'%s' % (self.loan)


class Application(models.Model):
  """This stores information a user fills while applying for a new loan. This information is transferred to loan object once the application is approved."""
  name = models.CharField(max_length=50)
  loanType = models.CharField(max_length=100, choices=LOAN_TYPES)
  amountAppliedFor = models.DecimalField(max_digits=15, decimal_places=2)
  dateApplied = models.DateTimeField(auto_now_add=True)
  security = models.CharField(max_length=100, choices=SECURITY_TYPES)
  customer = models.ForeignKey(Customer)
  amountAllotted = models.DecimalField(max_digits=15, decimal_places=2, default = 0)
  interestCategory = models.CharField(max_length=10, blank=True)
  interestRate = models.DecimalField(max_digits=6, decimal_places=2, default = 0) # This is annual interest rate in percentage.
  dateOfAllotment = models.DateTimeField(auto_now_add=True)
  loan = models.ForeignKey(Loan, blank=True, null=True)
  status = models.CharField(max_length=20, blank=True) # Active, Allotted, Rejected, Cancelled
  isArchived = models.BooleanField(default=False) # User can archive the application if he doesn't want to see it again on his screen.
  remark = models.TextField(blank=True)


class SupportTicket(models.Model):
  """This stores information about any complaint a user might have."""
  loan = models.ForeignKey(Loan, blank=True, null=True)
  complaintType = models.CharField(max_length=20, choices=COMPLAINT_TYPES)
  complaintMessage = models.TextField()
  customer = models.ForeignKey(Customer)

#class Merchant(models.Model):

#class IdentityModule(models.Model):

#class AccountsModule(models.Model):

#class TransactionsModule(models.Model):
