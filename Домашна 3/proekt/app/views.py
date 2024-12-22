import os

from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO, StringIO
import base64
import matplotlib
from django.conf import settings

matplotlib.use("Agg")

from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .vizuelizacija import kod_za_generiranje_dijagram

class StartingPageView(View):
    def get(self, request):
        plot_data1 = kod_za_generiranje_dijagram('data_for_KMB.csv')
        plot_data2 = kod_za_generiranje_dijagram('data_for_ALK.csv')
        plot_data3 = kod_za_generiranje_dijagram('data_for_ADIN.csv')
        return render(request, "app/starting_page.html",{'plot_data1': plot_data1, 'plot_data2': plot_data2, 'plot_data3':plot_data3})


class LoginPage(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'app/login_form.html', {'loginform': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect("dashboard-page")
        else:
            return render(request, 'app/login_form.html', {'loginform': form})




class RegisterPage(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'app/register_form.html', {'registerform': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login-page")
        else:
            return render(request, 'app/register_form.html', {'registerform': form})


class DashboardPageView(LoginRequiredMixin, View):
    login_url = 'login-page'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        # Path to the 'Data' folder
        data_folder_path = os.path.join(settings.BASE_DIR, 'Data')

        # Get all CSV file names and clean them up
        csv_files = [
            {
                'full_name': file,  # Full file name
                'display_name': file.replace("data_for_", "").replace(".csv", "")  # Cleaned display name
            }
            for file in os.listdir(data_folder_path)
            if file.endswith('.csv')
        ]

        # Optionally generate the first graph for the first file
        first_file = csv_files[0]['full_name'] if csv_files else None
        plot_data = kod_za_generiranje_dijagram(first_file) if first_file else None

        # Pass the list of cleaned CSV file names and initial graph data to the template
        return render(
            request,
            "app/dashboard_page.html",
            {
                'csv_files': csv_files,
                'plot_data': plot_data
            }
        )

class UpdateGraphView(LoginRequiredMixin, View):
    def get(self, request):
        filename = request.GET.get('filename')
        if filename:
            try:
                plot_data = kod_za_generiranje_dijagram(filename)
                return JsonResponse({'plot_data': plot_data}, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        return JsonResponse({'error': 'No filename provided'}, status=400)







def user_logout(request):

    auth.logout(request)
    return redirect("starting-page")






class Test(View): #ZA DIJAGRAM PRAENJE
    def get(self, request):
        plot_data1 = kod_za_generiranje_dijagram('data_for_KMB.csv')
        plot_data2 = kod_za_generiranje_dijagram('data_for_ALK.csv')
        plot_data3 = kod_za_generiranje_dijagram('data_for_ADIN.csv')
        return render(request, 'app/test.html', {'plot_data1': plot_data1, 'plot_data2': plot_data2, 'plot_data3':plot_data3})



# <img src="data:image/png;base64,{{ plot_data }}" alt="Ценовни трендови">


