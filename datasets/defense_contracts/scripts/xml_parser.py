"""
Parser de contratos XML del Departamento de Defensa
"""
import xml.etree.ElementTree as ET
import json
import os


def parse_xml_contratos(filepath):
    """
    Parsea archivo XML de contratos y retorna lista de diccionarios
    """
    tree = ET.parse(filepath)
    root = tree.getroot()

    contratos = []

    for contrato_elem in root.findall('Contrato'):
        contrato = {
            'id': contrato_elem.get('id'),
            'agencia': contrato_elem.find('Agencia').text,
            'division': contrato_elem.find('División').text,
            'titulo': contrato_elem.find('Titulo').text,
            'contratista': contrato_elem.find('Contratista').text,
            'monto': float(contrato_elem.find('Monto').text),
            'moneda': contrato_elem.find('Moneda').text,
            'fecha_inicio': contrato_elem.find('FechaInicio').text,
            'fecha_fin': contrato_elem.find('FechaFin').text,
            'estado': contrato_elem.find('Estado').text,
            'clasificacion': contrato_elem.find('Clasificacion').text,
            'ubicacion': contrato_elem.find('Ubicacion').text
        }
        contratos.append(contrato)

    return contratos


def save_to_json(data, filepath):
    """Guarda datos en formato JSON"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Guardados {len(data)} registros en {filepath}")


def analyze_contratos(contratos):
    """Genera análisis de contratos"""

    total_monto = sum(c['monto'] for c in contratos)

    # Por división
    por_division = {}
    for c in contratos:
        div = c['division']
        if div not in por_division:
            por_division[div] = {'count': 0, 'total': 0}
        por_division[div]['count'] += 1
        por_division[div]['total'] += c['monto']

    # Por clasificación
    por_clasificacion = {}
    for c in contratos:
        cla = c['clasificacion']
        if cla not in por_clasificacion:
            por_clasificacion[cla] = {'count': 0, 'total': 0}
        por_clasificacion[cla]['count'] += 1
        por_clasificacion[cla]['total'] += c['monto']

    return {
        'total_contratos': len(contratos),
        'monto_total': total_monto,
        'monto_promedio': total_monto / len(contratos) if contratos else 0,
        'por_division': por_division,
        'por_clasificacion': por_clasificacion
    }


if __name__ == "__main__":
    print("=" * 60)
    print("PARSER XML - Contratos de Defensa")
    print("=" * 60)

    # Obtener ruta base relativa a este script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Parsear XML
    xml_path = os.path.join(base_dir, 'data', 'raw', 'contratos.xml')
    contratos = parse_xml_contratos(xml_path)

    print(f"\nContratos parseados: {len(contratos)}")

    for c in contratos:
        print(f"\n   {c['id']}")
        print(f"      {c['titulo']}")
        print(f"      Contratista: {c['contratista']}")
        print(f"      Monto: ${c['monto']:,.2f}")
        print(f"      División: {c['division']}")

    # Análisis
    analisis = analyze_contratos(contratos)

    print(f"\nResumen Financiero:")
    print(f"   Total contratos: {analisis['total_contratos']}")
    print(f"   Monto total: ${analisis['monto_total']:,.2f}")
    print(f"   Monto promedio: ${analisis['monto_promedio']:,.2f}")

    print(f"\nPor División:")
    for div, data in analisis['por_division'].items():
        print(f"   {div}: {data['count']} contratos, ${data['total']:,.2f}")

    # Guardar como JSON
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    save_to_json(contratos, os.path.join(processed_dir, 'contratos_parseados.json'))
    save_to_json(analisis, os.path.join(processed_dir, 'analisis_contratos.json'))
