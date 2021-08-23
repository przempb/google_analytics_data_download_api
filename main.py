#TODO: CLEAN AND COMMENT FILE

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials #you may need to use pip install --upgrade google-api-python-client oauth2client
import pandas as pd


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'credentials.json' #deliver your credentials.json file from Google Cloud Platrofm IAM - more info about authorization in readme file
VIEW_ID = 'PASS HERE YOUR GOOGLE ANALYTICS VIEW ID'



def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  report = analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID, #HERE YOU PASS SPECIFIC METRICS AND DIMENSIONS YOU ARE INTERESTED IN
          'dateRanges': [{'startDate': '2021-04-01', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:totalValue'},
                      # {'expression': 'ga:transactionRevenue'},
                      ],
          'dimensions': [{"name": "ga:date"},
                         {'name': 'ga:sourceMedium'},
                         {"name": "ga:transactionId"},],
          # 'orderBys': [{"fieldName": "ga:totalValue", "sortOrder": "DESCENDING"}],
          'pageSize': 1000
        }]
      }
  ).execute()
  dimensions = report['reports'][0]['columnHeader']['dimensions']
  metrics = report['reports'][0]['columnHeader']['metricHeader']['metricHeaderEntries']
  metrics_headers = []
  for names in metrics:
      name = names['name']
      metrics_headers.append(name)
  merged_headers = dimensions + metrics_headers

  return report, merged_headers


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
  for report in response.get('reports', []):
    listofrows = []
    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])
      values = dateRangeValues[0]["values"]
      rows = dimensions + values
      listofrows.append(rows)
    return listofrows


def main():
  analytics = initialize_analyticsreporting()
  response, dimensions = get_report(analytics)
  analytics_raw_data = print_response(response)
  df = pd.DataFrame(analytics_raw_data, columns=dimensions)
  df.to_excel("analytics_report.xlsx")


if __name__ == '__main__':
  main()
