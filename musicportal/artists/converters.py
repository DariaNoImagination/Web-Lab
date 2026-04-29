class YearRangeConverter:
    regex = r'\d{4}\s*-\s*(?:present|\d{4})'

    def to_python(self, value):
        print(f"DEBUG to_python: {value}")  # Отладка
        parts = value.split('-')
        start_year = int(parts[0].strip())
        end_part = parts[1].strip()

        if end_part.lower() == 'present':
            end_year = None
            is_present = True
        else:
            end_year = int(end_part)
            is_present = False

        result = {
            'start': start_year,
            'end': end_year,
            'is_present': is_present,
            'display': f"{start_year}-{'present' if is_present else end_year}"
        }
        print(f"DEBUG to_python result: {result}")
        return result

    def to_url(self, value):
        if isinstance(value, dict):
            if value.get('is_present'):
                return f"{value['start']} - present"
            return f"{value['start']} - {value['end']}"
        return str(value)