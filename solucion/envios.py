from abc import ABC, abstractmethod

class Pedido:
    def __init__(self, peso_kg, distancia_km, politica_envio):
        self.peso_kg = peso_kg
        self.distancia_km = distancia_km
        self.politica_envio = politica_envio

    def costo_envio(self):
        return self.politica_envio.costo(self.peso_kg, self.distancia_km)

    def cambiar_politica(self, nueva_politica):
        self.politica_envio = nueva_politica

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

class SeguroEnvio(PoliticaEnvio):

    def __init__(self, politica_envio):
        self.politica_envio = politica_envio

    def costo(self, peso_kg, distancia_km):
        costo_base = self.politica_envio.costo(peso_kg, distancia_km)
        return costo_base + 200

class DescuentoEnvio(PoliticaEnvio):

    def __init__(self, politica_envio, porcentaje):
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100")
        self.politica_envio = politica_envio
        self.porcentaje = porcentaje

    def costo(self, peso_kg, distancia_km):
        costo_base = self.politica_envio.costo(peso_kg, distancia_km)
        return round((costo_base - (costo_base * self.porcentaje/100)), 2)