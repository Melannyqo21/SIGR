# Historial de Cambios (CHANGELOG)

## [v1.0.0] - 2026-11-11 — Establecimiento de Línea Base
### Añadido
- **Módulo 1 (Autenticación y Usuarios):** Inicio/cierre de sesión, hash de contraseñas con Werkzeug y control de acceso por roles (`administrador`, `mesero`, `cliente`).
- **Módulo 2 (Menú Digital):** Creación de categorías, registro, consulta, edición y desactivación lógica de platos.
- **Módulo 3 (Pedidos):** Toma de pedidos por mesa, cálculo automático de subtotales/totales y máquina de estados (`pendiente`, `en preparación`, `listo`, `entregado`).
- **Módulo 4 (Reservas):** Registro y actualización de reservas con estados (`pendiente`, `confirmada`, `cancelada`, `atendida`).
- **Módulo 5 (Caja y Reportes):** Generación automática de venta única al entregar pedidos, cierre de caja diario y reporte de ingresos por fecha.
- **Pruebas:** Suite de pruebas de integración con `pytest`.