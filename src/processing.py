def filter_by_state(data, state='EXECUTED'):
    """
    фильтрует список словарей по значению ключа 'state'.
    """
    return [item for item in data if item.get('state') == state]


def sort_by_date(data, descending=True):
    """
    сортирует список словарей по ключу 'date'.
    """
    return sorted(data, key=lambda x: x.get('date'), reverse=descending)