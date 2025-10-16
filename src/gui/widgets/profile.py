import customtkinter as ctk

CENTER_ON_FRAME_DICT = {"row": 0, "column": 0, "padx": 20, "pady": 20}

class profileWidget(ctk.CTkFrame):
    def __init__(self, master, USER_USERNAME: str):
        super().__init__(master)
        self.USERNAME_LABEL = ctk.CTkLabel(self, text=f"🔗 Connected as: {USER_USERNAME}")
        self.USERNAME_LABEL.grid(**CENTER_ON_FRAME_DICT)



