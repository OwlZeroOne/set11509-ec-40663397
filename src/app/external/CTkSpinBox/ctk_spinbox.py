from typing import Union, Callable

import customtkinter

class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 # EDIT: Added to enable adjustment of the initial value
                 default: float = 0.0,
                 # EDIT: Added to enable entry font adjustment
                 font: tuple[str, int],
                 fg_color = ("gray78", "gray28"),
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=fg_color)  # set frame color

        self.grid_columnconfigure((0, 1, 3, 4), weight=0)  # buttons don't expand
        self.grid_columnconfigure(2, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height - 6, height=height - 6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.subtract_double_button = customtkinter.CTkButton(self, text="x2", width=height-6, height=height-6,
                                                       command=lambda:self.subtract_button_callback(double=True))
        self.subtract_double_button.grid(row=0, column=1, padx=(0, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, font=font)
        self.entry.grid(row=0, column=2, columnspan=1, padx=0, pady=0, sticky="ew")

        self.add_double_button = customtkinter.CTkButton(self, text="x2", width=height - 6, height=height - 6,
                                                  command=lambda:self.add_button_callback(double=True))
        self.add_double_button.grid(row=0, column=3, padx=(0, 0), pady=3)

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=4, padx=(0, 3), pady=3)

        # default value
        self.set(default)

    def add_button_callback(self, double:bool=False):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self._double_stepsize(double=double)
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self, double:bool=False):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self._double_stepsize(double=double)
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))

    def _double_stepsize(self, double:bool=False):
        return self.step_size * 2 if double else self.step_size