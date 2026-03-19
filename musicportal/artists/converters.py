class YearRangeConverter:
    regex = r'\d{4}\s*-\s*(?:present|\d{4})'

    def to_python(self, value):
        parts = value.split('-')
        start_year = int(parts[0].strip())
        end_part = parts[1].strip()

        if end_part.lower() == 'present':
            end_year = None
        else:
            end_year = int(end_part)

        return {
            'start': start_year,
            'end': end_year,
            'is_present': end_year is None,
            'display': f"{start_year} - {'present' if end_year is None else end_year}"
        }

    def to_url(self, value):
        if isinstance(value, dict):
            if value.get('is_present'):
                return f"{value['start']} - present"
            return f"{value['start']} - {value['end']}"
        return str(value)