import json
from pathlib import Path

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


DATA_DIR = Path(__file__).resolve().parent / 'data'
DATASETS = [
    ('red_electrica', 'wayne_red_electrica_gotham_5000.xlsx'),
    ('logistica', 'wayne_logistica_shipping_5000.xlsx'),
]


def _safe_numeric_summary(df):
    numeric_cols = [c for c in df.select_dtypes(include='number').columns if c]
    if not numeric_cols:
        return {'total': 0, 'columns': [], 'top_values': []}

    summary = []
    for col in numeric_cols[:4]:
        s = pd.to_numeric(df[col], errors='coerce').dropna()
        summary.append({
            'column': col,
            'total': float(s.sum()) if not s.empty else 0,
            'avg': float(s.mean()) if not s.empty else 0,
            'max': float(s.max()) if not s.empty else 0,
            'min': float(s.min()) if not s.empty else 0,
        })
    return {'total': len(numeric_cols), 'columns': numeric_cols, 'top_values': summary}


def _safe_categorical_summary(df):
    text_cols = [c for c in df.columns if df[c].dtype == 'object' or pd.api.types.is_string_dtype(df[c])]
    if not text_cols:
        return {'columns': [], 'top_values': []}

    top_values = []
    for col in text_cols[:4]:
        counts = df[col].fillna('Sin dato').astype(str).value_counts().head(6)
        top_values.append({
            'column': col,
            'items': [{'label': str(k), 'value': int(v)} for k, v in counts.items()],
        })
    return {'columns': text_cols, 'top_values': top_values}


def _load_dataset(name, filename):
    path = DATA_DIR / filename
    if not path.exists():
        return {'name': name, 'file': filename, 'available': False, 'error': 'Archivo no encontrado.'}

    try:
        df = pd.read_excel(path, sheet_name=0)
        df = df.rename(columns=lambda c: str(c).strip())
        numeric = _safe_numeric_summary(df)
        categories = _safe_categorical_summary(df)
        return {
            'name': name,
            'file': filename,
            'available': True,
            'rows': int(len(df)),
            'columns': int(len(df.columns)),
            'sheets': pd.ExcelFile(path).sheet_names,
            'numeric': numeric,
            'categories': categories,
            'sample_columns': list(df.columns[:8]),
            'preview': df.head(5).to_dict(orient='records'),
        }
    except Exception as exc:
        return {'name': name, 'file': filename, 'available': False, 'error': str(exc)}


def home(request):
    return render(request, 'industries/home.html')


@login_required
def dashboard(request):
    datasets = [_load_dataset(name, filename) for name, filename in DATASETS]
    context = {
        'datasets': datasets,
        'red_dataset': datasets[0],
        'shipping_dataset': datasets[1],
        'datasets_json': json.dumps(datasets),
    }
    return render(request, 'industries/dashboard.html', context)
