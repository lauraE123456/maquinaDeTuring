import time
from datetime import datetime

# 1. TABLA DE TRANSICIONES MEJORADA
# Representa el conocimiento de la máquina: "Si estoy en q0 y leo 'B', sigo buscando Bogota"
tabla_turing = {
    "BOGOTA": {"pais": "COLOMBIA", "offset": 0},
    "MADRID": {"pais": "ESPAÑA", "offset": 6},
    "TOKYO": {"pais": "JAPÓN", "offset": 14},
    "LONDRES": {"pais": "INGLATERRA", "offset": 5},
    "SIDNY": {"pais": "AUSTRALIA", "offset": 15}
}

def turing(entrada_usuario):
    """
    Función para la API: ejecuta la máquina de Turing y devuelve el resultado como diccionario.
    """
    cinta = list(entrada_usuario.upper()) + ["#"]
    cabezal = 0
    estado = "q_leyendo"
    palabra_acumulada = ""
    
    while estado != "HALT":
        simbolo_actual = cinta[cabezal]
        
        if simbolo_actual != "#":
            palabra_acumulada += simbolo_actual
            cabezal += 1
        else:
            estado = "q_verificando"
            
            if palabra_acumulada in tabla_turing:
                datos = tabla_turing[palabra_acumulada]
                hora_utc = datetime.now().hour
                hora_destino = (hora_utc + datos["offset"]) % 24
                
                def obtener_periodo(h):
                    if 6 <= h < 12: return "Mañana"
                    if 12 <= h < 18: return "Tarde"
                    return "Noche"
                
                return {
                    "ciudad": palabra_acumulada,
                    "pais": datos["pais"],
                    "hora": f"{hora_destino}:00",
                    "periodo": obtener_periodo(hora_destino),
                    "offset": datos["offset"]
                }
            else:
                return {"error": "Ciudad no encontrada en la base de datos"}
    
    return {"error": "Error en la ejecución"}

# Función original para simulación en consola
def ejecutar_maquina_turing(entrada_usuario):
    # La CINTA contiene la palabra más un símbolo de fin (BLANK)
    cinta = list(entrada_usuario.upper()) + ["#"]
    cabezal = 0
    estado = "q_leyendo"
    palabra_acumulada = ""
    
    print(f"\nConfiguración inicial de la cinta: {' '.join(cinta)}")
    print("-" * 45)

    # El ciclo continúa hasta que el estado sea HALT (parada)
    while estado != "HALT":
        simbolo_actual = cinta[cabezal]
        
        # Simulación visual del cabezal
        visualizacion = [" "] * len(cinta)
        visualizacion[cabezal] = "^"
        print(f"Cinta:  {' '.join(cinta)}")
        print(f"Cabeza: {' '.join(visualizacion)} (Estado: {estado})")
        time.sleep(0.5) # Pausa para ver el efecto de movimiento

        if simbolo_actual != "#":
            # La máquina está "escaneando" y acumulando en su memoria interna
            palabra_acumulada += simbolo_actual
            print(f"Acción: Leyendo '{simbolo_actual}', moviendo R (derecha)...")
            cabezal += 1
        else:
            # Hemos llegado al final de la palabra (#)
            print(f"\nAcción: Fin de palabra detectado. Verificando '{palabra_acumulada}'...")
            estado = "q_verificando"
            
            if palabra_acumulada in tabla_turing:
                datos = tabla_turing[palabra_acumulada]
                # Cálculo de hora lógica
                hora_utc = datetime.now().hour
                hora_destino = (hora_utc + datos["offset"]) % 24
                print(f"RESULTADO: Ciudad encontrada en la base de transiciones.")
                mostrar_reporte(datos, hora_destino)
                estado = "HALT"
            else:
                print("RESULTADO: Error 404 - Ciudad no definida en la tabla.")
                estado = "HALT"

def mostrar_reporte(datos, hora):
    def obtener_periodo(h):
        if 6 <= h < 12: return "Mañana"
        if 12 <= h < 18: return "Tarde"
        return "Noche"

    print("\n" + "="*30)
    print(f"   REPORTE GEOTEMPORAL")
    print("="*30)
    print(list(f"País:{datos['pais']}"))
    print(list( f"Hora:{hora}:00") )
    print(list(f"Periodo:{obtener_periodo(hora)}"))
    print(f"Offset:    +{datos['offset']}h")
    print("="*30)

if __name__ == "__main__":
    print("--- SIMULADOR DE MÁQUINA DE TURING GEOTEMPORAL ---")
    ciudad = input("Escriba la ciudad (Bogota, Madrid, Tokyo, etc): ").strip()
    if ciudad:
        ejecutar_maquina_turing(ciudad)
    else:
        print("Entrada vacía.")