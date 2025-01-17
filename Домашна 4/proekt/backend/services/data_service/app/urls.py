from django.urls import path
from .views import MarketSummaryAPIView
from .views import ScrapeTableView
from .views import ScrapeSEINetNewsView

urlpatterns = [
    path("get-market-summary/", MarketSummaryAPIView.as_view(), name="market-summary"),
    path("get-scrape-table/", ScrapeTableView.as_view(), name="scrape-table"),
    path("get-sei-net-news/", ScrapeSEINetNewsView.as_view(), name="sei-net-news"),
]
