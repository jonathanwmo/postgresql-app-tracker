from datetime import datetime

class Application:
    """A class for applications"""

    def __init__(
            self,
            company,
            progress="Applied",
            interview_status=None,
            apply_date=datetime.now(),
            response_date=None,
            listing_link=None,
            contacts=None,
            notes=None):
        self.company = company
        self.progress = progress
        self.interview_status = interview_status
        self.apply_date = apply_date
        self.response_date = response_date
        self.listing_link = listing_link
        self.contacts = contacts
        self.notes = notes

    def __str__(self):
        return "Application tracker for {}, " \
               "applied on {}".format(
            self.company, self.apply_date)
