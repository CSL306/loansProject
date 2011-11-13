from django.contrib import admin
from loansProject.loans.models import *

admin.site.register(Customers)
admin.site.register(Loans)
admin.site.register(PaidInstallments)
admin.site.register(Applications)
admin.site.register(SupportTickets)
