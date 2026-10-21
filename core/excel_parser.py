# core/excel_parser.py
import pandas as pd
from datetime import datetime

def parse_expiry_excel(file_path: str) -> list[dict]:
    df = pd.read_excel(file_path)
    
    # Регистронезависимый поиск колонок
    cols = {str(c).lower(): c for c in df.columns}
    
    name_col = next((v for k, v in cols.items() if 'наимен' in k or 'товар' in k), None)
    expiry_col = next((v for k, v in cols.items() if 'годен' in k or 'срок' in k or 'exp' in k), None)
    
    if not name_col or not expiry_col:
        raise ValueError("Не найдены колонки с названием или сроком годности")
    
    # Парсим даты, невалидные отбрасываем
    df['_expiry'] = pd.to_datetime(df[expiry_col], errors='coerce', dayfirst=True)
    df = df.dropna(subset=['_expiry', name_col])
    
    # Сортируем: сначала самые горящие
    df = df.sort_values('_expiry')
    
    today = pd.Timestamp.now().normalize()
    result = []
    for _, row in df.iterrows():
        days_left = (row['_expiry'] - today).days
        result.append({
            'name': str(row[name_col]),
            'expiry_date': row['_expiry'].date(),
            'days_left': days_left
        })
    return result
