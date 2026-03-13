"""
Backend simulado para App de Buses
===================================
Simula: rutas, pasajeros, cobros, recaudación y reportes.
Incluye funciones extra con if, elif, else, for y datos simulados.
"""

from datetime import datetime
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
    def __init__(self, id_bus, placa, capacidad, ruta: "Ruta"):
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
            print(f"   🛣️  Viajes registrados      : {r['viajes_registrados']}")
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
        print("─" * 70)
        for v in bus.viajes:
            print(
                f"  [{v['hora']}] {v['origen']} → {v['destino']} | "
                f"↑{v['subieron']} ↓{v['bajaron']} | "
                f"En bus: {v['pasajeros_en_bus']} | Cobrado: ${v['cobrado']:,.2f}"
            )


# ─────────────────────────────────────────────
# FUNCIONES EXTRA CON IF, ELIF, ELSE, FOR
# ─────────────────────────────────────────────

def estado_bus(bus: Bus):
    """Evalúa el nivel de ocupación del bus."""
    ocupacion = bus.pasajeros_actuales / bus.capacidad

    if ocupacion == 0:
        print(f"🚌 Bus {bus.placa}: vacío")
    elif ocupacion < 0.5:
        print(f"🚌 Bus {bus.placa}: ocupación baja")
    elif ocupacion < 0.9:
        print(f"🚌 Bus {bus.placa}: ocupación media")
    elif ocupacion < 1:
        print(f"🚌 Bus {bus.placa}: casi lleno")
    else:
        print(f"🚌 Bus {bus.placa}: lleno")


def verificar_capacidad(bus: Bus):
    """Muestra alerta según la capacidad actual."""
    if bus.pasajeros_actuales > bus.capacidad:
        print(f"⚠ ALERTA: El bus {bus.placa} está sobrecargado")
    elif bus.pasajeros_actuales == bus.capacidad:
        print(f"⚠ El bus {bus.placa} está lleno")
    else:
        print(f"✔ El bus {bus.placa} está dentro de la capacidad permitida")


def calcular_pago(precio, tipo_pasajero):
    """Simula descuentos según tipo de pasajero."""
    if tipo_pasajero == "estudiante":
        return precio * 0.5
    elif tipo_pasajero == "adulto_mayor":
        return precio * 0.3
    elif tipo_pasajero == "discapacidad":
        return 0
    else:
        return precio


def simular_metodo_pago():
    """Simula el método de pago con if / elif."""
    metodos = ["efectivo", "tarjeta", "app"]
    metodo = random.choice(metodos)
    monto = random.randint(1000, 3000)

    if metodo == "efectivo":
        print(f"💵 Pago en efectivo por ${monto}")
    elif metodo == "tarjeta":
        print(f"💳 Pago con tarjeta por ${monto}")
    elif metodo == "app":
        print(f"📱 Pago con app móvil por ${monto}")


def clasificar_recaudacion(sistema: SistemaRecaudacion):
    """Clasifica los buses por nivel de recaudación."""
    print("\n📈 Clasificación de recaudación")
    print("─" * 40)
    for bus in sistema.buses:
        if bus.recaudacion_dia < 20000:
            nivel = "BAJA"
        elif bus.recaudacion_dia < 50000:
            nivel = "MEDIA"
        else:
            nivel = "ALTA"

        print(f"Bus {bus.placa} → ${bus.recaudacion_dia:,.2f} → {nivel}")


def analizar_viajes(bus: Bus):
    """Suma subidas y bajadas de cada bus."""
    total_subieron = 0
    total_bajaron = 0
    total_cobrado = 0

    for viaje in bus.viajes:
        total_subieron += viaje["subieron"]
        total_bajaron += viaje["bajaron"]
        total_cobrado += viaje["cobrado"]

    print(f"\n🔎 Análisis del bus {bus.placa}")
    print(f"   Total subieron : {total_subieron}")
    print(f"   Total bajaron  : {total_bajaron}")
    print(f"   Total cobrado  : ${total_cobrado:,.2f}")

    if total_subieron > total_bajaron:
        print("   Resultado      : Subieron más personas de las que bajaron")
    elif total_subieron < total_bajaron:
        print("   Resultado      : Bajaron más personas de las que subieron")
    else:
        print("   Resultado      : Subidas y bajadas equilibradas")


def ranking_buses(sistema: SistemaRecaudacion):
    """Muestra ranking de buses por recaudación."""
    buses_ordenados = sorted(
        sistema.buses,
        key=lambda b: b.recaudacion_dia,
        reverse=True
    )

    print("\n🏆 RANKING DE BUSES POR RECAUDACIÓN")
    print("─" * 45)
    for i, bus in enumerate(buses_ordenados, start=1):
        print(f"{i}. {bus.placa} | Ruta: {bus.ruta.nombre} | ${bus.recaudacion_dia:,.2f}")


def bus_mas_pasajeros(sistema: SistemaRecaudacion):
    """Encuentra el bus con más pasajeros en el día."""
    if not sistema.buses:
        print("No hay buses en el sistema.")
        return

    mejor = sistema.buses[0]

    for bus in sistema.buses:
        if bus.total_pasajeros_dia > mejor.total_pasajeros_dia:
            mejor = bus

    print("\n👑 Bus con más pasajeros transportados")
    print("─" * 45)
    print(f"Bus: {mejor.placa}")
    print(f"Ruta: {mejor.ruta.nombre}")
    print(f"Pasajeros del día: {mejor.total_pasajeros_dia}")


def promedio_pasajeros_por_viaje(bus: Bus):
    """Calcula promedio de pasajeros subidos por viaje."""
    if len(bus.viajes) == 0:
        print(f"Bus {bus.placa}: no tiene viajes registrados.")
        return

    suma = 0
    for viaje in bus.viajes:
        suma += viaje["subieron"]

    promedio = suma / len(bus.viajes)

    print(f"\n📊 Promedio de pasajeros por viaje - Bus {bus.placa}")
    print(f"Promedio: {promedio:.2f}")

    if promedio < 5:
        print("Nivel de demanda: baja")
    elif promedio < 10:
        print("Nivel de demanda: media")
    else:
        print("Nivel de demanda: alta")


def simular_horas_pico():
    """Simulación independiente de horas pico."""
    print("\n🕒 Simulación de horas pico")
    print("─" * 40)

    for hora in range(6, 22):
        pasajeros = random.randint(0, 50)

        if 7 <= hora <= 9:
            estado = "Hora pico de la mañana"
        elif 17 <= hora <= 19:
            estado = "Hora pico de la tarde"
        else:
            estado = "Horario normal"

        print(f"{hora:02d}:00 → {pasajeros:02d} pasajeros → {estado}")


def simular_cobros_por_tipo_pasajero(ruta: Ruta, cantidad=10):
    """Simula cobros con descuentos según tipo de pasajero."""
    print(f"\n💰 Simulación de cobros en ruta {ruta.nombre}")
    print("─" * 55)

    tipos = ["normal", "estudiante", "adulto_mayor", "discapacidad"]
    total = 0

    for i in range(1, cantidad + 1):
        tipo = random.choice(tipos)
        pago = calcular_pago(ruta.precio_pasaje, tipo)
        total += pago
        print(f"Pasajero {i:02d} | Tipo: {tipo:14} | Pago: ${pago:,.2f}")

    print("─" * 55)
    print(f"Total recaudado en simulación: ${total:,.2f}")


def mostrar_alertas(sistema: SistemaRecaudacion):
    """Genera alertas según resultados simulados."""
    print("\n🚨 ALERTAS DEL SISTEMA")
    print("─" * 40)

    for bus in sistema.buses:
        if bus.recaudacion_dia < 15000:
            print(f"⚠ El bus {bus.placa} tiene recaudación muy baja")
        elif bus.total_pasajeros_dia > 30:
            print(f"📌 El bus {bus.placa} tuvo alta demanda")
        else:
            print(f"✔ El bus {bus.placa} operó sin novedades")


def menu_analisis_extra(sistema: SistemaRecaudacion):
    """Ejecuta todas las funciones extra."""
    print("\n" + "═" * 60)
    print("         🧠 ANÁLISIS EXTRA DEL SISTEMA")
    print("═" * 60)

    clasificar_recaudacion(sistema)
    ranking_buses(sistema)
    bus_mas_pasajeros(sistema)
    mostrar_alertas(sistema)
    simular_horas_pico()

    print("\n💳 Simulación de métodos de pago")
    print("─" * 40)
    for _ in range(5):
        simular_metodo_pago()

    for bus in sistema.buses:
        estado_bus(bus)
        verificar_capacidad(bus)
        analizar_viajes(bus)
        promedio_pasajeros_por_viaje(bus)

    if sistema.buses:
        simular_cobros_por_tipo_pasajero(sistema.buses[0].ruta, cantidad=8)


# ─────────────────────────────────────────────
# SIMULACIÓN
# ─────────────────────────────────────────────

def simular_dia():
    # 1. Crear rutas
    ruta_norte = Ruta("R1", "Centro → Norte", precio_pasaje=1500)
    ruta_sur = Ruta("R2", "Centro → Sur", precio_pasaje=1200)
    ruta_este = Ruta("R3", "Terminal → Este", precio_pasaje=1800)

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

    # 4. Paradas por ruta
    paradas_norte = ["Centro", "Parque", "Mercado", "Hospital", "Norte Terminal"]
    paradas_sur = ["Centro", "Estadio", "Villa Sur", "Sur Terminal"]
    paradas_este = ["Terminal", "Zona Industrial", "Av. Este", "Barrio Nuevo", "Este Final"]

    rutas_paradas = {
        bus1: paradas_norte,
        bus2: paradas_sur,
        bus3: paradas_este,
    }

    print("\n🚌 Iniciando simulación del día operativo...\n")

    # 5. Simular viajes
    for bus, paradas in rutas_paradas.items():
        print(f"▶ Simulando bus {bus.placa} en ruta '{bus.ruta.nombre}'")
        bus.pasajeros_actuales = 0

        for i in range(len(paradas) - 1):
            origen = paradas[i]
            destino = paradas[i + 1]

            # Bajan pasajeros
            bajaron = bus.bajar_pasajeros(
                random.randint(0, max(1, bus.pasajeros_actuales // 2))
            )

            # Suben pasajeros
            nuevos_pasajeros = random.randint(2, 15)
            subieron, cobrado = bus.subir_pasajeros(nuevos_pasajeros)

            bus.registrar_viaje(origen, destino, subieron, bajaron, cobrado)

        print(f"   ✅ Completado. Recaudado hoy: ${bus.recaudacion_dia:,.2f}\n")

    # 6. Imprimir reportes
    sistema.reporte_general()

    print("\n📋 Detalle de viajes por bus:")
    for bus in sistema.buses:
        sistema.reporte_viajes_bus(bus.id_bus)

    # 7. Ejecutar análisis extra
    menu_analisis_extra(sistema)

    return sistema


# ─────────────────────────────────────────────
# ENTRADA PRINCIPAL
# ─────────────────────────────────────────────

if __name__ == "__main__":
    sistema = simular_dia()
    
