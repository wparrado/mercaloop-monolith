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

---

## Bloque 3: Ejercicio práctico — Patrón Strangler Fig

Este bloque agrega dos carpetas nuevas al repo, sin tocar nada dentro de
`app/` (el monolito viejo queda exactamente igual, acoplamientos ocultos
incluidos):

- **`catalog-service/`** — copia funcional independiente, SOLO del
  módulo catálogo (listar productos / consultar por SKU), con su propia
  copia en memoria del inventario semilla. Corre en el puerto `8001`.
- **`gateway/`** — proxy/router mínimo en el puerto `9000`: las rutas
  que empiezan con `/catalog` van al `catalog-service` nuevo; todo lo
  demás sigue yendo al monolito viejo en `8000`.

Así se ve, en miniatura, el patrón **Strangler Fig**: un módulo se
"corta" del monolito y se pone detrás de un gateway, mientras el resto
del tráfico sigue fluyendo al sistema viejo sin cambios.

### Cómo levantar los 3 procesos (en 3 terminales del mismo Codespace)

**Terminal 1 — monolito viejo (puerto 8000):**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — catalog-service nuevo (puerto 8001):**
```bash
cd catalog-service
pip install --break-system-packages -r requirements.txt   # si no corrió postCreateCommand
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**Terminal 3 — gateway (puerto 9000):**
```bash
cd gateway
pip install --break-system-packages -r requirements.txt   # si no corrió postCreateCommand
uvicorn app.main:app --reload --host 0.0.0.0 --port 9000
```

Abre la pestaña **Ports** y verifica que `8000`, `8001` y `9000` estén
reenviados con sus etiquetas ("Monolito viejo", "Catalog Service nuevo",
"Gateway").

### Qué comparar

1. Confirma que los tres `/health` responden (`8000`, `8001`, `9000`).
2. Consulta un producto **a través del gateway**:
   ```bash
   curl http://localhost:9000/catalog/products/PROD-002
   ```
   Esa respuesta viene del `catalog-service` nuevo, no del monolito.
3. Anota el `stock` de ese producto visto desde:
   - el gateway → `catalog-service` nuevo (`GET /catalog/products/{sku}` vía `9000`)
   - el monolito viejo, directo (`GET /catalog/products/{sku}` vía `8000`)

   Ahora crea un pedido **a través del gateway** (que internamente cae en
   el monolito viejo en `8000`):
   ```bash
   curl -X POST http://localhost:9000/orders \
     -H "Content-Type: application/json" \
     -d '{"sku": "PROD-002", "quantity": 2, "customer_email": "test@correo.com"}'
   ```
   Vuelve a consultar el stock del mismo producto desde ambos lados y
   compara contra lo que anotaste antes. ¿Cambió igual en los dos
   lugares?

### Pregunta guía de cierre

Ya tienen dos copias del "mismo" catálogo que pueden divergir en
silencio simplemente por operar el sistema a través del gateway. Sin
implementarlo todavía: **¿qué patrón usarían para que ambas copias del
inventario se mantengan consistentes mientras el catálogo sigue
"cortado" del monolito, sin volver a fusionarlos en un solo proceso?**
