# google_analytics_data_download_api
A bit optimized way of downloading Google Analytics data to excel spreadsheet.
Most of the source code comes from Google Analytics API documentation: https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py

How to get authorization?
1. Log in to Google Cloud Platform.
2. Go to APIs & Services. From Library enable Google Analytics API.
3. Go to IAM & Admin > Service accounts. Create new service account.
4. Click on Actions button > Manage Keys. Generate and download new key using ADD KEY. Please remember to keep it safe on your device.
5. Go back to Service Accounts and copy generated service email. Now you have to add that e-mail address to your Google Analytics view as user as least with Read credentials.
 

Tip 1. If you want to check the possibility of mixing specific dimensions and metrics, you can check it in the request composer: https://ga-dev-tools.web.app/request-composer/
