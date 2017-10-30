import pytz
import datetime


class DateHandler:

    @staticmethod
    def get_datetime_now():
        datestring = str(
            datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        unaware_dat = datetime.datetime.utcnow().strptime(datestring, "%Y-%m-%d %H:%M:%S")
        localtz = pytz.timezone('UTC')
        aware_est = localtz.localize(unaware_dat)
        ber = pytz.timezone("Europe/Berlin")
        return aware_est.astimezone(ber)
