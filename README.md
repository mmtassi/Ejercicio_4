## Decisiones de diseño

Se separó el cálculo del costo de envío del objeto `Pedido` usando distintas políticas de envío. De esta manera, el pedido no necesita concer la fórmula de cada tipo de envío y puede cambiar de política sin modificar su propia lógica.

Para los adicionales se implementaron dos alternativas. En la primera se usaron decoradores, donde cada adicional envuelve a otra política y modifica el resultado que recibe. En la segunda se usó una lista de modificadores dentro de `PedidoConModificadores`, que los aplica en el orden en que fueron agregados.

También se validan los colaboradores antes de guardarlos para evitar dejar los objetos en un estado inválido. Los datos del pedido se mantienen como estado interno y se exponen mediante propiedades de solo lectura. En el caso de los modificadores se devuelve una tupla para no permitir cambios diretos sobre la colección interna.