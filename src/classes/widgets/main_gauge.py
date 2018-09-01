"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame

class MainGauge(Frame):
    """
        A gauge that displays any kind of information.
        It contains a title and three data fields.
        One large and two smaller ones.
    """

    title_label = None
    main_gauge_label = None
    sub_gauge1_label = None
    sub_gauge2_label = None

    # Private methods
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.__initialize_fonts()
        self.__initialize_widgets()
        self.__place_widgets()

    def __initialize_fonts(self):
        self.title_font = font.Font(family="Helvetica", size=8, weight="normal")
        self.value_font = font.Font(family="FreeMono", size=25, weight="bold")
        self.subvalue_font = font.Font(family="FreeMono", size=16, weight="bold")

    def __initialize_widgets(self):
        self.title_label = Label(self,
                                 text="---",
                                 background="white",
                                 fg="black",
                                 font=self.title_font)

        self.main_gauge_label = Label(self,
                                      text="--.-",
                                      background="white",
                                      fg="black",
                                      font=self.value_font)

        self.sub_gauge1_label = Label(self,
                                      text="--.-",
                                      background="white",
                                      fg="black",
                                      font=self.subvalue_font)

        self.sub_gauge2_label = Label(self,
                                      text="--.-",
                                      background="white",
                                      fg="black",
                                      font=self.subvalue_font)

    def __place_widgets(self):
        self.title_label.pack(pady=(5, 0))
        self.main_gauge_label.pack(pady=(0, 0))
        self.sub_gauge1_label.pack(pady=(0, 0))
        self.sub_gauge2_label.pack(pady=(0, 0))

    # Public methods
    def update_values(self, title=None, value=None, subvalue=None, subvalue2=None):
        """Updates the gauges."""
        if title is not None:
            self.title_label.config(text=title)
        if value is not None:
            self.main_gauge_label.config(text=str(value))
        if subvalue is not None:
            self.sub_gauge1_label.config(text=str(subvalue))
        if subvalue2 is not None:
            self.sub_gauge2_label.config(text=str(subvalue2))

    def set_background_color(self, color):
        self.configure(background=color)
        self.title_label.configure(background=color)
        self.main_gauge_label.configure(background=color)
        self.sub_gauge1_label.configure(background=color)
        self.sub_gauge2_label.configure(background=color)

    def set_text_color(self, color):
        self.title_label.configure(fg=color)
        self.main_gauge_label.configure(fg=color)
        self.sub_gauge1_label.configure(fg=color)
        self.sub_gauge2_label.configure(fg=color)

