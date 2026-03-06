"""
Backend simulado para App de Buses
===================================
Simula: rutas, pasajeros, cobros, recaudación y reportes.
"""

from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────────
# MODELOS DE DATOS
# ─────────────────────────────────────────────

class Ruta:
    def __init__(self, id_ruta, nombre, precio_pasaje):
        self.id_ruta = id_ruta
        self.nombre = nombre
        self.precio_pasaje = precio_pasaje  # en pesos / moneda local

    def __repr__(self):
        return f"Ruta({self.id_ruta} - {self.nombre} | ${self.precio_pasaje})"


class Bus:
    def __init__(self, id_bus, placa, capacidad, ruta: Ruta):
        self.id_bus = id_bus
        self.placa = placa
        self.capacidad = capacidad
        self.ruta = ruta
        self.pasajeros_actuales = 0
        self.total_pasajeros_dia = 0
        self.recaudacion_dia = 0.0
        self.viajes = []

    def subir_pasajeros(self, cantidad):
        espacio = self.capacidad - self.pasajeros_actuales
        subieron = min(cantidad, espacio)
        self.pasajeros_actuales += subieron
        cobrado = subieron * self.ruta.precio_pasaje
        self.recaudacion_dia += cobrado
        self.total_pasajeros_dia += subieron
        return subieron, cobrado

    def bajar_pasajeros(self, cantidad):
        bajaron = min(cantidad, self.pasajeros_actuales)
        self.pasajeros_actuales -= bajaron
        return bajaron

    def registrar_viaje(self, parada_origen, parada_destino, pasajeros_subieron, pasajeros_bajaron, cobrado):
        self.viajes.append({
            "hora": datetime.now().strftime("%H:%M:%S"),
            "origen": parada_origen,
            "destino": parada_destino,
            "subieron": pasajeros_subieron,
            "bajaron": pasajeros_bajaron,
            "cobrado": cobrado,
            "pasajeros_en_bus": self.pasajeros_actuales,
        })

    def resumen(self):
        return {
            "bus": self.placa,
            "ruta": self.ruta.nombre,
            "total_pasajeros_dia": self.total_pasajeros_dia,
            "recaudacion_dia": round(self.recaudacion_dia, 2),
            "viajes_registrados": len(self.viajes),
        }


class SistemaRecaudacion:
    def __init__(self):
        self.buses: list[Bus] = []
        self.rutas: dict[str, Ruta] = {}

    def agregar_ruta(self, ruta: Ruta):
        self.rutas[ruta.id_ruta] = ruta

    def agregar_bus(self, bus: Bus):
        self.buses.append(bus)

    def recaudacion_total(self):
        return round(sum(b.recaudacion_dia for b in self.buses), 2)

    def pasajeros_totales(self):
        return sum(b.total_pasajeros_dia for b in self.buses)

    def reporte_general(self):
        print("\n" + "═" * 55)
        print("       📊  REPORTE GENERAL DEL DÍA")
        print("═" * 55)
        for bus in self.buses:
            r = bus.resumen()
            print(f"\n🚌  Bus: {r['bus']}  |  Ruta: {r['ruta']}")
            print(f"   👥 Pasajeros transportados : {r['total_pasajeros_dia']}")
            print(f"   💰 Recaudación             : ${r['recaudacion_dia']:,.2f}")
            print(f"   🛣️  Viajes registrados       : {r['viajes_registrados']}")
        print("\n" + "─" * 55)
        print(f"   TOTAL PASAJEROS   : {self.pasajeros_totales()}")
        print(f"   TOTAL RECAUDADO   : ${self.recaudacion_total():,.2f}")
        print("═" * 55)

    def reporte_viajes_bus(self, id_bus):
        bus = next((b for b in self.buses if b.id_bus == id_bus), None)
        if not bus:
            print(f"Bus {id_bus} no encontrado.")
            return
        print(f"\n📋 Viajes del bus {bus.placa} — Ruta: {bus.ruta.nombre}")
        print("─" * 60)
        for v in bus.viajes:
            print(
                f"  [{v['hora']}] {v['origen']} → {v['destino']} | "
                f"↑{v['subieron']} ↓{v['bajaron']} | "
                f"En bus: {v['pasajeros_en_bus']} | Cobrado: ${v['cobrado']:,.2f}"
            )


# ─────────────────────────────────────────────
# SIMULACIÓN
# ─────────────────────────────────────────────

def simular_dia():
    # 1. Crear rutas
    ruta_norte = Ruta("R1", "Centro → Norte", precio_pasaje=1500)
    ruta_sur   = Ruta("R2", "Centro → Sur",   precio_pasaje=1200)
    ruta_este  = Ruta("R3", "Terminal → Este", precio_pasaje=1800)

    # 2. Crear buses
    bus1 = Bus("B1", "ABC-123", capacidad=40, ruta=ruta_norte)
    bus2 = Bus("B2", "DEF-456", capacidad=35, ruta=ruta_sur)
    bus3 = Bus("B3", "GHI-789", capacidad=50, ruta=ruta_este)

    # 3. Inicializar sistema
    sistema = SistemaRecaudacion()
    for ruta in [ruta_norte, ruta_sur, ruta_este]:
        sistema.agregar_ruta(ruta)
    for bus in [bus1, bus2, bus3]:
        sistema.agregar_bus(bus)

    # 4. Paradas por ruta (hardcodeadas)
    paradas_norte = ["Centro", "Parque", "Mercado", "Hospital", "Norte Terminal"]
    paradas_sur   = ["Centro", "Estadio", "Villa Sur", "Sur Terminal"]
    paradas_este  = ["Terminal", "Zona Industrial", "Av. Este", "Barrio Nuevo", "Este Final"]

    rutas_paradas = {
        bus1: paradas_norte,
        bus2: paradas_sur,
        bus3: paradas_este,
    }

    print("\n🚌  Iniciando simulación del día operativo...\n")

    # 5. Simular viajes
    for bus, paradas in rutas_paradas.items():
        print(f"▶ Simulando bus {bus.placa} en ruta '{bus.ruta.nombre}'")
        bus.pasajeros_actuales = 0  # inicia vacío

        for i in range(len(paradas) - 1):
            origen  = paradas[i]
            destino = paradas[i + 1]

            # Bajan algunos pasajeros
            bajaron = bus.bajar_pasajeros(random.randint(0, max(1, bus.pasajeros_actuales // 2)))

            # Suben nuevos
            nuevos_pasajeros = random.randint(2, 15)
            subieron, cobrado = bus.subir_pasajeros(nuevos_pasajeros)

            bus.registrar_viaje(origen, destino, subieron, bajaron, cobrado)

        print(f"   ✅ Completado. Recaudado hoy: ${bus.recaudacion_dia:,.2f}\n")

    # 6. Imprimir reportes
    sistema.reporte_general()

    print("\n📋 Detalle de viajes por bus:")
    for bus in sistema.buses:
        sistema.reporte_viajes_bus(bus.id_bus)

    return sistema


# ─────────────────────────────────────────────
# ENTRADA PRINCIPAL
# ─────────────────────────────────────────────

if __name__ == "__main__":
    sistema = simular_dia()