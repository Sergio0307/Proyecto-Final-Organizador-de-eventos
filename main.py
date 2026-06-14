# main.py
import frontend
import backend

def main():
    print("=" * 50)
    print("🎬 CINE EVENTOS PRO - STARTING APPLICATION 🎬")
    print("=" * 50)
    
    try:
        print("📂 Loading data from JSON files...")
        gestor_datos = backend.GestorDatos()
        logica_negocio = backend.LogicaNegocio(gestor_datos)
        print("✅ Data loaded successfully")
        
        print("🖥️  Starting graphical interface...")
        app = frontend.AplicacionEventos(gestor_datos, logica_negocio)
        
        print("\n" + "=" * 50)
        print("🎉 APPLICATION READY - Enjoy your cinematic journey!")
        print("=" * 50 + "\n")
        
        app.ejecutar()
        
        print("👋 Application closed. Data saved successfully.")
        
    except Exception as e:
        print(f"\n❌ ERROR: Could not start application")
        print(f"Error details: {e}")
        print("\nPlease ensure you have installed all requirements:")
        print("pip install Pillow tkcalendar")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()