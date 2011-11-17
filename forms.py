from django import forms
from loans.models import *

class SupportForm(forms.Form):
  complaintType = forms.ChoiceField(choices=COMPLAINT_TYPES)
  message = forms.CharField(widget=forms.Textarea)
  
  def __init__(self, customerId, data = None):
    self.customerId = customerId
    super(SupportForm, self).__init__(data)
    self.fields['loan'] = forms.ModelChoiceField(queryset=Loan.objects.filter(customer__id=customerId))
    
  def clean_loan(self):
    loan = self.cleaned_data["loan"]
    if loan not in Loan.objects.filter(customer__id=self.customerId):
      raise forms.ValidationError('The loan provided is not valid.')
    else:
      return loan
    
class ApplicationForm(forms.Form):
  loanName = forms.CharField()
  loanAmount = forms.DecimalField(min_value=10000, decimal_places=2)
  loanCategory = forms.ChoiceField(choices=LOAN_TYPES)
  security = forms.ChoiceField(choices=SECURITY_TYPES)
  acceptedTerms = forms.BooleanField()
  
class PrepaymentForm(forms.Form):
  prepaymentAmount = forms.DecimalField()
  
  def __init__(self, loanId, data = None):
    self.loanId = loanId
    super(PrepaymentForm, self).__init__(data)
  
  def clean_prepaymenAmount(self):
    formAmount = form.cleaned_data["prepaymentAmount"]
    maxAmount = Loan.objects.get(id=self.loanId).activeloan.outstandingLoanBalance
    if (formAmount > maxAmount):
      raise forms.ValidationError('Prepayment amount cannot be more than the outstanding amount for the loan.')
    else: 
      return formAmount
