"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import *
from loans.models import *


class SimpleTest(TestCase):
  fixtures=['loan']

  def test_basic_addition(self):
    """
    Tests that 1 + 1 always equals 2.
    """
    self.failUnlessEqual(1 + 1, 2)
  
  def setUp(self):
    self.client=Client()

  def test_basic_views(self):
    """
    Testing views
    """
    self.loan=Loan.objects.filter(id=1)
    self.assertEqual(self.loan[0].id,1)
    
    response = self.client.get('/allLoans/')
    self.assertEqual(response.status_code, 200)
    
    response = self.client.get('/loanDetails/1/')
    self.assertEqual(response.status_code, 200)
    
    response = self.client.get('/allApplications/')
    self.assertEqual(response.status_code, 200)
    
    response = self.client.get('/dueInstallments/')
    self.assertEqual(response.status_code, 200)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}
