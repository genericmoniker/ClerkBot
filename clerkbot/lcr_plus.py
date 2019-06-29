from datetime import datetime
from lcr import API as LCR, LCR_DOMAIN

LCRF_DOMAIN = 'lcrf.churchofjesuschrist.org'


class API(LCR):
    def ward_mission_report(self):
        year = datetime.now().year
        account_id = '14685'  # TODO: How to get internalAccountId?!!

        request = {
            'url': f'https://{LCRF_DOMAIN}/finance/income-expenses',
            'params': {
                'fromDate': f'{year}-01-01',
                'toDate': f'{year}-12-31',
                'internalAccountId': account_id,
            },
        }
        result = self._make_request(request)
        data = result.json()
        for category in data:
            if category['categoryName'] == 'Ward Missionary Fund':
                return category
        raise Exception('Ward Mission Fund not found!')

    def quarterly_report_potential_streaming(self, line, year, quarter):
        request = {
            'url': f'https://{LCR_DOMAIN}/report/quarterly-report-details-print',
            'params': {
                'pdf': 'true',
                'lang': 'eng',
                'rowNumber': line,
                'unitNumber': self.unit_number,
                'showAge': 'false',
                'year': year,
                'quarter': quarter,
                'filter': 'POTENTIAL',
                'sort': 'nameOrder',
            },
            'stream': True,
        }
        return self._make_request(request)
