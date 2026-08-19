import http.server
import socketserver
import socket
import sys

# Puerto asignado para la suite Sarovi
PUERTO = 8080
Handler = http.server.SimpleHTTPRequestHandler

def obtener_ip_local():
    """Detecta la IP interna de la computadora dentro de la red local WiFi/Ethernet."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No realiza una conexion real, solo mapea la interfaz de red activa
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def iniciar_servidor():
    ip_local = obtener_ip_local()
    
    # Configuración para evitar el error habitual "Address already in use" al reiniciar seguido
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", PUERTO), Handler) as httpd:
            print("=========================================================")
            print("   🌐 SERVIDOR LOCAL ULTRA-LIGERO - SUITE SAROVI")
            print("=========================================================")
            print(f"✅ Servidor montado exitosamente en el puerto: {PUERTO}")
            print("")
            print(f"💻 Desde esta PC accede en:  http://localhost:{PUERTO}")
            print(f"📱 Desde tu movil/tablet:    http://{ip_local}:{PUERTO}")
            print("")
            print("=========================================================")
            print("👉 Para apagar el servidor presiona: CTRL + C en esta ventana.")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor Sarovi apagado de forma segura.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error crítico al levantar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    iniciar_servidor()
