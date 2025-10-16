import asyncio
import threading
import customtkinter as ctk
from gui.frames.login import loginFrame

def start_asyncio_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":
    # Start asyncio loop in a background thread
    threading.Thread(target=start_asyncio_loop, daemon=True).start()

    # Create GUI
    app = ctk.CTk()
    app.title("BrightSpace Scraper")

    frame = loginFrame(app, on_login_callback=lambda u, p: print(f"Logging in {u}:{p}"))
    frame.pack(expand=True, fill="both")

    app.mainloop()