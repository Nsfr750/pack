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
        "terminal": "Open Terminal",
        "failed_to_open_terminal": "Failed to open terminal",
        
        # Help menu
        "documentation": "Documentation",
        "report_issue": "Report Issue",
        "about": "About",
        "help": "Help",
        "usage_tab": "Usage",
        "features_tab": "Features",
        "help_usage": "Python Package Manager - Usage Guide\n\n1. Creating a New Project:\n   - Click on 'File' > 'New Project'\n   - Select a directory for your project\n   - Enter your package details\n   - Click 'Create' to initialize the package structure\n\n2. Building Packages:\n   - Open your project\n   - Click on 'Build' to create distribution packages\n   - Find your packages in the 'dist' directory\n\n3. Installing Packages:\n   - Open your project\n   - Click on 'Install' to install in development mode",
        "help_features": "Python Package Manager - Features\n\n• Project Management:\n  - Create new Python packages\n  - Manage project metadata\n  - Handle package dependencies\n\n• Building and Distribution:\n  - Build source distributions\n  - Create wheel packages\n  - Generate setup.py and pyproject.toml\n\n• Development Tools:\n  - Integrated terminal\n  - Log viewer\n  - Package manager integration",
        
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
        "sign_package": "Sign Package",
        "list_installed": "List Installed",
        "search_package": "Search Package",
        "uninstall_package": "Uninstall Package",

        # Virtual Environment
        "virtual_environment": "Virtual Environment",
        "python_interpreter": "Python Interpreter:",
        "venv_directory": "Virtual Env Directory:",
        "create_venv": "Create",
        "activate_venv": "Activate",
        "deactivate_venv": "Deactivate",
        "install_package_venv": "Install Package",
        
        # Repository Management
        "add_repository": "Add Repository",
        "edit_repository": "Edit Repository",
        "remove_repository": "Remove Repository",
        "set_as_default": "Set as Default",
        "name": "Name",
        "url": "URL",
        "username": "Username",
        "password": "Password",
        "authentication": "Authentication",
        "default": "Default",
        "name_required": "Repository name is required",
        "url_required": "Repository URL is required",
        "repository_not_found": "Repository not found",
        "confirm_removal": "Confirm Removal",
        "confirm_remove_repository": "Are you sure you want to remove the repository '{name}'?",
        
        # Dependency Resolution
        "resolving_dependencies": "Resolving Dependencies...",
        "dependencies_resolved": "Dependencies resolved successfully",
        "dependency_resolution_failed": "Failed to resolve dependencies",
        "installing_dependencies": "Installing Dependencies...",
        "dependencies_installed": "Dependencies installed successfully",
        "dependency_installation_failed": "Failed to install dependencies",
        "checking_conflicts": "Checking for conflicts...",
        "conflicts_found": "Conflicts found in dependencies",
        "no_conflicts": "No conflicts found",
        "install": "Install",
        "uninstall": "Uninstall",
        "update": "Update",
        "package": "Package",
        "version": "Version",
        "required_by": "Required By",
        "conflict": "Conflict",
        "no_package_selected": "No package selected",
        "install_package": "Install Package",
        "package_name": "Package Name",
        "package_version": "Version (optional)",
        "install_options": "Install Options",
        "upgrade": "Upgrade if needed",
        "force_reinstall": "Force reinstall",
        "no_deps": "Don't install dependencies",
        "pre_release": "Include pre-release versions",
        "install_btn": "Install",
        "close_btn": "Close",
        
        # Templates
        "new_project": "New Project",
        "project_name": "Project Name",
        "location": "Location",
        "browse": "Browse...",
        "select_directory": "Select Directory",
        "template": "Template",
        "project_name_required": "Project name is required",
        "location_required": "Location is required",
        "template_required": "Please select a template",
        "project_creation_failed": "Failed to create project at {path}",
        "project_creation_error": "Error creating project: {error}",
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

        # Pacchetto
        "sign_package": "Firma Pacchetto",
        "list_installed": "Lista Pacchetti Installati",
        "search_package": "Cerca Pacchetto",
        "install_package_venv": "Installa Pacchetto",
        "uninstall_package": "Disinstalla Pacchetto",

        # Virtual Environment
        "virtual_environment": "Ambiente Virtuale",
        "python_interpreter": "Interprete Python:",
        "venv_directory": "Directory Ambiente Virtuale:",
        "create_venv": "Crea",
        "activate_venv": "Attiva",
        "deactivate_venv": "Disattiva",        

        # Repository Management
        "add_repository": "Aggiungi Repository",
        "edit_repository": "Modifica Repository",
        "remove_repository": "Rimuovi Repository",
        "set_as_default": "Imposta come Predefinito",
        "name": "Nome",
        "url": "URL",
        "username": "Nome Utente",
        "password": "Password",
        "authentication": "Autenticazione",
        "default": "Predefinito",
        "name_required": "Il nome del repository è obbligatorio",
        "url_required": "L'URL del repository è obbligatorio",
        "repository_not_found": "Repository non trovato",
        "confirm_removal": "Conferma Rimozione",
        "confirm_remove_repository": "Sei sicuro di voler rimuovere il repository '{name}'?",
        
        # Dependency Resolution
        "resolving_dependencies": "Risoluzione delle dipendenze...",
        "dependencies_resolved": "Dipendenze risolte con successo",
        "dependency_resolution_failed": "Impossibile risolvere le dipendenze",
        "installing_dependencies": "Installazione delle dipendenze...",
        "dependencies_installed": "Dipendenze installate con successo",
        "dependency_installation_failed": "Impossibile installare le dipendenze",
        "checking_conflicts": "Verifica dei conflitti...",
        "conflicts_found": "Trovati conflitti nelle dipendenze",
        "no_conflicts": "Nessun conflitto trovato",
        "install": "Installa",
        "uninstall": "Disinstalla",
        "update": "Aggiorna",
        "package": "Pacchetto",
        "version": "Versione",
        "required_by": "Richiesto da",
        "conflict": "Conflitto",
        "no_package_selected": "Nessun pacchetto selezionato",
        "install_package": "Installa Pacchetto",
        "package_name": "Nome Pacchetto",
        "package_version": "Versione (opzionale)",
        "install_options": "Opzioni di Installazione",
        "upgrade": "Aggiorna se necessario",
        "force_reinstall": "Forza reinstallazione",
        "no_deps": "Non installare le dipendenze",
        "pre_release": "Includi versioni pre-release",
        "install_btn": "Installa",
        "close_btn": "Chiudi",
        
        # Templates
        "project_name": "Nome Progetto",
        "project_location": "Posizione",
        "browse": "Sfoglia...",
        "select_template": "Seleziona Modello",
        "create": "Crea",
        "cancel": "Annulla",
        "new_project": "Nuovo Progetto",
        "project_created": "Progetto creato con successo!",
        "project_creation_error": "Errore durante la creazione del progetto: {error}",
        "template_required": "Seleziona un modello",
        "project_creation_failed": "Impossibile creare il progetto in {path}",
        "project_creation_error": "Errore durante la creazione del progetto: {error}",
        
        # Menu
        "app_title": "Python Package Manager",
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
        "failed_to_open_terminal": "Impossibile aprire il terminale",
        
        # Tools menu
        "package_manager": "Gestione Pacchetti",
        "check_for_updates": "Controlla Aggiornamenti",
        "view_log": "Visualizza Log",
        "terminal": "ApriTerminale",
        
        # Help menu
        "documentation": "Documentazione",
        "report_issue": "Segnala Problema",
        "about": "Informazioni",
        "help": "Aiuto",
        "usage_tab": "Utilizzo",
        "features_tab": "Funzionalità",
        "help_usage": "Python Package Manager - Guida all'Uso\n\n1. Creazione di un Nuovo Progetto:\n   - Clicca su 'File' > 'Nuovo Progetto'\n   - Seleziona una directory per il tuo progetto\n   - Inserisci i dettagli del pacchetto\n   - Clicca 'Crea' per inizializzare la struttura del pacchetto\n\n2. Creazione dei Pacchetti:\n   - Apri il tuo progetto\n   - Clicca su 'Costruisci' per creare i pacchetti di distribuzione\n   - Trova i tuoi pacchetti nella directory 'dist'\n\n3. Installazione dei Pacchetti:\n   - Apri il tuo progetto\n   - Clicca su 'Installa' per l'installazione in modalità sviluppo",
        "help_features": "Python Package Manager - Funzionalità\n\n• Gestione Progetti:\n  - Crea nuovi pacchetti Python\n  - Gestisci i metadati del progetto\n  - Gestisci le dipendenze\n\n• Creazione e Distribuzione:\n  - Crea distribuzioni sorgente\n  - Crea pacchetti wheel\n  - Genera setup.py e pyproject.toml\n\n• Strumenti di Sviluppo:\n  - Terminale integrato\n  - Visualizzatore log\n  - Integrazione con il gestore pacchetti",
        
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
        "package_version": "Versione Pacchetto",
        "version": "Versione",
        "description": "Descrizione",
        "status": "Stato",
        "install_btn": "Installa",
        "uninstall_btn": "Disinstalla",
        "update_btn": "Aggiorna",
        "force_reinstall": "Forza Reinstallazione",
        "no_deps": "Senza Dipendenze",
        "pre_release": "Includi Pre-release",
        "loading_dependencies": "Caricamento dipendenze...",
        "dependencies_loaded": "Dipendenze caricate",
        "dependencies_installed": "Dipendenze installate con successo",
        "packages_updated": "Pacchetti aggiornati con successo",
        "packages_uninstalled": "Pacchetti disinstallati con successo",
        "checking_conflicts": "Controllo conflitti in corso...",
        "error_loading_dependencies": "Errore nel caricamento delle dipendenze",
        "error_installing_dependencies": "Errore durante l'installazione delle dipendenze",
        "error_executing_command": "Errore durante l'esecuzione del comando",
        "unexpected_error": "Si è verificato un errore imprevisto",
        "no_package_selected": "Nessun pacchetto selezionato",
        "confirm_removal": "Conferma Rimozione",
        "confirm_uninstall_packages": "Sei sicuro di voler disinstallare i seguenti pacchetti?\n\n{}",
        "confirm_update": "Conferma Aggiornamento",
        "confirm_update_all_packages": "Sei sicuro di voler aggiornare tutti i pacchetti?",
        "conflicts_found": "Conflitti Trovati",
        "conflicts_detected": "Sono stati rilevati i seguenti conflitti tra dipendenze:",
        "no_conflicts": "Nessun conflitto trovato",
        "no_conflicts_found": "Nessun conflitto tra le dipendenze trovato.",
        "error_checking_conflicts": "Errore durante il controllo dei conflitti",
        "manage_requirements": "Gestisci Requisiti",
        "requirements_file": "File dei Requisiti",
        "requirements_saved": "Requisiti salvati con successo",
        "error_saving_requirements": "Errore nel salvataggio dei requisiti",
        "requirements_installed": "Requisiti installati con successo",
        "error_installing_requirements": "Errore durante l'installazione dei requisiti",
        "gpg_not_found": "GPG Non Trovato",
        "gpg_not_found_message": "GPG è richiesto per firmare i pacchetti. Si prega di installare GPG e riprovare.",
        "build_error": "Errore di Compilazione",
        "build_directory_not_found": "Directory di compilazione non trovata. Si prega di compilare il pacchetto prima.",
        "no_package_found": "Nessun Pacchetto Trovato",
        "no_package_found_message": "Nessun file del pacchetto trovato nella cartella dist.",
        "sign_error": "Errore di Firma",
        "failed_to_sign_package": "Impossibile firmare il pacchetto",
        "error_signing_package": "Errore durante la firma del pacchetto",
        "sign_success": "Pacchetto Firmato",
        "package_signed_successfully": "Pacchetto firmato con successo",
        "no_project": "Nessun Progetto Aperto",
        "no_project_message": "Si prega di aprire o creare un progetto prima.",
        "no_project_open": "Nessun progetto aperto al momento.",
        "managing_repositories": "Gestione repository in corso...",
        "dependencies_managed": "Dipendenze gestite con successo",
        "error_managing_dependencies": "Errore nella gestione delle dipendenze",
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
