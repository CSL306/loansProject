from django.contrib import admin
from loansProject.loans.models import *

admin.site.register(Customer)
admin.site.register(Loan)
admin.site.register(ActiveLoan)
admin.site.register(CompletedLoan)
admin.site.register(Payment)
admin.site.register(OverdueInstallment)
admin.site.register(Application)
admin.site.register(AlottedApplication)
admin.site.register(ActiveApplication)
admin.site.register(SupportTicket)
