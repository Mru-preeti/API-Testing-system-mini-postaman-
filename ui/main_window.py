import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
import json
import time
from datetime import datetime
from pathlib import Path
import threading


class APITesterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("API Tester - Postman Style")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Configure style
        self.setup_styles()

        # Data storage
        self.history_file = Path(__file__).parent.parent / "data" / "history.json"
        self.request_history = self.load_history()

        # Create UI
        self.create_menu()
        self.create_main_layout()

    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')

        # Button style
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'))

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Response", command=self.export_response)
        file_menu.add_command(label="View History", command=self.view_history_window)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_main_layout(self):
        """Create main layout with request and response sections"""
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Request form
        left_panel = ttk.LabelFrame(main_container, text="REQUEST", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Right panel - Response
        right_panel = ttk.LabelFrame(main_container, text="RESPONSE", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.create_request_form(left_panel)
        self.create_response_display(right_panel)

    def create_request_form(self, parent):
        """Create request form UI"""
        # URL section
        url_frame = ttk.Frame(parent)
        url_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(url_frame, text="URL:").pack(side=tk.LEFT, padx=(0, 5))
        self.url_entry = ttk.Entry(url_frame, width=40)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.url_entry.insert(0, "https://httpbin.org/get")

        # HTTP Method section
        method_frame = ttk.Frame(parent)
        method_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(method_frame, text="Method:").pack(side=tk.LEFT, padx=(0, 5))
        self.method_var = tk.StringVar(value="GET")
        method_combo = ttk.Combobox(
            method_frame,
            textvariable=self.method_var,
            values=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
            state="readonly",
            width=10
        )
        method_combo.pack(side=tk.LEFT)

        # Headers section
        ttk.Label(parent, text="Headers (JSON format):", font=('Segoe UI', 9, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        self.headers_text = scrolledtext.ScrolledText(parent, height=4, width=40, wrap=tk.WORD)
        self.headers_text.pack(fill=tk.X, pady=(0, 10))
        self.headers_text.insert("1.0", '{\n    "Content-Type": "application/json"\n}')

        # Body section
        ttk.Label(parent, text="Request Body:", font=('Segoe UI', 9, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        self.body_text = scrolledtext.ScrolledText(parent, height=6, width=40, wrap=tk.WORD)
        self.body_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Buttons section
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        send_btn = ttk.Button(button_frame, text="🚀 Send Request", command=self.send_request)
        send_btn.pack(side=tk.LEFT, padx=(0, 5))

        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_request)
        clear_btn.pack(side=tk.LEFT)

    def create_response_display(self, parent):
        """Create response display area"""
        # Status frame
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(status_frame, text="Status:", font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        self.status_label = ttk.Label(status_frame, text="Ready", foreground="blue")
        self.status_label.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(status_frame, text="Time:", font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        self.time_label = ttk.Label(status_frame, text="0ms")
        self.time_label.pack(side=tk.LEFT)

        # Tabs for response sections
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Body tab
        body_frame = ttk.Frame(self.notebook)
        self.notebook.add(body_frame, text="Body")
        self.response_text = scrolledtext.ScrolledText(body_frame, wrap=tk.WORD)
        self.response_text.pack(fill=tk.BOTH, expand=True)

        # Headers tab
        headers_frame = ttk.Frame(self.notebook)
        self.notebook.add(headers_frame, text="Headers")
        self.response_headers_text = scrolledtext.ScrolledText(headers_frame, wrap=tk.WORD)
        self.response_headers_text.pack(fill=tk.BOTH, expand=True)

        # Pretty JSON tab
        pretty_frame = ttk.Frame(self.notebook)
        self.notebook.add(pretty_frame, text="Pretty")
        self.response_pretty_text = scrolledtext.ScrolledText(pretty_frame, wrap=tk.WORD)
        self.response_pretty_text.pack(fill=tk.BOTH, expand=True)

        # Copy button
        copy_btn = ttk.Button(parent, text="📋 Copy Response", command=self.copy_response)
        copy_btn.pack(fill=tk.X, pady=(10, 0))

    def send_request(self):
        """Send API request (runs in separate thread)"""
        thread = threading.Thread(target=self._do_request)
        thread.daemon = True
        thread.start()

    def _do_request(self):
        """Perform the actual request"""
        try:
            url = self.url_entry.get().strip()
            if not url:
                self.update_status("Error: URL is empty", "red")
                return

            method = self.method_var.get()

            # Parse headers
            try:
                headers_text = self.headers_text.get("1.0", tk.END).strip()
                headers = json.loads(headers_text) if headers_text else {}
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON in headers")
                return

            # Parse body
            body = self.body_text.get("1.0", tk.END).strip()

            # Prepare request kwargs
            kwargs = {
                'headers': headers,
                'timeout': 10
            }

            if body and method != "GET":
                kwargs['data'] = body

            # Send request
            self.update_status("Sending...", "blue")
            start_time = time.time()

            response = requests.request(method, url, **kwargs)

            elapsed_time = (time.time() - start_time) * 1000  # Convert to ms

            # Store in history
            self.save_to_history(url, method, headers, body, response)

            # Display response
            self.display_response(response, elapsed_time)

        except requests.exceptions.MissingSchema:
            self.update_status("Error: Invalid URL format", "red")
        except requests.exceptions.ConnectionError:
            self.update_status("Error: Connection failed", "red")
        except requests.exceptions.Timeout:
            self.update_status("Error: Request timeout", "red")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")

    def display_response(self, response, elapsed_time):
        """Display response in UI"""
        # Update status
        status_code = response.status_code
        color = "green" if 200 <= status_code < 300 else "orange" if 400 <= status_code < 500 else "red"
        self.update_status(f"Status: {status_code}", color)
        self.update_time(f"{elapsed_time:.2f}ms")

        # Body
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert("1.0", response.text)
        self.response_text.config(state=tk.DISABLED)

        # Headers
        headers_str = "\n".join([f"{k}: {v}" for k, v in response.headers.items()])
        self.response_headers_text.config(state=tk.NORMAL)
        self.response_headers_text.delete("1.0", tk.END)
        self.response_headers_text.insert("1.0", headers_str)
        self.response_headers_text.config(state=tk.DISABLED)

        # Pretty JSON
        try:
            json_obj = response.json()
            pretty_json = json.dumps(json_obj, indent=2)
        except:
            pretty_json = "Response is not valid JSON"

        self.response_pretty_text.config(state=tk.NORMAL)
        self.response_pretty_text.delete("1.0", tk.END)
        self.response_pretty_text.insert("1.0", pretty_json)
        self.response_pretty_text.config(state=tk.DISABLED)

        self.notebook.select(0)  # Show body tab

    def update_status(self, status, color="black"):
        """Update status label"""
        self.status_label.config(text=status, foreground=color)

    def update_time(self, time_str):
        """Update time label"""
        self.time_label.config(text=time_str)

    def clear_request(self):
        """Clear all request fields"""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, "https://httpbin.org/get")
        self.method_var.set("GET")
        self.headers_text.delete("1.0", tk.END)
        self.headers_text.insert("1.0", '{\n    "Content-Type": "application/json"\n}')
        self.body_text.delete("1.0", tk.END)
        self.update_status("Ready")
        self.update_time("0ms")

    def load_history(self):
        """Load request history from JSON"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_to_history(self, url, method, headers, body, response):
        """Save request to history"""
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)

            entry = {
                "timestamp": datetime.now().isoformat(),
                "url": url,
                "method": method,
                "headers": headers,
                "body": body,
                "status_code": response.status_code,
                "response": response.text[:500]  # Store first 500 chars
            }

            self.request_history.append(entry)

            # Keep only last 50 requests
            if len(self.request_history) > 50:
                self.request_history = self.request_history[-50:]

            with open(self.history_file, 'w') as f:
                json.dump(self.request_history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def export_response(self):
        """Export current response"""
        if not self.response_text.get("1.0", tk.END).strip():
            messagebox.showwarning("Warning", "No response to export")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                content = self.response_text.get("1.0", tk.END)
                with open(file_path, 'w') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Response exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")

    def copy_response(self):
        """Copy response to clipboard"""
        content = self.response_text.get("1.0", tk.END)
        if content.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Success", "Response copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No response to copy")

    def view_history_window(self):
        """Show history in new window"""
        if not self.request_history:
            messagebox.showinfo("History", "No requests in history")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("Request History")
        history_window.geometry("700x400")

        tree = ttk.Treeview(history_window, columns=("Time", "Method", "URL", "Status"), height=15)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree.heading("#0", text="")
        tree.heading("Time", text="Time")
        tree.heading("Method", text="Method")
        tree.heading("URL", text="URL")
        tree.heading("Status", text="Status")

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Time", width=150)
        tree.column("Method", width=60)
        tree.column("URL", width=300)
        tree.column("Status", width=50)

        for req in reversed(self.request_history[-20:]):
            tree.insert("", 0, values=(
                req["timestamp"],
                req["method"],
                req["url"][:50],
                req["status_code"]
            ))

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About API Tester",
            "API Tester v1.0\n\nA Postman-like desktop application for testing APIs.\n\nBuilt with Python & Tkinter"
        )
