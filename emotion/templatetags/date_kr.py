from django import template
from datetime import datetime

register = template.Library()

@register.filter
def date_kr(value):
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return value
    days = {
        'Monday': '월',
        'Tuesday': '화',
        'Wednesday': '수',
        'Thursday': '목',
        'Friday': '금',
        'Saturday': '토',
        'Sunday': '일',
    }
    return days.get(value.strftime('%A'), '')
