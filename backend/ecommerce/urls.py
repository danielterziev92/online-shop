from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from ecommerce.accounts.views.sign_in import sign_in_router

api = NinjaAPI(docs_url='docs/')
api.add_router('auth/', router=sign_in_router)

urlpatterns = (
    path('admin/', admin.site.urls),
    path('api/', api.urls),
)
