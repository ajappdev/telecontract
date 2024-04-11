# create the register instance by initializing it with the Library instance.
from django import template
from django.utils.safestring import mark_safe
from datetime import date
from dateutil import parser

import locale
locale.setlocale(locale.LC_ALL, '')

register = template.Library()


@register.filter(name='sign')
def sign(value):
    if value == "" or value is None:
        return ""
    try:
        val = float(value.replace(',', '.'))
    except Exception:
        val = value
    if val > 0:
        safe_text = f'<span class="badge badge-success-light" style="color: #1fbb72;"> <i class="mdi mdi-arrow-bottom-right"></i> +{round(val, 2)}% </span>'
        return mark_safe(safe_text)
    elif val < 0:
        safe_text = f'<span class="badge badge-danger-light" style="color: #e72626;"> <i class="mdi mdi-arrow-bottom-right"></i> {round(val, 2)}% </span>'
        return mark_safe(safe_text)
    else:
        return ""


@register.filter(name='interne_externe')
def interne_externe(value):
    if value == "Externe":
        safe_text = f'<label class="label label-primary">Externe</label>'
        return mark_safe(safe_text)
    else:
        safe_text = f'<label class="label label-warning">Interne</label>'
        return mark_safe(safe_text)


@register.filter(name='valeur_jours')
def valeur_jours(value):
    if value <= 1:
        safe_text = f'{value} <span class="text-muted text-little"> jour</span>'
        return mark_safe(safe_text)
    elif value > 1:
        safe_text = f'{value} <span class="text-muted text-little"> jours</span>'
        return mark_safe(safe_text)


@register.filter(name='statut_conge')
def statut_conge(value):
    if value == "En attente":
        safe_text = f'<label class="label label-warning">En attente</label>'
        return mark_safe(safe_text)
    elif value == "Acceptée":
        safe_text = f'<label class="label label-success">Acceptée</label>'
        return mark_safe(safe_text)
    elif value == "Refusée":
        safe_text = f'<label class="label label-danger">Refusée</label>'
        return mark_safe(safe_text)


@register.filter(name='sign_inv')
def sign_inv(value):
    if value == "" or value is None:
        return ""
    try:
        val = float(value.replace(',', '.'))
    except Exception:
        val = value
    if val < 0:
        safe_text = f'<span class="badge badge-success-light" style="color: #1fbb72;"> <i class="mdi mdi-arrow-bottom-right"></i> {round(val, 2)}% </span>'
        return mark_safe(safe_text)
    elif val > 0:
        safe_text = f'<span class="badge badge-danger-light" style="color: #e72626;"> <i class="mdi mdi-arrow-bottom-right"></i> +{round(val, 2)}% </span>'
        return mark_safe(safe_text)
    else:
        return ""


@register.filter(name='nok_ok')
def nok_ok(value):

    if value == "OK":
        safe_text = f'<span class="badge badge-success-light" style="color: #1fbb72;"> <i class="mdi mdi-arrow-bottom-right"></i> {value} </span>'
        return mark_safe(safe_text)
    else:
        safe_text = f'<span class="badge badge-danger-light" style="color: #e72626;"> <i class="mdi mdi-arrow-bottom-right"></i> {value} </span>'
        return mark_safe(safe_text)


@register.filter(name='value_prc')
def value_prc(value):
    if value >= 0:
        return mark_safe(f'<span class="badge bg-primary">+{round(value)}% </span>')
    else:
        return mark_safe(f'<span class="badge bg-primary">{round(value)}% </span>')


@register.filter(name='etat_data_date')
def etat_data_date(value):

    try:
        jour = parser.parse(str(value)).date()
    except Exception:
        jour = parser.parse(str("1970-01-01")).date()

    if jour == date.today():
        safe_text = f'<span class="badge bg-success">{str(jour)[0:16]}</span>'
        return mark_safe(safe_text)
    elif jour < date.today() and jour != parser.parse(str("1970-01-01")).date():
        safe_text = f'<span class="badge bg-warning">{str(jour)[0:16]}</span>'
        return mark_safe(safe_text)
    else:
        safe_text = '<span class="badge bg-danger">NA</span>'
        return mark_safe(safe_text)


@register.filter(name='etat_data_datetime')
def etat_data_datetime(value):

    try:
        jour = parser.parse(str(value)).date()
    except Exception:
        jour = parser.parse(str("1970-01-01")).date()

    if jour == date.today():
        safe_text = f'<span class="badge bg-success">{str(value)[0:16]}</span>'
        return mark_safe(safe_text)
    elif jour < date.today() and jour != parser.parse(str("1970-01-01")).date():
        safe_text = f'<span class="badge bg-warning">{str(value)[0:16]}</span>'
        return mark_safe(safe_text)
    else:
        safe_text = '<span class="badge bg-danger">NA</span>'
        return mark_safe(safe_text)