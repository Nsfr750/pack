"""
Language support module for Python Package Manager.

This module provides internationalization (i18n) support for the application,
allowing for easy translation of all user-facing strings.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Union

# Configuration file path
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.python_package_manager')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

def _load_config() -> Dict[str, Any]:
    """Load configuration from file."""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
    return {}

def _save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving config: {e}", file=sys.stderr)

# Default language (English)
DEFAULT_LANGUAGE = "en"

# Supported languages with their display names
SUPPORTED_LANGUAGES = {
    "en": "English",
    "it": "Italiano",
    # Add more languages here as needed
}

# Language strings
TRANSLATIONS = {
    "en": {
        # Main window
        "app_title": "Python Package Manager",
        "menu_file": "File",
        "menu_edit": "Edit",
        "menu_view": "View",
        "menu_tools": "Tools",
        "menu_help": "Help",
        "menu_language": "Language",
        
        # File menu
        "new_project": "New Project",
        "open_project": "Open Project",
        "save_project": "Save Project",
        "save_project_as": "Save Project As...",
        "exit": "Exit",
        
        # Edit menu
        "undo": "Undo",
        "redo": "Redo",
        "cut": "Cut",
        "copy": "Copy",
        "paste": "Paste",
        "delete": "Delete",
        "preferences": "Preferences",
        
        # View menu
        "toolbar": "Toolbar",
        "status_bar": "Status Bar",
        "console": "Console",
        "refresh": "Refresh",
        "zoom_in": "Zoom In",
        "zoom_out": "Zoom Out",
        "reset_zoom": "Reset Zoom",
        
        # Tools menu
        "package_manager": "Package Manager",
        "check_for_updates": "Check for Updates",
        "view_log": "View Log",
        "terminal": "Terminal",
        
        # Help menu
        "documentation": "Documentation",
        "report_issue": "Report Issue",
        "about": "About",
        
        # Common buttons
        "ok": "OK",
        "cancel": "Cancel",
        "apply": "Apply",
        "save": "Save",
        "close": "Close",
        "yes": "Yes",
        "no": "No",
        
        # Status messages
        "ready": "Ready",
        "operation_completed": "Operation completed successfully",
        "operation_failed": "Operation failed",
        "saving": "Saving...",
        "loading": "Loading...",
        "processing": "Processing...",
        
        # Dialogs
        "confirm_exit": "Are you sure you want to exit?",
        "unsaved_changes": "You have unsaved changes. Save before exiting?",
        "error": "Error",
        "warning": "Warning",
        "information": "Information",
        "question": "Question",
        
        # Package management
        "install": "Install",
        "uninstall": "Uninstall",
        "upgrade": "Upgrade",
        "dependencies": "Dependencies",
        "installed_packages": "Installed Packages",
        "available_updates": "Available Updates",
        "package_name": "Package Name",
        "version": "Version",
        "description": "Description",
        "status": "Status",
        "search_packages": "Search packages...",
        "install_package": "Install Package",
        "uninstall_package": "Uninstall Package",
        "upgrade_package": "Upgrade Package",
        "package_details": "Package Details",
        "required_by": "Required By",
        "latest_version": "Latest Version",
        "installed_version": "Installed Version",
        "license": "License",
        "author": "Author",
        "homepage": "Homepage",
        "project_name": "Project Name",
        "project_path": "Project Path",
        "browse": "Browse...",
        "create_project": "Create Project",
        "open_project": "Open Project",
        "recent_projects": "Recent Projects",
        "project_settings": "Project Settings",
        "add_files": "Add Files",
        "remove_files": "Remove Files",
        "build_project": "Build Project",
        "run_project": "Run Project",
        "debug_project": "Debug Project",
        "stop_execution": "Stop Execution",
        "console": "Console",
        "output": "Output",
        "errors": "Errors",
        "warnings": "Warnings",
        "clear_console": "Clear Console",
        "copy_output": "Copy Output",
        "save_output": "Save Output...",
        "word_wrap": "Word Wrap",
        "settings": "Settings",
        "appearance": "Appearance",
        "theme": "Theme",
        "light_theme": "Light",
        "dark_theme": "Dark",
        "system_theme": "System",
        "font_size": "Font Size",
        "font_family": "Font Family",
        "language": "Language",
        "python_interpreter": "Python Interpreter",
        "select_interpreter": "Select Python Interpreter...",
        "auto_detect": "Auto-detect",
        "virtual_environment": "Virtual Environment",
        "create_venv": "Create Virtual Environment...",
        "select_venv": "Select Virtual Environment...",
        "new_file": "New File",
        "open_file": "Open File",
        "save_file": "Save File",
        "save_all": "Save All",
        "close_file": "Close File",
        "close_all_files": "Close All Files",
        "file_properties": "File Properties",
        "file_encoding": "File Encoding",
        "line_endings": "Line Endings",
        "search": "Search",
        "replace": "Replace",
        "find_next": "Find Next",
        "find_previous": "Find Previous",
        "go_to_line": "Go to Line...",
        "select_all": "Select All",
        "time_date": "Time/Date",
        "comment": "Comment",
        "uncomment": "Uncomment",
        "indent": "Indent",
        "unindent": "Unindent",
        "format": "Format",
        "run_selection": "Run Selection",
        "debug_selection": "Debug Selection",
        "evaluate_expression": "Evaluate Expression",
        "command_palette": "Command Palette...",
        "keyboard_shortcuts": "Keyboard Shortcuts",
        "user_guide": "User Guide",
        "check_for_updates": "Check for Updates",
        "release_notes": "Release Notes",
        "python_documentation": "Python Documentation",
        "python_package_index": "Python Package Index",
        "send_feedback": "Send Feedback",
        "about_qt": "About Qt",
        "about_app": "About Application",
        "quit_application": "Quit Application",

        # Sponsor window
        "sponsor": "Sponsor Us",
        "spomsor_title": "Sponsor",
        "spomsor_message": "Sponsor",
        "spomsor_ok": "OK",
        "spomsor_cancel": "Cancel",
        "spomsor_yes": "Yes",
        "spomsor_no": "No",
        "spomsor_ok": "OK",
        "spomsor_cancel": "Cancel",
        "sponsor_on_github": "Sponsor on GitHub",
        "join_discord": "Join Discord",
        "buy_me_a_coffee": "Buy me a coffee",
        "join_the_patreon": "Join the Patreon",
        
        # Project
        "project_info": "Project Information",
        "project_path": "Project Path",
        "package_name": "Package Name",
        "version": "Version",
        "browse": "Browse...",
        
        # Buttons
        "package_actions": "Package Actions",
        "initialize_package": "Initialize Package",
        "build_package": "Build Package",
        "install_package": "Install Package",
        "upload_to_pypi": "Upload to PyPI",
        "open_project": "Open Project",
        "save_project": "Save Project",
        "save_project_as": "Save Project As...",
        "exit": "Exit",
        "output": "Output",
    },
    "it": {
        # Sponsor window
        "sponsor": "Sponsorizzaci",
        "spomsor_title": "Sponsor",
        "spomsor_message": "Sponsor",
        "spomsor_ok": "OK",
        "spomsor_cancel": "Annulla",
        "spomsor_yes": "Sì",
        "spomsor_no": "No",
        "sponsor_on_github": "Sostienici su GitHub",
        "join_discord": "Unisciti a Discord",
        "buy_me_a_coffee": "Offrici un caffè",
        "join_the_patreon": "Unisciti a Patreon",
        
        # Progetto
        "project_info": "Informazioni Progetto",
        "project_path": "Percorso Progetto",
        "package_name": "Nome Pacchetto",
        "version": "Versione",
        "browse": "Sfoglia...",
        
        # Pulsanti
        "package_actions": "Azioni Pacchetto",
        "initialize_package": "Inizializza Pacchetto",
        "build_package": "Costruisci Pacchetto",
        "install_package": "Installa Pacchetto",
        "upload_to_pypi": "Carica su PyPI",
        "open_project": "Apri Progetto",
        "save_project": "Salva Progetto",
        "save_project_as": "Salva Progetto Come...",
        "exit": "Esci",
        "output": "Output",

        # Main window
        "app_title": "Gestore Pacchetti Python",
        "menu_file": "File",
        "menu_edit": "Modifica",
        "menu_view": "Visualizza",
        "menu_tools": "Strumenti",
        "menu_help": "Aiuto",
        "menu_language": "Lingua",
        
        # File menu
        "new_project": "Nuovo Progetto",
        "open_project": "Apri Progetto",
        "save_project": "Salva Progetto",
        "save_project_as": "Salva Progetto Come...",
        "exit": "Esci",
        
        # Edit menu
        "undo": "Annulla",
        "redo": "Ripristina",
        "cut": "Taglia",
        "copy": "Copia",
        "paste": "Incolla",
        "delete": "Elimina",
        "preferences": "Preferenze",
        
        # View menu
        "toolbar": "Barra strumenti",
        "status_bar": "Barra di stato",
        "console": "Console",
        "refresh": "Aggiorna",
        "zoom_in": "Ingrandisci",
        "zoom_out": "Riduci",
        "reset_zoom": "Ripristina zoom",
        
        # Tools menu
        "package_manager": "Gestione Pacchetti",
        "check_for_updates": "Controlla Aggiornamenti",
        "view_log": "Visualizza Log",
        "terminal": "Terminale",
        
        # Help menu
        "documentation": "Documentazione",
        "report_issue": "Segnala Problema",
        "about": "Informazioni",
        
        # Common buttons
        "ok": "OK",
        "cancel": "Annulla",
        "apply": "Applica",
        "save": "Salva",
        "close": "Chiudi",
        "yes": "Sì",
        "no": "No",
        
        # Status messages
        "ready": "Pronto",
        "operation_completed": "Operazione completata con successo",
        "operation_failed": "Operazione fallita",
        "saving": "Salvataggio in corso...",
        "loading": "Caricamento in corso...",
        "processing": "Elaborazione in corso...",
        
        # Dialogs
        "confirm_exit": "Sei sicuro di voler uscire?",
        "unsaved_changes": "Ci sono modifiche non salvate. Salvare prima di uscire?",
        "error": "Errore",
        "warning": "Avviso",
        "information": "Informazione",
        "question": "Domanda",
        
        # Package management
        "install": "Installa",
        "uninstall": "Disinstalla",
        "upgrade": "Aggiorna",
        "dependencies": "Dipendenze",
        "installed_packages": "Pacchetti Installati",
        "available_updates": "Aggiornamenti Disponibili",
        "package_name": "Nome Pacchetto",
        "version": "Versione",
        "description": "Descrizione",
        "status": "Stato",
        "search_packages": "Cerca pacchetti...",
        "install_package": "Installa Pacchetto",
        "uninstall_package": "Disinstalla Pacchetto",
        "upgrade_package": "Aggiorna Pacchetto",
        "package_details": "Dettagli Pacchetto",
        "required_by": "Richiesto Da",
        "latest_version": "Ultima Versione",
        "installed_version": "Versione Installata",
        "license": "Licenza",
        "author": "Autore",
        "homepage": "Pagina Principale",
        "project_name": "Nome Progetto",
        "project_path": "Percorso Progetto",
        "browse": "Sfoglia...",
        "create_project": "Crea Progetto",
        "open_project": "Apri Progetto",
        "recent_projects": "Progetti Recenti",
        "project_settings": "Impostazioni Progetto",
        "add_files": "Aggiungi File",
        "remove_files": "Rimuovi File",
        "build_project": "Compila Progetto",
        "run_project": "Esegui Progetto",
        "debug_project": "Debug Progetto",
        "stop_execution": "Interrompi Esecuzione",
        "console": "Console",
        "output": "Output",
        "errors": "Errori",
        "warnings": "Avvisi",
        "clear_console": "Pulisci Console",
        "copy_output": "Copia Output",
        "save_output": "Salva Output...",
        "word_wrap": "A Capo Automatico",
        "settings": "Impostazioni",
        "appearance": "Aspetto",
        "theme": "Tema",
        "light_theme": "Chiaro",
        "dark_theme": "Scuro",
        "system_theme": "Sistema",
        "font_size": "Dimensione Carattere",
        "font_family": "Tipo di Carattere",
        "language": "Lingua",
        "python_interpreter": "Interprete Python",
        "select_interpreter": "Seleziona Interprete Python...",
        "auto_detect": "Rilevamento Automatico",
        "virtual_environment": "Ambiente Virtuale",
        "create_venv": "Crea Ambiente Virtuale...",
        "select_venv": "Seleziona Ambiente Virtuale...",
        "new_file": "Nuovo File",
        "open_file": "Apri File",
        "save_file": "Salva File",
        "save_all": "Salva Tutto",
        "close_file": "Chiudi File",
        "close_all_files": "Chiudi Tutti i File",
        "file_properties": "Proprietà File",
        "file_encoding": "Codifica File",
        "line_endings": "Terminazioni di Linea",
        "search": "Cerca",
        "replace": "Sostituisci",
        "find_next": "Trova Successivo",
        "find_previous": "Trova Precedente",
        "go_to_line": "Vai alla Linea...",
        "select_all": "Seleziona Tutto",
        "time_date": "Ora/Data",
        "comment": "Commenta",
        "uncomment": "Togli Commento",
        "indent": "Aumenta Rientro",
        "unindent": "Riduci Rientro",
        "format": "Formatta",
        "run_selection": "Esegui Selezione",
        "debug_selection": "Debug Selezione",
        "evaluate_expression": "Valuta Espressione",
        "command_palette": "Tavolozza Comandi...",
        "keyboard_shortcuts": "Scorciatoie da Tastiera",
        "user_guide": "Guida Utente",
        "check_for_updates": "Controlla Aggiornamenti",
        "release_notes": "Note di Rilascio",
        "python_documentation": "Documentazione Python",
        "python_package_index": "Indice Pacchetti Python",
        "send_feedback": "Invia Feedback",
        "about_qt": "Informazioni su Qt",
        "about_app": "Informazioni sull'Applicazione",
        "quit_application": "Esci dall'Applicazione",
    }
}

class Translator:
    """Handles language translation for the application."""
    
    _instance = None
    _current_language = DEFAULT_LANGUAGE
    _config_loaded = False
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(Translator, cls).__new__(cls)
            # Load saved language or use default
            config = _load_config()
            saved_lang = config.get('language', DEFAULT_LANGUAGE)
            cls._instance._load_language(saved_lang)
        return cls._instance
    
    def _load_language(self, lang_code: str) -> None:
        """Load translations for the specified language code."""
        self._current_language = lang_code
        self._translations = TRANSLATIONS.get(lang_code, TRANSLATIONS[DEFAULT_LANGUAGE])
        
        # Save the language preference if it's different from the current config
        if not self._config_loaded:
            self._config_loaded = True
            return
            
        config = _load_config()
        if config.get('language') != lang_code:
            config['language'] = lang_code
            _save_config(config)
    
    def set_language(self, lang_code: str) -> bool:
        """
        Set the current language.
        
        Args:
            lang_code: Language code (e.g., 'en', 'it')
            
        Returns:
            bool: True if language was changed, False otherwise
        """
        if lang_code in SUPPORTED_LANGUAGES and lang_code != self._current_language:
            self._load_language(lang_code)
            return True
        return False
    
    def get_language(self) -> str:
        """Get the current language code."""
        return self._current_language
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get a dictionary of supported language codes and their display names."""
        return SUPPORTED_LANGUAGES
    
    def translate(self, key: str, default: Optional[str] = None) -> str:
        """
        Translate a string key to the current language.
        
        Args:
            key: Translation key
            default: Default value if key is not found
            
        Returns:
            str: Translated string or the key if not found
        """
        return self._translations.get(key, default or key)
    
    def __call__(self, key: str, default: Optional[str] = None) -> str:
        """Alias for translate method to allow using the instance as a function."""
        return self.translate(key, default)


# Create a global instance
translator = Translator()

# Shortcut function for translation
def tr(key: str, default: Optional[str] = None) -> str:
    """
    Shortcut function to translate a string.
    
    Args:
        key: Translation key
        default: Default value if key is not found
        
    Returns:
        str: Translated string or the key if not found
    """
    return translator(key, default)
