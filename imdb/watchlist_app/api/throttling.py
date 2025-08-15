from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    """
    Custom throttle class to limit the number of review creation requests.
    This allows a user to create a maximum of 5 reviews per day.
    """
    scope = 'review_create'

    def get_rate(self):
        return '5/day'  # Limit to 5 review creations per day
    

class ReviewListThrottle(UserRateThrottle):
    """
    Custom throttle class to limit the number of review listing requests.
    This allows a user to list reviews a maximum of 10 times per day.
    """
    scope = 'review_list'

    def get_rate(self):
        return '10/day'  # Limit to 10 review listings per day