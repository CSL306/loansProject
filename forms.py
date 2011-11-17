from django import forms
from loans.models import LOAN_TYPES, COMPLAINT_TYPES, SECURITY_TYPES

class supportForm(forms.Form):
  complaintType = forms.ChoiceField(choices=COMPLAINT_TYPES)
  loanId = forms.IntegerField()
  message = forms.CharField(widget=forms.Textarea)
  
  def supportForm(self, customerId):
    self.customerId = customerId
    
  # TODO: Validate the loanId is valid for the given customer
  def clean_loanId(self):
    return loanId
    
class ApplicationForm(forms.Form):
  loanName = forms.CharField()
  loanAmount = forms.DecimalField(min_value=10000, decimal_places=2)
  loanCategory = forms.ChoiceField(choices=LOAN_TYPES)
  security = forms.ChoiceField(choices=SECURITY_TYPES)
  acceptedTerms = forms.BooleanField()
  
class PrepaymentForm(forms.Form):
  prepaymentAmount = forms.DecimalField(min_value=5000)
  
  def PrepaymentForm(self, loanId):
    self.loanId = loanId
  
  #TODO: Validate against the outstanding loan balance.
  def clean_prepaymenAmount(self):
    return prepaymentAmount