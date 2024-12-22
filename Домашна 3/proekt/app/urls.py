from django.urls import path
from . import views
urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("test", views.Test.as_view(), name="test-page"),
    path("login", views.LoginPage.as_view(), name="login-page"),
    path("register", views.RegisterPage.as_view(), name="register-page"),
    path("dashboard", views.DashboardPageView.as_view(), name="dashboard-page"),
    path("user-logout", views.user_logout, name="user-logout"),
    path('update-graph', views.UpdateGraphView.as_view(), name='update-graph'),

]