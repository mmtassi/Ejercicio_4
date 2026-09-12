from abc import ABC, abstractmethod

class Pedido:
    def __init__(self, peso_kg, distancia_km, politica_envio):
        if peso_kg <= 0:
            raise ValueError("El peso debe ser mayor que 0")

        if distancia_km <= 0:
            raise ValueError("La distancia debe ser mayor que 0")

        if not isinstance(politica_envio, PoliticaEnvio):
            raise TypeError("La política debe ser una PoliticaEnvio")

        self._peso_kg = peso_kg
        self._distancia_km = distancia_km
        self._politica_envio = politica_envio

    def costo_envio(self):
        return self._politica_envio.costo(self._peso_kg, self._distancia_km)

    def cambiar_politica(self, nueva_politica):
        if not isinstance(nueva_politica, PoliticaEnvio):
            raise TypeError("La política debe ser una PoliticaEnvio")
        self._politica_envio = nueva_politica

class PoliticaEnvio(ABC):

    @abstractmethod
    def costo(self, peso_kg, distancia_km):
        pass

class RetiroSucursal(PoliticaEnvio):

    def costo(self, peso_kg, distancia_km):
        return 0

class EnvioUrbano(PoliticaEnvio):

    def costo(self, peso_kg, distancia_km):
        return 1500

class EnvioInterior(PoliticaEnvio):

    def costo(self, peso_kg, distancia_km):
        return 1500 + 80 * distancia_km

class EnvioExpress(PoliticaEnvio):

    def costo(self, peso_kg, distancia_km):
        return 3000 + 100 * distancia_km

class DecoradorEnvio(PoliticaEnvio):

    def __init__(self, politica_envio):
        if not isinstance(politica_envio, PoliticaEnvio):
            raise TypeError("La política de envío debe ser una instancia de PoliticaEnvio")
        self.politica_envio = politica_envio

    @abstractmethod
    def costo(self, peso_kg, distancia_km):
        pass

class SeguroEnvio(DecoradorEnvio):

    def costo(self, peso_kg, distancia_km):
        costo_base = self.politica_envio.costo(peso_kg, distancia_km)
        return costo_base + 200

class DescuentoEnvio(DecoradorEnvio):

    def __init__(self, politica_envio, porcentaje):
        super().__init__(politica_envio)

        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100")

        self.porcentaje = porcentaje

    def costo(self, peso_kg, distancia_km):
        costo_base = self.politica_envio.costo(peso_kg, distancia_km)
        return round((costo_base - (costo_base * self.porcentaje/100)), 2)

def total_envios(pedidos):
    total = 0
    for pedido in pedidos:
        total += pedido.costo_envio()
    return total

class ModificadorCosto(ABC):

    @abstractmethod
    def aplicar(self, costo):
        pass

class Seguro(ModificadorCosto):

    def aplicar(self, costo):
        return costo + 200

class Descuento(ModificadorCosto):

    def __init__(self, porcentaje):
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100")

        self.porcentaje = porcentaje

    def aplicar(self, costo):
        return round(costo - (costo * self.porcentaje / 100), 2)

class PedidoConModificadores:

    def __init__(self, peso_kg, distancia_km, politica_envio):
        if peso_kg <= 0:
            raise ValueError("El peso debe ser mayor que 0")

        if distancia_km < 0:
            raise ValueError("La distancia debe ser mayor que 0")

        if not isinstance(politica_envio, PoliticaEnvio):
            raise TypeError("La política debe ser una PoliticaEnvio")

        self._peso_kg = peso_kg
        self._distancia_km = distancia_km
        self._politica_envio = politica_envio

        self._modificadores = []

    def agregar_modificador(self, modificador):
        if not isinstance(modificador, ModificadorCosto):
            raise TypeError("El modificador debe ser una instancia de ModificadorCosto")
        self._modificadores.append(modificador)

    def costo_envio(self):
        costo_base = self._politica_envio.costo(self._peso_kg, self._distancia_km)
        for modificador in self._modificadores:
            costo_base = modificador.aplicar(costo_base)
        return costo_base

    def cambiar_politica(self, nueva_politica):
        if not isinstance(nueva_politica, PoliticaEnvio):
            raise TypeError("La política debe ser una PoliticaEnvio")

        self._politica_envio = nueva_politica

    @property
    def peso_kg(self):
        return self._peso_kg

    @property
    def distancia_km(self):
        return self._distancia_km

    @property
    def modificadores(self):
        return tuple(self._modificadores)


pedido = PedidoConModificadores(2, 8, EnvioUrbano())
pedido.agregar_modificador(Descuento(10))
pedido.agregar_modificador(Seguro())
print(pedido.costo_envio())