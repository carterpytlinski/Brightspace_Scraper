import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import customtkinter as ctk
import asyncio
import threading
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from models.user import User
from gui.frames.login import loginFrame
from gui.widgets.profile import profileWidget
from gui.widgets.header import headerWidget
from brightspace_scraper.modules.auth import login
from brightspace_scraper.utils.courses import getCourses, getCourseId
from brightspace_scraper.modules.assignments import getAssignments
from async_loop import start_asyncio_loop

load_dotenv()

CENTER_ON_WINDOW_DICT = {"column": 0}
TOP_RIGHT_ON_WINDOW_DICT = {"column": 0,"sticky": 'nw'}

def PADDING(padding: int) -> dict[int]:
    return {"padx": padding, "pady": padding}

def STICKY(sticky: str) -> dict[str]:
    return {"sticky": sticky}

BRIGHTSPACE_URL = os.environ.get("BRIGHTSPACE_URL")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1600x1000")
        self.title("Better Brightspace")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.logged_in = False

        self.current_user: User = None
        self.PROFILE_WIDGET: profileWidget = None

        self.HEADER_WIDGET: headerWidget = headerWidget(master=self)
        self.AUTH_FRAME: loginFrame = loginFrame(master=self, on_login_callback=self.handleLogin)

        self.HEADER_WIDGET.grid(row=0, **CENTER_ON_WINDOW_DICT, **PADDING(0), **STICKY('n'))
        self.AUTH_FRAME.grid(row=0, **CENTER_ON_WINDOW_DICT, **PADDING(50))

        self.LOADING_BAR = ctk.CTkProgressBar(self, width=400)
        self.LOADING_BAR.set(0) 

    async def handleLogin(self, USER_USERNAME: str, USER_PASSWORD: str) -> None:
        print(f"Starting login for {USER_USERNAME}...")

        self.LOADING_BAR.grid(row=1, **CENTER_ON_WINDOW_DICT, **PADDING(10))
        self.LOADING_BAR.start()

        await self.scrapeBrightspace(USER_USERNAME=USER_USERNAME, USER_PASSWORD=USER_PASSWORD)

        self.LOADING_BAR.stop()
        self.LOADING_BAR.set(1.0)

        print("Login complete ✅")
        self.logged_in = True
        self.AUTH_FRAME.grid_remove()

        self.current_user = User(USER_USERNAME=USER_USERNAME, USER_PASSWORD=USER_PASSWORD)
        self.PROFILE_WIDGET = profileWidget(master=self, USER_USERNAME=self.current_user.USER_USERNAME)
        self.PROFILE_WIDGET.grid(row=0, **TOP_RIGHT_ON_WINDOW_DICT, **PADDING(20))

        self.after(1000, lambda: self.LOADING_BAR.grid_forget())

    async def scrapeBrightspace(self, USER_USERNAME: str, USER_PASSWORD: str):
        async with async_playwright() as p:
            BROWSER = await p.chromium.launch(headless=True)
            CONTEXT = await BROWSER.new_context()
            PAGE = await CONTEXT.new_page()

            await login(PAGE, BRIGHTSPACE_URL, USER_USERNAME, USER_PASSWORD)
            print(f'Logged in as: {USER_USERNAME}')

            COURSES: dict[str] = await getCourses(PAGE)
            COURSE_ID: list[str] = await getCourseId(COURSES)

            ASSIGNMENTS: list[str] = await getAssignments(PAGE, COURSE_ID)

            await BROWSER.close()
        
        return ASSIGNMENTS


if __name__ == "__main__":
    threading.Thread(target=start_asyncio_loop, daemon=True).start()

    app = App()
    app.mainloop()