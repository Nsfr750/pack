"""
Language support module for Python Package Manager.

This module provides internationalization (i18n) support for the application,
allowing for easy translation of all user-facing strings.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Union, Callable

# Configuration file path
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.python_package_manager')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

# Default language (English)
DEFAULT_LANGUAGE = "en"

# Supported languages with their display names
SUPPORTED_LANGUAGES = {
    "en": "English",
    "it": "Italiano",
    "es": "Español",
    "pt": "Português",
    "de": "Deutsch",
    "fr": "Français",
    "ru": "Русский"
}

def _load_config() -> Dict[str, Any]:
    """Load configuration from file.
    
    Returns:
        Dict[str, Any]: The loaded configuration or an empty dict if there was an error
    """
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except json.JSONDecodeError:
        # If the config file is corrupted, back it up and create a new one
        try:
            backup_file = f"{CONFIG_FILE}.bak"
            if os.path.exists(CONFIG_FILE):
                import shutil
                shutil.copy2(CONFIG_FILE, backup_file)
                print(f"Config file was corrupted. A backup was saved to {backup_file}", file=sys.stderr)
        except Exception as e:
            print(f"Error backing up corrupted config: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
    return {}

def _save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file.
    
    Args:
        config: The configuration dictionary to save
    """
    temp_file = f"{CONFIG_FILE}.tmp"
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        # Create a temporary file first to ensure we don't corrupt the config on write failure
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        # On Windows, we need to remove the destination file first if it exists
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        os.rename(temp_file, CONFIG_FILE)
    except Exception as e:
        print(f"Error saving config: {e}", file=sys.stderr)
        # Clean up temp file if it exists
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass

# Language strings
TRANSLATIONS = {
    "en": {
        # Main window
        "app_title": "Gestore Pacchetti Python",
        "menu_file": "File",
        "menu_edit": "Edit",
        "menu_view": "View",
        "menu_tools": "Tools",
        "menu_language": "Language",
        "menu_help": "Help",
        "status_ready": "Ready",
        "status_processing": "Status Processing...",
        "status_done": "Done",
        "status_error": "Error",
        "exit": "Exit",

        # Menu Modifica
        "undo": "Undo",
        "redo": "Redo",
        "cut": "Cut",
        "copy": "Copy",
        "paste": "Paste",
        "delete": "Delete",

        # Menu Visualizza
        "toolbar": "Tool Bar",
        "status_bar": "Staus Bar",
        "console": "Console",
        "zoom_in": "Zoom In",
        "zoom_out": "Zoom Out",
        "reset_zoom": "Reset Zoom",

        # Menu Aiuto
        "documentation": "Documentation",
        "report_issue": "Report Issue",
        "about": "About",
        "sponsor": "Sponsor Us",

        # Menu Strumenti
        "package_manager": "Package Manager",
        "view_log": "Show Log",
        "terminal": "Opena a Terminal",
        "check_for_update": "Check for Update",

        # Sponsor Dialog
        "sponsor_on_github": "Sponsor on GitHub",
        "join_discord": "Join Discord",
        "buy_me_a_coffee": "Buy me a coffee",
        "join_the_patreon": "Join Patreon",
        "close": "Close",
        
        # Buttons & Common UI
        "btn_ok": "OK",
        "btn_cancel": "Cancel",
        "btn_apply": "Apply",
        "btn_close": "Close",
        "btn_yes": "Yes",
        "btn_no": "No",
        "btn_browse": "Browse...",
        "btn_save": "Save",
        "btn_install": "Install",
        "btn_uninstall": "Uninstall",
        "btn_update": "Update",
        "btn_check": "Check",
        "btn_confirm": "Confirm",
        "btn_delete": "Delete",
        "btn_edit": "Edit",
        "btn_add": "Add",
        "btn_remove": "Remove",
        "btn_refresh": "Refresh",
        "btn_search": "Search",
       
        "uninstall_package": "Uninstall Package",
        "update_package": "Update Package",
        "manage_repositories": "Manage Repository",
        "manage_dependencies": "Manage Dependencies",
        "welcome_message": "Welcome on PyPackager",
        "no_recent_projects": "No recent projects",
        "ready": "Ready",

        # Dependency Management
        "dependencies": "Dependencies",
        "install_package": "Install Package",
        "package_name": "Package Name",
        "package_version": "Version",
        "upgrade": "Upgrade",
        "force_reinstall": "Force Reinstall",
        "no_deps": "No Dependencies",
        "pre_release": "Pre-release",
        "install_btn": "Install",
        "uninstall": "Uninstall",
        "update": "Update",
        "check_conflicts": "Check Conflicts",
        "package": "Package",
        "version": "Version",
        "required_by": "Required By",
        "loading_dependencies": "Loading dependencies",
        "dependencies_loaded": "Dependencies loaded",
        "error_loading_dependencies": "Error loading dependencies",
        "warning": "Warning",
        "no_package_selected": "No package selected",
        "installing_dependencies": "Installing dependencies",
        "dependencies_installed": "Dependencies installed successfully",
        "confirm_removal": "Confirm Removal",
        "confirm_uninstall_packages": "Are you sure you want to uninstall the following packages?\n\n{}",
        "uninstalling_packages": "Uninstalling packages",
        "packages_uninstalled": "Packages uninstalled successfully",
        "confirm_update": "Confirm Update",
        "confirm_update_all_packages": "Are you sure you want to update all packages to their latest versions?",
        "updating_packages": "Updating packages",
        "packages_updated": "Packages updated successfully",
        "checking_conflicts": "Checking for conflicts...",
        "conflicts_found": "Conflicts Found",
        "conflicts_detected": "The following conflicts were detected:\n\n{}",
        "no_conflicts": "No conflicts found",
        "no_conflicts_found": "No dependency conflicts were found.",
        "error_checking_conflicts": "Error checking for conflicts",
        "error_executing_command": "Error executing command",
        "unexpected_error": "An unexpected error occurred",
        "error": "Error",
        "manage_requirements": "Manage Requirements",
        "requirements_file": "Requirements File",
        "install_requirements": "Install Requirements",
        "success": "Success",
        "requirements_saved": "Requirements saved successfully",
        "error_saving_requirements": "Error saving requirements",
        
        # Project Management
        "project": "Project",
        "new_project": "New Project",
        "open_project": "Open Project",
        "save_project": "Save Project",
        "save_project_as": "Save Project As...",
        "close_project": "Close Project",
        "project_properties": "Project Properties",
        "project_created": "Project created successfully!",
        "project_creation_error": "Error creating project: {error}",
        "template_required": "Please select a template",
        "project_creation_failed": "Failed to create project at {path}",
        "project_opened": "Project opened successfully",
        "project_open_failed": "Failed to open project at {path}",
        "project_saved": "Project saved successfully",
        "project_save_failed": "Failed to save project at {path}",
        "project_closed": "Project closed",
        "project_not_found": "Project not found at {path}",
        "project_already_open": "A project is already open. Please close it first.",
        "no_project_open": "No project is currently open",
        "quit_confirmation": "Are you sure you want to quit?",
    },
    "it": {
        # Main window
        "app_title": "Gestore Pacchetti Python",
        "menu_file": "File",
        "menu_edit": "Modifica",
        "menu_view": "Visualizza",
        "menu_tools": "Strumenti",
        "menu_language": "Lingua",
        "menu_help": "Aiuto",
        "status_ready": "Pronto",
        "status_processing": "Elaborazione in corso...",
        "status_done": "Fatto",
        "status_error": "Errore",
        "exit": "Esci",

        # Menu Modifica
        "undo": "Annulla",
        "redo": "Ripeti",
        "cut": "Taglia",
        "copy": "Copia",
        "paste": "Incolla",
        "delete": "Cancella",

        # Menu Visualizza
        "toolbar": "Barra Degli Strumenti",
        "status_bar": "Barra di Stato",
        "console": "Console",
        "zoom_in": "Zoom In",
        "zoom_out": "Zoom Out",
        "reset_zoom": "Reset Zoom",


        # Menu Aiuto
        "documentation": "Documentazione",
        "report_issue": "Segnala un problema",
        "about": "Informazioni",
        "sponsor": "Sponsorizza",

        # Menu Strumenti
        "package_manager": "Gestore Pacchetti",
        "view_log": "Visualizza Log",
        "terminal": "Apri un Terminale",

        # Sponsor Dialog
        "sponsor_on_github": "Sponsorizza su GitHub",
        "join_discord": "Unisciti a Discord",
        "buy_me_a_coffee": "Offrimi un caffè",
        "join_the_patreon": "Unisciti a Patreon",
        "close": "Chiudi",

        # Buttons & Common UI
        "btn_ok": "OK",
        "btn_cancel": "Annulla",
        "btn_apply": "Applica",
        "btn_close": "Chiudi",
        "btn_yes": "Sì",
        "btn_no": "No",
        "btn_browse": "Sfoglia...",
        "btn_save": "Salva",
        "btn_install": "Installa",
        "btn_uninstall": "Disinstalla",
        "btn_update": "Aggiorna",
        "btn_check": "Controlla",
        "btn_confirm": "Conferma",
        "btn_delete": "Elimina",
        "btn_edit": "Modifica",
        "btn_add": "Aggiungi",
        "btn_remove": "Rimuovi",
        "btn_refresh": "Aggiorna",
        "btn_search": "Cerca",
        
        "uninstall_package": "Disinstalla Pacchetto",
        "update_package": "Aggiorna Pacchetto",
        "manage_repositories": "Gestisci Repository",
        "manage_dependencies": "Gestisci DIpendenze",
        "welcome_message": "Benvenuto in PyPackager",
        "no_recent_projects": "Nessun progetto recente",
        "ready": "Pronto",

        # Gestione Dipendenze
        "dependencies": "Dipendenze",
        "install_package": "Installa Pacchetto",
        "package_name": "Nome Pacchetto",
        "package_version": "Versione",
        "upgrade": "Aggiorna",
        "force_reinstall": "Reinstalla Forzatamente",
        "no_deps": "Senza Dipendenze",
        "pre_release": "Versione Preliminare",
        "install_btn": "Installa",
        "uninstall": "Disinstalla",
        "update": "Aggiorna",
        "check_conflicts": "Controlla Conflitti",
        "package": "Pacchetto",
        "version": "Versione",
        "required_by": "Richiesto Da",
        "loading_dependencies": "Caricamento dipendenze",
        "dependencies_loaded": "Dipendenze caricate",
        "error_loading_dependencies": "Errore nel caricamento delle dipendenze",
        "warning": "Attenzione",
        "no_package_selected": "Nessun pacchetto selezionato",
        "installing_dependencies": "Installazione dipendenze in corso",
        "dependencies_installed": "Dipendenze installate con successo",
        "confirm_removal": "Conferma Rimozione",
        "confirm_uninstall_packages": "Sei sicuro di voler disinstallare i seguenti pacchetti?\n\n{}",
        "uninstalling_packages": "Disinstallazione pacchetti in corso",
        "packages_uninstalled": "Pacchetti disinstallati con successo",
        "confirm_update": "Conferma Aggiornamento",
        "confirm_update_all_packages": "Sei sicuro di voler aggiornare tutti i pacchetti all'ultima versione disponibile?",
        "updating_packages": "Aggiornamento pacchetti in corso",
        "packages_updated": "Pacchetti aggiornati con successo",
        "checking_conflicts": "Controllo conflitti in corso...",
        "conflicts_found": "Conflitti Trovati",
        "conflicts_detected": "Sono stati rilevati i seguenti conflitti:\n\n{}",
        "no_conflicts": "Nessun conflitto",
        "no_conflicts_found": "Nessun conflitto di dipendenze rilevato.",
        "error_checking_conflicts": "Errore durante il controllo dei conflitti",
        "error_executing_command": "Errore durante l'esecuzione del comando",
        "unexpected_error": "Si è verificato un errore imprevisto",
        "error": "Errore",
        "manage_requirements": "Gestisci Requisiti",
        "requirements_file": "File dei Requisiti",
        "install_requirements": "Installa Requisiti",
        "success": "Operazione Completata",
        "requirements_saved": "Requisiti salvati con successo",
        "error_saving_requirements": "Errore nel salvataggio dei requisiti",
        
        # Gestione Progetti
        "project": "Progetto",
        "new_project": "Nuovo Progetto",
        "open_project": "Apri Progetto",
        "save_project": "Salva Progetto",
        "save_project_as": "Salva Progetto Come...",
        "close_project": "Chiudi Progetto",
        "project_properties": "Proprietà Progetto",
        "project_created": "Progetto creato con successo!",
        "project_creation_error": "Errore durante la creazione del progetto: {error}",
        "template_required": "Seleziona un modello",
        "project_creation_failed": "Impossibile creare il progetto in {path}",
        "project_opened": "Progetto aperto con successo",
        "project_open_failed": "Impossibile aprire il progetto in {path}",
        "project_saved": "Progetto salvato con successo",
        "project_save_failed": "Impossibile salvare il progetto in {path}",
        "project_closed": "Progetto chiuso",
        "project_not_found": "Progetto non trovato in {path}",
        "project_already_open": "Un progetto è già aperto. Chiudilo prima di aprirne un altro.",
        "no_project_open": "Nessun progetto attualmente aperto",
        
        # Help Dialog - Italian
        "help": "Aiuto",
        "close": "Chiudi",
        "usage_tab": "Utilizzo",
        "features_tab": "Funzionalità",
        "package_signing": "Firma dei Pacchetti",
        "usage_guide": "Guida all'Utilizzo",
        "creating_project": "Creazione di un Progetto",
        "click_file_new_project": "Clicca su 'File' > 'Nuovo Progetto'",
        "select_project_directory": "Seleziona la directory del progetto",
        "enter_package_details": "Inserisci i dettagli del pacchetto (nome, versione, ecc.)",
        "click_create_to_initialize": "Clicca 'Crea' per inizializzare il progetto",
        "building_packages": "Creazione dei Pacchetti",
        "open_your_project": "Apri il tuo progetto nell'applicazione",
        "click_build_to_create": "Clicca 'Crea' per generare i pacchetti di distribuzione",
        "find_packages_in_dist": "Trova i tuoi pacchetti nella directory 'dist'",
        "installing_packages": "Installazione dei Pacchetti",
        "click_install_dev_mode": "Clicca 'Installa' per l'installazione in modalità sviluppo",
        "use_uninstall_to_remove": "Usa 'Disinstalla' per rimuovere il pacchetto",
        "managing_dependencies": "Gestione delle Dipendenze",
        "add_remove_dependencies": "Aggiungi o rimuovi dipendenze del pacchetto",
        "check_dependency_conflicts": "Controlla i conflitti tra le dipendenze",
        "ensure_gpg_installed": "Assicurati che GPG sia installato sul tuo sistema",
        "click_sign_to_sign": "Clicca 'Firma' per firmare il tuo pacchetto",
        "verify_signatures_gpg": "Verifica le firme utilizzando gli strumenti GPG",
        "features_overview": "Panoramica delle Funzionalità",
        "project_management": "Gestione Progetti",
        "create_new_packages": "Crea nuovi pacchetti Python",
        "manage_project_metadata": "Gestisci metadati e configurazioni del progetto",
        "handle_dependencies": "Gestisci le dipendenze dei pacchetti",
        "building_distribution": "Creazione Distribuzione",
        "build_source_distributions": "Crea distribuzioni sorgente",
        "create_wheel_packages": "Crea pacchetti wheel",
        "generate_setup_files": "Genera file setup.py",
        "sign_packages": "Firma i pacchetti con GPG",
        "dependency_management": "Gestione Dipendenze",
        "check_for_updates": "Controlla aggiornamenti pacchetti",
        "resolve_conflicts": "Risolvi i conflitti tra dipendenze",
        "manage_requirements": "Gestisci i file dei requisiti",
        "repository_support": "Supporto Repository",
        "add_custom_repositories": "Aggiungi repository di pacchetti personalizzati",
        "manage_repository_creds": "Gestisci credenziali dei repository",
        "publish_to_pypi": "Pubblica su PyPI",
        "development_tools": "Strumenti di Sviluppo",
        "integrated_terminal": "Terminale integrato",
        "log_viewer": "Visualizzatore di log",
        "package_manager_integration": "Integrazione con il gestore pacchetti",
        "adding_dependencies": "Aggiunta Dipendenze",
        "click_add_dependencies": "Clicca su 'Aggiungi Dipendenze'",
        "enter_package_details": "Inserisci nome e versione del pacchetto",
        "choose_install_options": "Scegli le opzioni di installazione",
        "updating_dependencies": "Aggiornamento Dipendenze",
        "select_packages_update": "Seleziona i pacchetti da aggiornare",
        "click_update_versions": "Clicca 'Aggiorna' per installare le nuove versioni",
        "resolving_conflicts": "Risoluzione Conflitti",
        "click_check_conflicts": "Clicca 'Controlla Conflitti'",
        "review_resolve_issues": "Rivedi e risolvi eventuali problemi",
        "requirements_files": "File dei Requisiti",
        "import_from_requirements": "Importa da requirements.txt",
        "export_current_dependencies": "Esporta le dipendenze correnti",
        "install_from_requirements": "Installa da file dei requisiti",
        "package_signing_with_gpg": "Firma dei Pacchetti con GPG",
        "prerequisites": "Prerequisiti",
        "install_gnupg_system": "Installa GnuPG sul tuo sistema",
        "setup_gpg_key_pair": "Configura una coppia di chiavi GPG",
        "configure_git_signing": "Configura Git per la firma dei commit",
        "signing_packages": "Firma dei Pacchetti",
        "build_your_package": "Prima crea il tuo pacchetto",
        "verify_using_gpg_tools": "Verifica utilizzando gli strumenti GPG",
        "verifying_signatures": "Verifica delle Firma",
        "use_gpg_verify": "Usa 'gpg --verify' per controllare le firme",
        "configure_pip_verify": "Configura pip per verificare le firme dei pacchetti",
        "troubleshooting": "Risoluzione dei Problemi",
        "ensure_gpg_in_path": "Assicurati che GPG sia nel tuo PATH di sistema",
        "check_key_permissions": "Controlla i permessi e l'accessibilità delle chiavi",
        "verify_key_not_expired": "Verifica che la tua chiave GPG non sia scaduta",
        "quit_confirmation": "Sei sicuro di volere uscire?",
    },
    "es": {
        # Main window
        "app_title": "Gestor de Paquetes Python",
        "menu_file": "Archivo",
        "menu_edit": "Editar",
        "menu_view": "Ver",
        "menu_tools": "Herramientas",
        "menu_language": "Idioma",
        "menu_help": "Ayuda",
        "status_ready": "Listo",
        "status_processing": "Procesando...",
        "status_done": "Hecho",
        "status_error": "Error",
        "exit": "Salir",

        # Menu Editar
        "undo": "Deshacer",
        "redo": "Rehacer",
        "cut": "Cortar",
        "copy": "Copiar",
        "paste": "Pegar",
        "delete": "Eliminar",

        # Menu Ver
        "toolbar": "Barra de herramientas",
        "status_bar": "Barra de estado",
        "console": "Consola",
        "zoom_in": "Acercar",
        "zoom_out": "Alejar",
        "reset_zoom": "Restablecer zoom",

        # Menu Ayuda
        "documentation": "Documentación",
        "report_issue": "Reportar problema",
        "about": "Acerca de",
        "sponsor": "Patrocinar",

        # Menu Herramientas
        "package_manager": "Gestor de paquetes",
        "view_log": "Ver registro",
        "terminal": "Abrir terminal",
        "check_for_update": "Buscar actualizaciones",

        # Sponsor Dialog
        "sponsor_on_github": "Patrocinar en GitHub",
        "join_discord": "Unirse a Discord",
        "buy_me_a_coffee": "Invitarme un café",
        "join_the_patreon": "Unirse a Patreon",
        "close": "Cerrar",
        
        # Buttons & Common UI
        "btn_ok": "Aceptar",
        "btn_cancel": "Cancelar",
        "btn_apply": "Aplicar",
        "btn_close": "Cerrar",
        "btn_yes": "Sí",
        "btn_no": "No",
        "btn_browse": "Examinar...",
        "btn_save": "Guardar",
        "btn_install": "Instalar",
        "btn_uninstall": "Desinstalar",
        "btn_update": "Actualizar",
        "btn_check": "Comprobar",
        "btn_confirm": "Confirmar",
        "btn_delete": "Eliminar",
        "btn_edit": "Editar",
        "btn_add": "Añadir",
        "btn_remove": "Eliminar",
        "btn_refresh": "Actualizar",
        "btn_search": "Buscar",
       
        "uninstall_package": "Desinstalar paquete",
        "update_package": "Actualizar paquete",
        "manage_repositories": "Gestionar repositorios",
        "manage_dependencies": "Gestionar dependencias",
        "welcome_message": "Bienvenido a PyPackager",
        "no_recent_projects": "No hay proyectos recientes",
        "ready": "Listo",

        # Gestión de Dependencias
        "dependencies": "Dependencias",
        "install_package": "Instalar paquete",
        "package_name": "Nombre del paquete",
        "package_version": "Versión",
        "upgrade": "Actualizar",
        "force_reinstall": "Reinstalar forzadamente",
        "no_deps": "Sin dependencias",
        "pre_release": "Versión preliminar",
        "install_btn": "Instalar",
        "uninstall": "Desinstalar",
        "update": "Actualizar",
        "check_conflicts": "Comprobar conflictos",
        "package": "Paquete",
        "version": "Versión",
        "required_by": "Requerido por",
        "loading_dependencies": "Cargando dependencias",
        "dependencies_loaded": "Dependencias cargadas",
        "error_loading_dependencies": "Error al cargar las dependencias",
        "warning": "Advertencia",
        "no_package_selected": "Ningún paquete seleccionado",
        "installing_dependencies": "Instalando dependencias",
        "dependencies_installed": "Dependencias instaladas correctamente",
        "confirm_removal": "Confirmar eliminación",
        "confirm_uninstall_packages": "¿Está seguro de que desea desinstalar los siguientes paquetes?\n\n{}",
        "uninstalling_packages": "Desinstalando paquetes",
        "packages_uninstalled": "Paquetes desinstalados correctamente",
        "confirm_update": "Confirmar actualización",
        "confirm_update_all_packages": "¿Está seguro de que desea actualizar todos los paquetes a sus últimas versiones?",
        "updating_packages": "Actualizando paquetes",
        "packages_updated": "Paquetes actualizados correctamente",
        "checking_conflicts": "Comprobando conflictos...",
        "conflicts_found": "Conflictos encontrados",
        "conflicts_detected": "Se han detectado los siguientes conflictos:\n\n{}",
        "no_conflicts": "Sin conflictos",
        "no_conflicts_found": "No se encontraron conflictos de dependencias.",
        "error_checking_conflicts": "Error al comprobar conflictos",
        "error_executing_command": "Error al ejecutar el comando",
        "unexpected_error": "Se ha producido un error inesperado",
        "error": "Error",
        "manage_requirements": "Gestionar requisitos",
        "requirements_file": "Archivo de requisitos",
        "install_requirements": "Instalar requisitos",
        "success": "Éxito",
        "requirements_saved": "Requisitos guardados correctamente",
        "error_saving_requirements": "Error al guardar los requisitos",
        
        # Gestión de Proyectos
        "project": "Proyecto",
        "new_project": "Nuevo proyecto",
        "open_project": "Abrir proyecto",
        "save_project": "Guardar proyecto",
        "save_project_as": "Guardar proyecto como...",
        "close_project": "Cerrar proyecto",
        "project_properties": "Propiedades del proyecto",
        "project_created": "¡Proyecto creado correctamente!",
        "project_creation_error": "Error al crear el proyecto: {error}",
        "template_required": "Seleccione una plantilla",
        "project_creation_failed": "No se pudo crear el proyecto en {path}",
        "project_opened": "Proyecto abierto correctamente",
        "project_open_failed": "No se pudo abrir el proyecto en {path}",
        "project_saved": "Proyecto guardado correctamente",
        "project_save_failed": "No se pudo guardar el proyecto en {path}",
        "project_closed": "Proyecto cerrado",
        "project_not_found": "Proyecto no encontrado en {path}",
        "project_already_open": "Ya hay un proyecto abierto. Ciérrelo primero.",
        "no_project_open": "No hay ningún proyecto abierto actualmente",
        "quit_confirmation": "¿Estás seguro de que quieres salir?",
    },
    "pt": {
        # Main window
        "app_title": "Gerenciador de Pacotes Python",
        "menu_file": "Arquivo",
        "menu_edit": "Editar",
        "menu_view": "Visualizar",
        "menu_tools": "Ferramentas",
        "menu_language": "Idioma",
        "menu_help": "Ajuda",
        "status_ready": "Pronto",
        "status_processing": "Processando...",
        "status_done": "Concluído",
        "status_error": "Erro",
        "exit": "Sair",

        # Menu Editar
        "undo": "Desfazer",
        "redo": "Refazer",
        "cut": "Recortar",
        "copy": "Copiar",
        "paste": "Colar",
        "delete": "Excluir",

        # Menu Visualizar
        "toolbar": "Barra de ferramentas",
        "status_bar": "Barra de status",
        "console": "Console",
        "zoom_in": "Aumentar zoom",
        "zoom_out": "Diminuir zoom",
        "reset_zoom": "Redefinir zoom",

        # Menu Ajuda
        "documentation": "Documentação",
        "report_issue": "Relatar problema",
        "about": "Sobre",
        "sponsor": "Apoiar",

        # Menu Ferramentas
        "package_manager": "Gerenciador de pacotes",
        "view_log": "Visualizar log",
        "terminal": "Abrir terminal",
        "check_for_update": "Verificar atualizações",

        # Diálogo de Apoio
        "sponsor_on_github": "Apoiar no GitHub",
        "join_discord": "Entrar no Discord",
        "buy_me_a_coffee": "Comprar um café",
        "join_the_patreon": "Apoiar no Patreon",
        "close": "Fechar",
        
        # Botões e Interface Comum
        "btn_ok": "OK",
        "btn_cancel": "Cancelar",
        "btn_apply": "Aplicar",
        "btn_close": "Fechar",
        "btn_yes": "Sim",
        "btn_no": "Não",
        "btn_browse": "Procurar...",
        "btn_save": "Salvar",
        "btn_install": "Instalar",
        "btn_uninstall": "Desinstalar",
        "btn_update": "Atualizar",
        "btn_check": "Verificar",
        "btn_confirm": "Confirmar",
        "btn_delete": "Excluir",
        "btn_edit": "Editar",
        "btn_add": "Adicionar",
        "btn_remove": "Remover",
        "btn_refresh": "Atualizar",
        "btn_search": "Pesquisar",
       
        "uninstall_package": "Desinstalar pacote",
        "update_package": "Atualizar pacote",
        "manage_repositories": "Gerenciar repositórios",
        "manage_dependencies": "Gerenciar dependências",
        "welcome_message": "Bem-vindo ao PyPackager",
        "no_recent_projects": "Nenhum projeto recente",
        "ready": "Pronto",

        # Gerenciamento de Dependências
        "dependencies": "Dependências",
        "install_package": "Instalar pacote",
        "package_name": "Nome do pacote",
        "package_version": "Versão",
        "upgrade": "Atualizar",
        "force_reinstall": "Forçar reinstalação",
        "no_deps": "Sem dependências",
        "pre_release": "Versão pré-lançamento",
        "install_btn": "Instalar",
        "uninstall": "Desinstalar",
        "update": "Atualizar",
        "check_conflicts": "Verificar conflitos",
        "package": "Pacote",
        "version": "Versão",
        "required_by": "Requerido por",
        "loading_dependencies": "Carregando dependências",
        "dependencies_loaded": "Dependências carregadas",
        "error_loading_dependencies": "Erro ao carregar dependências",
        "warning": "Aviso",
        "no_package_selected": "Nenhum pacote selecionado",
        "installing_dependencies": "Instalando dependências",
        "dependencies_installed": "Dependências instaladas com sucesso",
        "confirm_removal": "Confirmar remoção",
        "confirm_uninstall_packages": "Tem certeza de que deseja desinstalar os seguintes pacotes?\n\n{}",
        "uninstalling_packages": "Desinstalando pacotes",
        "packages_uninstalled": "Pacotes desinstalados com sucesso",
        "confirm_update": "Confirmar atualização",
        "confirm_update_all_packages": "Tem certeza de que deseja atualizar todos os pacotes para as versões mais recentes?",
        "updating_packages": "Atualizando pacotes",
        "packages_updated": "Pacotes atualizados com sucesso",
        "checking_conflicts": "Verificando conflitos...",
        "conflicts_found": "Conflitos encontrados",
        "conflicts_detected": "Os seguintes conflitos foram detectados:\n\n{}",
        "no_conflicts": "Sem conflitos",
        "no_conflicts_found": "Nenhum conflito de dependências encontrado.",
        "error_checking_conflicts": "Erro ao verificar conflitos",
        "error_executing_command": "Erro ao executar o comando",
        "unexpected_error": "Ocorreu um erro inesperado",
        "error": "Erro",
        "manage_requirements": "Gerenciar requisitos",
        "requirements_file": "Arquivo de requisitos",
        "install_requirements": "Instalar requisitos",
        "success": "Sucesso",
        "requirements_saved": "Requisitos salvos com sucesso",
        "error_saving_requirements": "Erro ao salvar os requisitos",
        
        # Gerenciamento de Projetos
        "project": "Projeto",
        "new_project": "Novo projeto",
        "open_project": "Abrir projeto",
        "save_project": "Salvar projeto",
        "save_project_as": "Salvar projeto como...",
        "close_project": "Fechar projeto",
        "project_properties": "Propriedades do projeto",
        "project_created": "Projeto criado com sucesso!",
        "project_creation_error": "Erro ao criar o projeto: {error}",
        "template_required": "Selecione um modelo",
        "project_creation_failed": "Falha ao criar o projeto em {path}",
        "project_opened": "Projeto aberto com sucesso",
        "project_open_failed": "Falha ao abrir o projeto em {path}",
        "project_saved": "Projeto salvo com sucesso",
        "project_save_failed": "Falha ao salvar o projeto em {path}",
        "project_closed": "Projeto fechado",
        "project_not_found": "Projeto não encontrado em {path}",
        "project_already_open": "Já há um projeto aberto. Feche-o primeiro.",
        "no_project_open": "Nenhum projeto aberto",
        "quit_confirmation": "Tem a certeza de que deseja sair do programa?",
    },
    "de": {
        # Main window
        "app_title": "Python-Paketverwaltung",
        "menu_file": "Datei",
        "menu_edit": "Bearbeiten",
        "menu_view": "Ansicht",
        "menu_tools": "Werkzeuge",
        "menu_language": "Sprache",
        "menu_help": "Hilfe",
        "status_ready": "Bereit",
        "status_processing": "Wird verarbeitet...",
        "status_done": "Fertig",
        "status_error": "Fehler",
        "exit": "Beenden",

        # Menu Bearbeiten
        "undo": "Rückgängig",
        "redo": "Wiederholen",
        "cut": "Ausschneiden",
        "copy": "Kopieren",
        "paste": "Einfügen",
        "delete": "Löschen",

        # Menu Ansicht
        "toolbar": "Symbolleiste",
        "status_bar": "Statusleiste",
        "console": "Konsole",
        "zoom_in": "Vergrößern",
        "zoom_out": "Verkleinern",
        "reset_zoom": "Zoom zurücksetzen",

        # Menu Hilfe
        "documentation": "Dokumentation",
        "report_issue": "Problem melden",
        "about": "Über",
        "sponsor": "Unterstützen",

        # Menu Werkzeuge
        "package_manager": "Paketverwaltung",
        "view_log": "Protokoll anzeigen",
        "terminal": "Terminal öffnen",
        "check_for_update": "Auf Aktualisierungen prüfen",

        # Spenden-Dialog
        "sponsor_on_github": "Auf GitHub unterstützen",
        "join_discord": "Discord beitreten",
        "buy_me_a_coffee": "Kauf mir einen Kaffee",
        "join_the_patreon": "Patreon beitreten",
        "close": "Schließen",
        
        # Schaltflächen und allgemeine Benutzeroberfläche
        "btn_ok": "OK",
        "btn_cancel": "Abbrechen",
        "btn_apply": "Übernehmen",
        "btn_close": "Schließen",
        "btn_yes": "Ja",
        "btn_no": "Nein",
        "btn_browse": "Durchsuchen...",
        "btn_save": "Speichern",
        "btn_install": "Installieren",
        "btn_uninstall": "Deinstallieren",
        "btn_update": "Aktualisieren",
        "btn_check": "Überprüfen",
        "btn_confirm": "Bestätigen",
        "btn_delete": "Löschen",
        "btn_edit": "Bearbeiten",
        "btn_add": "Hinzufügen",
        "btn_remove": "Entfernen",
        "btn_refresh": "Aktualisieren",
        "btn_search": "Suchen",
       
        "uninstall_package": "Paket deinstallieren",
        "update_package": "Paket aktualisieren",
        "manage_repositories": "Repositorys verwalten",
        "manage_dependencies": "Abhängigkeiten verwalten",
        "welcome_message": "Willkommen bei PyPackager",
        "no_recent_projects": "Keine kürzlichen Projekte",
        "ready": "Bereit",

        # Abhängigkeitsverwaltung
        "dependencies": "Abhängigkeiten",
        "install_package": "Paket installieren",
        "package_name": "Paketname",
        "package_version": "Version",
        "upgrade": "Aktualisieren",
        "force_reinstall": "Erneut installieren",
        "no_deps": "Keine Abhängigkeiten",
        "pre_release": "Vorabversion",
        "install_btn": "Installieren",
        "uninstall": "Deinstallieren",
        "update": "Aktualisieren",
        "check_conflicts": "Konflikte prüfen",
        "package": "Paket",
        "version": "Version",
        "required_by": "Erforderlich für",
        "loading_dependencies": "Lade Abhängigkeiten...",
        "dependencies_loaded": "Abhängigkeiten geladen",
        "error_loading_dependencies": "Fehler beim Laden der Abhängigkeiten",
        "warning": "Warnung",
        "no_package_selected": "Kein Paket ausgewählt",
        "installing_dependencies": "Installiere Abhängigkeiten...",
        "dependencies_installed": "Abhängigkeiten erfolgreich installiert",
        "confirm_removal": "Löschen bestätigen",
        "confirm_uninstall_packages": "Sind Sie sicher, dass Sie die folgenden Pakete deinstallieren möchten?\n\n{}",
        "uninstalling_packages": "Deinstalliere Pakete...",
        "packages_uninstalled": "Pakete erfolgreich deinstalliert",
        "confirm_update": "Aktualisierung bestätigen",
        "confirm_update_all_packages": "Möchten Sie wirklich alle Pakete auf die neuesten Versionen aktualisieren?",
        "updating_packages": "Aktualisiere Pakete...",
        "packages_updated": "Pakete erfolgreich aktualisiert",
        "checking_conflicts": "Prüfe auf Konflikte...",
        "conflicts_found": "Konflikte gefunden",
        "conflicts_detected": "Folgende Konflikte wurden erkannt:\n\n{}",
        "no_conflicts": "Keine Konflikte",
        "no_conflicts_found": "Keine Abhängigkeitskonflikte gefunden.",
        "error_checking_conflicts": "Fehler bei der Konfliktprüfung",
        "error_executing_command": "Fehler beim Ausführen des Befehls",
        "unexpected_error": "Ein unerwarteter Fehler ist aufgetreten",
        "error": "Fehler",
        "manage_requirements": "Anforderungen verwalten",
        "requirements_file": "Anforderungsdatei",
        "install_requirements": "Anforderungen installieren",
        "success": "Erfolg",
        "requirements_saved": "Anforderungen erfolgreich gespeichert",
        "error_saving_requirements": "Fehler beim Speichern der Anforderungen",
        
        # Projektverwaltung
        "project": "Projekt",
        "new_project": "Neues Projekt",
        "open_project": "Projekt öffnen",
        "save_project": "Projekt speichern",
        "save_project_as": "Projekt speichern unter...",
        "close_project": "Projekt schließen",
        "project_properties": "Projekteigenschaften",
        "project_created": "Projekt erfolgreich erstellt!",
        "project_creation_error": "Fehler beim Erstellen des Projekts: {error}",
        "template_required": "Bitte wählen Sie eine Vorlage aus",
        "project_creation_failed": "Projekt konnte unter {path} nicht erstellt werden",
        "project_opened": "Projekt erfolgreich geöffnet",
        "project_open_failed": "Projekt konnte unter {path} nicht geöffnet werden",
        "project_saved": "Projekt erfolgreich gespeichert",
        "project_save_failed": "Projekt konnte unter {path} nicht gespeichert werden",
        "project_closed": "Projekt geschlossen",
        "project_not_found": "Projekt unter {path} nicht gefunden",
        "project_already_open": "Ein Projekt ist bereits geöffnet. Bitte schließen Sie es zuerst.",
        "no_project_open": "Nenhum Projekt geöffnet",
        "quit_confirmation": "Sind Sie sicher, dass Sie das Programm beenden möchten?",
    },
    "fr": {
        # Fenêtre principale
        "app_title": "Gestionnaire de paquets Python",
        "menu_file": "Fichier",
        "menu_edit": "Édition",
        "menu_view": "Affichage",
        "menu_tools": "Outils",
        "menu_language": "Langue",
        "menu_help": "Aide",
        "status_ready": "Prêt",
        "status_processing": "Traitement en cours...",
        "status_done": "Terminé",
        "status_error": "Erreur",
        "exit": "Quitter",

        # Menu Édition
        "undo": "Annuler",
        "redo": "Rétablir",
        "cut": "Couper",
        "copy": "Copier",
        "paste": "Coller",
        "delete": "Supprimer",

        # Menu Affichage
        "toolbar": "Barre d'outils",
        "status_bar": "Barre d'état",
        "console": "Console",
        "zoom_in": "Zoom avant",
        "zoom_out": "Zoom arrière",
        "reset_zoom": "Réinitialiser le zoom",

        # Menu Aide
        "documentation": "Documentation",
        "report_issue": "Signaler un problème",
        "about": "À propos",
        "sponsor": "Soutenir",

        # Menu Outils
        "package_manager": "Gestionnaire de paquets",
        "view_log": "Voir le journal",
        "terminal": "Ouvrir le terminal",
        "check_for_update": "Vérifier les mises à jour",

        # Dialogue de soutien
        "sponsor_on_github": "Soutenir sur GitHub",
        "join_discord": "Rejoindre Discord",
        "buy_me_a_coffee": "M'offrir un café",
        "join_the_patreon": "Devenir mécène",
        "close": "Fermer",
        
        # Boutons et interface commune
        "btn_ok": "OK",
        "btn_cancel": "Annuler",
        "btn_apply": "Appliquer",
        "btn_close": "Fermer",
        "btn_yes": "Oui",
        "btn_no": "Non",
        "btn_browse": "Parcourir...",
        "btn_save": "Enregistrer",
        "btn_install": "Installer",
        "btn_uninstall": "Désinstaller",
        "btn_update": "Mettre à jour",
        "btn_check": "Vérifier",
        "btn_confirm": "Confirmer",
        "btn_delete": "Supprimer",
        "btn_edit": "Modifier",
        "btn_add": "Ajouter",
        "btn_remove": "Supprimer",
        "btn_refresh": "Actualiser",
        "btn_search": "Rechercher",
       
        "uninstall_package": "Désinstaller le paquet",
        "update_package": "Mettre à jour le paquet",
        "manage_repositories": "Gérer les dépôts",
        "manage_dependencies": "Gérer les dépendances",
        "welcome_message": "Bienvenue sur PyPackager",
        "no_recent_projects": "Aucun projet récent",
        "ready": "Prêt",

        # Gestion des dépendances
        "dependencies": "Dépendances",
        "install_package": "Installer un paquet",
        "package_name": "Nom du paquet",
        "package_version": "Version",
        "upgrade": "Mettre à jour",
        "force_reinstall": "Réinstaller",
        "no_deps": "Aucune dépendance",
        "pre_release": "Version préliminaire",
        "install_btn": "Installer",
        "uninstall": "Désinstaller",
        "update": "Mettre à jour",
        "check_conflicts": "Vérifier les conflits",
        "package": "Paquet",
        "version": "Version",
        "required_by": "Nécessité pour",
        "loading_dependencies": "Chargement des dépendances...",
        "dependencies_loaded": "Dépendances chargées",
        "error_loading_dependencies": "Erreur lors du chargement des dépendances",
        "warning": "Avertissement",
        "no_package_selected": "Aucun paquet sélectionné",
        "installing_dependencies": "Installation des dépendances...",
        "dependencies_installed": "Dépendances installées avec succès",
        "confirm_removal": "Confirmer la suppression",
        "confirm_uninstall_packages": "Êtes-vous sûr de vouloir désinstaller les paquets suivants ?\n\n{}",
        "uninstalling_packages": "Désinstallation des paquets...",
        "packages_uninstalled": "Paquets désinstallés avec succès",
        "confirm_update": "Confirmer la mise à jour",
        "confirm_update_all_packages": "Voulez-vous vraiment mettre à jour tous les paquets vers leurs dernières versions ?",
        "updating_packages": "Mise à jour des paquets...",
        "packages_updated": "Paquets mis à jour avec succès",
        "checking_conflicts": "Vérification des conflits...",
        "conflicts_found": "Conflits trouvés",
        "conflicts_detected": "Les conflits suivants ont été détectés :\n\n{}",
        "no_conflicts": "Aucun conflit",
        "no_conflicts_found": "Aucun conflit de dépendances trouvé.",
        "error_checking_conflicts": "Erreur lors de la vérification des conflits",
        "error_executing_command": "Erreur lors de l'exécution de la commande",
        "unexpected_error": "Une erreur inattendue est survenue",
        "error": "Erreur",
        "manage_requirements": "Gérer les exigences",
        "requirements_file": "Fichier des exigences",
        "install_requirements": "Installer les exigences",
        "success": "Succès",
        "requirements_saved": "Exigences enregistrées avec succès",
        "error_saving_requirements": "Erreur lors de l'enregistrement des exigences",
        
        # Gestion de projet
        "project": "Projet",
        "new_project": "Nouveau projet",
        "open_project": "Ouvrir un projet",
        "save_project": "Enregistrer le projet",
        "save_project_as": "Enregistrer le projet sous...",
        "close_project": "Fermer le projet",
        "project_properties": "Propriétés du projet",
        "project_created": "Projet créé avec succès !",
        "project_creation_error": "Erreur lors de la création du projet : {error}",
        "template_required": "Veuillez sélectionner un modèle",
        "project_creation_failed": "Échec de la création du projet à l'emplacement {path}",
        "project_opened": "Projet ouvert avec succès",
        "project_open_failed": "Échec de l'ouverture du projet à l'emplacement {path}",
        "project_saved": "Projet enregistré avec succès",
        "project_save_failed": "Échec de l'enregistrement du projet à l'emplacement {path}",
        "project_closed": "Projet fermé",
        "project_not_found": "Projet introuvable à l'emplacement {path}",
        "project_already_open": "Un projet est déjà ouvert. Veuillez d'abord le fermer.",
        "no_project_open": "Aucun projet ouvert",
         "quit_confirmation": "Êtes-vous sûr de vouloir quitter le programme?",
    },
    "ru": {
        # Главное окно
        "app_title": "Менеджер пакетов Python",
        "menu_file": "Файл",
        "menu_edit": "Правка",
        "menu_view": "Вид",
        "menu_tools": "Инструменты",
        "menu_language": "Язык",
        "menu_help": "Справка",
        "status_ready": "Готово",
        "status_processing": "Обработка...",
        "status_done": "Готово",
        "status_error": "Ошибка",
        "exit": "Выход",

        # Меню Правка
        "undo": "Отменить",
        "redo": "Повторить",
        "cut": "Вырезать",
        "copy": "Копировать",
        "paste": "Вставить",
        "delete": "Удалить",

        # Меню Вид
        "toolbar": "Панель инструментов",
        "status_bar": "Строка состояния",
        "console": "Консоль",
        "zoom_in": "Увеличить",
        "zoom_out": "Уменьшить",
        "reset_zoom": "Сбросить масштаб",

        # Меню Справка
        "documentation": "Документация",
        "report_issue": "Сообщить о проблеме",
        "about": "О программе",
        "sponsor": "Поддержать",

        # Меню Инструменты
        "package_manager": "Менеджер пакетов",
        "view_log": "Просмотр лога",
        "terminal": "Открыть терминал",
        "check_for_update": "Проверить обновления",

        # Диалог поддержки
        "sponsor_on_github": "Поддержать на GitHub",
        "join_discord": "Присоединиться к Discord",
        "buy_me_a_coffee": "Купить мне кофе",
        "join_the_patreon": "Стать спонсором на Patreon",
        "close": "Закрыть",
        
        # Кнопки и общий интерфейс
        "btn_ok": "ОК",
        "btn_cancel": "Отмена",
        "btn_apply": "Применить",
        "btn_close": "Закрыть",
        "btn_yes": "Да",
        "btn_no": "Нет",
        "btn_browse": "Обзор...",
        "btn_save": "Сохранить",
        "btn_install": "Установить",
        "btn_uninstall": "Удалить",
        "btn_update": "Обновить",
        "btn_check": "Проверить",
        "btn_confirm": "Подтвердить",
        "btn_delete": "Удалить",
        "btn_edit": "Редактировать",
        "btn_add": "Добавить",
        "btn_remove": "Удалить",
        "btn_refresh": "Обновить",
        "btn_search": "Поиск",
       
        "uninstall_package": "Удалить пакет",
        "update_package": "Обновить пакет",
        "manage_repositories": "Управление репозиториями",
        "manage_dependencies": "Управление зависимостями",
        "welcome_message": "Добро пожаловать в PyPackager",
        "no_recent_projects": "Нет недавних проектов",
        "ready": "Готово",

        # Управление зависимостями
        "dependencies": "Зависимости",
        "install_package": "Установить пакет",
        "package_name": "Имя пакета",
        "package_version": "Версия",
        "upgrade": "Обновить",
        "force_reinstall": "Переустановить",
        "no_deps": "Нет зависимостей",
        "pre_release": "Предварительная версия",
        "install_btn": "Установить",
        "uninstall": "Удалить",
        "update": "Обновить",
        "check_conflicts": "Проверить конфликты",
        "package": "Пакет",
        "version": "Версия",
        "required_by": "Требуется для",
        "loading_dependencies": "Загрузка зависимостей...",
        "dependencies_loaded": "Зависимости загружены",
        "error_loading_dependencies": "Ошибка загрузки зависимостей",
        "warning": "Предупреждение",
        "no_package_selected": "Пакет не выбран",
        "installing_dependencies": "Установка зависимостей...",
        "dependencies_installed": "Зависимости успешно установлены",
        "confirm_removal": "Подтверждение удаления",
        "confirm_uninstall_packages": "Вы уверены, что хотите удалить следующие пакеты?\n\n{}",
        "uninstalling_packages": "Удаление пакетов...",
        "packages_uninstalled": "Пакеты успешно удалены",
        "confirm_update": "Подтверждение обновления",
        "confirm_update_all_packages": "Вы действительно хотите обновить все пакеты до последних версий?",
        "updating_packages": "Обновление пакетов...",
        "packages_updated": "Пакеты успешно обновлены",
        "checking_conflicts": "Проверка конфликтов...",
        "conflicts_found": "Обнаружены конфликты",
        "conflicts_detected": "Обнаружены следующие конфликты:\n\n{}",
        "no_conflicts": "Нет конфликтов",
        "no_conflicts_found": "Конфликты зависимостей не найдены.",
        "error_checking_conflicts": "Ошибка при проверке конфликтов",
        "error_executing_command": "Ошибка выполнения команды",
        "unexpected_error": "Произошла непредвиденная ошибка",
        "error": "Ошибка",
        "manage_requirements": "Управление требованиями",
        "requirements_file": "Файл требований",
        "install_requirements": "Установить требования",
        "success": "Успешно",
        "requirements_saved": "Требования успешно сохранены",
        "error_saving_requirements": "Ошибка сохранения требований",
        
        # Управление проектом
        "project": "Проект",
        "new_project": "Новый проект",
        "open_project": "Открыть проект",
        "save_project": "Сохранить проект",
        "save_project_as": "Сохранить проект как...",
        "close_project": "Закрыть проект",
        "project_properties": "Свойства проекта",
        "project_created": "Проект успешно создан!",
        "project_creation_error": "Ошибка при создании проекта: {error}",
        "template_required": "Пожалуйста, выберите шаблон",
        "project_creation_failed": "Не удалось создать проект по пути {path}",
        "project_opened": "Проект успешно открыт",
        "project_open_failed": "Не удалось открыть проект по пути {path}",
        "project_saved": "Проект успешно сохранен",
        "project_save_failed": "Не удалось сохранить проект по пути {path}",
        "project_closed": "Проект закрыт",
        "project_not_found": "Проект не найден по пути {path}",
        "project_already_open": "Проект уже открыт. Пожалуйста, сначала закройте его.",
        "no_project_open": "Нет открытых проектов",
        "quit_confirmation": "Вы уверены, что хотите выйти из программы?",
    }
}


class Translator:
    """Handles language translation for the application."""
    
    def __init__(self):
        self._translations = TRANSLATIONS
        # Try to load language from config, fall back to default
        try:
            config = _load_config()
            lang = config.get('language', DEFAULT_LANGUAGE)
            if lang in self._translations:
                self._language = lang
            else:
                self._language = DEFAULT_LANGUAGE
        except Exception as e:
            print(f"Error loading language preference: {e}", file=sys.stderr)
            self._language = DEFAULT_LANGUAGE
    
    def set_language(self, lang_code: str) -> bool:
        """Set the current language and save the preference.
        
        Args:
            lang_code: The language code to set (e.g., 'en', 'it')
            
        Returns:
            bool: True if the language was set successfully, False otherwise
        """
        if lang_code in self._translations and lang_code != self._language:
            self._language = lang_code
            # Save the preference to config
            try:
                config = _load_config()
                config['language'] = lang_code
                _save_config(config)
                return True
            except Exception as e:
                print(f"Error saving language preference: {e}", file=sys.stderr)
                return False
        return False
    
    def get_language(self) -> str:
        """Get the current language code."""
        return self._language
    
    def translate(self, key: str, **kwargs) -> str:
        """Translate a key to the current language."""
        try:
            # Try to get the translation
            translation = self._translations[self._language].get(key, 
                self._translations[DEFAULT_LANGUAGE].get(key, key))
            
            # Format the string with any provided kwargs
            if kwargs:
                try:
                    return translation.format(**kwargs)
                except (KeyError, IndexError):
                    return translation
            return translation
        except Exception as e:
            print(f"Translation error for key '{key}': {e}", file=sys.stderr)
            return key


# Create a global translator instance
translator = Translator()

# Create a shortcut function for easier access
def tr(key: str, **kwargs) -> str:
    """Translate the given key to the current language."""
    return translator.translate(key, **kwargs)
