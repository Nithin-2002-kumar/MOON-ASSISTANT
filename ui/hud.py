import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import logging

log = logging.getLogger("moon.ui")
log.setLevel(logging.INFO)


class MoonHUD:
    """
    Minimal futuristic HUD with:
      - central status text
      - log box
      - small control buttons (Listen / Stop / Shutdown)
    The HUD exposes helper methods the main assistant can call (update_status, log).
    """

    def __init__(self, assistant, fullscreen=False):
        """
        assistant: reference to MoonAssistant instance (used for callbacks)
        """
        self.assistant = assistant
        self.root = tk.Tk()
        self.root.title("MOON Assistant")
        self.root.configure(bg="#0f0f0f")
        if fullscreen:
            self.root.attributes("-fullscreen", True)
        self._build_ui()
        # run a small background thread to keep UI reactive for long ops
        self._ui_lock = threading.Lock()

    def _build_ui(self):
        # top frame: status
        self.status_var = tk.StringVar(value="Status: Idle")
        status_label = tk.Label(self.root, textvariable=self.status_var, fg="#00ffff", bg="#0f0f0f",
                                font=("Orbitron", 18, "bold"))
        status_label.pack(pady=(10, 6))

        # log area
        self.log_box = scrolledtext.ScrolledText(self.root, width=100, height=20, bg="#0b0b0b",
                                                 fg="#00ffcc", font=("Consolas", 11), borderwidth=0)
        self.log_box.pack(padx=12, pady=(0, 12))

        # controls
        ctrl = tk.Frame(self.root, bg="#0f0f0f")
        ctrl.pack(pady=(0, 12))
        self.listen_btn = ttk.Button(ctrl, text="🎤 Listen", command=self._on_listen)
        self.listen_btn.grid(row=0, column=0, padx=6)
        self.stop_btn = ttk.Button(ctrl, text="⏹ Stop", command=self._on_stop)
        self.stop_btn.grid(row=0, column=1, padx=6)
        self.shutdown_btn = ttk.Button(ctrl, text="🛑 Shutdown", command=self._on_shutdown)
        self.shutdown_btn.grid(row=0, column=2, padx=6)

    # UI callbacks
    def _on_listen(self):
        # start a short thread to avoid blocking UI
        threading.Thread(target=self._listen_then_process, daemon=True).start()

    def _listen_then_process(self):
        self.update_status("Listening for wake word...")
        text = self.assistant.speech.listen()
        if text:
            self.log(f"User (raw): {text}")
            # If wake word present, ask for command
            if self.assistant.wake_word in text:
                self.assistant.speech.say("Yes?")
                self.update_status("Awaiting command...")
                cmd = self.assistant.speech.listen()
                if cmd:
                    self.log(f"User command: {cmd}")
                    # Process in background so UI remains responsive
                    threading.Thread(target=self.assistant.process_command, args=(cmd,), daemon=True).start()
        else:
            self.update_status("No speech detected.")

    def _on_stop(self):
        self.update_status("Stopped listening.")

    def _on_shutdown(self):
        self.update_status("Shutting down...")
        self.assistant.speech.say("Shutting down. Goodbye.")
        try:
            # terminate app cleanly
            self.root.quit()
        except Exception:
            log.exception("Error when quitting HUD")

    # helpers
    def run(self):
        self.root.mainloop()

    def update_status(self, text: str):
        self.status_var.set(f"Status: {text}")
        self.log(f"[STATUS] {text}")

    def log(self, text: str):
        self.log_box.insert(tk.END, f"{text}\n")
        self.log_box.see(tk.END)
        log.info(text)
