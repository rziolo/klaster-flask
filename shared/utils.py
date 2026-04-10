# /var/www/html/flask/shared/utils.py

def format_pl(value):
    """Formatowanie liczby na format: 123 456,78"""
    if value is None: return "0,00"
    try:
        # Formatowanie z odstępem tysięcznym i przecinkiem
        return "{:,.2f}".format(float(value)).replace(",", " ").replace(".", ",").replace(" ", " ")
    except (ValueError, TypeError):
        return value

# EOF
