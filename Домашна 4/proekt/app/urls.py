from django.urls import path
from . import views
urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("login", views.LoginPage.as_view(), name="login-page"),
    path("register", views.RegisterPage.as_view(), name="register-page"),
    path("dashboard", views.DashboardPageView.as_view(), name="dashboard-page"),
    path("user-logout", views.user_logout, name="user-logout"),
    path('update-graph', views.UpdateGraphView.as_view(), name='update-graph'),


    path('train-model', views.TrainModelView.as_view(), name='train-model'),

    path('search-results-vizuelizacija', views.SearchResultsViewVizuelizacija.as_view(), name='search-results-page-vizuelizacija'),
    path('search-results-tehnicka', views.SearchResultsViewTehnicka.as_view(), name='search-results-page-tehnicka'),
    path('search-results-fundamentalna', views.SearchResultsViewFundamentalna.as_view(), name='search-results-page-fundamentalna'),
    path('search-results-predviduvanje', views.SearchResultsViewPredviduvanje.as_view(), name='search-results-page-predviduvanje'),

    path('graph-data', views.get_graph_dataView.as_view(), name='graph-data'),
    path('table-data', views.get_table_dataView.as_view(), name='table-data'),

    path('card-data', views.get_card_dataView.as_view(), name='card-data'),

    path('add-to-favorites/', views.AddToFavoritesView.as_view(), name='add-to-favorites'),
    path('get-favorites/', views.GetFavoritesView.as_view(), name='get-favorites'),
    path('remove-from-favorites/', views.RemoveFromFavoritesView.as_view(), name='remove-from-favorites'),
]

