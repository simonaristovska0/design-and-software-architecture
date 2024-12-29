
from django.shortcuts import render, HttpResponse, redirect
import matplotlib

matplotlib.use("Agg")

from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import FavoriteQuery
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .vizuelizacija import kod_za_generiranje_dijagram, kod_za_generiranje_tabela, generate_karticki_dashboard
from .train_model import func
from django.views import View
from django.shortcuts import render
import csv
from app.utils.indicators import (
    calculate_rsi, calculate_stochastic, calculate_cci, calculate_adx,
    calculate_sma, calculate_ema, calculate_wma, calculate_hma, calculate_typical_price, calculate_roc
)
from app.utils.visualizations import generate_summary, generate_gauge


class StartingPageView(View):
    def get(self, request):
        mse_csv_path = os.path.join(settings.BASE_DIR, "za_homepage", "mse_table.csv")
        sei_net_csv_path = os.path.join(settings.BASE_DIR, "za_homepage", "sei_net_news_only.csv")
        market_summary_csv_path = os.path.join(settings.BASE_DIR, "za_homepage", "market_summary.csv")

        mse_table_data = []
        with open(mse_csv_path, newline='', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    change = float(row["% пром."].replace(",", "."))
                    if change > 0:
                        row["color"] = "#2DCE89"  # Green
                    elif change < 0:
                        row["color"] = "#F5365C"  # Red
                    else:
                        row["color"] = "#5E5DFF"  # Blue
                except ValueError:
                    row["color"] = "#000000"  # Black
                mse_table_data.append(row)

        sei_net_news = []
        with open(sei_net_csv_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sei_net_news.append(row.get("News", "Unknown"))

        market_summary_data = []
        with open(market_summary_csv_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                market_summary_data.append(row)

        context = {
            "table_data": mse_table_data,
            "sei_net_news": sei_net_news,
            "market_summary": market_summary_data,
        }
        return render(request, "app/starting_page.html", context)

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





class SearchResultsViewFundamentalna(LoginRequiredMixin, View):
    login_url = 'login-page'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        query = request.GET.get('query')

        base_dir = os.path.join(settings.BASE_DIR, 'fundumental_analysis', 'pdf_downloads', query)

        sentiment_file = os.path.join(base_dir, f'sentiment_{query}_combined.txt')
        translated_file = os.path.join(base_dir, f'translated_{query}_combined.txt')
        original_file = os.path.join(base_dir, f'{query}_combined.txt')

        def read_file(file_path):
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            return "Фајлот не е достапен."

        def parse_sentiment(content):
            lines = content.split("\n", 1)
            sentiment_score = lines[0] if len(lines) > 0 else "Нема податоци за сентиментот."
            sentiment_advice = lines[1] if len(lines) > 1 else "Нема препораки."
            return sentiment_score, sentiment_advice

        sentiment_content_raw = read_file(sentiment_file)
        sentiment_score, sentiment_advice = parse_sentiment(sentiment_content_raw)
        translated_content = read_file(translated_file)
        original_content = read_file(original_file)

        return render(request, 'app/search_result_page-fundamentalna.html', {
            'query': query,
            'sentiment_score': sentiment_score,
            'sentiment_advice': sentiment_advice,
            'translated_content': translated_content,
            'original_content': original_content,
            "username": request.user.username
        })

class SearchResultsViewVizuelizacija(LoginRequiredMixin,View):
    login_url = 'login-page'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        query = request.GET.get('query')
        results = []

        return render(request, 'app/search_result_page-vizuelizacija.html', {
            'query': query,
            'results': results,
            "username": request.user.username
        })

class SearchResultsViewPredviduvanje(LoginRequiredMixin,View):
    login_url = 'login-page'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        query = request.GET.get('query')
        results = []

        return render(request, 'app/search_result_page-predviduvanje.html', {
            'query': query,
            'results': results,
            "username": request.user.username
        })

class DashboardPageView(LoginRequiredMixin, View):
    login_url = 'login-page'
    redirect_field_name = 'redirect_to'# ovie mora da se navedeni za da redirektne na login-page ako ne e najaven korisnikot

    def get(self, request):
        return render(
            request,
            "app/dashboard_page.html",
            {"username": request.user.username}
        )





class TrainModelView(LoginRequiredMixin, View):
    def get(self, request):
        issuer = request.GET.get('issuer')
        filename = f'data_for_{issuer}.csv'
        return func(filename)


def user_logout(request):

    auth.logout(request)
    return redirect("starting-page")






class get_graph_dataView(View): # za graf na dashboard
    def get(self, request):
        kolku_denovi_unazad = request.GET.get('kolku_denovi_unazad')  # Get the search query from the request
        issuer = request.GET.get('issuer')
        attribute = request.GET.get('attribute', 'Просечна цена')
        return kod_za_generiranje_dijagram(f'data_for_{issuer}.csv',kolku_denovi_unazad,attribute)


class get_table_dataView(View): # za tabela na dashboard
    def get(self, request):
        issuer = request.GET.get('issuer')
        if not issuer:
            return JsonResponse({"error": "Issuer is required"}, status=400)
        try:
            return kod_za_generiranje_tabela(f'data_for_{issuer}.csv')
        except FileNotFoundError:
            return JsonResponse({"error": f"Data file for issuer '{issuer}' not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse
import pandas as pd
import os
from django.conf import settings

class get_card_dataView(View): # za karticki na dashboard
    def get(self, request):
        issuer = request.GET.get('issuer')
        if not issuer:
            return JsonResponse({"error": "Issuer is required"}, status=400)
        return generate_karticki_dashboard(f'data_for_{issuer}.csv')



class AddToFavoritesView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            query = data.get('query')

            if not query:
                return JsonResponse({'error': 'Query is required'}, status=400)

            favorite, created = FavoriteQuery.objects.get_or_create(user=request.user, query=query)
            if not created:
                return JsonResponse({'message': 'Query is already in favorites'}, status=200)

            return JsonResponse({'message': 'Query added to favorites successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON provided'}, status=400)

class GetFavoritesView(View):
    @method_decorator(login_required)
    def get(self, request):
        favorites = FavoriteQuery.objects.filter(user=request.user).values_list('query', flat=True)
        return JsonResponse({'favorites': list(favorites)}, status=200)

class RemoveFromFavoritesView(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            # Parse the JSON payload
            data = json.loads(request.body.decode('utf-8'))
            query = data.get('query')

            if not query:
                return JsonResponse({'error': 'Query is required'}, status=400)

            # Check if the query exists in the user's favorites
            favorite = FavoriteQuery.objects.filter(user=request.user, query=query).first()
            if not favorite:
                return JsonResponse({'error': 'Query not found in favorites'}, status=404)

            # Remove the query from favorites
            favorite.delete()
            return JsonResponse({'message': 'Query removed from favorites successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON provided'}, status=400)


class SearchResultsViewTehnicka(LoginRequiredMixin, TemplateView):
    template_name = "app/search_result_page-tehnicka.html"
    login_url = 'login-page'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get("query", "").upper()
        timeframe = self.request.GET.get("timeframe", "daily")  # Default to daily
        context = super().get_context_data(**kwargs)
        context["query"] = query
        #"username": request.user.username
        context["username"] = self.request.user.username
        context["timeframe"] = timeframe

        # Default summary
        context["summary"] = {
            "oscillators": {"Buy": 0, "Neutral": 0, "Sell": 0},
            "movingAverages": {"Buy": 0, "Neutral": 0, "Sell": 0}
        }
        context["oscillators"] = []
        context["moving_averages"] = []

        # Check if the query (company code) is provided
        if not query:
            context["error"] = "Мора да внесете име на компанија за анализа."
            return context

        # Locate the company CSV
        file_path = os.path.join(settings.BASE_DIR, "data", f"data_for_{query}.csv")
        if not os.path.exists(file_path):
            context["error"] = f"Податоците за компанијата '{query}' не се пронајдени."
            return context

        try:
            # Load and preprocess the CSV
            df = pd.read_csv(file_path)
            df["Датум"] = pd.to_datetime(df["Датум"], format="%d.%m.%Y")
            df["close"] = df["Цена на последна трансакција"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
            df["high"] = df["Мак."].str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
            df["low"] = df["Мин."].str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
            df["volume"] = df["Количина"].astype(int)

            # Filter data for the selected timeframe
            if timeframe == "daily":
                filtered_data = df[df["Датум"] >= df["Датум"].max() - pd.Timedelta(days=30)]
            elif timeframe == "weekly":
                filtered_data = df[df["Датум"] >= df["Датум"].max() - pd.Timedelta(weeks=12)]
            elif timeframe == "monthly":
                filtered_data = df[df["Датум"] >= df["Датум"].max() - pd.Timedelta(days=365)]
            else:
                context["error"] = "Невалидна временска рамка е избрана."
                return context

            if filtered_data.empty:
                context["error"] = "Недоволно податоци за техничка анализа."
                return context

            # Perform technical analysis
            results = []

            def append_indicator(name, value, action):
                """Helper to add indicator results."""
                if pd.isna(value):  # Skip if value is NaN
                    return
                results.append({"Name": name, "Value": round(value, 2), "Action": action})


            # Oscillators
            if len(filtered_data) >= 14:
                # Relative Strength Index (RSI)
                rsi_value = calculate_rsi(filtered_data).iloc[-1]
                rsi_action = "Buy" if rsi_value < 30 else "Sell" if rsi_value > 70 else "Neutral"
                append_indicator("Relative Strength Index (RSI)", rsi_value, rsi_action)

                # Stochastic Oscillator
                stochastic_value = calculate_stochastic(filtered_data).iloc[-1]
                stochastic_action = "Buy" if stochastic_value < 20 else "Sell" if stochastic_value > 80 else "Neutral"
                append_indicator("Stochastic %K", stochastic_value, stochastic_action)
                #cci
                cci_series = calculate_cci(filtered_data)
                if not cci_series.dropna().empty:
                    cci_value = cci_series.dropna().iloc[-1]
                    cci_action = "Buy" if cci_value < -100 else "Sell" if cci_value > 100 else "Neutral"
                    append_indicator("Commodity Channel Index (CCI)", cci_value, cci_action)
                else:
                    print("CCI not calculated due to insufficient or invalid data.")

                # Average Directional Index (ADX)
                adx_series = calculate_adx(filtered_data)
                if not adx_series.dropna().empty:
                    adx_value = adx_series.dropna().iloc[-1]
                    adx_action = "Neutral" if adx_value < 25 else "Buy"
                    append_indicator("Average Directional Index (ADX)", adx_value, adx_action)
                else:
                    print("ADX not calculated due to insufficient or invalid data.")

            # Moving Averages
            if len(filtered_data) >= 10:
                # Simple Moving Average (SMA)
                sma_value = calculate_sma(filtered_data).iloc[-1]
                sma_action = "Buy" if filtered_data["close"].iloc[-1] > sma_value else "Sell"
                append_indicator("Simple Moving Average (SMA)", sma_value, sma_action)

                # Exponential Moving Average (EMA)
                ema_value = calculate_ema(filtered_data).iloc[-1]
                ema_action = "Buy" if filtered_data["close"].iloc[-1] > ema_value else "Sell"
                append_indicator("Exponential Moving Average (EMA)", ema_value, ema_action)

                # Weighted Moving Average (WMA)
                wma_value = calculate_wma(filtered_data).iloc[-1]
                wma_action = "Buy" if filtered_data["close"].iloc[-1] > wma_value else "Sell"
                append_indicator("Weighted Moving Average (WMA)", wma_value, wma_action)

                # Hull Moving Average (HMA)
                hma_value = calculate_hma(filtered_data).iloc[-1]
                hma_action = "Buy" if filtered_data["close"].iloc[-1] > hma_value else "Sell"
                append_indicator("Hull Moving Average (HMA)", hma_value, hma_action)

            # Replace VWAP with Median Price (Typical Price)
            if len(filtered_data) >= 3:  # Smaller data requirement
                typical_price = (filtered_data["high"] + filtered_data["low"] + filtered_data["close"]) / 3
                typical_price_value = typical_price.iloc[-1]
                typical_price_action = "Buy" if filtered_data["close"].iloc[-1] > typical_price_value else "Sell"
                append_indicator("Typical Price (Median Price)", typical_price_value, typical_price_action)

            # Replace Williams %R with Rate of Change (ROC)
            if len(filtered_data) >= 5:  # Requires fewer periods than Williams %R
                roc = (filtered_data["close"].pct_change(periods=4) * 100).iloc[-1]  # Change over 5 periods
                roc_action = "Buy" if roc > 0 else "Sell" if roc < 0 else "Neutral"
                append_indicator("Rate of Change (ROC)", roc, roc_action)

            summary = generate_summary(results)

            context["oscillators"] = [
                r for r in results if r["Name"] in [
                    "Relative Strength Index (RSI)",
                    "Stochastic %K",
                    "Commodity Channel Index (CCI)",
                    "Average Directional Index (ADX)",
                    "Rate of Change (ROC)"
                ]
            ]
            context["moving_averages"] = [
                r for r in results if r["Name"] in [
                    "Simple Moving Average (SMA)",
                    "Exponential Moving Average (EMA)",
                    "Weighted Moving Average (WMA)",
                    "Hull Moving Average (HMA)",
                    "Typical Price (Median Price)"
                ]
            ]

            context["summary"] = summary


        except Exception as e:
            context["error"] = f"Грешка при обработката на податоците: {str(e)}"

        return context
