from django.urls import path
from .views import MarketSummaryAPIView, ScrapeTableView, ScrapeSEINetNewsView
from django.http import JsonResponse

urlpatterns = [
    path('', lambda request: JsonResponse({'message': 'Welcome to Data Service API'})),
    path("get-market-summary/", MarketSummaryAPIView.as_view(), name="market-summary"),
    path("get-scrape-table/", ScrapeTableView.as_view(), name="scrape-table"),
    path("get-sei-net-news/", ScrapeSEINetNewsView.as_view(), name="sei-net-news"),
]