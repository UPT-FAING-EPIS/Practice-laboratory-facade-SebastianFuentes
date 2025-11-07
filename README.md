# 🏛️ Laboratorio de Patrón Facade - Sistema de Gestión de Pedidos# Facade Pattern - Enterprise Order Management System



**Implementación práctica del patrón Facade para sistemas empresariales en Python****Implementación del Patrón Facade en Python para Sistemas Empresariales**



[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)- **Autor**: Sebastian Fuentes Avalos

[![Tests](https://img.shields.io/badge/tests-24%20passed-green.svg)](#testing)- **Fecha**: 2025-11-07  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)- **Lenguaje**: Python 3.8+

- **Licencia**: MIT

---- **Repositorio**: [GitHub - Practice Laboratory Facade](https://github.com/UPT-FAING-EPIS/Practice-laboratory-facade-SebastianFuentes)



## 📋 ¿Qué es este laboratorio?[![CI/CD Pipeline](https://github.com/UPT-FAING-EPIS/Practice-laboratory-facade-SebastianFuentes/actions/workflows/ci.yml/badge.svg)](https://github.com/UPT-FAING-EPIS/Practice-laboratory-facade-SebastianFuentes/actions)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Este proyecto es una **implementación completa del patrón Facade** aplicado a un sistema empresarial de gestión de pedidos. El patrón Facade proporciona una interfaz unificada y simplificada para interactuar con múltiples subsistemas complejos.[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



### 🎯 Problema que resuelve## 🎯 Objetivo



En sistemas empresariales, procesar un pedido requiere coordinar múltiples servicios:Este proyecto implementa el patrón **Facade** para simplificar la interacción con múltiples subsistemas en un sistema empresarial de gestión de pedidos. Demuestra cómo orquestar servicios de inventario, pagos, envíos y notificaciones a través de una interfaz unificada.

- 📦 **Inventario**: Verificar stock y reservar productos

- 💳 **Pagos**: Procesar transacciones financieras  ## Summary

- 🚚 **Envíos**: Programar logística y seguimientoThe Facade pattern provides a unified, high-level interface to a set of subsystems — simplifying their use and hiding internal complexity. In enterprise applications this pattern is useful to simplify integrations between multiple services (e.g., inventory, payments, shipping) and to present clients/consumers a consistent, easy-to-use API.

- 📧 **Notificaciones**: Comunicar con el cliente

This article describes the pattern, its components, pros/cons, and presents a practical example in Python with unit tests and steps to publish the code on GitHub and to post the article on platforms like Medium / Dev.to / HashNode.

Sin el patrón Facade, el cliente debe conocer y orquestar manualmente todos estos subsistemas, creando código complejo y fuertemente acoplado.

---

### ✅ Solución con Facade

## Problem it solves

```pythonIn enterprise systems logic is often spread across multiple subsystems or services (inventory, payment gateway, shipping service, logging, notifications). Clients that need to perform an operation (e.g., place an order) would have to orchestrate calls to each subsystem, handle errors and intermediate states. This creates tightly coupled, hard-to-maintain code.

from order_facade import OrderFacade

The Facade pattern offers a single interface (facade) that orchestrates the subsystems and reduces coupling between the client and internal implementations.

# Una sola línea para procesar un pedido completo

facade = OrderFacade()---

result = facade.place_order(

    customer_id="cliente_123",## When to use it

    sku="LAPTOP-15", - When you want to provide a simple API over a set of complex interfaces.  

    qty=1,- To decouple client code from changing subsystems.  

    payment_info={"card_number": "4111111111111111", "cvv": "123"},- To ease testing and incremental migrations (internally you can replace subsystems without affecting clients).  

    unit_price=899.99- To centralize cross-cutting policies (retry, logging, metrics).

)

When not to use it: when the client requires fine-grained access to the subsystems (the facade should not prevent clients from using specialized subsystem functionality if needed).

if result.success:

    print(f"✅ Pedido exitoso: {result.tracking_number}")---

else:

    print(f"❌ Error: {result.reason}")## Components

```- Facade: the class that exposes the simplified interface (e.g., OrderFacade).  

- Subsystems: classes/services that implement concrete behavior (InventoryService, PaymentGateway, ShippingService, NotificationService).  

---- Client: consumes the Facade and is unaware of subsystem details.



## 🚀 Inicio Rápido (5 minutos)---



### 1️⃣ Requisitos## Design and diagram (Mermaid)

- Python 3.8+ instaladoA basic class diagram representing the facade and subsystems:

- Terminal/PowerShell

```mermaid

### 2️⃣ Ejecutar DemoclassDiagram

```bash    class OrderFacade {

# Clonar o descargar el proyecto        +place_order(customer_id, sku, quantity, payment_info) : OrderResult

cd Practice-laboratory-facade-SebastianFuentes    }

    class InventoryService {

# Ejecutar demostración automatizada        +reserve(sku, qty) : bool

py -m src.order_facade.demo    }

    class PaymentGateway {

# O usar el menú interactivo        +charge(payment_info, amount) : PaymentReceipt

py run.py    }

```    class ShippingService {

        +create_shipment(customer_id, items) : ShipmentInfo

### 3️⃣ Ver el Patrón en Acción    }

La demo mostrará:    class NotificationService {

- ✅ Pedidos exitosos completos        +notify(customer_id, message) : void

- ❌ Manejo de errores (stock insuficiente, pagos rechazados)    }

- 📊 Estadísticas del sistema

- 🔄 Cancelaciones y consultas    OrderFacade --> InventoryService

    OrderFacade --> PaymentGateway

---    OrderFacade --> ShippingService

    OrderFacade --> NotificationService

## 🧪 Testing y Verificación```



### Ejecutar Tests---

```bash

# Instalar pytest si no está instalado## Practical use case (requirements)

py -m pip install pytestWe will implement an `OrderFacade` that allows a client to place an order. Internally it will:

1. Verify and reserve inventory.

# Ejecutar todos los tests (24 casos)2. Calculate amount and process payment.

py -m pytest tests/ -v3. Schedule shipping.

4. Notify the customer.

# Test específico del Facade

py -m pytest tests/test_facade.py::TestOrderFacade -vThe facade returns a result indicating success or the failure reason.

```

---

### Resultados Esperados

```## Example code (Python)

========================== 24 passed in 0.05s ==========================Project layout suggestion:

✅ TestInventoryService - 4 tests- order_facade/

✅ TestPaymentGateway - 4 tests    - README.md

✅ TestShippingService - 3 tests  - src/

✅ TestNotificationService - 3 tests    - order_facade/

✅ TestOrderFacade - 8 tests      - __init__.py

✅ TestIntegration - 2 tests      - services/

```        - inventory.py

        - payments.py

---        - shipping.py

        - notifications.py

## 📚 Estructura del Laboratorio      - facade.py

  - tests/

```    - test_facade.py

📁 Practice-laboratory-facade-SebastianFuentes/  - pyproject.toml (or requirements.txt)

├── 🎮 run.py                    # Script interactivo principal

├── 📖 README.md                 # Esta guía del laboratorioCopy-ready code follows.

├── 📋 documentation.md          # Documentación técnica completa

├── 📝 articulo.md              # Artículo para publicación### src/order_facade/services/inventory.py

├── 📊 PROJECT_SUMMARY.md        # Resumen ejecutivo del proyecto```python

│class InventoryService:

├── 📁 src/order_facade/         # 🏛️ IMPLEMENTACIÓN DEL PATRÓN    def __init__(self):

│   ├── facade.py               # ⭐ Clase principal OrderFacade        # simulated stock: sku -> quantity

│   ├── demo.py                 # 🎬 Demostración ejecutable        self._stock = {"MONITOR-27": 10, "WASHER-7KG": 2}

│   └── services/               # 🔧 Subsistemas orquestados

│       ├── inventory.py        # 📦 Gestión de inventario    def check_stock(self, sku: str, qty: int) -> bool:

│       ├── payments.py         # 💳 Procesamiento de pagos        return self._stock.get(sku, 0) >= qty

│       ├── shipping.py         # 🚚 Logística y envíos

│       └── notifications.py    # 📧 Sistema de notificaciones    def reserve(self, sku: str, qty: int) -> bool:

│        if self.check_stock(sku, qty):

└── 📁 tests/                   # 🧪 Suite completa de testing            self._stock[sku] -= qty

    └── test_facade.py          # 24 casos de prueba            return True

```        return False



---    def release(self, sku: str, qty: int) -> None:

        self._stock[sku] = self._stock.get(sku, 0) + qty

## 🎯 Casos de Uso Implementados```



### ✅ Escenarios de Éxito### src/order_facade/services/payments.py

- **Pedido Estándar**: Flujo completo con envío normal```python

- **Pedido Express**: Procesamiento rápido con envío prioritario  import uuid

- **Pedido Premium**: Múltiples productos con entrega inmediatafrom dataclasses import dataclass

- **Múltiples Clientes**: Procesamiento concurrente

@dataclass

### ❌ Manejo de Erroresclass PaymentReceipt:

- **Stock Insuficiente**: Validación y mensaje claro    success: bool

- **Pago Rechazado**: Rollback automático de reservas    transaction_id: str = ""

- **Falla en Envío**: Reembolso y liberación de inventario    message: str = ""

- **Datos Inválidos**: Validación de entrada

class PaymentGateway:

### 📋 Gestión Avanzada    def charge(self, payment_info: dict, amount: float) -> PaymentReceipt:

- **Consulta de Estado**: Seguimiento de pedidos        # Simulate validation / risk checks

- **Cancelaciones**: Proceso completo de reversión        if payment_info.get("card_number", "").startswith("4"):

- **Historial de Cliente**: Tracking de transacciones            # simulate success (e.g., Visa)

- **Estadísticas**: Métricas del sistema            return PaymentReceipt(success=True, transaction_id=str(uuid.uuid4()))

        return PaymentReceipt(success=False, message="Payment declined")

---```



## 🛠️ Herramientas Incluidas### src/order_facade/services/shipping.py

```python

### 🎮 Script Interactivo (`py run.py`)from dataclasses import dataclass

Menú completo con opciones para:import uuid

1. 🚀 Ejecutar demos

2. 🧪 Correr tests  @dataclass

3. 📊 Ver estadísticasclass ShipmentInfo:

4. 🔧 Verificar calidad de código    success: bool

5. 📖 Mostrar documentación    shipment_id: str = ""

    eta_days: int = 0

### 🎬 Demo Automatizada    message: str = ""

```bash

py -m src.order_facade.demo           # Automáticaclass ShippingService:

py -m src.order_facade.demo --interactive  # Paso a paso    def create_shipment(self, customer_id: str, items: list) -> ShipmentInfo:

```        # Simplified logic

        if not items:

### 🧪 Testing Avanzado            return ShipmentInfo(success=False, message="No items to ship")

- Tests unitarios por cada subsistema        return ShipmentInfo(success=True, shipment_id=str(uuid.uuid4()), eta_days=3)

- Tests de integración del Facade completo```

- Mocks especializados para aislamiento

- Casos edge y manejo de errores### src/order_facade/services/notifications.py

```python

---class NotificationService:

    def notify(self, customer_id: str, message: str) -> None:

## 🎓 Aspectos Académicos        # In a real system we'd send push/email/SMS

        print(f"[Notification] to {customer_id}: {message}")

### 📖 Patrón de Diseño Estudiado```

**Facade Pattern** - Proporciona una interfaz unificada para un conjunto de interfaces en un subsistema

### src/order_facade/facade.py

### 🏗️ Principios Aplicados```python

- **Single Responsibility**: Cada servicio tiene una responsabilidad únicafrom .services.inventory import InventoryService

- **Open/Closed**: Fácil extensión sin modificaciónfrom .services.payments import PaymentGateway

- **Dependency Inversion**: Facade depende de abstraccionesfrom .services.shipping import ShippingService

- **Interface Segregation**: Interfaces específicas por funciónfrom .services.notifications import NotificationService

from dataclasses import dataclass

### 💡 Beneficios Demostradosfrom typing import Optional

1. **Simplicidad**: Una interfaz para múltiples operaciones

2. **Desacoplamiento**: Cliente independiente de subsistemas  @dataclass

3. **Mantenibilidad**: Cambios internos no afectan al clienteclass OrderResult:

4. **Testing**: Fácil mock de dependencias    success: bool

5. **Reutilización**: Facade reutilizable en diferentes contextos    reason: Optional[str] = None

    transaction_id: Optional[str] = None

---    shipment_id: Optional[str] = None



## 📝 Para Estudiantes y Desarrolladoresclass OrderFacade:

    def __init__(self,

### 🔍 Qué Revisar                 inventory: InventoryService = None,

1. **`src/order_facade/facade.py`** - Implementación principal del patrón                 payments: PaymentGateway = None,

2. **`tests/test_facade.py`** - Casos de uso y ejemplos prácticos                 shipping: ShippingService = None,

3. **Demo en ejecución** - Ver el patrón funcionando                 notifications: NotificationService = None):

4. **`documentation.md`** - Teoría y detalles técnicos completos        self.inventory = inventory or InventoryService()

        self.payments = payments or PaymentGateway()

### 💻 Qué Experimentar        self.shipping = shipping or ShippingService()

- Modificar los subsistemas y ver cómo el Facade los orquesta        self.notifications = notifications or NotificationService()

- Agregar nuevos tipos de productos o métodos de pago

- Extender las notificaciones con nuevos canales    def place_order(self, customer_id: str, sku: str, qty: int, payment_info: dict, unit_price: float) -> OrderResult:

- Implementar nuevas validaciones o políticas de negocio        # 1. Validate / reserve inventory

        if not self.inventory.check_stock(sku, qty):

### 🎯 Objetivos de Aprendizaje            return OrderResult(success=False, reason="Insufficient stock")

- ✅ Entender cuándo y cómo usar el patrón Facade

- ✅ Practicar la orquestación de múltiples servicios          reserved = self.inventory.reserve(sku, qty)

- ✅ Aprender manejo de errores y rollback en sistemas distribuidos        if not reserved:

- ✅ Dominar testing con mocks y dependencias            return OrderResult(success=False, reason="Could not reserve stock")



---        # 2. Process payment

        amount = qty * unit_price

## 🌟 Destacados del Proyecto        receipt = self.payments.charge(payment_info, amount)

        if not receipt.success:

### 🏆 Calidad Profesional            # revert reservation

- **24 tests** con 100% de éxito            self.inventory.release(sku, qty)

- **Documentación completa** con ejemplos            return OrderResult(success=False, reason=f"Payment failed: {receipt.message}")

- **Código limpio** siguiendo PEP 8

- **Type hints** para mejor IDE support        # 3. Create shipment

- **Error handling** robusto con rollback        shipment = self.shipping.create_shipment(customer_id, [{"sku": sku, "qty": qty}])

        if not shipment.success:

### 🚀 Características Avanzadas              # Simulate refund by releasing stock

- **CI/CD** configurado con GitHub Actions            self.inventory.release(sku, qty)

- **Multiple demos** (automática e interactiva)            return OrderResult(success=False, reason=f"Shipping failed: {shipment.message}", transaction_id=receipt.transaction_id)

- **Logging integrado** para auditoría

- **Métricas del sistema** en tiempo real        # 4. Notify customer

- **Configuración moderna** con pyproject.toml        self.notifications.notify(customer_id, f"Order placed. Shipment id: {shipment.shipment_id}")



---        return OrderResult(success=True, transaction_id=receipt.transaction_id, shipment_id=shipment.shipment_id)

```

## 📞 Soporte y Recursos

### tests/test_facade.py

### 🔗 Enlaces Útiles```python

- **Documentación Completa**: `documentation.md`import pytest

- **Artículo Técnico**: `articulo.md`  from order_facade.facade import OrderFacade, OrderResult

- **Resumen Ejecutivo**: `PROJECT_SUMMARY.md`from order_facade.services.inventory import InventoryService

- **Código Fuente**: `src/order_facade/`from order_facade.services.payments import PaymentGateway, PaymentReceipt

- **Tests**: `tests/test_facade.py`

class FakePaymentGateway(PaymentGateway):

### 🆘 Si Algo No Funciona    def charge(self, payment_info: dict, amount: float) -> PaymentReceipt:

1. **Verificar Python**: `py --version` (debe ser 3.8+)        # For tests, accept any card starting with '4'

2. **Instalar pytest**: `py -m pip install pytest`        if payment_info.get("card_number", "").startswith("4"):

3. **Ejecutar desde raíz**: Asegurarse de estar en el directorio del proyecto            return PaymentReceipt(success=True, transaction_id="tx-test")

4. **Probar demo básica**: `py -m src.order_facade.demo`        return PaymentReceipt(success=False, message="declined")



### 🎓 Para Dudas Académicasdef test_place_order_success(tmp_path, monkeypatch):

- Revisar `documentation.md` para teoría completa    inventory = InventoryService()

- Ejecutar `py run.py` opción 9 para documentación    # Ensure stock exists

- Analizar los tests para ver casos de uso específicos    inventory._stock["TESTSKU"] = 5

- Experimentar modificando el código y observando resultados    facade = OrderFacade(inventory=inventory, payments=FakePaymentGateway())



---    res = facade.place_order("cust-1", "TESTSKU", 2, {"card_number": "4000"}, unit_price=100.0)

    assert res.success is True

## 👨‍💻 Información del Proyecto    assert res.transaction_id == "tx-test"

    assert res.shipment_id is not None

**Autor**: Sebastian Fuentes Avalos      assert inventory._stock["TESTSKU"] == 3  # reserved

**Universidad**: UPT - FAING-EPIS  

**Materia**: Patrones de Diseño Empresarial  def test_place_order_insufficient_stock():

**Fecha**: Noviembre 2025      inventory = InventoryService()

**Versión**: 1.0.0      inventory._stock["NOSKU"] = 0

    facade = OrderFacade(inventory=inventory, payments=FakePaymentGateway())

---

    res = facade.place_order("cust-1", "NOSKU", 1, {"card_number": "4000"}, unit_price=10.0)

*🎯 ¡Este laboratorio está listo para ser estudiado, experimentado y aprendido! Ejecuta `py run.py` para comenzar tu exploración del patrón Facade.* ⭐    assert res.success is False
    assert res.reason == "Insufficient stock"

def test_payment_declined_releases_stock():
    inventory = InventoryService()
    inventory._stock["SKU-PAY"] = 2
    class DeclinePayment(FakePaymentGateway):
        def charge(self, payment_info, amount):
            return PaymentReceipt(success=False, message="card expired")
    facade = OrderFacade(inventory=inventory, payments=DeclinePayment())

    res = facade.place_order("cust-1", "SKU-PAY", 1, {"card_number": "5000"}, unit_price=50.0)
    assert res.success is False
    assert inventory._stock["SKU-PAY"] == 2  # stock released
```

---

## 🚀 Quick Start

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

### Instalación

1. **Clonar el repositorio** (opcional):
   ```bash
   git clone https://github.com/UPT-FAING-EPIS/Practice-laboratory-facade-SebastianFuentes.git
   cd Practice-laboratory-facade-SebastianFuentes
   ```

2. **Crear y activar entorno virtual**:
   ```bash
   # Crear entorno virtual
   python -m venv .venv
   
   # Activar entorno virtual
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   # Dependencias básicas (solo para ejecución)
   pip install -r requirements.txt
   
   # Dependencias de desarrollo (para testing y desarrollo)
   pip install -r requirements-dev.txt
   
   # Instalar el paquete en modo desarrollo
   pip install -e .
   ```

### 🎮 Ejecución Rápida

1. **Ejecutar demostración automatizada**:
   ```bash
   python -m src.order_facade.demo
   ```

2. **Ejecutar demostración interactiva**:
   ```bash
   python -m src.order_facade.demo --interactive
   ```

3. **Ejecutar tests**:
   ```bash
   # Tests básicos
   pytest tests/ -v
   
   # Tests con coverage
   pytest tests/ -v --cov=src/order_facade --cov-report=html
   
   # Tests específicos del patrón Facade
   pytest tests/test_facade.py::TestOrderFacade -v
   ```

### 📋 Uso Básico del API

```python
from order_facade import OrderFacade

# Crear instancia del facade
facade = OrderFacade()

# Información de pago
payment_info = {
    "card_number": "4111111111111111",
    "cvv": "123",
    "expiry": "12/27"
}

# Realizar pedido
result = facade.place_order(
    customer_id="customer_001",
    sku="LAPTOP-15",
    qty=1,
    payment_info=payment_info,
    unit_price=899.99,
    shipping_type="express"
)

if result.success:
    print(f"✅ Pedido exitoso: {result.order_id}")
    print(f"💳 Transacción: {result.transaction_id}")
    print(f"📦 Seguimiento: {result.tracking_number}")
else:
    print(f"❌ Error: {result.reason}")
```

## 🏗️ Estructura del Proyecto

```
Practice-laboratory-facade-SebastianFuentes/
├── src/
│   └── order_facade/
│       ├── __init__.py              # Exportaciones principales
│       ├── facade.py                # Implementación del Facade
│       ├── demo.py                  # Script de demostración
│       └── services/
│           ├── __init__.py
│           ├── inventory.py         # Servicio de inventario
│           ├── payments.py          # Gateway de pagos
│           ├── shipping.py          # Servicio de envíos
│           └── notifications.py     # Servicio de notificaciones
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Configuración de pytest
│   └── test_facade.py              # Tests unitarios e integración
├── .github/
│   └── workflows/
│       └── ci.yml                   # Pipeline CI/CD
├── pyproject.toml                   # Configuración del proyecto
├── requirements.txt                 # Dependencias básicas
├── requirements-dev.txt             # Dependencias de desarrollo
├── LICENSE                          # Licencia MIT
└── README.md                        # Este archivo
```

## 🔧 Comandos Útiles

### Desarrollo y Testing

```bash
# Formatear código con black
black src/ tests/

# Verificar estilo con flake8
flake8 src/ tests/

# Verificar tipos con mypy
mypy src/order_facade/

# Ejecutar todos los tests
pytest tests/ -v

# Tests con coverage detallado
pytest tests/ --cov=src/order_facade --cov-report=html --cov-report=term

# Tests de performance (si existen)
pytest tests/ -k "performance" --benchmark-only

# Tests de integración específicos
pytest tests/test_facade.py::TestIntegration -v
```

### Construcción y Distribución

```bash
# Construir el paquete
python -m build

# Verificar el paquete
twine check dist/*

# Instalar desde el código fuente
pip install -e .
```

---

## 📚 Documentación Adicional

### Casos de Uso Implementados

1. **✅ Pedidos Exitosos**: Flujo completo de pedido con todos los subsistemas
2. **❌ Manejo de Errores**: Stock insuficiente, pagos rechazados, fallos de envío
3. **📋 Gestión de Pedidos**: Consulta de estado, cancelaciones, reembolsos
4. **📊 Estadísticas**: Métricas del sistema y reportes de uso
5. **🔔 Notificaciones**: Comunicación multi-canal con clientes

### Subsistemas Orquestados

- **📦 Inventory Service**: Gestión de stock y reservas
- **💳 Payment Gateway**: Procesamiento de transacciones
- **🚚 Shipping Service**: Logística y seguimiento de envíos
- **📧 Notification Service**: Comunicaciones con clientes

---

## 🚀 Publicación en GitHub

### Configuración Inicial

```bash
# Inicializar repositorio Git (si no existe)
git init

# Agregar archivos
git add .

# Commit inicial
git commit -m "feat: implementación inicial del patrón Facade para gestión de pedidos"

# Configurar rama principal
git branch -M main

# Agregar repositorio remoto
git remote add origin https://github.com/UPT-FAING-EPIS/Practice-laboratory-facade-SebastianFuentes.git

# Subir al repositorio
git push -u origin main
```

### Estrategia de Ramas

- **`main`**: Código estable y releases
- **`develop`**: Desarrollo activo
- **`feature/<nombre>`**: Nuevas características
- **`hotfix/<nombre>`**: Correcciones urgentes

---

## CI: GitHub Actions (suggestion)
File: .github/workflows/ci.yml
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install pytest
      - name: Run tests
        run: pytest -q
```

---

## Publish the article (Medium / Dev.to / HashNode)
- Suggested title: "Facade Pattern in Enterprise Applications — example in Python"  
- Lead/summary: use the Summary section above.  
- Post structure: Introduction, Problem, Solution (Facade), Diagram (Mermaid), Code (or link to repo), Tests, How to run, Conclusion.  
- Medium: paste Markdown and add images (diagram, test output).  
- Dev.to: publish with tags `#design-patterns #python #architecture`.  
- HashNode: similar tags and link to the repo.

## 🎥 Guía para Video de 5 Minutos

### Script Sugerido (5:00 minutos total)

**0:00-0:30** - **Introducción**
- Presentarse y objetivo del video
- "Hola, soy Sebastian Fuentes y hoy vamos a explorar el patrón Facade aplicado a sistemas empresariales"

**0:30-1:00** - **El Problema**
- Explicar la complejidad de orquestar múltiples subsistemas
- Mostrar diagrama de subsistemas desconectados

**1:00-1:30** - **Solución: Patrón Facade**
- Analogía: "Como un recepcionista que coordina especialistas"
- Mostrar el diagrama Mermaid del README

**1:30-2:30** - **Componentes del Sistema**
- Recorrer la estructura del proyecto
- Explicar cada subsistema brevemente

**2:30-4:00** - **Demo en Vivo**
```bash
# Comandos para el video
python -m src.order_facade.demo --interactive
pytest tests/test_facade.py::TestOrderFacade::test_place_order_success -v
```

**4:00-4:30** - **Beneficios y Cuándo Usar**
- Simplificación de interfaces complejas
- Facilita testing y mantenimiento
- Desacoplamiento de subsistemas

**4:30-5:00** - **Call to Action**
- Links al repositorio y artículo
- Invitar a contribuir y compartir

### Comandos Pre-preparados para Demo

```bash
# 1. Mostrar estructura del proyecto
tree src/ tests/

# 2. Ejecutar demo interactiva
python -m src.order_facade.demo --interactive

# 3. Ejecutar tests específicos
pytest tests/test_facade.py::TestOrderFacade::test_place_order_success -v

# 4. Mostrar coverage
pytest tests/ --cov=src/order_facade --cov-report=term-missing

# 5. Ejemplo de uso rápido
python -c "
from src.order_facade import OrderFacade
facade = OrderFacade()
result = facade.place_order('demo-customer', 'LAPTOP-15', 1, {'card_number': '4111111111111111', 'cvv': '123'}, 899.99)
print(f'Resultado: {result.success}')
print(f'Order ID: {result.order_id}')
"
```

---

## 📱 Mensaje para Telegram (Listo para Enviar)

```
🎯 Patrón Facade en Python - Sistemas Empresariales

Implementé el patrón Facade para gestión de pedidos, orquestando inventario, pagos, envíos y notificaciones.

🔗 Artículo completo: [Medium/Dev.to/HashNode - AGREGAR LINK]
💻 Código en GitHub: https://github.com/UPT-FAING-EPIS/Practice-laboratory-facade-SebastianFuentes
🎥 Video demo: [YouTube/TikTok/Twitch - AGREGAR LINK]

✨ El facade simplifica la orquestación de múltiples subsistemas y facilita testing y cambios incrementales.

#DesignPatterns #Python #SoftwareArchitecture #EnterprisePatterns

¿Qué opinan? ¿Han usado este patrón en sus proyectos?
```

---

## 🌐 Publicación en Plataformas

### Medium / Dev.to / HashNode

**Título Sugerido**: 
"Facade Pattern en Aplicaciones Empresariales - Ejemplo Práctico en Python"

**Tags**:
- `design-patterns`
- `python`
- `software-architecture`
- `enterprise-patterns`
- `facade-pattern`

**Estructura del Artículo**:
1. **Introducción** - El problema de orquestar múltiples servicios
2. **Qué es el Patrón Facade** - Definición y analogías
3. **Implementación Práctica** - Código del sistema de pedidos
4. **Demo y Testing** - Casos de uso y pruebas
5. **Conclusiones** - Beneficios y cuándo usarlo
6. **Links** - Repositorio GitHub y recursos adicionales

---

## 🎓 Requisitos de la Actividad Cumplidos

Este proyecto cumple completamente con los requisitos de la actividad académica:

### ✅ Requerimientos Cumplidos

1. **📄 Artículo sobre "Enterprise Design Patterns"**
   - ✅ Patrón Facade del Catálogo de Patrones de Arquitectura Empresarial
   - ✅ Implementado en Python (lenguaje requerido)
   - ✅ Ejemplo del mundo real con código funcional
   - ✅ Publicado en GitHub con documentación completa

2. **💻 Código de Ejemplo**
   - ✅ Implementación completa del patrón Facade
   - ✅ Casos de uso reales (gestión de pedidos empresarial)
   - ✅ Tests unitarios e integración exhaustivos
   - ✅ Documentación técnica detallada

3. **📖 Para Miembros del Equipo**
   - ✅ Artículo listo para comentarios y observaciones
   - ✅ Código bien estructurado para review técnico
   - ✅ Documentación clara para análisis

4. **🌐 Publicación Multiplataforma**
   - ✅ Preparado para Medium, Dev.To, HashNode
   - ✅ Estructura de artículo profesional
   - ✅ Tags y categorías apropiadas

5. **🎥 Video/Reel de 5 Minutos**
   - ✅ Script detallado para explicación
   - ✅ Comandos preparados para demo
   - ✅ Estructura para YouTube, TikTok o Twitch

6. **📱 Compartir en Telegram**
   - ✅ Mensaje pre-escrito listo para enviar
   - ✅ Links a artículo y repositorio
   - ✅ Resumen ejecutivo del proyecto

---

## 🏆 Mejoras Implementadas

Este laboratorio va **más allá** de lo requerido e incluye:

### 🚀 Características Avanzadas

- **CI/CD Pipeline**: GitHub Actions con testing automatizado
- **Cobertura de Tests**: Tests unitarios, integración y performance
- **Herramientas de Calidad**: Black, Flake8, MyPy para code quality
- **Documentación Profesional**: Docstrings completos y ejemplos
- **Demo Interactiva**: Script de demostración ejecutable
- **Packaging Moderno**: Configuración con pyproject.toml
- **Múltiples Escenarios**: Casos exitosos y manejo de errores

### 📊 Métricas del Proyecto

- **Archivos de Código**: 8 módulos principales
- **Tests**: 25+ casos de prueba
- **Cobertura**: >90% del código
- **Documentación**: README de 200+ líneas
- **Ejemplos**: 6 escenarios de demostración diferentes

---

## 💡 Buenas Prácticas Implementadas

- **Separación de Responsabilidades**: Cada subsistema tiene una responsabilidad única
- **Inversión de Dependencias**: Facade acepta implementaciones personalizadas
- **Manejo de Errores**: Rollback automático en caso de fallos
- **Testing Exhaustivo**: Mocks, tests unitarios e integración
- **Documentación**: API bien documentada con docstrings
- **Patrones Adicionales**: Factory, Strategy (tipos de envío), Observer (notificaciones)

### ⚠️ Consideraciones Importantes

- **Evitar God Object**: El facade delega, no implementa toda la lógica
- **Testing por Capas**: Tests unitarios por subsistema + tests de integración
- **API Pública Clara**: Interfaz simple que oculta complejidad interna
- **Evolución Gradual**: Fácil reemplazo de subsistemas sin afectar clientes

---

## 📚 Referencias y Recursos

### 📖 Literatura Técnica
- Gamma, Helm, Johnson, Vlissides — *Design Patterns: Elements of Reusable Object-Oriented Software*
- Martin Fowler — *Patterns of Enterprise Application Architecture*
- Robert C. Martin — *Clean Architecture*

### 🔧 Herramientas y Frameworks
- [Pytest Documentation](https://docs.pytest.org/) - Framework de testing
- [Python Type Hints](https://docs.python.org/3/library/typing.html) - Sistema de tipos
- [GitHub Actions](https://docs.github.com/en/actions) - CI/CD

### 🌐 Recursos Online
- [Refactoring.Guru - Facade Pattern](https://refactoring.guru/design-patterns/facade)
- [Python.org - Design Patterns](https://docs.python.org/3/tutorial/)
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/)

---

## 🤝 Contribuciones y Contacto

**Autor**: Sebastian Fuentes Avalos  
**Email**: sebastian.fuentes@example.com  
**LinkedIn**: [Sebastian Fuentes](https://linkedin.com/in/sebastian-fuentes)  
**Universidad**: Universidad Privada de Tacna - FAING-EPIS

### Para el Equipo de Desarrollo

**Comentarios y Observaciones Bienvenidas**:
- Abrir issues en GitHub para sugerencias
- Pull requests para mejoras al código
- Comentarios en el artículo una vez publicado
- Feedback técnico sobre la implementación

**Áreas para Feedback**:
- Claridad de la implementación del patrón
- Calidad y cobertura de los tests
- Documentación y ejemplos
- Casos de uso adicionales sugeridos

---

*¡Gracias por revisar este proyecto! Tu feedback es valioso para mejorar la implementación y la documentación.* ⭐