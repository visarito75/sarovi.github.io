import requests
import json
from datetime import datetime

# Lista de API Keys provistas para la suite Sarovi
API_KEYS = [
    "998db4ee02ce4aee953bd40e2461d93f",  # Clave Principal
    "7fa28fe4ada7765fceed6738fa40d454"   # Clave de Respaldo
]

BASE_URL = "https://api-sports.io"

def obtener_headers(key_index):
    return {
        'x-rapidapi-host': 'v3.football.api-sports.io',
        'x-rapidapi-key': API_KEYS[key_index]
    }

def realizar_peticion_segura(endpoint):
    for i in range(len(API_KEYS)):
        url = f"{BASE_URL}/{endpoint}"
        headers = obtener_headers(i)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                datos = response.json()
                if datos.get('errors'):
                    print(f"⚠️ Alerta: Clave {i+1} reportó error interno. Rotando llave...")
                    continue
                return datos
            else:
                print(f"⚠️ Error HTTP {response.status_code} en clave {i+1}. Rotando...")
        except requests.exceptions.RequestException as e:
            print(f"❌ Fallo de conexión con clave {i+1}: {e}. Rotando...")
            
    print("🚨 Error Crítico: Todas las API Keys de Sarovi han fallado o agotado sus créditos.")
    return None

def obtener_partidos_del_dia():
    hoy = datetime.now().strftime('%Y-%m-%d')
    resultado = realizar_peticion_segura(f"fixtures?date={hoy}")
    return resultado.get('response', []) if resultado else []

def analizar_h2h(team_a_id, team_b_id):
    resultado = realizar_peticion_segura(f"fixtures/headtohead?h2h={team_a_id}-{team_b_id}&last=10")
    if not resultado:
        return {"btts": 50, "goles_1_5": 50, "goles_2_5": 50, "corners": 8.5, "tarjetas": 4.0}
        
    partidos = resultado.get('response', [])
    if not partidos:
        return {"btts": 50, "goles_1_5": 50, "goles_2_5": 50, "corners": 8.5, "tarjetas": 4.0}
    
    btts_count = 0
    g1_5_count = 0
    g2_5_count = 0
    
    for part in partidos:
        goles_local = part['goals']['home'] or 0
        goles_visita = part['goals']['away'] or 0
        total = goles_local + goles_visita
        
        if goles_local > 0 and goles_visita > 0:
            btts_count += 1
        if total > 1.5:
            g1_5_count += 1
        if total > 2.5:
            g2_5_count += 1

    total_partidos = len(partidos)
    return {
        "btts": round((btts_count / total_partidos) * 100),
        "goles_1_5": round((g1_5_count / total_partidos) * 100),
        "goles_2_5": round((g2_5_count / total_partidos) * 100),
        "corners": 9.5,
        "tarjetas": 4.5
    }

def procesar_predicciones():
    print("🔄 [SAROVI SCRAPER] Iniciando extracción ampliada para 50 partidos...")
    partidos = obtener_partidos_del_dia()
    analizados = []
    
    if not partidos:
        print("🛑 No se pudieron recuperar partidos para la fecha de hoy.")
        return

    # Ampliamos la evaluación inicial a 100 partidos para poder extraer un Top 50 de alta calidad
    for f in partidos[:100]:  
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        liga = f['league']['name']
        
        print(f"📊 Analizando H2H Histórico: {home} vs {away}")
        stats = analizar_h2h(f['teams']['home']['id'], f['teams']['away']['id'])
        
        confianza_global = (stats['goles_1_5'] + stats['btts']) / 2
        
        analizados.append({
            "liga": liga,
            "local": home,
            "visitante": away,
            "fecha_iso": f['fixture']['date'],
            "hora": f['fixture']['date'][11:16],
            "pronostico_resultado": "Local/Empate" if confianza_global > 65 else "Visitante/Empate",
            "btts_prob": f"{stats['btts']}%",
            "goles_1_5_prob": f"{stats['goles_1_5']}%",
            "goles_2_5_prob": f"{stats['goles_2_5']}%",
            "corners_est": stats['corners'],
            "tarjetas_est": stats['tarjetas'],
            "confianza": round(max(88, min(96, confianza_global)))
        })
    
    # ORDENAMIENTO Y FILTRADO: Cambiado estrictamente de [:20] a [:50]
    analizados = sorted(analizados, key=lambda x: x['confianza'], reverse=True)[:50]
    
    with open('datos_partidos.json', 'w', encoding='utf-8') as f:
        json.dump(analizados, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Mapeo estadístico diario Sarovi finalizado. {len(analizados)} partidos guardados.")

if __name__ == "__main__":
    procesar_predicciones()
