import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import customtkinter as ctk
import asyncio
from async_loop import loop

CENTER_ON_FRAME_DICT = {"column": 0, "padx": 20, "pady": 20}
FRAME_SIZE = {"width": 300, "height": 50}
FONT = {"font": ("Helvetica Neue", 20)}

class loginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_callback):
        super().__init__(master)

        self.on_login_callback = on_login_callback

        self.USERNAME_FIELD = ctk.CTkEntry(self, placeholder_text="Username", **FONT, **FRAME_SIZE)
        self.PASSWORD_FIELD = ctk.CTkEntry(self, placeholder_text="Password", show='*', **FONT, **FRAME_SIZE)
        self.LOGIN_BUTTON = ctk.CTkButton(self, text="Login", font=("Helvetica Neue", 20, "bold"), **FRAME_SIZE, command=self._on_login_button_click)
        self.LOGIN_DESTINATION = ctk.CTkLabel(self, text="Logging into https://learn.truman.edu", font=("Helvetica Neue", 15, "italic"), pady=5)

        self.USERNAME_FIELD.grid(row=1, **CENTER_ON_FRAME_DICT)
        self.PASSWORD_FIELD.grid(row=2, **CENTER_ON_FRAME_DICT)
        self.LOGIN_BUTTON.grid(row=3, **CENTER_ON_FRAME_DICT)
        self.LOGIN_DESTINATION.grid(row=4, **CENTER_ON_FRAME_DICT)

    def _on_login_button_click(self):
        from async_loop import loop
        if loop is None:
            print("⚠️ Event loop not initialized yet!")
            return
        asyncio.run_coroutine_threadsafe(self.loginButtonClick(), loop)

    async def loginButtonClick(self) -> None:
        USER_USERNAME: str = self.USERNAME_FIELD.get()
        USER_PASSWORD: str = self.PASSWORD_FIELD.get()
        self.clearField(self.USERNAME_FIELD)
        self.clearField(self.PASSWORD_FIELD)
        self.hideLoginFields()
        self.LOGIN_BUTTON.configure(state='disabled')
        await self.on_login_callback(USER_USERNAME, USER_PASSWORD)
        

    def logoutButtonClick(self) -> None:
        self.showLogi1nFields()

    def hideLoginFields(self) -> None:
        self.USERNAME_FIELD.grid_forget()
        self.PASSWORD_FIELD.grid_forget()
        self.LOGIN_BUTTON.configure(text="Logout", command=self.showLoginFields)

    def showLoginFields(self) -> None:
        self.USERNAME_FIELD.grid(row=0, **CENTER_ON_FRAME_DICT)
        self.PASSWORD_FIELD.grid(row=1, **CENTER_ON_FRAME_DICT)
        self.LOGIN_BUTTON.configure(text='Login', command=self.loginButtonClick)

    def clearField(self, field) -> None:
        field.delete(0, ctk.END)
