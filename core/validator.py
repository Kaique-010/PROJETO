import re
from django.core.exceptions import ValidationError

def validate_cnpj(value):
    cnpj_pattern = r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$'
    if not re.match(cnpj_pattern, value):
        raise ValidationError('CNPJ inválido')
