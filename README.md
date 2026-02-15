# Receipt_Analyzer-with-LLM

AI Receipt Analyzer (Blurry Images Supported)

“Analyze your receipts quickly and get actionable insights even from blurry images.”

Overview

AI Receipt Analyzer is a Streamlit-based app that extracts information from receipt images, categorizes expenses, calculates totals, visualizes spending, and provides AI-generated financial advice.

This tool is perfect for tracking spending, budgeting, and quickly understanding your purchases without manually entering data.

Features

Upload receipt images (JPG/PNG)

OCR text extraction (works even for blurry images)

Structured table of items, prices, and categories

Totals per category and overall spending

Spending chart visualization

AI-powered financial insights and budgeting suggestions

Professional summary of spending at a glance

Demo

You can see the uploaded receipt, extracted data, totals, and AI insights directly in the Streamlit app.

Installation

Clone this repository:

git clone https://github.com/yourusername/ai-receipt-analyzer.git
cd ai-receipt-analyzer


Install required packages:

pip install -r requirements.txt


Replace the Gemini AI key in app.py:

client = genai.Client(api_key="YOUR_GEMINI_API_KEY_HERE")


Run the app:

streamlit run app.py

Usage

Open the Streamlit app in your browser.

Upload a receipt image (JPG, PNG, JPEG).

Wait for the AI to process the image.

View:

Extracted items and prices

Categorized totals

Spending chart

AI financial insights

Summary of your spending

Requirements

Python 3.10+

Streamlit

PIL (Pillow)

pandas

matplotlib

google-genai (for Gemini AI)

base64, io, json, re (built-in)

How It Works

Upload Receipt: User uploads an image via Streamlit.

AI OCR: Gemini AI extracts items, prices, and categories from the receipt (even blurry images).

Data Structuring: Extracted JSON is converted to a table and categorized.

Visualization: Spending per category is shown in a bar chart.

AI Insights: Gemini AI generates recommendations for saving and budgeting.

Summary: Shows total spending, top category, and number of items.

License

This project is open-source and free to use under the MIT License.

Contact

Developed by kiran Hamza
