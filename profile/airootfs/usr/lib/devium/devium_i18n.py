"""Translations for the Devium apps.

T("English text") returns the text in the user's language (from $LANGUAGE / $LANG,
or ~/.config/devium/language), falling back to English. Languages: ga (Irish / Gaeilge),
es, fr, de. To add a language, add a column to STRINGS below - missing entries stay English.
"""
import os

LANGUAGES = {"en": "English", "ga": "Gaeilge (Irish)", "es": "Español", "fr": "Français", "de": "Deutsch"}

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
    row = STRINGS.get(text)
    return row[_COLS.index(_LANG)] if row else text


def set_language(code):
    os.makedirs(os.path.expanduser("~/.config/devium"), exist_ok=True)
    with open(os.path.expanduser("~/.config/devium/language"), "w") as f:
        f.write(code)
