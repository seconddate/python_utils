import datetime

class TimeUtils:

    def get_now_string(self):
        now = datetime.datetime.now()
        today = now.strftime('%Y-%m-%d %H:%M')

        return today

    def get_today_string(self):
        now = datetime.datetime.now()
        today = now.strftime('%Y%m%d_%H%M')

        return today
    
    def get_year_month_string(self):
        now = datetime.datetime.now()
        today = now.strftime('%Y%m')

        return today

    def get_timestamp_string(self):
        now = datetime.datetime.now()
        today = now.strftime('%Y%m%d%H%M%S%f')

        return today