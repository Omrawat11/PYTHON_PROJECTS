"""
=============================================================================
                  🛡️  ADVANCED CAPTCHA GENERATOR & VERIFIER  🛡️
=============================================================================
A modern, feature-rich, standalone CAPTCHA security tool and verification suite
built with Python, Tkinter, and PIL (Pillow).

Features:
- Dual Rendering Engine: Advanced PIL Engine (Warp, Noise, Curves) & ImageCaptcha
- Multi-Challenge Modes: Alphanumeric, Numeric (PIN), Math Challenge, Words
- Audio CAPTCHA (Text-to-Speech for Accessibility via Windows SAPI / pyttsx3)
- Modern Dark Aesthetic UI with real-time feedback, streak counter, and accuracy stats
- Dynamic Difficulty levels (Easy, Medium, Hard)
- Export to PNG, Copy to Clipboard, Full Keyboard Shortcuts
=============================================================================
"""

import os
import sys
import random
import string
import math
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter

# Enable High DPI on Windows for crisp rendering
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Check third-party captcha package availability safely without self-import collision
HAS_IMAGE_CAPTCHA = False
try:
    _cur_dir = sys.path[0] if sys.path else ""
    if _cur_dir in sys.path:
        sys.path.remove(_cur_dir)
    try:
        from captcha.image import ImageCaptcha as ExternalImageCaptcha
        HAS_IMAGE_CAPTCHA = True
    except Exception:
        HAS_IMAGE_CAPTCHA = False
    finally:
        if _cur_dir and _cur_dir not in sys.path:
            sys.path.insert(0, _cur_dir)
except Exception:
    HAS_IMAGE_CAPTCHA = False


# =============================================================================
#                              CAPTCHA ENGINE
# =============================================================================
class CaptchaEngine:
    """High-fidelity CAPTCHA rendering engine with wave distortions, Bezier curves, and noise."""
    
    def __init__(self, width=320, height=110):
        self.width = width
        self.height = height
        self.fonts = self._load_system_fonts()

    def _load_system_fonts(self):
        font_candidates = [
            "arial.ttf", "arialbd.ttf", "calibri.ttf", "calibrib.ttf",
            "comic.ttf", "comicbd.ttf", "consola.ttf", "consolab.ttf",
            "georgia.ttf", "georgiab.ttf", "impact.ttf", "segoeui.ttf",
            "segoeuib.ttf", "times.ttf", "timesbd.ttf", "trebuc.ttf",
            "trebucbd.ttf", "verdana.ttf", "verdanab.ttf"
        ]
        loaded_fonts = []
        for font_name in font_candidates:
            # Check current working directory or system Fonts folder
            search_paths = [
                font_name,
                os.path.join("C:/Windows/Fonts", font_name),
                os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", font_name)
            ]
            for path in search_paths:
                if os.path.exists(path):
                    try:
                        f = ImageFont.truetype(path, 38)
                        loaded_fonts.append(f)
                        break
                    except Exception:
                        continue
        
        if not loaded_fonts:
            try:
                loaded_fonts.append(ImageFont.load_default())
            except Exception:
                pass
        return loaded_fonts

    def generate_challenge(self, mode="alphanumeric", length=6):
        """Generates challenge text and expected solution."""
        if mode == "numeric":
            text = "".join(random.choices(string.digits, k=length))
            solution = text
            speech_text = " ".join(list(text))
        elif mode == "math":
            op = random.choice(["+", "-", "*"])
            if op == "+":
                a = random.randint(10, 50)
                b = random.randint(5, 40)
                solution = str(a + b)
                speech_text = f"What is {a} plus {b}?"
            elif op == "-":
                a = random.randint(20, 60)
                b = random.randint(5, a)
                solution = str(a - b)
                speech_text = f"What is {a} minus {b}?"
            else:
                a = random.randint(2, 12)
                b = random.randint(2, 9)
                solution = str(a * b)
                speech_text = f"What is {a} times {b}?"
            text = f"{a} {op} {b} = ?"
        elif mode == "words":
            words_pool = [
                "SPRING", "ORANGE", "SHADOW", "BRIDGE", "ROCKET", "PLANET",
                "SILVER", "CASTLE", "FOREST", "GOLDEN", "BREEZE", "FLIGHT",
                "WONDER", "STORM", "VALLEY", "STREAM", "KNIGHT", "BEACON",
                "CRYSTAL", "GALAXY", "HARBOR", "ISLAND", "JUNGLE", "MATRIX"
            ]
            word = random.choice(words_pool)
            text = word
            solution = word
            speech_text = "Word: " + ", ".join(list(word))
        else:
            # Alphanumeric: Exclude ambiguous characters (0, O, o, 1, I, l) for better human readability
            allowed_chars = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz"
            text = "".join(random.choices(allowed_chars, k=length))
            solution = text
            speech_parts = []
            for ch in text:
                if ch.isupper():
                    speech_parts.append(f"Capital {ch}")
                elif ch.islower():
                    speech_parts.append(f"Lower {ch}")
                else:
                    speech_parts.append(ch)
            speech_text = ", ".join(speech_parts)

        return text, solution, speech_text

    def render_pil(self, text, difficulty="medium", has_noise=True, is_dark_captcha=False):
        """Creates a distorted, secure, and visually appealing CAPTCHA image."""
        bg_base = (28, 30, 44) if is_dark_captcha else (246, 248, 252)
        img = Image.new("RGB", (self.width, self.height), color=bg_base)
        draw = ImageDraw.Draw(img)

        # Subtle wave gradient background
        for y in range(self.height):
            wave = int(8 * math.sin(y / 8.0))
            if is_dark_captcha:
                r = max(20, min(50, bg_base[0] + wave))
                g = max(20, min(50, bg_base[1] - wave))
                b = max(30, min(65, bg_base[2] + wave))
            else:
                r = max(230, min(255, bg_base[0] + wave))
                g = max(230, min(255, bg_base[1] - wave))
                b = max(235, min(255, bg_base[2] + wave))
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))

        # Color palettes for characters
        if is_dark_captcha:
            char_colors = [
                (139, 233, 253), (80, 250, 123), (255, 121, 198), (189, 147, 249),
                (241, 250, 140), (255, 184, 108), (100, 210, 255), (255, 140, 140)
            ]
        else:
            char_colors = [
                (24, 43, 73), (179, 48, 30), (37, 85, 153), (108, 43, 156),
                (18, 128, 92), (184, 92, 10), (133, 30, 89), (34, 112, 147)
            ]

        # Draw characters with jitter, rotation, and soft shadow
        num_chars = len(text)
        avail_width = self.width - 40
        step = avail_width / max(num_chars, 1)

        for i, char in enumerate(text):
            color = random.choice(char_colors)
            font = random.choice(self.fonts) if self.fonts else ImageFont.load_default()
            
            char_canvas = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
            c_draw = ImageDraw.Draw(char_canvas)

            # Shadow offset
            shadow_color = (0, 0, 0, 80) if is_dark_captcha else (190, 195, 205, 140)
            c_draw.text((19, 19), char, font=font, fill=shadow_color)
            c_draw.text((16, 16), char, font=font, fill=color)

            # Rotation angle
            if difficulty == "hard":
                angle = random.randint(-30, 30)
            elif difficulty == "medium":
                angle = random.randint(-18, 18)
            else:
                angle = random.randint(-8, 8)

            rotated = char_canvas.rotate(angle, expand=1, resample=Image.BICUBIC)

            x_pos = int(20 + i * step + random.randint(-3, 3))
            y_pos = int((self.height - rotated.height) / 2 + random.randint(-4, 4))
            
            img.paste(rotated, (x_pos, y_pos), rotated)

        # Draw interference bezier curves & noise
        if has_noise:
            num_curves = 4 if difficulty == "hard" else (2 if difficulty == "medium" else 1)
            for _ in range(num_curves):
                curve_color = random.choice(char_colors)
                x1, y1 = random.randint(0, 40), random.randint(15, self.height - 15)
                x2, y2 = random.randint(self.width - 40, self.width), random.randint(15, self.height - 15)
                cx, cy = random.randint(60, self.width - 60), random.randint(5, self.height - 5)
                
                # Quadratic Bezier Curve interpolation
                points = []
                for t in [step_i / 25.0 for step_i in range(26)]:
                    px = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t ** 2 * x2
                    py = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t ** 2 * y2
                    points.append((px, py))
                
                draw.line(points, fill=curve_color, width=2)

            # Draw noise splatter dots
            num_dots = 120 if difficulty == "hard" else (60 if difficulty == "medium" else 20)
            for _ in range(num_dots):
                dx = random.randint(0, self.width)
                dy = random.randint(0, self.height)
                dot_color = random.choice(char_colors)
                draw.point((dx, dy), fill=dot_color)

        # Sine wave horizontal warp for medium/hard
        if difficulty in ["medium", "hard"]:
            amp = 4 if difficulty == "hard" else 2
            img = self._wave_distort(img, amplitude=amp, is_dark=is_dark_captcha)

        return img

    def render_external(self, text):
        """Fallback to third-party ImageCaptcha library if installed."""
        if HAS_IMAGE_CAPTCHA:
            try:
                gen = ExternalImageCaptcha(width=self.width, height=self.height)
                data = gen.generate(text)
                return Image.open(data)
            except Exception:
                pass
        return self.render_pil(text)

    def _wave_distort(self, img, amplitude=3, is_dark=False):
        w, h = img.size
        bg_col = (28, 30, 44) if is_dark else (246, 248, 252)
        distorted = Image.new("RGB", (w, h), bg_col)
        freq = 0.04
        pixels_in = img.load()
        pixels_out = distorted.load()

        for x in range(w):
            for y in range(h):
                offset_y = int(amplitude * math.sin(x * freq + 1.2))
                new_y = y + offset_y
                if 0 <= new_y < h:
                    pixels_out[x, new_y] = pixels_in[x, y]
                else:
                    pixels_out[x, y] = pixels_in[x, y]
        return distorted


# =============================================================================
#                        AUDIO SPEECH SYNTHESIZER
# =============================================================================
class CaptchaVoice:
    """Speaks CAPTCHA characters cleanly in background threads for accessibility."""
    @staticmethod
    def speak(text):
        def _runner():
            # Try Windows SAPI native dispatch
            try:
                import win32com.client
                import pythoncom
                pythoncom.CoInitialize()
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Rate = -1  # Slightly slower for clear dictation
                speaker.Speak(text)
                pythoncom.CoUninitialize()
                return
            except Exception:
                pass
            
            # Fallback to pyttsx3 if installed
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.setProperty("rate", 140)
                engine.say(text)
                engine.runAndWait()
            except Exception:
                pass

        threading.Thread(target=_runner, daemon=True).start()


# =============================================================================
#                          MODERN GUI APPLICATION
# =============================================================================
class CaptchaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Captcha Security Studio & Generator")
        self.root.geometry("640x760")
        self.root.minsize(580, 680)

        # Color Palette - Modern Dark Theme
        self.c_bg = "#13141c"            # Dark charcoal background
        self.c_card = "#1e202e"          # Elevated card surface
        self.c_card_border = "#2d3148"   # Card border stroke
        self.c_primary = "#6366f1"       # Indigo accent
        self.c_primary_hover = "#4f46e5" # Darker indigo
        self.c_success = "#10b981"       # Vibrant emerald
        self.c_error = "#ef4444"         # Crimson red
        self.c_text_bright = "#f8fafc"   # White text
        self.c_text_muted = "#94a3b8"    # Subtle secondary text
        self.c_input_bg = "#161824"      # Input background
        self.c_btn_sec = "#2a2d40"       # Secondary button
        self.c_btn_sec_hover = "#373b54"

        self.root.configure(bg=self.c_bg)

        # Engine & State
        self.engine = CaptchaEngine(width=340, height=115)
        self.current_text = ""
        self.current_solution = ""
        self.current_speech = ""
        self.current_image = None
        self.current_photo = None
        
        # Statistics
        self.stat_verified = 0
        self.stat_attempts = 0
        self.stat_streak = 0
        self.stat_best_streak = 0
        self.start_time = time.time()

        # Options Variables
        self.var_mode = tk.StringVar(value="alphanumeric")
        self.var_diff = tk.StringVar(value="medium")
        self.var_length = tk.IntVar(value=6)
        self.var_case = tk.BooleanVar(value=False)
        self.var_noise = tk.BooleanVar(value=True)
        self.var_dark_captcha = tk.BooleanVar(value=False)
        self.var_engine = tk.StringVar(value="PIL Engine")

        self._init_ui()
        self.refresh_captcha()
        self._bind_shortcuts()

    def _init_ui(self):
        """Constructs the modern Tkinter UI."""
        # Outer scrollable or centered container
        main_frame = tk.Frame(self.root, bg=self.c_bg)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        # Header Title
        header_box = tk.Frame(main_frame, bg=self.c_bg)
        header_box.pack(fill=tk.X, pady=(0, 15))

        title_lbl = tk.Label(
            header_box,
            text="🛡️ CAPTCHA Studio",
            font=("Segoe UI", 20, "bold"),
            fg=self.c_text_bright,
            bg=self.c_bg
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            header_box,
            text="Interactive Security Verification & Multi-Engine Generator",
            font=("Segoe UI", 10),
            fg=self.c_text_muted,
            bg=self.c_bg
        )
        subtitle_lbl.pack(anchor="w")

        # Stats Bar (Streak, Score, Accuracy)
        self.stats_frame = tk.Frame(main_frame, bg=self.c_card, highlightbackground=self.c_card_border, highlightthickness=1)
        self.stats_frame.pack(fill=tk.X, pady=(0, 15), ipady=6)

        self.lbl_streak = tk.Label(
            self.stats_frame,
            text="🔥 Streak: 0",
            font=("Segoe UI", 10, "bold"),
            fg="#f59e0b",
            bg=self.c_card
        )
        self.lbl_streak.pack(side=tk.LEFT, padx=20)

        self.lbl_verified = tk.Label(
            self.stats_frame,
            text="✅ Verified: 0",
            font=("Segoe UI", 10, "bold"),
            fg=self.c_success,
            bg=self.c_card
        )
        self.lbl_verified.pack(side=tk.LEFT, padx=20)

        self.lbl_accuracy = tk.Label(
            self.stats_frame,
            text="🎯 Accuracy: 100%",
            font=("Segoe UI", 10, "bold"),
            fg="#60a5fa",
            bg=self.c_card
        )
        self.lbl_accuracy.pack(side=tk.RIGHT, padx=20)

        # Main Display Card
        card = tk.Frame(main_frame, bg=self.c_card, highlightbackground=self.c_card_border, highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 15), ipady=10, padx=2)

        # Captcha Image Container
        img_container = tk.Frame(card, bg=self.c_card)
        img_container.pack(pady=10)

        # Outer border around captcha image
        img_border = tk.Frame(img_container, bg=self.c_card_border, padx=3, pady=3)
        img_border.pack(side=tk.LEFT)

        self.lbl_captcha = tk.Label(img_border, bg="#f6f8fc", width=340, height=115)
        self.lbl_captcha.pack()

        # Side Action buttons for Captcha (Reload & Audio)
        action_bar = tk.Frame(img_container, bg=self.c_card)
        action_bar.pack(side=tk.LEFT, padx=(10, 0), fill=tk.Y)

        self.btn_refresh = tk.Button(
            action_bar,
            text="🔄",
            font=("Segoe UI Emoji", 14),
            bg=self.c_btn_sec,
            fg=self.c_text_bright,
            activebackground=self.c_btn_sec_hover,
            activeforeground=self.c_text_bright,
            bd=0,
            cursor="hand2",
            width=3,
            height=1,
            command=self.refresh_captcha
        )
        self.btn_refresh.pack(pady=(0, 6))

        self.btn_audio = tk.Button(
            action_bar,
            text="🔊",
            font=("Segoe UI Emoji", 14),
            bg=self.c_btn_sec,
            fg=self.c_text_bright,
            activebackground=self.c_btn_sec_hover,
            activeforeground=self.c_text_bright,
            bd=0,
            cursor="hand2",
            width=3,
            height=1,
            command=self.play_audio
        )
        self.btn_audio.pack()

        # Status Message Banner
        self.lbl_status = tk.Label(
            card,
            text="Type the characters above and press Enter",
            font=("Segoe UI", 10, "italic"),
            fg=self.c_text_muted,
            bg=self.c_card,
            wraplength=450
        )
        self.lbl_status.pack(pady=(4, 8))

        # Input & Submit Box
        input_container = tk.Frame(card, bg=self.c_card)
        input_container.pack(fill=tk.X, padx=30, pady=(0, 10))

        # Stylized Entry Box
        entry_wrap = tk.Frame(input_container, bg=self.c_card_border, padx=2, pady=2)
        entry_wrap.pack(fill=tk.X, pady=(0, 10))

        self.entry_input = tk.Entry(
            entry_wrap,
            font=("Consolas", 16, "bold"),
            bg=self.c_input_bg,
            fg=self.c_text_bright,
            insertbackground=self.c_primary,
            bd=0,
            justify="center"
        )
        self.entry_input.pack(fill=tk.X, ipady=8)
        self.entry_input.focus_set()

        # Buttons Row: Verify & Auxiliary actions
        btn_row = tk.Frame(input_container, bg=self.c_card)
        btn_row.pack(fill=tk.X)

        self.btn_verify = tk.Button(
            btn_row,
            text="Verify Solution  ↵",
            font=("Segoe UI", 11, "bold"),
            bg=self.c_primary,
            fg=self.c_text_bright,
            activebackground=self.c_primary_hover,
            activeforeground=self.c_text_bright,
            bd=0,
            cursor="hand2",
            pady=8,
            command=self.verify_captcha
        )
        self.btn_verify.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        self.btn_save = tk.Button(
            btn_row,
            text="💾 Save PNG",
            font=("Segoe UI", 9),
            bg=self.c_btn_sec,
            fg=self.c_text_bright,
            activebackground=self.c_btn_sec_hover,
            activeforeground=self.c_text_bright,
            bd=0,
            cursor="hand2",
            padx=10,
            pady=8,
            command=self.save_captcha_image
        )
        self.btn_save.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_copy = tk.Button(
            btn_row,
            text="📋 Copy Code",
            font=("Segoe UI", 9),
            bg=self.c_btn_sec,
            fg=self.c_text_bright,
            activebackground=self.c_btn_sec_hover,
            activeforeground=self.c_text_bright,
            bd=0,
            cursor="hand2",
            padx=10,
            pady=8,
            command=self.copy_code_to_clipboard
        )
        self.btn_copy.pack(side=tk.LEFT)

        # Settings & Customization Panel
        settings_card = tk.LabelFrame(
            main_frame,
            text="  ⚙️ Configuration & Challenge Options  ",
            font=("Segoe UI", 10, "bold"),
            fg=self.c_text_bright,
            bg=self.c_bg,
            bd=1,
            relief=tk.GROOVE
        )
        settings_card.pack(fill=tk.BOTH, expand=True, padx=2, pady=5)

        # Options Grid
        opt_grid = tk.Frame(settings_card, bg=self.c_bg)
        opt_grid.pack(fill=tk.X, padx=15, pady=10)

        # Mode Selection
        tk.Label(opt_grid, text="Type:", font=("Segoe UI", 9, "bold"), fg=self.c_text_muted, bg=self.c_bg).grid(row=0, column=0, sticky="w", pady=4)
        mode_menu = ttk.Combobox(
            opt_grid,
            textvariable=self.var_mode,
            values=["alphanumeric", "numeric", "math", "words"],
            state="readonly",
            width=14
        )
        mode_menu.grid(row=0, column=1, sticky="w", padx=(6, 20), pady=4)
        mode_menu.bind("<<ComboboxSelected>>", lambda e: self.refresh_captcha())

        # Difficulty Selection
        tk.Label(opt_grid, text="Difficulty:", font=("Segoe UI", 9, "bold"), fg=self.c_text_muted, bg=self.c_bg).grid(row=0, column=2, sticky="w", pady=4)
        diff_menu = ttk.Combobox(
            opt_grid,
            textvariable=self.var_diff,
            values=["easy", "medium", "hard"],
            state="readonly",
            width=10
        )
        diff_menu.grid(row=0, column=3, sticky="w", padx=(6, 0), pady=4)
        diff_menu.bind("<<ComboboxSelected>>", lambda e: self.refresh_captcha())

        # Length Selection
        tk.Label(opt_grid, text="Length:", font=("Segoe UI", 9, "bold"), fg=self.c_text_muted, bg=self.c_bg).grid(row=1, column=0, sticky="w", pady=4)
        len_menu = ttk.Combobox(
            opt_grid,
            textvariable=self.var_length,
            values=[4, 5, 6, 7, 8],
            state="readonly",
            width=14
        )
        len_menu.grid(row=1, column=1, sticky="w", padx=(6, 20), pady=4)
        len_menu.bind("<<ComboboxSelected>>", lambda e: self.refresh_captcha())

        # Engine Selection
        tk.Label(opt_grid, text="Engine:", font=("Segoe UI", 9, "bold"), fg=self.c_text_muted, bg=self.c_bg).grid(row=1, column=2, sticky="w", pady=4)
        engine_options = ["PIL Engine"]
        if HAS_IMAGE_CAPTCHA:
            engine_options.append("ImageCaptcha Lib")
        engine_menu = ttk.Combobox(
            opt_grid,
            textvariable=self.var_engine,
            values=engine_options,
            state="readonly",
            width=10
        )
        engine_menu.grid(row=1, column=3, sticky="w", padx=(6, 0), pady=4)
        engine_menu.bind("<<ComboboxSelected>>", lambda e: self.refresh_captcha())

        # Checkbox Toggles
        chk_row = tk.Frame(settings_card, bg=self.c_bg)
        chk_row.pack(fill=tk.X, padx=15, pady=(0, 8))

        c1 = tk.Checkbutton(
            chk_row,
            text="Case-Sensitive Verification",
            variable=self.var_case,
            font=("Segoe UI", 9),
            fg=self.c_text_bright,
            bg=self.c_bg,
            selectcolor=self.c_card,
            activebackground=self.c_bg,
            activeforeground=self.c_text_bright
        )
        c1.pack(side=tk.LEFT, padx=(0, 15))

        c2 = tk.Checkbutton(
            chk_row,
            text="Security Noise & Waves",
            variable=self.var_noise,
            font=("Segoe UI", 9),
            fg=self.c_text_bright,
            bg=self.c_bg,
            selectcolor=self.c_card,
            activebackground=self.c_bg,
            activeforeground=self.c_text_bright,
            command=self.refresh_captcha
        )
        c2.pack(side=tk.LEFT, padx=(0, 15))

        c3 = tk.Checkbutton(
            chk_row,
            text="Dark CAPTCHA Theme",
            variable=self.var_dark_captcha,
            font=("Segoe UI", 9),
            fg=self.c_text_bright,
            bg=self.c_bg,
            selectcolor=self.c_card,
            activebackground=self.c_bg,
            activeforeground=self.c_text_bright,
            command=self.refresh_captcha
        )
        c3.pack(side=tk.LEFT)

        # Footer Shortcuts Info
        footer_lbl = tk.Label(
            main_frame,
            text="Shortcuts: [Enter] Verify  |  [Ctrl+R / F5] Refresh  |  [Ctrl+L] Audio  |  [Esc] Clear",
            font=("Segoe UI", 8),
            fg=self.c_text_muted,
            bg=self.c_bg
        )
        footer_lbl.pack(side=tk.BOTTOM, pady=(4, 0))

    def _bind_shortcuts(self):
        """Binds useful keyboard shortcuts."""
        self.root.bind("<Return>", lambda e: self.verify_captcha())
        self.root.bind("<Control-r>", lambda e: self.refresh_captcha())
        self.root.bind("<F5>", lambda e: self.refresh_captcha())
        self.root.bind("<Escape>", lambda e: self._clear_input())
        self.root.bind("<Control-l>", lambda e: self.play_audio())
        self.root.bind("<Control-s>", lambda e: self.save_captcha_image())

    def _clear_input(self):
        self.entry_input.delete(0, tk.END)

    def refresh_captcha(self):
        """Generates a new CAPTCHA and renders it."""
        mode = self.var_mode.get()
        length = self.var_length.get()
        difficulty = self.var_diff.get()
        has_noise = self.var_noise.get()
        is_dark = self.var_dark_captcha.get()
        engine_choice = self.var_engine.get()

        # Generate text & solution
        self.current_text, self.current_solution, self.current_speech = self.engine.generate_challenge(
            mode=mode,
            length=length
        )

        # Render Image
        if engine_choice == "ImageCaptcha Lib" and HAS_IMAGE_CAPTCHA and mode != "math":
            self.current_image = self.engine.render_external(self.current_text)
        else:
            self.current_image = self.engine.render_pil(
                self.current_text,
                difficulty=difficulty,
                has_noise=has_noise,
                is_dark_captcha=is_dark
            )

        # Update Tkinter Display
        self.current_photo = ImageTk.PhotoImage(self.current_image)
        self.lbl_captcha.config(image=self.current_photo)
        self.lbl_captcha.image = self.current_photo  # Prevent GC

        # Reset Status & focus input
        self.lbl_status.config(
            text="Type the characters above and press Enter",
            fg=self.c_text_muted
        )
        self._clear_input()
        self.entry_input.focus_set()

    def verify_captcha(self):
        """Validates the user input against the current solution."""
        user_input = self.entry_input.get().strip()

        if not user_input:
            self.lbl_status.config(
                text="⚠️ Please enter the CAPTCHA code before submitting!",
                fg="#f59e0b"
            )
            return

        self.stat_attempts += 1
        is_correct = False

        if self.var_case.get():
            is_correct = (user_input == self.current_solution)
        else:
            is_correct = (user_input.lower() == self.current_solution.lower())

        if is_correct:
            self.stat_verified += 1
            self.stat_streak += 1
            if self.stat_streak > self.stat_best_streak:
                self.stat_best_streak = self.stat_streak

            self.lbl_status.config(
                text=f"🎉 Verified Successfully! (+10 pts) — Streak: {self.stat_streak}",
                fg=self.c_success
            )
            self._update_stats()
            # Brief delay before generating next challenge for smooth experience
            self.root.after(700, self.refresh_captcha)
        else:
            self.stat_streak = 0
            self.lbl_status.config(
                text=f"❌ Incorrect! Expected '{self.current_solution}'. New challenge generated.",
                fg=self.c_error
            )
            self._update_stats()
            self._clear_input()
            self.refresh_captcha()

    def _update_stats(self):
        """Updates the statistics labels."""
        self.lbl_streak.config(text=f"🔥 Streak: {self.stat_streak}")
        self.lbl_verified.config(text=f"✅ Verified: {self.stat_verified}")
        
        acc = (self.stat_verified / self.stat_attempts * 100) if self.stat_attempts > 0 else 100
        self.lbl_accuracy.config(text=f"🎯 Accuracy: {acc:.0f}%")

    def play_audio(self):
        """Speaks the current CAPTCHA aloud."""
        if not self.current_speech:
            return
        self.lbl_status.config(
            text="🔊 Speaking CAPTCHA audio...",
            fg="#60a5fa"
        )
        CaptchaVoice.speak(self.current_speech)

    def save_captcha_image(self):
        """Exports the generated CAPTCHA to a PNG file."""
        if not self.current_image:
            return
        default_name = f"captcha_{self.current_solution}_{int(time.time())}.png"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
            initialfile=default_name
        )
        if filepath:
            try:
                self.current_image.save(filepath)
                self.lbl_status.config(
                    text=f"💾 Saved to {os.path.basename(filepath)}",
                    fg=self.c_success
                )
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save image: {e}")

    def copy_code_to_clipboard(self):
        """Copies the solution to clipboard for testing/debugging."""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_solution)
        self.lbl_status.config(
            text=f"📋 Copied '{self.current_solution}' to clipboard!",
            fg="#a78bfa"
        )


# =============================================================================
#                                 MAIN ENTRY
# =============================================================================
def main():
    root = tk.Tk()
    app = CaptchaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
