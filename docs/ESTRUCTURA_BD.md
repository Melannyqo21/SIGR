# Documentación de la Estructura de Base de Datos (`sigr.db` - SQLite)

El modelo relacional gestionado mediante SQLAlchemy está compuesto por 8 tablas:

1. **`users`**: Almacena los usuarios del sistema (`id`, `nombre`, `username`, `password_hash`, `rol`, `activo`).
2. **`categories`**: Categorías del menú digital (`id`, `nombre`, `descripcion`).
3. **`dishes`**: Platos y productos (`id`, `nombre`, `descripcion`, `precio`, `disponible`, `activo`, `category_id`).
4. **`orders`**: Encabezado de pedidos (`id`, `cliente_nombre`, `mesa`, `estado`, `total`, `fecha_creacion`, `cliente_id`, `mesero_id`).
5. **`order_items`**: Detalle de platos y subtotales por pedido (`id`, `order_id`, `dish_id`, `cantidad`, `precio_unitario`, `subtotal`).
6. **`bookings`**: Registro de reservas por fecha y hora (`id`, `cliente_nombre`, `contacto`, `fecha`, `hora`, `personas`, `estado`, `user_id`).
7. **`cash_closures`**: Registro de cierres de caja diarios (`id`, `fecha`, `total_pedidos`, `total_ingresos`, `observaciones`, `cerrado_por_id`, `fecha_cierre`).
8. **`sales`**: Ventas generadas automáticamente al entregar un pedido (`id`, `order_id` [Unique], `monto`, `fecha`, `fecha_hora`, `closure_id`).
