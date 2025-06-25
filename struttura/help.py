import os
import re
import webbrowser
import tkinter as tk
from tkinter import ttk, font as tkfont
from tkinter.scrolledtext import ScrolledText
import markdown2
from io import StringIO
from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()
    
    def handle_data(self, d):
        self.text.write(d)
    
    def get_data(self):
        return self.text.getvalue()

def strip_html(html):
    """Remove all HTML tags from the given HTML string."""
    if not html:
        return ""
    # Remove script and style elements
    clean = re.compile(r'<(script|style).*?>.*?</\1>', re.DOTALL | re.IGNORECASE)
    html = re.sub(clean, '', html)
    
    # Replace <br> and other self-closing tags with newlines
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    
    # Remove HTML comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # Remove all other HTML tags
    html = re.sub(r'<[^>]+>', '', html)
    
    # Decode HTML entities
    try:
        from html import unescape
        html = unescape(html)
    except ImportError:
        import html.parser
        html = html.parser.HTMLParser().unescape(html)
    
    # Normalize whitespace
    html = ' '.join(html.split())
    return html.strip()

def show_help():
    """Display the help window with styled Markdown content from HELP.md"""
    # Create a new window
    help_window = tk.Toplevel()
    help_window.title("Help - Python Package Manager")
    help_window.geometry("900x700")
    help_window.minsize(600, 400)
    
    # Configure grid weights
    help_window.grid_rowconfigure(0, weight=1)
    help_window.grid_columnconfigure(0, weight=1)
    
    # Create main frame
    main_frame = ttk.Frame(help_window, padding="10")
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    
    # Create text widget with scrollbar
    text_frame = ttk.Frame(main_frame)
    text_frame.grid(row=0, column=0, sticky="nsew")
    text_frame.grid_rowconfigure(0, weight=1)
    text_frame.grid_columnconfigure(0, weight=1)
    
    # Create a custom text widget with better font handling
    text_widget = ScrolledText(
        text_frame,
        wrap=tk.WORD,
        font=('Segoe UI', 10),
        padx=10,
        pady=10,
        undo=True,
        bg='white',
        fg='#333333',
        insertbackground='black',
        selectbackground='#b1d7fe',
        selectforeground='black',
        inactiveselectbackground='#e6e6e6'
    )
    
    # Configure tags for different markdown elements
    text_widget.tag_configure('h1', font=('Segoe UI', 18, 'bold'), spacing3=10)
    text_widget.tag_configure('h2', font=('Segoe UI', 16, 'bold'), spacing3=8)
    text_widget.tag_configure('h3', font=('Segoe UI', 14, 'bold'), spacing3=6)
    text_widget.tag_configure('code', font=('Consolas', 10), background='#f5f5f5', 
                             relief='flat', borderwidth=1, lmargin1=20, lmargin2=20, rmargin=20)
    text_widget.tag_configure('link', foreground='#0066cc', underline=1)
    text_widget.tag_configure('bold', font=('Segoe UI', 10, 'bold'))
    text_widget.tag_configure('italic', font=('Segoe UI', 10, 'italic'))
    text_widget.tag_configure('list', lmargin1=20, lmargin2=40, rmargin=10)
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    # Grid layout
    text_widget.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    # Add close button at the bottom
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=1, column=0, sticky="e", pady=(10, 0))
    
    close_btn = ttk.Button(button_frame, text="Close", command=help_window.destroy)
    close_btn.pack(side=tk.RIGHT, padx=5)
    
    # Function to handle hyperlinks
    def on_link_click(event):
        index = text_widget.index(f"@{event.x},{event.y}")
        tags = text_widget.tag_names(index)
        
        for tag in tags:
            if tag.startswith('link-'):
                url = tag[5:]
                try:
                    webbrowser.open(url)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open URL: {e}")
                break
    
    text_widget.tag_bind("link", "<Button-1>", on_link_click)
    
    def clean_html(html):
        """Clean HTML content by removing unwanted tags and attributes."""
        # Remove script and style elements
        clean = re.compile(r'<(script|style|span|pre|code|/pre|/code|/span).*?>', re.IGNORECASE)
        html = re.sub(clean, '', html)
        
        # Remove all attributes from remaining tags
        html = re.sub(r'<([a-z][a-z0-9]*)[^>]*>', r'<\1>', html, flags=re.IGNORECASE)
        
        # Replace multiple newlines with a single one
        html = re.sub(r'\n+', '\n', html)
        return html.strip()
    
    try:
        # Get the root directory of the application
        app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        readme_path = os.path.join(app_root, 'HELP.md')
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert markdown to HTML with minimal extras
        html = markdown2.markdown(
            markdown_content,
            extras=[
                'fenced-code-blocks',
                'break-on-newline',
                'code-friendly'
            ]
        )
        
        # Clean the HTML before processing
        html = clean_html(html)
        
        # Insert HTML content into the text widget
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        
        # Split into lines and process each one
        lines = html.split('\n')
        in_code_block = False
        code_block_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                text_widget.insert(tk.END, '\n')
                continue
                
            # Handle code blocks
            if line == '<pre>':
                in_code_block = True
                code_block_lines = []
                continue
                
            if line == '</pre>':
                in_code_block = False
                if code_block_lines:
                    # Join code lines and remove the first and last empty lines if they exist
                    code_text = '\n'.join(code_block_lines).strip()
                    text_widget.insert(tk.END, code_text + '\n\n', 'code')
                continue
                
            if in_code_block:
                code_block_lines.append(line)
                continue
                
            # Handle headers
            if line.startswith('<h1>'):
                text = strip_html(line)
                text_widget.insert(tk.END, text + '\n\n', 'h1')
            elif line.startswith('<h2>'):
                text = strip_html(line)
                text_widget.insert(tk.END, text + '\n\n', 'h2')
            elif line.startswith('<h3>'):
                text = strip_html(line)
                text_widget.insert(tk.END, text + '\n\n', 'h3')
                
            # Handle links
            elif line.startswith('<a '):
                url_match = re.search(r'href=[\'"]([^\"]+)[\'"]', line)
                link_text = strip_html(line.replace('<a>', '').replace('</a>', ''))
                if url_match:
                    url = url_match.group(1)
                    tag_name = f'link-{url}'
                    text_widget.tag_config(tag_name, foreground='blue', underline=1)
                    text_widget.insert(tk.END, link_text, ('link', tag_name))
                    text_widget.insert(tk.END, ' ')
                    
            # Handle lists
            elif line.startswith('<li>'):
                text = '• ' + strip_html(line)
                text_widget.insert(tk.END, text + '\n', 'list')
                
            # Handle inline code
            elif '<code>' in line:
                parts = re.split(r'(<code>.*?</code>)', line)
                for part in parts:
                    if part.startswith('<code>') and part.endswith('</code>'):
                        code = part[6:-7]  # Remove <code> and </code>
                        text_widget.insert(tk.END, code, 'code')
                    else:
                        text_widget.insert(tk.END, strip_html(part))
                text_widget.insert(tk.END, '\n')
                
            # Handle other text
            else:
                text = strip_html(line)
                if text.strip():
                    text_widget.insert(tk.END, text + '\n')
        
        text_widget.config(state=tk.DISABLED)
        text_widget.see('1.0')
        
    except Exception as e:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"Error loading help content: {str(e)}\n\n")
        text_widget.insert(tk.END, f"File path: {readme_path}")
        text_widget.config(state=tk.DISABLED)
    
    # Add some padding and focus the window
    help_window.update()
    help_window.focus_set()
