import tkinter as tk
from tkinter import ttk, messagebox
from .lang import tr

class Help:
    
    @staticmethod
    def show_help(parent):
        """
        Display the Help dialog.
        
        This method creates and shows a modal dialog with help information
        organized in tabs. The dialog includes sections for usage instructions,
        features, and tips.
        
        Args:
            parent (tk.Tk): The parent window for the dialog
        """
        # Create and configure the help window
        help_window = tk.Toplevel(parent)
        help_window.title(tr('help'))
        help_window.geometry("800x600")
        help_window.minsize(600, 400)
        
        # Make the window modal
        help_window.transient(parent)
        help_window.grab_set()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(help_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add tabs with translated titles
        Help._add_usage_tab(notebook, tr('usage_tab'))
        Help._add_features_tab(notebook, tr('features_tab'))
        Help._add_dependencies_tab(notebook, tr('dependencies'))
        Help._add_signing_tab(notebook, tr('package_signing'))
        
        # Add close button
        btn_frame = ttk.Frame(help_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(
            btn_frame, 
            text=tr('close'), 
            command=help_window.destroy
        ).pack(side=tk.RIGHT)
        
        # Wait for the window to close
        parent.wait_window(help_window)
    
    @staticmethod
    def _add_usage_tab(notebook, tab_title):
        """
        Add usage instructions tab.
        
        Args:
            notebook: Notebook widget to add the tab to
            tab_title: Title for the tab
        """
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=tab_title)
        
        # Create a scrollable frame for better content organization
        canvas = tk.Canvas(frame, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the scrollable area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add help content with translations
        sections = [
            (tr('creating_project'), [
                tr('click_file_new_project'),
                tr('select_project_directory'),
                tr('enter_package_details'),
                tr('click_create_to_initialize')
            ]),
            (tr('building_packages'), [
                tr('open_your_project'),
                tr('click_build_to_create'),
                tr('find_packages_in_dist')
            ]),
            (tr('installing_packages'), [
                tr('open_your_project'),
                tr('click_install_dev_mode'),
                tr('use_uninstall_to_remove')
            ]),
            (tr('managing_dependencies'), [
                tr('click_dependencies'),
                tr('add_remove_dependencies'),
                tr('check_dependency_conflicts')
            ]),
            (tr('package_signing'), [
                tr('ensure_gpg_installed'),
                tr('click_sign_to_sign'),
                tr('verify_signatures_gpg')
            ])
        ]
        
        # Add title
        title = ttk.Label(
            scrollable_frame, 
            text=tr('usage_guide'),
            font=('TkDefaultFont', 12, 'bold')
        )
        title.pack(pady=(0, 10), anchor='w')
        
        # Add content
        for i, (section_title, items) in enumerate(sections, 1):
            # Section title
            ttk.Label(
                scrollable_frame,
                text=f"{i}. {section_title}",
                font=('TkDefaultFont', 10, 'bold')
            ).pack(anchor='w', pady=(10, 5))
            
            # Bullet points
            for item in items:
                ttk.Label(
                    scrollable_frame,
                    text=f"   • {item}",
                    wraplength=700,
                    justify='left'
                ).pack(anchor='w', padx=20)
    
    @staticmethod
    def _add_features_tab(notebook, tab_title):
        """
        Add features tab.
        
        Args:
            notebook: Notebook widget to add the tab to
            tab_title: Title for the tab
        """
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=tab_title)
        
        # Create a scrollable frame for better content organization
        canvas = tk.Canvas(frame, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the scrollable area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add title
        title = ttk.Label(
            scrollable_frame, 
            text=tr('features_overview'),
            font=('TkDefaultFont', 12, 'bold')
        )
        title.pack(pady=(0, 10), anchor='w')
        
        # Feature categories
        categories = [
            (tr('project_management'), [
                tr('create_new_packages'),
                tr('manage_project_metadata'),
                tr('handle_dependencies')
            ]),
            (tr('building_distribution'), [
                tr('build_source_distributions'),
                tr('create_wheel_packages'),
                tr('generate_setup_files'),
                tr('sign_packages')
            ]),
            (tr('dependency_management'), [
                tr('add_remove_dependencies'),
                tr('check_for_updates'),
                tr('resolve_conflicts'),
                tr('manage_requirements')
            ]),
            (tr('repository_support'), [
                tr('add_custom_repositories'),
                tr('manage_repository_creds'),
                tr('publish_to_pypi')
            ]),
            (tr('development_tools'), [
                tr('integrated_terminal'),
                tr('log_viewer'),
                tr('package_manager_integration')
            ])
        ]
        
        # Add content
        for category, items in categories:
            # Category title
            ttk.Label(
                scrollable_frame,
                text=f"• {category}:",
                font=('TkDefaultFont', 10, 'bold')
            ).pack(anchor='w', pady=(10, 5))
            
            # Feature items
            for item in items:
                ttk.Label(
                    scrollable_frame,
                    text=f"  - {item}",
                    wraplength=700,
                    justify='left'
                ).pack(anchor='w', padx=20)
    
    @staticmethod
    def _add_dependencies_tab(notebook, tab_title):
        """
        Add dependencies management tab.
        
        Args:
            notebook: Notebook widget to add the tab to
            tab_title: Title for the tab
        """
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=tab_title)
        
        # Create a scrollable frame for better content organization
        canvas = tk.Canvas(frame, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the scrollable area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add title
        title = ttk.Label(
            scrollable_frame, 
            text=tr('managing_dependencies'),
            font=('TkDefaultFont', 12, 'bold')
        )
        title.pack(pady=(0, 10), anchor='w')
        
        # Add content sections
        sections = [
            (tr('adding_dependencies'), [
                tr('click_add_dependencies'),
                tr('enter_package_details'),
                tr('choose_install_options')
            ]),
            (tr('updating_dependencies'), [
                tr('select_packages_update'),
                tr('click_update_versions')
            ]),
            (tr('resolving_conflicts'), [
                tr('click_check_conflicts'),
                tr('review_resolve_issues')
            ]),
            (tr('requirements_files'), [
                tr('import_from_requirements'),
                tr('export_current_dependencies'),
                tr('install_from_requirements')
            ])
        ]
        
        # Add content
        for i, (section_title, items) in enumerate(sections, 1):
            # Section title
            ttk.Label(
                scrollable_frame,
                text=f"{i}. {section_title}:",
                font=('TkDefaultFont', 10, 'bold')
            ).pack(anchor='w', pady=(10, 5))
            
            # Section items
            for item in items:
                ttk.Label(
                    scrollable_frame,
                    text=f"   • {item}",
                    wraplength=700,
                    justify='left'
                ).pack(anchor='w', padx=20)
    
    @staticmethod
    def _add_signing_tab(notebook, tab_title):
        """
        Add package signing tab.
        
        Args:
            notebook: Notebook widget to add the tab to
            tab_title: Title for the tab
        """
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=tab_title)
        
        # Create a scrollable frame for better content organization
        canvas = tk.Canvas(frame, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the scrollable area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add title
        title = ttk.Label(
            scrollable_frame, 
            text=tr('package_signing_with_gpg'),
            font=('TkDefaultFont', 12, 'bold')
        )
        title.pack(pady=(0, 10), anchor='w')
        
        # Add content sections
        sections = [
            (tr('prerequisites'), [
                tr('install_gnupg_system'),
                tr('setup_gpg_key_pair'),
                tr('configure_git_signing')
            ]),
            (tr('signing_packages'), [
                tr('build_your_package'),
                tr('click_sign_to_sign'),
                tr('verify_using_gpg_tools')
            ]),
            (tr('verifying_signatures'), [
                tr('use_gpg_verify'),
                tr('configure_pip_verify')
            ]),
            (tr('troubleshooting'), [
                tr('ensure_gpg_in_path'),
                tr('check_key_permissions'),
                tr('verify_key_not_expired')
            ])
        ]
        
        # Add content
        for i, (section_title, items) in enumerate(sections, 1):
            # Section title
            ttk.Label(
                scrollable_frame,
                text=f"{i}. {section_title}:",
                font=('TkDefaultFont', 10, 'bold')
            ).pack(anchor='w', pady=(10, 5))
            
            # Section items
            for item in items:
                ttk.Label(
                    scrollable_frame,
                    text=f"   • {item}",
                    wraplength=700,
                    justify='left'
                ).pack(anchor='w', padx=20)
