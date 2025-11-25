import tkinter as tk
from tkinter import scrolledtext, messagebox, font
from openai import OpenAI
import ctypes
from ctypes import windll
import json
import os

# --- DPI AWARE ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# --- Modern Color Palette ---
COLORS = {
    'bg_dark': '#0F0F1E',
    'bg_medium': '#1A1A2E',
    'bg_card': '#16213E',
    'accent_primary': '#7C3AED',
    'accent_secondary': '#6366F1',
    'accent_success': '#10B981',
    'accent_hover': '#8B5CF6',
    'text_primary': '#FFFFFF',
    'text_secondary': '#A0AEC0',
    'border': '#2D3748',
    'input_bg': '#1F2937',
    'input_focus': '#374151',
}

# --- Fonts ---
try:
    title_font = font.Font(family="Poppins", size=20, weight="bold")
    header_font = font.Font(family="Poppins", size=12, weight="bold")
    body_font = font.Font(family="Poppins", size=10)
    button_font = font.Font(family="Poppins", size=11, weight="bold")
except:
    title_font = ("Segoe UI", 20, "bold")
    header_font = ("Segoe UI", 12, "bold")
    body_font = ("Segoe UI", 10)
    button_font = ("Segoe UI", 11, "bold")

# --- Config Management ---
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "api_key": "",
    "base_url": "https://openrouter.ai/api/v1",
    "model": "google/gemini-2.0-flash-exp:free",
    "system_prompt": """You are a release note generator for the Fling application.
Your task is to take raw developer notes and version numbers and convert them into professional, engaging release notes.
Keep the tone exciting but professional. Use emojis where appropriate.
Categorize changes into: New Features, Improvements, and Bug Fixes."""
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except:
            pass
    return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

current_config = load_config()

# --- API Client ---
# --- API Client ---
def get_client():
    api_key = current_config.get("api_key")
    base_url = current_config.get("base_url")
    
    if not api_key:
        return None
        
    return OpenAI(base_url=base_url, api_key=api_key)


def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("500x400")
    settings_window.configure(bg=COLORS['bg_dark'])
    settings_window.overrideredirect(True) # Custom window for settings too? Maybe keep it simple for now or match style.
    # Let's match style but keep it simple
    
    # Center window
    x = root.winfo_x() + (root.winfo_width() // 2) - 250
    y = root.winfo_y() + (root.winfo_height() // 2) - 200
    settings_window.geometry(f"+{x}+{y}")

    # Custom Title Bar for Settings
    s_title_bar = tk.Frame(settings_window, bg=COLORS['bg_medium'], height=30)
    s_title_bar.pack(fill='x')
    
    def s_start_move(event):
        settings_window._offsetx = event.x
        settings_window._offsety = event.y

    def s_on_move(event):
        x = settings_window.winfo_pointerx() - settings_window._offsetx
        y = settings_window.winfo_pointery() - settings_window._offsety
        settings_window.geometry(f'+{x}+{y}')
        
    s_title_bar.bind('<Button-1>', s_start_move)
    s_title_bar.bind('<B1-Motion>', s_on_move)
    
    tk.Label(s_title_bar, text="⚙️ Settings", font=header_font, bg=COLORS['bg_medium'], fg=COLORS['text_primary']).pack(side='left', padx=10)
    
    tk.Button(s_title_bar, text="✕", command=settings_window.destroy, bg=COLORS['bg_medium'], fg=COLORS['text_primary'], bd=0, font=("Segoe UI", 10)).pack(side='right', padx=5)

    # Content
    content = tk.Frame(settings_window, bg=COLORS['bg_dark'], padx=20, pady=20)
    content.pack(fill='both', expand=True)

    # API Key
    tk.Label(content, text="API Key", font=header_font, bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(anchor='w')
    api_key_entry = tk.Entry(content, font=body_font, bg=COLORS['input_bg'], fg=COLORS['text_primary'], insertbackground='white', relief='flat', bd=1)
    api_key_entry.pack(fill='x', pady=(5, 15), ipady=5)
    api_key_entry.insert(0, current_config.get("api_key", ""))

    # Base URL
    tk.Label(content, text="Base URL", font=header_font, bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(anchor='w')
    base_url_entry = tk.Entry(content, font=body_font, bg=COLORS['input_bg'], fg=COLORS['text_primary'], insertbackground='white', relief='flat', bd=1)
    base_url_entry.pack(fill='x', pady=(5, 15), ipady=5)
    base_url_entry.insert(0, current_config.get("base_url", ""))

    # Model
    tk.Label(content, text="Model", font=header_font, bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(anchor='w')
    model_entry = tk.Entry(content, font=body_font, bg=COLORS['input_bg'], fg=COLORS['text_primary'], insertbackground='white', relief='flat', bd=1)
    model_entry.pack(fill='x', pady=(5, 15), ipady=5)
    model_entry.insert(0, current_config.get("model", ""))

    # System Prompt
    tk.Label(content, text="System Prompt", font=header_font, bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(anchor='w')
    prompt_text = scrolledtext.ScrolledText(content, font=body_font, height=8, bg=COLORS['input_bg'], fg=COLORS['text_primary'], insertbackground='white', relief='flat', bd=1)
    prompt_text.pack(fill='both', expand=True, pady=(5, 15))
    prompt_text.insert("1.0", current_config.get("system_prompt", DEFAULT_CONFIG["system_prompt"]))

    def save_and_close():
        current_config["api_key"] = api_key_entry.get().strip()
        current_config["base_url"] = base_url_entry.get().strip()
        current_config["model"] = model_entry.get().strip()
        current_config["system_prompt"] = prompt_text.get("1.0", tk.END).strip()
        save_config(current_config)
        settings_window.destroy()
        messagebox.showinfo("Success", "Settings saved!")

    tk.Button(content, text="Save Settings", command=save_and_close, bg=COLORS['accent_primary'], fg='white', font=button_font, relief='flat', pady=10).pack(fill='x', pady=20)


def on_button_enter(event):
    """Hover effect for buttons"""
    event.widget['bg'] = COLORS['accent_hover']

def on_button_leave(event):
    """Remove hover effect for buttons"""
    event.widget['bg'] = COLORS['accent_primary']

def on_clear_enter(event):
    """Hover effect for clear button"""
    event.widget['bg'] = '#DC2626'

def on_clear_leave(event):
    """Remove hover effect for clear button"""
    event.widget['bg'] = '#EF4444'

def clear_all():
    """Clear all input and output fields"""
    version_entry.delete(0, tk.END)
    notes_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    char_count_label.config(text="0 characters")

def copy_to_clipboard():
    """Copy generated output to clipboard"""
    output = output_text.get("1.0", tk.END).strip()
    if output:
        root.clipboard_clear()
        root.clipboard_append(output)
        root.update()
        # Show success feedback
        copy_btn.config(text="✓ Copied!")
        root.after(2000, lambda: copy_btn.config(text="📋 Copy"))
    else:
        messagebox.showwarning("Warning", "No content to copy!")

def update_char_count(event=None):
    """Update character count label"""
    content = notes_text.get("1.0", tk.END).strip()
    count = len(content)
    char_count_label.config(text=f"{count} characters")


def generate_notes():
    version = version_entry.get().strip()
    dev_notes = notes_text.get("1.0", tk.END).strip()

    if not version or not dev_notes:
        messagebox.showwarning("Missing Info", "Please enter version number and notes.")
        return
        
    client = get_client()
    if not client:
        messagebox.showerror("Configuration Error", "API Key is missing. Please configure it in Settings.")
        open_settings()
        return

    # Show loading state
    generate_btn.config(text="⏳ Generating...", state=tk.DISABLED)
    root.update()

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "Fling Update Notes Generator"
            },
            model=current_config.get("model"),
            messages=[
                {"role": "system", "content": current_config.get("system_prompt", DEFAULT_CONFIG["system_prompt"])},
                {"role": "user", "content": f"Version {version} updates: {dev_notes}"}
            ]
        )
        output = completion.choices[0].message.content
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, output)
        
        # Show success state
        generate_btn.config(text="✓ Success!", bg=COLORS['accent_success'])
        root.after(2000, lambda: generate_btn.config(text="✨ Generate", bg=COLORS['accent_primary']))

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            messagebox.showerror("Rate Limit Reached", "The free API quota has been exceeded.\nPlease add your own API Key in Settings to continue.")
            open_settings()
        elif "401" in error_msg:
            messagebox.showerror("Authentication Error", "Invalid API Key.\nPlease check your API Key in Settings.")
            open_settings()
        else:
            messagebox.showerror("Error", f"An error occurred:\n{error_msg}")
            
        generate_btn.config(text="✨ Generate", bg=COLORS['accent_primary'])
    finally:
        generate_btn.config(state=tk.NORMAL)

# ... (GUI setup)

# Store window position for dragging
# Not needed for native drag

def start_move(event):
    """
    Use Windows native dragging to avoid visual glitches.
    """
    try:
        hwnd = windll.user32.GetParent(root.winfo_id())
        windll.user32.ReleaseCapture()
        windll.user32.SendMessageW(hwnd, 0xA1, 2, 0)
    except Exception as e:
        pass

def minimize_window():
    root.iconify()

def close_window():
    root.destroy()

def hide_title_bar(window):
    """
    Removes the Windows title bar but keeps the window manageable (taskbar, minimize).
    """
    window.update_idletasks()
    try:
        hwnd = windll.user32.GetParent(window.winfo_id())
        # GWL_STYLE = -16
        style = windll.user32.GetWindowLongW(hwnd, -16)
        # WS_CAPTION = 0x00C00000
        # WS_THICKFRAME = 0x00040000 (resize border)
        style = style & ~0x00C00000
        windll.user32.SetWindowLongW(hwnd, -16, style)
        # Force refresh
        windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x27)
    except Exception as e:
        print(f"Error hiding title bar: {e}")

# --- GUI ---
root = tk.Tk()
root.geometry("600x900")
root.configure(bg=COLORS['bg_dark'])

# Apply custom title bar style after window creation
root.after(10, lambda: hide_title_bar(root))

# Custom Title Bar
title_bar = tk.Frame(root, bg=COLORS['bg_medium'], height=40, relief='flat')
title_bar.pack(fill='x')

# Title bar content
title_bar_content = tk.Frame(title_bar, bg=COLORS['bg_medium'])
title_bar_content.pack(fill='both', expand=True, padx=10, pady=5)

# Bind dragging to title bar content
title_bar_content.bind('<Button-1>', start_move)

# App icon and title
title_label = tk.Label(
    title_bar_content,
    text="🚀 Fling Update Generator",
    font=body_font,
    bg=COLORS['bg_medium'],
    fg=COLORS['text_primary']
)
title_label.pack(side='left')
title_label.bind('<Button-1>', start_move)

# Window control buttons
controls_frame = tk.Frame(title_bar_content, bg=COLORS['bg_medium'])
controls_frame.pack(side='right')

minimize_btn = tk.Button(
    controls_frame,
    text="─",
    command=minimize_window,
    bg=COLORS['bg_medium'],
    fg=COLORS['text_primary'],
    font=("Segoe UI", 10),
    relief='flat',
    bd=0,
    padx=12,
    pady=0,
    cursor='hand2',
    activebackground='#374151',
    activeforeground=COLORS['text_primary']
)

close_btn = tk.Button(
    controls_frame,
    text="✕",
    command=close_window,
    bg=COLORS['bg_medium'],
    fg=COLORS['text_primary'],
    font=("Segoe UI", 10),
    relief='flat',
    bd=0,
    padx=12,
    pady=0,
    cursor='hand2',
    activebackground='#DC2626',
    activeforeground=COLORS['text_primary']
)

# Add Settings Button to Title Bar
settings_btn = tk.Button(
    controls_frame,
    text="⚙️",
    command=open_settings,
    bg=COLORS['bg_medium'],
    fg=COLORS['text_primary'],
    font=("Segoe UI", 10),
    relief='flat',
    bd=0,
    padx=12,
    pady=0,
    cursor='hand2',
    activebackground='#374151',
    activeforeground=COLORS['text_primary']
)
settings_btn.pack(side='left')

# Minimize button (re-pack to keep order if needed, or just pack settings first)
# Actually, let's repack controls to be: Settings - Minimize - Close
for widget in controls_frame.winfo_children():
    widget.pack_forget()

settings_btn.pack(side='left')
minimize_btn.pack(side='left')
close_btn.pack(side='left')

# ... (rest of GUI)

# Main container with padding
main_container = tk.Frame(root, bg=COLORS['bg_dark'])
main_container.pack(fill="both", expand=True, padx=25, pady=20)

# Header with icon
header_frame = tk.Frame(main_container, bg=COLORS['bg_dark'])
header_frame.pack(pady=(0, 20))

header = tk.Label(
    header_frame, 
    text="✨ Update Notes", 
    font=title_font,
    bg=COLORS['bg_dark'], 
    fg=COLORS['text_primary']
)
header.pack()

subtitle = tk.Label(
    header_frame,
    text="Create professional update notes",
    font=body_font,
    bg=COLORS['bg_dark'],
    fg=COLORS['text_secondary']
)
subtitle.pack(pady=(5, 0))

# Version Card
version_card = tk.Frame(main_container, bg=COLORS['bg_card'], padx=20, pady=15, relief="flat", bd=1)
version_card.pack(fill="x", pady=(0, 15))

version_label = tk.Label(
    version_card, 
    text="📌 Version Number", 
    font=header_font, 
    bg=COLORS['bg_card'], 
    fg=COLORS['text_primary']
)
version_label.pack(anchor="w", pady=(0, 8))

version_entry = tk.Entry(
    version_card, 
    font=body_font, 
    bg=COLORS['input_bg'], 
    fg=COLORS['text_primary'], 
    insertbackground=COLORS['text_primary'], 
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=COLORS['border'],
    highlightcolor=COLORS['accent_primary']
)
version_entry.pack(fill="x", ipady=8, ipadx=10)

# Developer Notes Card
notes_card = tk.Frame(main_container, bg=COLORS['bg_card'], padx=20, pady=15, relief="flat", bd=1)
notes_card.pack(fill="x", pady=(0, 15))

notes_header = tk.Frame(notes_card, bg=COLORS['bg_card'])
notes_header.pack(fill="x", pady=(0, 8))

notes_label = tk.Label(
    notes_header, 
    text="📝 Developer Notes", 
    font=header_font, 
    bg=COLORS['bg_card'], 
    fg=COLORS['text_primary']
)
notes_label.pack(side="left")

char_count_label = tk.Label(
    notes_header,
    text="0 characters",
    font=body_font,
    bg=COLORS['bg_card'],
    fg=COLORS['text_secondary']
)
char_count_label.pack(side="right")

notes_text = scrolledtext.ScrolledText(
    notes_card, 
    font=body_font, 
    height=6, 
    bg=COLORS['input_bg'], 
    fg=COLORS['text_primary'], 
    insertbackground=COLORS['text_primary'],
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=COLORS['border'],
    highlightcolor=COLORS['accent_primary'],
    padx=10,
    pady=10
)
notes_text.pack(fill="x")
notes_text.bind("<KeyRelease>", update_char_count)

# Action Buttons Frame
buttons_frame = tk.Frame(main_container, bg=COLORS['bg_dark'])
buttons_frame.pack(pady=15)

generate_btn = tk.Button(
    buttons_frame, 
    text="✨ Generate", 
    command=generate_notes,
    bg=COLORS['accent_primary'], 
    fg=COLORS['text_primary'], 
    font=button_font,
    activebackground=COLORS['accent_hover'], 
    activeforeground=COLORS['text_primary'], 
    relief="flat", 
    bd=0,
    padx=25,
    pady=10,
    cursor="hand2"
)
generate_btn.pack(side="left", padx=5)
generate_btn.bind("<Enter>", on_button_enter)
generate_btn.bind("<Leave>", on_button_leave)

clear_btn = tk.Button(
    buttons_frame,
    text="🗑️ Clear",
    command=clear_all,
    bg="#EF4444",
    fg=COLORS['text_primary'],
    font=button_font,
    activebackground="#DC2626",
    activeforeground=COLORS['text_primary'],
    relief="flat",
    bd=0,
    padx=20,
    pady=10,
    cursor="hand2"
)
clear_btn.pack(side="left", padx=5)
clear_btn.bind("<Enter>", on_clear_enter)
clear_btn.bind("<Leave>", on_clear_leave)

# Output Card
output_card = tk.Frame(main_container, bg=COLORS['bg_card'], padx=20, pady=15, relief="flat", bd=1)
output_card.pack(fill="both", expand=True)

output_header = tk.Frame(output_card, bg=COLORS['bg_card'])
output_header.pack(fill="x", pady=(0, 8))

output_label = tk.Label(
    output_header, 
    text="✅ Generated Notes", 
    font=header_font, 
    bg=COLORS['bg_card'], 
    fg=COLORS['text_primary']
)
output_label.pack(side="left")

copy_btn = tk.Button(
    output_header,
    text="📋 Copy",
    command=copy_to_clipboard,
    bg=COLORS['accent_secondary'],
    fg=COLORS['text_primary'],
    font=body_font,
    relief="flat",
    bd=0,
    padx=15,
    pady=5,
    cursor="hand2"
)
copy_btn.pack(side="right")

output_text = scrolledtext.ScrolledText(
    output_card, 
    font=body_font, 
    bg=COLORS['input_bg'], 
    fg=COLORS['text_primary'], 
    insertbackground=COLORS['text_primary'],
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=COLORS['border'],
    highlightcolor=COLORS['accent_primary'],
    padx=10,
    pady=10
)
output_text.pack(fill="both", expand=True)

# Footer
footer = tk.Label(
    main_container,
    text="Made with 💜 for Fling",
    font=("Poppins", 9),
    bg=COLORS['bg_dark'],
    fg=COLORS['text_secondary']
)
footer.pack(pady=(10, 0))

root.mainloop()
