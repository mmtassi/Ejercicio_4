import pytest
from solucion.envios import Pedido, RetiroSucursal, EnvioUrbano, EnvioInterior, SeguroEnvio, DescuentoEnvio, \
    EnvioExpress, total_envios, PedidoConModificadores, Descuento, Seguro


def test_retiro_sucursal():
    pedido = Pedido(1, 0, RetiroSucursal())

    assert pedido.costo_envio() == 0

def test_envio_urbano():
    pedido = Pedido(2, 8, EnvioUrbano())

    assert pedido.costo_envio() == 1500

def test_envio_interior():
    pedido = Pedido(3, 100, EnvioInterior())

    assert pedido.costo_envio() == 9500

def test_cambiar_politica():
    pedido = Pedido(2, 8, RetiroSucursal())

    assert pedido.costo_envio() == 0

    pedido.cambiar_politica(EnvioUrbano())

    assert pedido.costo_envio() == 1500
    assert pedido.peso_kg == 2
    assert pedido.distancia_km == 8

def test_cambio_politica_invalida_conserva_anterior():
    pedido = Pedido(2, 8, EnvioUrbano())

    with pytest.raises(TypeError):
        pedido.cambiar_politica("invalida")

    assert pedido.costo_envio() == 1500

def test_peso_invalido():
    with pytest.raises(ValueError):
        Pedido(0, 10, EnvioUrbano())

def test_peso_negativo():
    with pytest.raises(ValueError):
        Pedido(-1, 10, EnvioUrbano())

def test_politica_invalida_en_constructor():
    with pytest.raises(TypeError):
        Pedido(2, 8, "EnvioUrbano")

def test_seguro_envio():
    pedido = Pedido(2, 8, SeguroEnvio(EnvioUrbano()))

    assert pedido.costo_envio() == 1700

def test_descuento_envio():
    pedido = Pedido(2, 8, DescuentoEnvio(EnvioUrbano(), 10))

    assert pedido.costo_envio() == 1350

def test_descuento_despues_de_seguro():
    politica = DescuentoEnvio(
        SeguroEnvio(EnvioUrbano()),
        10
    )

    pedido = Pedido(2, 8, politica)

    assert pedido.costo_envio() == 1530

def test_seguro_sobre_retiro_sucursal():
    pedido = Pedido(1, 0, SeguroEnvio(RetiroSucursal()))

    assert pedido.costo_envio() == 200

def test_descuento_cero_por_ciento():
    pedido = Pedido(2, 8, DescuentoEnvio(EnvioUrbano(), 0))
    assert pedido.costo_envio() == 1500


def test_descuento_cien_por_ciento():
    pedido = Pedido(2, 8, DescuentoEnvio(EnvioUrbano(), 100))
    assert pedido.costo_envio() == 0


def test_descuento_porcentaje_negativo():
    with pytest.raises(ValueError):
        DescuentoEnvio(EnvioUrbano(), -10)


def test_descuento_porcentaje_mayor_a_cien():
    with pytest.raises(ValueError):
        DescuentoEnvio(EnvioUrbano(), 110)


def test_decorador_con_politica_invalida():
    with pytest.raises(TypeError):
        SeguroEnvio("invalida")

def test_envio_express_con_seguro():
    express = SeguroEnvio(EnvioExpress())
    pedido = Pedido(2, 8, express)

    assert pedido.costo_envio() == 4000


def test_total_envios():
    pedidos = [
        Pedido(1, 0, RetiroSucursal()),
        Pedido(2, 8, EnvioUrbano()),
        Pedido(3, 100, EnvioInterior()),
        Pedido(2, 8, SeguroEnvio(EnvioExpress()))
    ]

    assert total_envios(pedidos) == 15000

def test_pedido_con_modificadores_sin_modificadores():
    pedido = PedidoConModificadores(2, 8, EnvioUrbano())

    assert pedido.costo_envio() == 1500


def test_pedido_con_modificadores_seguro_y_descuento():
    pedido = PedidoConModificadores(2, 8, EnvioUrbano())

    pedido.agregar_modificador(Seguro())
    pedido.agregar_modificador(Descuento(10))

    assert pedido.costo_envio() == 1530


def test_pedido_con_modificadores_descuento_y_seguro():
    pedido = PedidoConModificadores(2, 8, EnvioUrbano())

    pedido.agregar_modificador(Descuento(10))
    pedido.agregar_modificador(Seguro())

    assert pedido.costo_envio() == 1550


def test_pedido_con_modificadores_recalcula_desde_la_politica():
    pedido = PedidoConModificadores(2, 8, EnvioUrbano())

    pedido.agregar_modificador(Seguro())
    pedido.agregar_modificador(Descuento(10))

    assert pedido.costo_envio() == 1530
    assert pedido.costo_envio() == 1530


def test_modificar_copia_no_modifica_pedido():
    pedido = PedidoConModificadores(2, 8, EnvioUrbano())

    pedido.agregar_modificador(Seguro())

    copia = list(pedido.modificadores)
    copia.append(Descuento(10))

    assert len(pedido.modificadores) == 1

def test_modificador_invalido():
    pedido = PedidoConModificadores(2, 8, EnvioUrbano())

    with pytest.raises(TypeError):
        pedido.agregar_modificador("invalido")


def test_descuento_modificador_porcentaje_negativo():
    with pytest.raises(ValueError):
        Descuento(-10)


def test_descuento_modificador_porcentaje_mayor_a_cien():
    with pytest.raises(ValueError):
        Descuento(110)


def test_pedido_con_modificadores_politica_invalida():
    with pytest.raises(TypeError):
        PedidoConModificadores(2, 8, "invalida")


def test_cambio_politica_invalida_en_pedido_con_modificadores():
    pedido = PedidoConModificadores(2, 8, EnvioUrbano())

    with pytest.raises(TypeError):
        pedido.cambiar_politica("invalida")

    assert pedido.costo_envio() == 1500

def test_equivalencia_decorator_y_pipeline():
    pedido_decorator = Pedido(
        2,
        8,
        DescuentoEnvio(
            SeguroEnvio(EnvioUrbano()),
            10
        )
    )

    pedido_pipeline = PedidoConModificadores(
        2,
        8,
        EnvioUrbano()
    )

    pedido_pipeline.agregar_modificador(Seguro())
    pedido_pipeline.agregar_modificador(Descuento(10))

    assert pedido_decorator.costo_envio() == 1530
    assert pedido_pipeline.costo_envio() == 1530