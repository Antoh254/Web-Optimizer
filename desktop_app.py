import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import utils
import threading

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Web Optimizr Desktop")
        self.geometry("600x500")

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="⚡ Web Optimizr", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Tabs
        self.tabview = ctk.CTkTabview(self, width=500)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Image Optimizer")
        self.tabview.add("Code Minifier")

        self.setup_image_tab()
        self.setup_code_tab()

    def setup_image_tab(self):
        tab = self.tabview.tab("Image Optimizer")
        tab.grid_columnconfigure(0, weight=1)

        # Instructions
        ctk.CTkLabel(tab, text="Select JPG/PNG images to convert to WebP", text_color="gray").grid(row=0, column=0, pady=10)

        # File Selection
        self.img_files = []
        self.btn_select_img = ctk.CTkButton(tab, text="Select Images", command=self.select_images)
        self.btn_select_img.grid(row=1, column=0, pady=10)
        
        self.lbl_img_count = ctk.CTkLabel(tab, text="0 files selected")
        self.lbl_img_count.grid(row=2, column=0, pady=5)

        # Options
        self.width_var = ctk.StringVar(value="1200")
        ctk.CTkLabel(tab, text="Max Width (px):").grid(row=3, column=0, pady=(10,0))
        ctk.CTkEntry(tab, textvariable=self.width_var).grid(row=4, column=0, pady=5)

        self.quality_var = ctk.DoubleVar(value=85)
        ctk.CTkLabel(tab, text="Quality (1-100):").grid(row=5, column=0, pady=(10,0))
        self.slider_quality = ctk.CTkSlider(tab, from_=10, to=100, variable=self.quality_var)
        self.slider_quality.grid(row=6, column=0, pady=5)
        
        # Process Button
        self.btn_process_img = ctk.CTkButton(tab, text="Optimize & Save", command=self.process_images, fg_color="green")
        self.btn_process_img.grid(row=7, column=0, pady=20)

    def setup_code_tab(self):
        tab = self.tabview.tab("Code Minifier")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Select CSS/JS files to minify", text_color="gray").grid(row=0, column=0, pady=10)

        self.code_files = []
        self.btn_select_code = ctk.CTkButton(tab, text="Select Code Files", command=self.select_code)
        self.btn_select_code.grid(row=1, column=0, pady=10)

        self.lbl_code_count = ctk.CTkLabel(tab, text="0 files selected")
        self.lbl_code_count.grid(row=2, column=0, pady=5)

        self.btn_process_code = ctk.CTkButton(tab, text="Minify & Save", command=self.process_code, fg_color="green")
        self.btn_process_code.grid(row=3, column=0, pady=20)

    def select_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if files:
            self.img_files = files
            self.lbl_img_count.configure(text=f"{len(files)} files selected")

    def select_code(self):
        files = filedialog.askopenfilenames(filetypes=[("Code", "*.css *.js")])
        if files:
            self.code_files = files
            self.lbl_code_count.configure(text=f"{len(files)} files selected")

    def process_images(self):
        if not self.img_files:
            messagebox.showwarning("Warning", "No images selected!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
        if not save_path:
            return

        try:
            width = int(self.width_var.get())
            quality = int(self.quality_var.get())
            
            # Using utils logic
            zip_buffer = utils.process_images(self.img_files, width, quality)
            
            with open(save_path, "wb") as f:
                f.write(zip_buffer.getvalue())
            
            messagebox.showinfo("Success", "Images optimized successfully!")
            self.img_files = []
            self.lbl_img_count.configure(text="0 files selected")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def process_code(self):
        if not self.code_files:
            messagebox.showwarning("Warning", "No code files selected!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
        if not save_path:
            return

        try:
            # Using utils logic
            zip_buffer = utils.process_code(self.code_files)
            
            with open(save_path, "wb") as f:
                f.write(zip_buffer.getvalue())
            
            messagebox.showinfo("Success", "Code minified successfully!")
            self.code_files = []
            self.lbl_code_count.configure(text="0 files selected")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()
