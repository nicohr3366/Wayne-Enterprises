"""
Transformador de licitaciones JSON
"""
import json
import os
from datetime import datetime


def load_licitaciones(filepath):
    """Carga archivo JSON de licitaciones"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('licitaciones', [])


def transform_licitaciones(licitaciones):
    """Transforma y enriquece datos de licitaciones"""
    transformadas = []

    for lic in licitaciones:
        # Calcular días restantes
        fecha_cierre = datetime.strptime(lic['fecha_cierre'], '%Y-%m-%d')
        hoy = datetime.now()
        dias_restantes = (fecha_cierre - hoy).days

        # Determinar urgencia
        if dias_restantes < 0:
            urgencia = 'Cerrada'
        elif dias_restantes <= 7:
            urgencia = 'Crítica'
        elif dias_restantes <= 30:
            urgencia = 'Alta'
        else:
            urgencia = 'Normal'

        # Calcular competencia (número de postores)
        num_postores = len(lic.get('postores', []))

        transformed = {
            'id': lic['id'],
            'titulo': lic['titulo'],
            'agencia': lic['agencia'],
            'monto_estimado': lic['monto_estimado'],
            'estado': lic['estado'],
            'dias_restantes': dias_restantes,
            'urgencia': urgencia,
            'numero_postores': num_postores,
            'competencia': 'Alta' if num_postores > 2 else 'Media' if num_postores > 1 else 'Baja',
            'wayne_participando': any('Wayne' in p for p in lic.get('postores', [])),
            'requisitos_count': len(lic.get('requisitos', [])),
            'categoria': categorizar_licitacion(lic['titulo'])
        }

        transformadas.append(transformed)

    return transformadas


def categorizar_licitacion(titulo):
    """Categoriza licitación por palabras clave"""
    titulo_lower = titulo.lower()

    if any(word in titulo_lower for word in ['energía', 'power', 'eléctrico']):
        return 'Energía'
    elif any(word in titulo_lower for word in ['ia', 'inteligencia', 'software', 'ciber']):
        return 'Tecnología/Software'
    elif any(word in titulo_lower for word in ['vehículo', 'automotriz', 'transporte']):
        return 'Transporte'
    elif any(word in titulo_lower for word in ['comunicación', 'radio', 'satélite']):
        return 'Comunicaciones'
    else:
        return 'Otros'


def analyze_opportunities(licitaciones):
    """Analiza oportunidades para Wayne"""

    oportunidades_wayne = [l for l in licitaciones if l['wayne_participando']]
    abiertas = [l for l in licitaciones if l['estado'] == 'Abierta']

    # Por urgencia
    criticas = [l for l in licitaciones if l['urgencia'] == 'Crítica']

    return {
        'total_licitaciones': len(licitaciones),
        'wayne_participando': len(oportunidades_wayne),
        'licitaciones_abiertas': len(abiertas),
        'oportunidades_criticas': len(criticas),
        'oportunidades_wayne': oportunidades_wayne,
        'montos_potenciales': sum(l['monto_estimado'] for l in oportunidades_wayne)
    }


def save_transformed(data, filepath):
    """Guarda datos transformados"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Guardado: {filepath}")


if __name__ == "__main__":
    print("=" * 60)
    print("TRANSFORMADOR JSON - Licitaciones")
    print("=" * 60)

    # Obtener ruta base
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Cargar
    json_path = os.path.join(base_dir, 'data', 'raw', 'licitaciones.json')
    licitaciones = load_licitaciones(json_path)
    print(f"\nLicitaciones cargadas: {len(licitaciones)}")

    # Transformar
    transformadas = transform_licitaciones(licitaciones)

    print(f"\nDatos transformados:")
    for lic in transformadas:
        print(f"\n   {lic['id']}")
        print(f"      {lic['titulo']}")
        print(f"      Monto: ${lic['monto_estimado']:,.0f}")
        print(f"      Urgencia: {lic['urgencia']} ({lic['dias_restantes']} días)")
        print(f"      Wayne participando: {'Sí' if lic['wayne_participando'] else 'No'}")

    # Análisis
    analisis = analyze_opportunities(transformadas)

    print(f"\nOportunidades para Wayne:")
    print(f"   Total licitaciones: {analisis['total_licitaciones']}")
    print(f"   Wayne participando: {analisis['wayne_participando']}")
    print(f"   Abiertas: {analisis['licitaciones_abiertas']}")
    print(f"   Críticas: {analisis['oportunidades_criticas']}")
    print(f"   Monto potencial: ${analisis['montos_potenciales']:,.0f}")

    # Guardar
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    save_transformed(transformadas, os.path.join(processed_dir, 'licitaciones_transformadas.json'))
    save_transformed(analisis, os.path.join(processed_dir, 'oportunidades_wayne.json'))
