import pandas as pd
import numpy as np
import os

# Ruta del archivo CSV
csv_path = os.path.join(os.path.dirname(__file__), 'WayneTech_Satellite_ErrorLogs.csv')

# Cargar el dataset
print("📥 Cargando dataset...")
df = pd.read_csv(csv_path)

print(f"Total de registros: {len(df)}")
print(f"Total de columnas: {len(df.columns)}")

# ============================================================================
# 1. LIMPIAR ESPACIOS EN BLANCO (LEADING/TRAILING)
# ============================================================================
print("\n🧹 Limpiando espacios en blanco...")
for col in df.columns:
    if df[col].dtype == 'object':  # Solo columnas de texto
        df[col] = df[col].str.strip()

# ============================================================================
# 2. NORMALIZAR VALORES DE SEVERIDAD
# ============================================================================
print("\n🔴 Normalizando severidades...")
severity_map = {
    'CRITICAL': 'CRITICAL',
    'CRITICALCRITICAL': 'CRITICAL',
    'HIGH': 'HIGH',
    'HIGHHIGH': 'HIGH',
    'high': 'HIGH',
    'MEDIUM': 'MEDIUM',
    'MEDIUMMEDIUM': 'MEDIUM',
    'medium': 'MEDIUM',
    'LOW': 'LOW',
    'LOWLOW': 'LOW',
    'low': 'LOW',
    '0': 'LOW',
    'N/A': 'MEDIUM',
    np.nan: 'MEDIUM'
}
df['severity'] = df['severity'].fillna('MEDIUM')
df['severity'] = df['severity'].replace(severity_map)
# Eliminar cualquier espacios residuales
df['severity'] = df['severity'].str.upper().str.strip()

# ============================================================================
# 3. NORMALIZAR IDS DE SATÉLITES
# ============================================================================
print("\n🛰️  Normalizando IDs de satélites...")
df['satellite_id'] = df['satellite_id'].str.upper()
# Reemplazar valores inválidos
invalid_sat_ids = ['0', 'N/A']
for idx, row in df.iterrows():
    if df.at[idx, 'satellite_id'] in invalid_sat_ids or pd.isna(df.at[idx, 'satellite_id']):
        # Usar el satellite_name para deducir el ID
        sat_name = df.at[idx, 'satellite_name']
        if 'Relay Alpha' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-001'
        elif 'Relay Beta' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-002'
        elif 'Relay Gamma' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-003'
        elif 'Relay Delta' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-004'
        elif 'Oracle Eye I' in sat_name and 'III' not in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-005'
        elif 'Oracle Eye II' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-006'
        elif 'Oracle Eye III' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-007'
        elif 'Sentinel Prime' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-008'
        elif 'Sentinel Echo' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-009'
        elif 'IoT Hub North' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-010'
        elif 'IoT Hub South' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-011'
        elif 'IoT Hub East' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-012'
        elif 'Deep Space Probe' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-015'
        elif 'Project Oracle Node B' in sat_name:
            df.at[idx, 'satellite_id'] = 'WTE-SAT-014'

# ============================================================================
# 4. NORMALIZAR ESTACIONES TERRESTRES
# ============================================================================
print("\n📡 Normalizando estaciones terrestres...")
df['ground_station'] = df['ground_station'].str.upper()
# Reemplazar valores inválidos
invalid_stations = ['0', 'N/A']
for idx, row in df.iterrows():
    if df.at[idx, 'ground_station'] in invalid_stations or pd.isna(df.at[idx, 'ground_station']):
        # Asignar una estación válida por defecto
        df.at[idx, 'ground_station'] = 'GS-GOTHAM-01'

# ============================================================================
# 5. NORMALIZAR OPERADORES
# ============================================================================
print("\n👤 Normalizando operadores...")
valid_operators = ['D.Pennyworth', 'L.Fox.Jr', 'B.Grayson', 'B.Banner', 'C.Danvers', 
                   'T.Fox', 'B.Wayne', 'N.Romanov', 'L.McGinnis', 'V.Stone', 
                   'L.Fox.Jr', 'R.Drake', 'S.Wayne', 'P.Parker', 'T.Stark', 
                   'O.Queen']
invalid_operators = ['0', 'N/A']
for idx, row in df.iterrows():
    op = df.at[idx, 'operator_id']
    if op in invalid_operators or pd.isna(op) or op not in valid_operators:
        # Asignar un operador válido por defecto
        df.at[idx, 'operator_id'] = 'B.Wayne'

# ============================================================================
# 6. NORMALIZAR PROTOCOLOS
# ============================================================================
print("\n📡 Normalizando protocolos...")
valid_protocols = ['TCP/IP-over-CCSDS', 'CCSDS', 'SpacePacket', 'TM/TC', 'AOS', 'DVB-S2']
invalid_protocols = ['0', 'N/A']
for idx, row in df.iterrows():
    proto = df.at[idx, 'protocol']
    if proto in invalid_protocols or pd.isna(proto) or proto not in valid_protocols:
        # Asignar un protocolo válido por defecto
        df.at[idx, 'protocol'] = 'CCSDS'

# ============================================================================
# 7. LIMPIAR COLUMNAS BOOLEANAS
# ============================================================================
print("\n✅ Limpiando columnas booleanas...")
bool_columns = ['requires_action', 'resolved']
for col in bool_columns:
    if col in df.columns:
        # Convertir a booleano
        df[col] = df[col].astype(str).str.upper()
        df[col] = df[col].map({'YES': True, 'NO': False, 'TRUE': True, 'FALSE': False})
        # Llenar valores faltantes con False
        df[col] = df[col].fillna(False)

# ============================================================================
# 8. LIMPIAR VALORES NUMÉRICOS
# ============================================================================
print("\n🔢 Limpiando valores numéricos...")
numeric_columns = ['frequency_mhz', 'snr_db', 'bit_error_rate', 'elevation_angle_deg', 
                   'event_duration_ms', 'retry_count', 'resolution_time_min']
for col in numeric_columns:
    if col in df.columns:
        # Convertir a numérico, los valores inválidos se convierten a NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Llenar NaN con 0
        df[col] = df[col].fillna(0)

# ============================================================================
# 9. REMOVER DUPLICADOS COMPLETOS
# ============================================================================
print("\n🔍 Removiendo duplicados...")
original_count = len(df)
df = df.drop_duplicates()
print(f"Registros removidos (duplicados): {original_count - len(df)}")

# ============================================================================
# 10. VALIDACIÓN FINAL
# ============================================================================
print("\n✨ Validación final...")
print("\nValores únicos por columna clave:")
print(f"Severidades: {df['severity'].unique()}")
print(f"Satélites únicos: {df['satellite_id'].nunique()}")
print(f"Estaciones únicas: {df['ground_station'].nunique()}")
print(f"Operadores únicos: {df['operator_id'].nunique()}")
print(f"Protocolos únicos: {df['protocol'].nunique()}")

# ============================================================================
# 11. GUARDAR DATASET LIMPIO
# ============================================================================
print("\n💾 Guardando dataset limpio...")
df.to_csv(csv_path, index=False)
print(f"✅ Dataset limpio guardado en: {csv_path}")
print(f"Total de registros finales: {len(df)}")

print("\n" + "="*70)
print("🎉 ¡Limpieza completada exitosamente!")
print("="*70)
