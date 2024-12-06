from database import init_db
from gui import start_gui

def main():
    # Initialiser la base de données
    init_db()
    
    # Lancer l'interface graphique
    start_gui()

if __name__ == "__main__":
    main()
