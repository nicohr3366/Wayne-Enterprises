"""
Generador de reporte HTML de contratos
"""
import json
import os


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_html_report():
    # Obtener rutas
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    output_dir = os.path.join(base_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Cargar datos procesados
    contratos = load_json(os.path.join(processed_dir, 'contratos_parseados.json'))
    analisis_contratos = load_json(os.path.join(processed_dir, 'analisis_contratos.json'))
    licitaciones = load_json(os.path.join(processed_dir, 'licitaciones_transformadas.json'))
    oportunidades = load_json(os.path.join(processed_dir, 'oportunidades_wayne.json'))

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Wayne Defense Contracts Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; margin: 0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ color: #e94560; border-bottom: 3px solid #e94560; padding-bottom: 10px; }}
        h2 {{ color: #3498db; margin-top: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; text-align: center; }}
        .stat-value {{ font-size: 36px; font-weight: bold; color: white; }}
        .stat-label {{ font-size: 14px; opacity: 0.9; margin-top: 5px; color: white; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: #16213e; }}
        th {{ background: #e94560; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #333; }}
        tr:hover {{ background: #1f2d4a; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
        .confidencial {{ background: #f39c12; color: black; }}
        .secreto {{ background: #e74c3c; color: white; }}
        .alto-secreto {{ background: #2c3e50; color: white; border: 1px solid #e74c3c; }}
        .critica {{ background: #e74c3c; color: white; }}
        .alta {{ background: #f39c12; color: black; }}
        .normal {{ background: #27ae60; color: white; }}
        .wayne-yes {{ color: #27ae60; font-weight: bold; }}
        .wayne-no {{ color: #7f8c8d; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Wayne Defense Contracts Dashboard</h1>
        <p>Departamento de Defensa de EE.UU. - Licitaciones y Contratos</p>

        <h2>Resumen General</h2>
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">{analisis_contratos['total_contratos']}</div>
                <div class="stat-label">Contratos Activos</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">${analisis_contratos['monto_total']/1e9:.2f}B</div>
                <div class="stat-label">Valor Total</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">${analisis_contratos['monto_promedio']/1e6:.1f}M</div>
                <div class="stat-label">Promedio por Contrato</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{oportunidades['total_licitaciones']}</div>
                <div class="stat-label">Licitaciones Totales</div>
            </div>
        </div>

        <h2>Contratos Vigentes</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Título</th>
                <th>División</th>
                <th>Contratista</th>
                <th>Monto</th>
                <th>Clasificación</th>
                <th>Estado</th>
            </tr>
"""

    for c in contratos:
        badge_class = c['clasificacion'].lower().replace(' ', '-')
        html += f"""
            <tr>
                <td>{c['id']}</td>
                <td>{c['titulo']}</td>
                <td>{c['division']}</td>
                <td>{c['contratista']}</td>
                <td>${c['monto']:,.0f}</td>
                <td><span class="badge {badge_class}">{c['clasificacion']}</span></td>
                <td>{c['estado']}</td>
            </tr>
"""

    html += """
        </table>

        <h2>Oportunidades de Licitación</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Título</th>
                <th>Agencia</th>
                <th>Monto Estimado</th>
                <th>Estado</th>
                <th>Urgencia</th>
                <th>Wayne</th>
            </tr>
"""

    for lic in licitaciones:
        urgencia_class = lic['urgencia'].lower()
        wayne_class = 'wayne-yes' if lic['wayne_participando'] else 'wayne-no'
        wayne_text = 'Participando' if lic['wayne_participando'] else 'No participa'

        html += f"""
            <tr>
                <td>{lic['id']}</td>
                <td>{lic['titulo']}</td>
                <td>{lic['agencia']}</td>
                <td>${lic['monto_estimado']:,.0f}</td>
                <td>{lic['estado']}</td>
                <td><span class="badge {urgencia_class}">{lic['urgencia']}</span></td>
                <td class="{wayne_class}">{wayne_text}</td>
            </tr>
"""

    html += """
        </table>

        <div style="margin-top: 40px; padding: 20px; background: #16213e; border-radius: 10px;">
            <h3>Análisis por División</h3>
            <ul style="line-height: 2;">
"""

    for div, data in analisis_contratos['por_division'].items():
        html += f"<li><strong>{div}</strong>: {data['count']} contratos, ${data['total']:,.0f}</li>"

    html += """
            </ul>
        </div>

        <p style="margin-top: 40px; color: #7f8c8d; font-size: 12px; text-align: center;">
            Reporte generado automáticamente - Wayne Enterprises Defense Division
        </p>
    </div>
</body>
</html>
"""

    output_path = os.path.join(output_dir, 'dashboard.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Reporte HTML generado: {output_path}")


if __name__ == "__main__":
    generate_html_report()
