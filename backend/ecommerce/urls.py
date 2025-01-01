from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from ecommerce.accounts.views.account_detail import account_detail_router
from ecommerce.accounts.views.sign_in import sign_in_router
from ecommerce.accounts.views.sign_up import sign_up_router
from ecommerce.accounts.views.verify_code import verify_code_router

api = NinjaAPI(docs_url='docs/')
[
    api.add_router('auth/', router=router)
    for router in [sign_in_router, sign_up_router, verify_code_router, account_detail_router]
]

urlpatterns = (
    path('admin/', admin.site.urls),
    path('api/', api.urls),
)
