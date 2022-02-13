from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from UserWalletsApp import views

urlpatterns=[
    url(r'^user$', views.userApi),
    url(r'^user/balances$', views.userBalancesApi),
    url(r'^user/transactions$', views.userTransactionsApi),

    url(r'^currency$', views.currenciesApi),

    url(r'^transaction$', views.transactionApi),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
