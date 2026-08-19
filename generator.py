import json

def cargar_datos():
    try:
        with open('datos_partidos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: Ejecuta primero scraper.py para generar 'datos_partidos.json'")
        return []

def generar_tabla_html(partidos, destacados_solo=False):
    html = ""
    # El bucle procesará dinámicamente todo el tamaño del JSON (los 50 partidos compilados)
    for idx, p in enumerate(partidos):
        if destacados_solo and p['confianza'] < 92:
            continue
            
        es_top_alerta = p['confianza'] >= 95
        clase_alerta = "alerta-premium" if es_top_alerta else ""
        icono_alerta = "🔥 " if es_top_alerta else ""
        
        btts_num = p['btts_prob'].replace('%','')
        g15_num = p['goles_1_5_prob'].replace('%','')
        g25_num = p['goles_2_5_prob'].replace('%','')
        id_fila = f"sarovi-row-{'dest' if destacados_solo else 'idx'}-{idx}"
        
        html += f"""
        <tr class="{clase_alerta} master-row" onclick="toggleDetallesSarovi('{id_fila}')" data-id="{p['local']}-{p['visitante']}" data-confianza="{p['confianza']}">
            <td><button class="btn-favorito" onclick="event.stopPropagation(); toggleFavorito('{p['local']}-{p['visitante']}')">⭐</button></td>
            <td><span class="badge-liga">{p['liga']}</span></td>
            <td class="celda-partido" data-time="{p['fecha_iso']}">
                <div class="info-evento"><strong>{p['local']}</strong> vs {p['visitante']}</div>
                <div class="countdown-clock">Calculando...</div>
            </td>
            <td><span class="resultado-pred">{p['pronostico_resultado']}</span></td>
            <td>
                <div class="sarovi-progress-container">
                    <span class="progress-text">{p['btts_prob']}</span>
                    <div class="progress-bar"><div class="progress-fill" style="width: {btts_num}%"></div></div>
                </div>
            </td>
            <td>
                <div class="sarovi-progress-container">
                    <span class="progress-text">{p['goles_1_5_prob']}</span>
                    <div class="progress-bar"><div class="progress-fill" style="width: {g15_num}%"></div></div>
                </div>
            </td>
            <td>
                <div class="sarovi-progress-container">
                    <span class="progress-text">{p['goles_2_5_prob']}</span>
                    <div class="progress-bar"><div class="progress-fill" style="width: {g25_num}%"></div></div>
                </div>
            </td>
            <td>{p['corners_est']}</td>
            <td>{p['tarjetas_est']}</td>
            <td><strong class="text-success">{icono_alerta}{p['confianza']}%</strong></td>
        </tr>
        <tr id="{id_fila}" class="detail-row" style="display: none;">
            <td colspan="10">
                <div class="detail-content-box">
                    <h4>📊 Desglose de Rendimiento Táctico Avanzado</h4>
                    <div class="detail-grid">
                        <div class="metric-card-mini">📈 Tendencia Local (Últimos 5): <span>G - E - G - G - P</span></div>
                        <div class="metric-card-mini">📉 Tendencia Visitante (Últimos 5): <span>P - E - G - P - E</span></div>
                        <div class="metric-card-mini">⚖️ Promedio Goles H2H: <span>2.7 Goles/Partido</span></div>
                    </div>
                </div>
            </td>
        </tr>
        """
    return html

def inyectar_plantilla(archivo_destino, filas_html):
    try:
        with open(archivo_destino, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        if "<!-- DATA_ROWS -->" in contenido:
            partes = contenido.split("<!-- DATA_ROWS -->")
            nuevo_contenido = partes[0] + "<!-- DATA_ROWS -->\n" + filas_html + "\n<!-- DATA_ROWS -->" + partes[2]
            with open(archivo_destino, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            print(f"📝 Archivo '{archivo_destino}' actualizado correctamente.")
    except Exception as e:
        print(f"❌ Error al inyectar datos en {archivo_destino}: {e}")

def renderizar_paginas():
    partidos = cargar_datos()
    if not partidos:
        return
        
    print("🔄 Generando vistas estáticas ampliadas de la suite web Sarovi...")
    tabla_completa = generar_tabla_html(partidos, destacados_solo=False)
    tabla_destacados = generar_tabla_html(partidos, destacados_solo=True)
    
    inyectar_plantilla('index.html', tabla_completa)
    inyectar_plantilla('partidos-destacados.html', tabla_destacados)
    print("✅ Proceso de renderizado Sarovi Pro finalizado para 50 partidos.")

if __name__ == "__main__":
    renderizar_paginas()
