from django.contrib import admin
from django.urls import path
from ninja_extra import NinjaExtraAPI

from server.api import HealthController

api = NinjaExtraAPI(
    title="Application API",
    version="1.0.0",
    docs_url="/docs",
)

api.register_controllers(HealthController)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
