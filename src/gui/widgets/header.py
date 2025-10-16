import customtkinter as ctk

class headerWidget(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.HEADER_LABEL = ctk.CTkLabel(
            self,
            text="Better Brightspace",
            font=("Helvetica Neue", 48, "bold"),
            text_color="#295B8E",
        )
        self.HEADER_LABEL.grid(row=0, column=0, padx=10, pady=20, sticky="n")