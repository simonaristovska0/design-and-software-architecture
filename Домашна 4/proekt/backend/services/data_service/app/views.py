import requests
from bs4 import BeautifulSoup
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.http import HttpResponse
import pandas as pd


class MarketSummaryAPIView(APIView):
    """
    API endpoint to scrape market summary data.
    """

    def get(self, request, *args, **kwargs):
        url = "https://www.mse.mk/"  # Replace with the correct URL
        try:
            # Fetch the HTML content
            response = requests.get(url)
            response.raise_for_status()

            # Parse the HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Locate the table
            table = soup.find("table", class_="table table-bordered table-condensed table-striped market-summary")
            if not table:
                raise APIException("Market summary table not found on the page.")

            # Extract table rows
            rows = table.find("tbody").find_all("tr")

            # Extract data
            table_data = []
            for row in rows:
                columns = row.find_all("td")
                if len(columns) == 2:  # Ensure the row has two columns
                    key = columns[0].text.strip()  # First column
                    value = columns[1].text.strip()  # Second column
                    table_data.append({"Field": key, "Value": value})


            # Debugging: print the data structure to understand it
            print(type(table_data))  # Should print <class 'list'>
            print(table_data)  # Inspect the data

            return Response({"status": "success", "data": table_data})

        except Exception as e:
            raise APIException(f"Error scraping market summary: {str(e)}")


class ScrapeTableView(APIView):
    """
    API endpoint to scrape table data from the MSE website.
    """

    def get(self, request, *args, **kwargs):
        url = "https://www.mse.mk/"
        try:
            # Send GET request
            response = requests.get(url)
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", class_="table table-bordered table-condensed table-striped")
            if not table:
                raise APIException("Table not found on the page.")

            # Extract headers
            headers = [th.text.strip() for th in table.find_all("th")]

            # Extract rows
            rows = []
            for row in table.find_all("tr")[1:]:  # Skip the header row
                cols = [td.text.strip() for td in row.find_all("td")]
                rows.append(cols)

            # Convert to a DataFrame
            df = pd.DataFrame(rows, columns=headers)

            # Convert to list of dictionaries
            data = df.to_dict(orient="records")

            # Debugging: print the data structure to understand it
            print(type(data))  # Should print <class 'list'>
            print(data)  # Inspect the data

            # Return data as JSON
            return Response(data)

        except Exception as e:
            raise APIException(f"An error occurred: {e}")

    def post(self, request, *args, **kwargs):
        """
        Endpoint to download the table as a CSV file.
        """
        url = "https://www.mse.mk/"
        try:
            # Send GET request
            response = requests.get(url)
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", class_="table table-bordered table-condensed table-striped")
            if not table:
                raise APIException("Table not found on the page.")

            # Extract headers
            headers = [th.text.strip() for th in table.find_all("th")]

            # Extract rows
            rows = []
            for row in table.find_all("tr")[1:]:  # Skip the header row
                cols = [td.text.strip() for td in row.find_all("td")]
                rows.append(cols)

            # Convert to a DataFrame
            df = pd.DataFrame(rows, columns=headers)

            # Save as CSV
            csv_file = "mse_table.csv"
            df.to_csv(csv_file, index=False, encoding="utf-8-sig")

            # Serve the CSV file as a response
            with open(csv_file, "rb") as f:
                response = HttpResponse(f.read(), content_type="text/csv")
                response["Content-Disposition"] = f'attachment; filename="{csv_file}"'
                return response

        except Exception as e:
            raise APIException(f"An error occurred: {e}")


class ScrapeSEINetNewsView(APIView):
    """
    API endpoint to scrape SEI-Net news data.
    """

    def get(self, request, *args, **kwargs):
        """
        Fetch the SEI-Net news and return it as JSON.
        """
        url = "https://www.mse.mk/"  # Replace with the correct URL
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            news_section = soup.find("div", class_="seiNetNews")
            news_items = news_section.find_all("li", class_="flex-item-3x4") if news_section else []

            # Extract news data
            news_data = []
            for news_item in news_items:
                try:
                    news_text_tag = news_item.find("h4")
                    full_text = news_text_tag.text.strip() if news_text_tag else None
                    if full_text:
                        news_data.append(full_text)
                except Exception as e:
                    print(f"Error processing news item: {e}")
                    continue

            if not news_data:
                raise APIException("No news data found.")

            return Response({"news": news_data})

        except Exception as e:
            raise APIException(f"An error occurred: {e}")

    def post(self, request, *args, **kwargs):
        """
        Fetch the SEI-Net news and return it as a downloadable CSV file.
        """
        url = "https://www.mse.mk/"  # Replace with the correct URL
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            news_section = soup.find("div", class_="seiNetNews")
            news_items = news_section.find_all("li", class_="flex-item-3x4") if news_section else []

            # Extract news data
            news_data = []
            for news_item in news_items:
                try:
                    news_text_tag = news_item.find("h4")
                    full_text = news_text_tag.text.strip() if news_text_tag else None
                    if full_text:
                        news_data.append(full_text)
                except Exception as e:
                    print(f"Error processing news item: {e}")
                    continue

            if not news_data:
                raise APIException("No news data found.")

            # Save to CSV
            csv_file = "sei_net_news_only.csv"
            with open(csv_file, mode="w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["News"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in news_data:
                    writer.writerow({"News": item})

            # Serve the CSV file as a response
            with open(csv_file, "rb") as f:
                response = HttpResponse(f.read(), content_type="text/csv")
                response["Content-Disposition"] = f'attachment; filename="{csv_file}"'
                return response

        except Exception as e:
            raise APIException(f"An error occurred: {e}")
