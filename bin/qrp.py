# -*- coding: utf-8 -*-

"""Script for downloading the "potential" reports for use in compiling the ward
quarterly report. The downloaded PDFs can be sent to the appropriate
organization secretaries so that they can compare their records with the
current headquarters records.

Output is written to '~/Clerk', in a subdirectory named for the quarter.
"""


from clerk.quarterly_report import download_potential_reports

download_potential_reports()
