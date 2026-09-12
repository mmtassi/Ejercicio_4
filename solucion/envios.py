class Pedido:
    def __init__(self, peso_kg, distancia_km, politica_envio):
        self.peso_kg = peso_kg
        self.distancia_km = distancia_km
        self.politica_envio = politica_envio

    def costo_envio(self):
        return self.politica_envio.calcular(self.peso_kg, self.distancia_km)