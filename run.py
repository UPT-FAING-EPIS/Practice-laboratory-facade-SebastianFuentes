#!/usr/bin/env python3
"""
Script de inicio rápido para el proyecto Facade Pattern.

Este script permite ejecutar rápidamente diferentes funcionalidades
del proyecto sin necesidad de recordar comandos complejos.
"""

import sys
import subprocess
import os
from pathlib import Path


def print_header():
    """Imprime el header del proyecto."""
    print("=" * 60)
    print("  🏛️  FACADE PATTERN - ENTERPRISE ORDER MANAGEMENT")
    print("  📚 Laboratorio de Patrones de Diseño Empresarial")
    print("  👨‍💻 Sebastian Fuentes Avalos - UPT FAING-EPIS")
    print("=" * 60)


def print_menu():
    """Muestra el menú de opciones disponibles."""
    print("\n📋 Opciones disponibles:")
    print("  1. 🚀 Ejecutar demo automatizada")
    print("  2. 🎮 Ejecutar demo interactiva") 
    print("  3. 🧪 Ejecutar todos los tests")
    print("  4. 📊 Ejecutar tests con coverage")
    print("  5. 🔍 Ejecutar solo tests del Facade")
    print("  6. 📈 Ver estadísticas del proyecto")
    print("  7. 🛠️  Verificar calidad del código")
    print("  8. 📦 Instalar dependencias de desarrollo")
    print("  9. 📖 Mostrar documentación")
    print("  0. ❌ Salir")


def run_command(command, description):
    """Ejecuta un comando del sistema."""
    print(f"\n🔄 {description}...")
    print(f"💻 Ejecutando: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando {description}: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n⏹️  {description} interrumpido por el usuario")
        return False


def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    try:
        import pytest
        return True
    except ImportError:
        print("⚠️  Dependencias no encontradas.")
        install = input("¿Deseas instalar las dependencias de desarrollo? (y/N): ")
        if install.lower() == 'y':
            return run_command("pip install -r requirements-dev.txt", "Instalación de dependencias")
        return False


def main():
    """Función principal del script."""
    print_header()
    
    # Verificar que estamos en el directorio correcto
    if not Path("src/order_facade").exists():
        print("❌ Error: Este script debe ejecutarse desde la raíz del proyecto")
        print("📁 Directorio actual:", os.getcwd())
        return 1
    
    while True:
        print_menu()
        
        try:
            choice = input("\n🎯 Selecciona una opción (0-9): ").strip()
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            return 0
        
        if choice == "0":
            print("\n👋 ¡Hasta luego!")
            break
            
        elif choice == "1":
            run_command("python -m src.order_facade.demo", "Demo automatizada")
            
        elif choice == "2":
            run_command("python -m src.order_facade.demo --interactive", "Demo interactiva")
            
        elif choice == "3":
            if check_dependencies():
                run_command("pytest tests/ -v", "Tests unitarios")
            
        elif choice == "4":
            if check_dependencies():
                run_command(
                    "pytest tests/ -v --cov=src/order_facade --cov-report=html --cov-report=term",
                    "Tests con coverage"
                )
                print("\n📊 Reporte HTML generado en: htmlcov/index.html")
            
        elif choice == "5":
            if check_dependencies():
                run_command(
                    "pytest tests/test_facade.py::TestOrderFacade -v",
                    "Tests específicos del Facade"
                )
            
        elif choice == "6":
            print("\n📈 Estadísticas del Proyecto:")
            print("-" * 30)
            
            # Contar archivos Python
            py_files = list(Path(".").rglob("*.py"))
            src_files = list(Path("src").rglob("*.py"))
            test_files = list(Path("tests").rglob("*.py"))
            
            print(f"📁 Total archivos Python: {len(py_files)}")
            print(f"🔧 Archivos fuente: {len(src_files)}")
            print(f"🧪 Archivos de test: {len(test_files)}")
            
            # Contar líneas de código
            total_lines = 0
            for file in src_files:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        total_lines += len(f.readlines())
                except:
                    pass
            
            print(f"📝 Líneas de código (aprox): {total_lines}")
            print(f"📦 Directorio actual: {os.getcwd()}")
            
        elif choice == "7":
            print("\n🛠️  Verificando calidad del código...")
            
            if not check_dependencies():
                continue
                
            print("\n1️⃣ Verificando formato con Black...")
            run_command("black --check src/ tests/", "Verificación de formato")
            
            print("\n2️⃣ Verificando estilo con Flake8...")
            run_command("flake8 src/ tests/", "Verificación de estilo")
            
            print("\n3️⃣ Verificando tipos con MyPy...")
            run_command("mypy src/order_facade/", "Verificación de tipos")
            
        elif choice == "8":
            run_command("pip install -r requirements-dev.txt", "Instalación de dependencias de desarrollo")
            run_command("pip install -e .", "Instalación del paquete en modo desarrollo")
            
        elif choice == "9":
            print("\n📖 Documentación del Proyecto")
            print("-" * 35)
            print("📄 README.md - Documentación principal")
            print("📁 src/order_facade/ - Código fuente documentado")
            print("🧪 tests/ - Casos de prueba con ejemplos")
            print("⚙️  pyproject.toml - Configuración del proyecto")
            print("🔄 .github/workflows/ci.yml - Pipeline CI/CD")
            
            print("\n🌐 Links útiles:")
            print("• GitHub: https://github.com/UPT-FAING-EPIS/Practice-laboratory-facade-SebastianFuentes")
            print("• Patrón Facade: https://refactoring.guru/design-patterns/facade")
            print("• Enterprise Patterns: https://martinfowler.com/eaaCatalog/")
            
        else:
            print("❌ Opción no válida. Por favor selecciona un número del 0 al 9.")
        
        if choice != "0":
            input("\n⏸️  Presiona Enter para continuar...")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())