# Mercaloop — Monolito de Diagnóstico

API de marketplace construida como monolito clásico: un único proceso,
una única base de datos en memoria, un único artefacto de despliegue.
Módulos: `catalog`, `orders`, `payments`, `notifications`.

## Arranque rápido (ya viene listo en Codespaces)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Abre la pestaña **Ports** y entra al puerto `8000`. Documentación interactiva en `/docs`.

Pedidos de prueba:

```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"sku": "PROD-001", "quantity": 2, "customer_email": "test@correo.com"}'
```

---

## Dinámica: La Autopsia del Código

Trabajan en equipo como "médicos forenses de software". Su objetivo NO es
arreglar nada todavía — solo diagnosticar.

### Instrucciones

1. Exploren el código en `app/`. Prueben la API desde `/docs` o con `curl`.
2. Para cada síntoma que encuentren, complétenlo en la matriz de abajo.
3. Preguntas guía (no son las únicas a buscar):
   - ¿Dónde falla el límite lógico entre módulos? ¿Algún módulo conoce
     detalles internos de otro que no debería?
   - ¿Alguna función/clase concentra demasiadas responsabilidades?
   - Si tuvieran que cambiar una sola línea de texto sin relación con
     la lógica de negocio, ¿qué tendrían que reconstruir y redesplegar?
   - Prueben crear el mismo pedido dos veces seguidas rápidamente.
     ¿El stock se descuenta como esperan?

### Entregable: Matriz de impactos

| Componente | Síntoma detectado | Tipo de acoplamiento | Lead Time estimado (cambio mínimo) | Riesgo de fallo total |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

---

## Bloque 2: De la autopsia a la cirugía

Elijan **un solo síntoma** de su matriz. Háganle el cambio mínimo necesario
para corregirlo. Luego desplieguen el monolito completo:

```bash
docker compose up --build
```

Midan cuánto tarda ese ciclo completo (build + deploy) para un cambio que,
en teoría, era pequeño. Comparen contra el Lead Time que estimaron en la
matriz.
