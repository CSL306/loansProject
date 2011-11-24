from django.test import *
from loans.models import *

class SimpleTest(TestCase):
  fixtures=['loans']
  """
  The fixture data has already been dumped and is a precondition for all the tests.
  """
  def setUp(self):
    self.c=Client()

  def numEntries(self,string,response):
    """
    Returns an integer number - the length of a dictionary/list present in the response.context object
    """
    self.alist=response.context[string]
    return len(self.alist)

  def test_newApplication(self):
    """
    Precondition: The user is logged in and has a valid customer ID.
    Page Behaviour: New Loan Applications is being created.
    Test: Testing whether all fields are being sent as required and whether the routing has been configured properly.
    """
    resp=self.c.post('/newApplication/',{'id_loanName':'Test',
                                        'id_loanAmount':100000, 
                                        'id_loanCategory':'Home',
                                        'id_security':'Car',
                                        'id_acceptedTerms':True,
    })
    self.assertEqual(len(resp.context['request'].POST),5)
    self.assertEqual(resp.status_code,200)

  def test_dueInstallments(self):
    """
    Precondition: The user is logged in and has a valid customer ID. The customer has an active loan.
    Page Behaviour: Displays all the dueinstallments for a customer.
    Test: Testing whether the reqiured information is prespent/passsed and whether the routing has been configured properly.
    """
    resp=self.c.get('/dueInstallments/')
    
    oi=resp.context['overdueInstallments'][0]
    self.assertTrue(len(oi)>=4)
    
    di=resp.context['dueInstallments'][0]
    self.assertTrue(len(di)>=4)
    
    payLink=oi['payLink']
    self.assertTrue(len(payLink)>0)
    
    self.assertEqual(resp.status_code,200)

  def test_allLoans(self):
    """
    Precondition: The user is logged in and has a valid customer ID.
    Page Behaviour: Displays all the loans taken by a customer.
    Test: Testing whether the reqiured information is prespent/passsed and whether the routing has been configured properly.
    """
    resp=self.c.get('/allLoans/')
    
    activeLoan=resp.context['actDict'][0]
    self.assertTrue(len(activeLoan)>=14)
    
    prepayLink=activeLoan['prepayNowLink']
    self.assertTrue(len(prepayLink)>0)
    
    detailLink=activeLoan['detailLink']
    self.assertTrue(len(detailLink)>0)
    
    completedLoan=resp.context['compDict'][0]
    self.assertTrue(len(completedLoan)>=10)
    
    detailLink=completedLoan['detailLink']
    self.assertTrue(len(detailLink)>0)
    
    self.assertEqual(resp.status_code,200)

    resp2=self.c.get('/loanDetails/1/')
    self.assertEqual(resp2.status_code,200)


  def test_applications(self):
    """
    Precondition: The user is logged in and has a valid customer ID. The customer has applied for some loans.
    Page Behaviour: Displays all the loan applications of a customer.
    Test: Testing whether the routing and Archive and Cancel/Archive buttons has been configured properly. 
    """
    resp=self.c.get('/allApplications/')
   
    applications=['processedApplications','underProcessingApplications','archivedApplications']   
    
    self.assertEqual(self.numEntries(applications[0],resp),1)
    self.assertEqual(self.numEntries(applications[1],resp),1)
    self.assertEqual(self.numEntries(applications[2],resp),1)
    
    link=resp.context[applications[0]][0]['archiveLink']
    resp=self.c.get(link,follow=True)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(self.numEntries(applications[0],resp),0)

    link=resp.context[applications[1]][0]['cancelLink']
    resp=self.c.get(link,follow=True)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(self.numEntries(applications[1],resp),0)

    self.assertEqual(self.numEntries(applications[2],resp),3)

  def test_allPayments(self):
    """
    Precondition: The user is logged in and has a valid customer ID.
    Page Behaviour: Displays all the payments made by the customer.
    Test: Testing whether the routing has been configured properly
    """
    resp=self.c.get('/allPayments/')
    self.assertEqual(resp.status_code,200)

  def test_payInstallment(self):
    """
    Precondition: The user is logged in and has a valid customer ID. The customer has an active loan.
    Page Behaviour: Displays the installment information.
    Test: Testing whether the routing has been configured and the database is updated properly.
    """
    activeLoan=ActiveLoan.objects.get(id=2)
    oldLoanBalance=activeLoan.outstandingLoanBalance
    resp=self.c.post('/payInstallment/2/')
    self.assertEqual(resp.status_code,302)
    activeLoan=ActiveLoan.objects.get(id=2)
    newLoanBalance=activeLoan.outstandingLoanBalance
    self.assertTrue(newLoanBalance<oldLoanBalance)
  
  def test_payPrepayment(self):
    """
    Precondition: The user is logged in and has a valid customer ID.
    Page Behaviour: Displays the form to enter prepayment amount.
    Test: Testing whether the routing has been configured properly.
    """
    resp=self.c.get('/payPrepayment/2/')
    self.assertEqual(resp.status_code,200)

  def test_support(self):
    """
    Precondition: The user is logged in and has a valid customer ID.
    Page Behaviour: Displays a form to file a support request.
    Test: Testing whether the routing has been configured properly
    """
    resp=self.c.get('/support/')
    self.assertEqual(resp.status_code,200)

