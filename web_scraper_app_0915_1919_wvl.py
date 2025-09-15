# 代码生成时间: 2025-09-15 19:19:59
# web_scraper_app
# Django application for scraping web content

"""
Web Scraper Application
==========================
This Django application provides a simple web content scraping tool.
Features include:
- Models for storing scraped data
- Views for handling scraping requests
- URLs for routing scraping requests
- Error handling and documentation

Usage:
- Install Django and create a new project
- Add this application to your Django project
- Implement the scraping logic in views.py
- Handle errors and exceptions
- Test the application

Authors:
- Your Name
"""

# Import necessary Django modules
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.views import View
from django.views.decorators.http import require_http_methods

# Import external libraries for web scraping
import requests
from bs4 import BeautifulSoup

# Define the ScrapedData model
class ScrapedData(models.Model):
    """Model for storing scraped data"""
    url = models.URLField(unique=True)
    data = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Scraped data from {self.url}"

# Define the ScraperView
class ScraperView(View):
    """
    View for handling scraping requests

    This view takes a URL as input, scrapes the content,
    and stores it in the database.
    """

    @require_http_methods(["GET"])
    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET requests to scrape web content"""
        url = request.GET.get("url")

        # Validate the input URL
        if not url:
            return HttpResponse("URL is required", status=400)

        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.prettify()  # Get the prettified HTML content

            # Store the scraped data in the database
            ScrapedData.objects.create(url=url, data=data)
            return HttpResponse("Scraped data stored successfully", status=200)

        except requests.exceptions.RequestException as e:
            # Handle request-related errors
            return HttpResponse(f"Request error: {e}