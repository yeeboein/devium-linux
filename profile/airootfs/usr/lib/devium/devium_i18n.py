"""Translations for the Devium apps.

T("English text") returns the text in the user's language (from $LANGUAGE / $LANG,
or ~/.config/devium/language), falling back to English. Languages: ga (Irish / Gaeilge),
es, fr, de, hu (Hungarian / Magyar). To add a language, add a column to STRINGS below - missing entries stay English.
"""
import os

LANGUAGES = {"en": "English", "ga": "Gaeilge (Irish)", "es": "Español", "fr": "Français", "de": "Deutsch",
             "hu": "Magyar (Hungarian)"}

# English: (Irish, Spanish, French, German)
STRINGS = {
    "Devium Tools": ("Uirlisí Devium", "Herramientas de Devium", "Outils Devium", "Devium-Werkzeuge"),
    "Everything to look after your computer, in one place.":
        ("Gach rud chun aire a thabhairt do do ríomhaire, in aon áit amháin.",
         "Todo para cuidar tu ordenador, en un solo lugar.",
         "Tout pour prendre soin de votre ordinateur, au même endroit.",
         "Alles, um deinen Computer zu pflegen, an einem Ort."),
    "Home": ("Baile", "Inicio", "Accueil", "Start"),
    "App Manager": ("Bainisteoir Aipeanna", "Gestor de aplicaciones", "Gestionnaire d'applications", "App-Verwaltung"),
    "Updates": ("Nuashonruithe", "Actualizaciones", "Mises à jour", "Aktualisierungen"),
    "Speed and memory": ("Luas agus cuimhne", "Velocidad y memoria", "Vitesse et mémoire", "Tempo und Speicher"),
    "Battery": ("Ceallra", "Batería", "Batterie", "Akku"),
    "Privacy": ("Príobháideacht", "Privacidad", "Confidentialité", "Datenschutz"),
    "Printers and scanners": ("Printéirí agus scanóirí", "Impresoras y escáneres", "Imprimantes et scanners", "Drucker und Scanner"),
    "Developer": ("Forbróir", "Desarrollo", "Développement", "Entwicklung"),
    "Coming from Windows": ("Ag teacht ó Windows", "Si vienes de Windows", "Vous venez de Windows", "Umstieg von Windows"),
    "Accessibility": ("Inrochtaineacht", "Accesibilidad", "Accessibilité", "Barrierefreiheit"),
    "Language": ("Teanga", "Idioma", "Langue", "Sprache"),
    "Get help": ("Faigh cabhair", "Obtener ayuda", "Obtenir de l'aide", "Hilfe holen"),
    "Remove": ("Bain", "Quitar", "Supprimer", "Entfernen"),
    "Refresh": ("Athnuaigh", "Actualizar", "Actualiser", "Aktualisieren"),
    "Search": ("Cuardaigh", "Buscar", "Rechercher", "Suchen"),
    "Name": ("Ainm", "Nombre", "Nom", "Name"),
    "Size": ("Méid", "Tamaño", "Taille", "Größe"),
    "Average RAM": ("Meán RAM", "RAM media", "RAM moyenne", "Durchschn. RAM"),
    "Type": ("Cineál", "Tipo", "Type", "Typ"),
    "not measured yet": ("gan tomhas fós", "aún sin medir", "pas encore mesuré", "noch nicht gemessen"),
    "Install updates": ("Suiteáil nuashonruithe", "Instalar actualizaciones", "Installer les mises à jour", "Updates installieren"),
    "Undo last update": ("Cealaigh an nuashonrú deireanach", "Deshacer la última actualización",
                         "Annuler la dernière mise à jour", "Letztes Update rückgängig machen"),
    "Automatic updates": ("Nuashonruithe uathoibríocha", "Actualizaciones automáticas", "Mises à jour automatiques",
                          "Automatische Updates"),
    "Arch Linux news": ("Nuacht Arch Linux", "Noticias de Arch Linux", "Actualités Arch Linux", "Arch-Linux-Neuigkeiten"),
    "Make it faster": ("Déan níos tapúla é", "Hazlo más rápido", "Rendre plus rapide", "Schneller machen"),
    "Low-RAM mode": ("Mód RAM íseal", "Modo poca RAM", "Mode peu de RAM", "Wenig-RAM-Modus"),
    "Charge limit": ("Teorainn luchtaithe", "Límite de carga", "Limite de charge", "Ladegrenze"),
    "Battery health": ("Sláinte an cheallra", "Salud de la batería", "Santé de la batterie", "Akkuzustand"),
    "Firewall": ("Balla dóiteáin", "Cortafuegos", "Pare-feu", "Firewall"),
    "Set up printing": ("Socraigh priontáil", "Configurar impresión", "Configurer l'impression", "Drucken einrichten"),
    "Connect Git and GitHub": ("Ceangail Git agus GitHub", "Conectar Git y GitHub", "Connecter Git et GitHub",
                               "Git und GitHub verbinden"),
    "Containers": ("Coimeádáin", "Contenedores", "Conteneurs", "Container"),
    "Report a problem": ("Tuairiscigh fadhb", "Informar de un problema", "Signaler un problème", "Problem melden"),
    "Fix common problems": ("Deisigh fadhbanna coitianta", "Arreglar problemas comunes", "Réparer les problèmes courants",
                            "Häufige Probleme beheben"),
    "Open Support": ("Oscail Tacaíocht", "Abrir Soporte", "Ouvrir l'aide", "Hilfe öffnen"),
    "Send": ("Seol", "Enviar", "Envoyer", "Senden"),
    "Cancel": ("Cealaigh", "Cancelar", "Annuler", "Abbrechen"),
    "Close": ("Dún", "Cerrar", "Fermer", "Schließen"),
    "Working...": ("Ag obair...", "Trabajando...", "En cours...", "Wird ausgeführt..."),
    "Done": ("Críochnaithe", "Hecho", "Terminé", "Fertig"),
    "Something went wrong": ("Chuaigh rud éigin mícheart", "Algo salió mal", "Un problème est survenu",
                             "Etwas ist schiefgelaufen"),
    "Larger text": ("Téacs níos mó", "Texto más grande", "Texte plus grand", "Größere Schrift"),
    "Screen reader": ("Léitheoir scáileáin", "Lector de pantalla", "Lecteur d'écran", "Bildschirmleser"),
    "Zoom": ("Súmáil", "Zoom", "Zoom", "Zoom"),
    "Sticky keys": ("Eochracha greamaitheacha", "Teclas especiales", "Touches rémanentes", "Einrastfunktion"),
    "Reduce motion": ("Laghdaigh gluaiseacht", "Reducir movimiento", "Réduire les animations", "Bewegung reduzieren"),
    "Restart the app to see the new language.": (
        "Atosaigh an aip chun an teanga nua a fheiceáil.", "Reinicia la aplicación para ver el nuevo idioma.",
        "Redémarrez l'application pour voir la nouvelle langue.", "Starte die App neu, um die neue Sprache zu sehen."),
}

_COLS = ["ga", "es", "fr", "de"]

# Hungarian (Magyar), contributed by the Devium community
HU = {
    "Version": "Verzió",
    "Beta": "Béta",
    "KDE Plasma edition": "KDE Plazma kiadás",
    "A light, fast Arch Linux desktop made for coding. Easy for beginners, nice for pros, and it runs well on "
    "older laptops. After installing, Devium Configure lets you pick exactly what you want, so nothing you "
    "don't need gets installed.":
        "Egy pehelysúlyú, gyors Arch Linux disztribúció kódoláshoz. Könnyű kezdőknek, jó profiknak, és jól fut "
        "régebbi gépeken. A telepítés után a Devium Configure-ral kiválaszthatod, pontosan mit szeretnél, így "
        "semmi olyan nem lesz telepítve, ami nem kell.",
    "Developers": "Fejlesztők",
    "Owner": "Tulajdonos",
    "Built with": "Készítve",
    "Dynamic-Island-style pill": "Dynamic-Island stílusú tabletta",
    "Lighter KDE Plasma": "Könnyebb KDE Plazma",
    "The base system": "A rendszeralap",
    "The desktop": "Az asztali környezet",
    "Live preview login: user devium, password devium":
        "Előnézet bejelentkezési adatok: felhasználó devium, jelszó devium",
    "Devium on GitHub": "Devium a GitHubon",
    "Join our Discord": "Csatlakozz a Discord szerverhez",
    "Install Devium": "Devium telepítése",
    "Close": "Bezárás",
    "About Devium": "A Deviumról",
    "Starting the Devium installer": "A Devium telepítő megnyitása",
    "Back": "Vissza",
    "Next": "Következő",
    "Cancel": "Megszakítás",
    "Install": "Telepítés",
    "Welcome": "Üdvözlés",
    "Desktop": "Asztal",
    "Password": "Jelszó",
}


def current():
    try:
        with open(os.path.expanduser("~/.config/devium/language")) as f:
            code = f.read().strip()
            if code in LANGUAGES:
                return code
    except OSError:
        pass
    for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        v = os.environ.get(var, "")
        if v:
            code = v.split(":")[0][:2].lower()
            return code if code in LANGUAGES else "en"
    return "en"


_LANG = current()


def T(text):
    if _LANG == "en":
        return text
    if _LANG == "hu":
        return HU.get(text, text)
    row = STRINGS.get(text)
    i = _COLS.index(_LANG) if _LANG in _COLS else -1
    return row[i] if row and 0 <= i < len(row) else text


def set_language(code):
    os.makedirs(os.path.expanduser("~/.config/devium"), exist_ok=True)
    with open(os.path.expanduser("~/.config/devium/language"), "w") as f:
        f.write(code)
