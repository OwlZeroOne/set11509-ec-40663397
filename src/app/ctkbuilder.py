from external.CTkDatePicker import CTkDatePicker
from external.CTkTable import CTkTable
from external.CTkSpinBox import FloatSpinbox
from dataclasses import dataclass
from customtkinter import *
from consts import Font

Container = CTk | CTkToplevel | CTkFrame | CTkScrollableFrame | CTkTabview
Widget = CTkLabel | CTkButton | CTkDatePicker | CTkComboBox | CTkEntry | CTkDatePicker | CTkTable


class CTkBuilderException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


@dataclass
class Padding:
    north : int
    east : int
    south : int
    west : int

    @classmethod
    def default(cls):
        return cls(0, 0, 0, 0)


class CTkProduct:
    def __init__(self, container):
        self._container = container
        self._widgets = {}

    def add(self, key, widget):
        self._widgets[key] = widget

    def remove(self, key):
        self._widgets.pop(key)

    def get_widget(self, key):
        return self._widgets[key]

    @property
    def container(self) -> Container:
        return self._container


@dataclass
class Size:
    width : int
    height : int

    @classmethod
    def default(cls):
        return cls(50, 50)


class CTkBuilder:
    
    def __init__(self, product: CTkProduct = None):
        self._product: CTkProduct = product
        # self._product.container: Container = None if product is None else product.container

    @classmethod
    def window(
            cls,
            title: str,
            resize_width:bool,
            resize_height: bool,
            grid_rows:int,
            grid_cols:int,
            size: Size=Size.default(),
            row_weights: list[int]=None,
            col_weights: list[int]=None,
            row_minsizes: list[int]=None,
            col_minsizes: list[int]=None,
            **kwargs
    ) -> "CTkBuilder":
        window_builder = cls()
        container = CTk(**kwargs)
        window_builder._product = CTkProduct(container)
        window_builder._init_window(title, resize_width, resize_height, size)
        window_builder._setup_grid(
            grid_rows,
            grid_cols,
            row_weights,
            col_weights,
            row_minsizes,
            col_minsizes
        )
        return window_builder

    @classmethod
    def popUp(
            cls,
            parent:Container,
            title: str,
            resize_width:bool,
            resize_height: bool,
            grid_rows:int,
            grid_cols:int,
            size: Size=Size.default(),
            row_weights: list[int]=None,
            col_weights: list[int]=None,
            row_minsizes: list[int]=None,
            col_minsizes: list[int]=None, **kwargs
    ) -> "CTkBuilder":
        popup_builder = cls()
        container = CTkToplevel(**kwargs)
        popup_builder._product = CTkProduct(container)
        popup_builder._init_window(title, resize_width, resize_height, size=size)
        popup_builder._setup_grid(
            grid_rows,
            grid_cols,
            row_weights,
            col_weights,
            row_minsizes,
            col_minsizes
        )
        popup_builder._product.container.after(100, popup_builder._product.container.lift)
        return popup_builder

    @classmethod
    def frame(
            cls,
            parent_product: CTkProduct,
            row: int,
            col: int,
            frame_type: str,
            grid_rows: int,
            grid_cols: int,
            rowspan=1,
            colspan=1,
            size: Size=Size.default(),
            pad: Padding=Padding.default(),
            row_weights: list[int]=None,
            col_weights: list[int]=None,
            row_minsizes: list[int]=None,
            col_minsizes: list[int]=None,
            sticky: str="",
            **kwargs
    ) -> "CTkBuilder":
        frame_builder = cls()
        container = frame_builder._frame_switch(parent_product, frame_type, size, **kwargs)
        frame_builder._container =container
        frame_builder._product = CTkProduct(container)
        frame_builder._setup_grid(grid_rows, grid_cols, row_weights, col_weights, row_minsizes, col_minsizes)
        container.grid(
            row=row,
            column=col,
            sticky=sticky,
            rowspan=rowspan,
            columnspan=colspan,
            pady=(pad.north,pad.south),
            padx=(pad.east,pad.west))
        return frame_builder

    @staticmethod
    def _frame_switch(
            parent_product: CTkProduct,
            frame_type: str,
            size: Size=Size.default(),
            **kwargs
    ) -> "Container":
        frames = ["frame", "scroll", "tab"]
        if not frame_type in frames:
            raise CTkBuilderException(f"{frame_type} is not a valid container choice. Must be one of {frames}.")
        if frame_type == "frame":
            return CTkFrame(parent_product.container, width=size.width, height=size.height, **kwargs)
        elif frame_type == "scroll":
            return CTkScrollableFrame(parent_product.container, width=size.width, height=size.height, **kwargs)
        elif frame_type == "tab":
            return CTkTabview(parent_product.container, width=size.width, height=size.height, **kwargs)
        else:
            raise CTkBuilderException(f"Unhandled frame type: {frame_type}.")

    def _init_window(self, title: str, resize_width: bool,resize_height: bool, size: Size=Size.default()):
        self._product.container.geometry(f"{size.width}x{size.height}")
        self._product.container.title(title)
        self._product.container.resizable(resize_width, resize_height)

    def _setup_grid(
            self,
            rows,
            cols,
            row_weights=None,
            col_weights=None,
            row_minsizes=None,
            col_minsizes=None
    ):
        rows = 1 if rows is None else rows
        cols = 1 if cols is None else cols
        row_weights = [1 for _ in range(rows)] if row_weights is None else row_weights
        col_weights = [1 for _ in range(cols)] if col_weights is None else col_weights
        row_minsizes = [0 for _ in range(rows)] if row_minsizes is None else row_minsizes
        col_minsizes = [0 for _ in range(cols)] if col_minsizes is None else col_minsizes

        for i in range(rows):
            self._product.container.grid_rowconfigure(i, weight=row_weights[i], minsize=row_minsizes[i])
        for i in range(cols):
            self._product.container.grid_columnconfigure(i, weight=col_weights[i], minsize=col_minsizes[i])

    def label(
            self,
            key:str,
            text: str,
            fontsize: int,
            row: int,
            col: int,
            typeface: str=Font.TF,
            pad:Padding=Padding.default(),
            rowspan: int=1,
            colspan: int=1,
            sticky: str='',
            underline: bool=False,
            bold: bool=False,
            italic: bool=False,
            overstrike: bool=False,
            **kwargs
    ) -> "CTkBuilder":
        font_style = self._text_style_builder(typeface, fontsize, underline, bold, italic, overstrike)
        label = CTkLabel(self._product.container, text=text, font=font_style, **kwargs)
        label.grid(
            column=col,
            row=row,
            rowspan=rowspan,
            columnspan=colspan,
            pady=(pad.north,pad.south),
            padx=(pad.west, pad.east),
            sticky=sticky
        )
        self._product.add(key, label)
        return self

    @staticmethod
    def _text_style_builder(typeface: str, fontsize: int, underline: bool, bold: bool, italic: bool, overstrike: bool) -> tuple[str, int, str]:
        style = ""
        if underline:
            style += " underline"
        if bold:
            style += " bold"
        if italic:
            style += " italic"
        if overstrike:
            style += " overstrike"

        style = style[1:]

        if not any([underline, bold, italic, overstrike]):
            style += "normal"

        return typeface, fontsize, style

    def button(
            self,
            key:str,
            text: str,
            fontsize: int,
            row: int,
            col: int,
            typeface: str=Font.TF,
            pad:Padding=Padding.default(),
            rowspan: int=1,
            colspan: int=1,
            sticky: str='',
            **kwargs
    ) -> "CTkBuilder":
        button = CTkButton(self._product.container, text=text, font=(typeface, fontsize), **kwargs)
        button.grid(column=col, row=row, rowspan=rowspan, columnspan=colspan, pady=(pad.north,pad.south), padx=(pad.west, pad.east), sticky=sticky)
        self._product.add(key, button)
        return self

    def entry(
            self,
            key:str,
            placeholder: str,
            fontsize: int,
            row: int,
            col: int,
            typeface: str=Font.TF,
            pad:Padding=Padding.default(),
            rowspan: int=1,
            colspan: int=1,
            sticky: str='',
            **kwargs
    ) -> "CTkBuilder":
        entry = CTkEntry(self._product.container, placeholder_text=placeholder, font=(typeface, fontsize), **kwargs)
        entry.grid(
            column=col,
            row=row,
            columnspan=colspan,
            rowspan=rowspan,
            pady=(pad.north,pad.south),
            padx=(pad.west, pad.east),
            sticky=sticky
        )
        self._product.add(key, entry)
        return self

    def segmentedButton(
            self,
            key: str,
            segments: list[str],
            default: str,
            fontsize: int,
            row: int,
            col: int,
            typeface: str=Font.TF,
            pad:Padding=Padding.default(),
            rowspan: int=1,
            colspan: int=1,
            sticky: str='',
            **kwargs
    ) -> "CTkBuilder":
        if default not in segments:
            raise CTkBuilderException(f"Default segment must be one of the passed segments: {segments}.")
        seg_button = CTkSegmentedButton(self._product.container, values=segments, font=(typeface, fontsize), **kwargs)
        seg_button.grid(
            column=col,
            row=row,
            columnspan=colspan,
            rowspan=rowspan,
            pady=(pad.north,pad.south),
            padx=(pad.west, pad.east),
            sticky=sticky)
        self._product.add(key, seg_button)
        seg_button.set(default)
        return self

    def comboBox(
            self,
            key: str,
            options: list[str],
            default: str,
            fontsize: int,
            row: int,
            col: int,
            typeface: str=Font.TF,
            pad:Padding=Padding.default(),
            rowspan: int=1,
            colspan: int=1,
            sticky: str='',
            allow_manual_input: bool=False,
            **kwargs
    ) -> "CTkBuilder":
        if default not in options:
            raise CTkBuilderException(f"Default segment must be one of the passed segments: {options}.")
        combo_box = CTkComboBox(self._product.container, values=options, font=(typeface, fontsize), **kwargs)
        combo_box.grid(
            column=col,
            row=row,
            rowspan=rowspan,
            columnspan=colspan,
            pady=(pad.north,pad.south),
            padx=(pad.west, pad.east),
            sticky=sticky
        )
        combo_box.configure(state=("normal" if allow_manual_input else "readonly"))
        combo_box.set(default)
        self._product.add(key, combo_box)
        return self

    def datePicker(
            self,
            key: str,
            row: int,
            col: int,
            default: str,
            rowspan: int=1,
            colspan: int=1,
            pad:Padding=Padding.default(),
            size:Size=Size.default(),
            allow_change_month: bool=True,
            allow_manual_input: bool=False,
            localization: str='en_EN',
            sticky=""
    ):
        date_picker = CTkDatePicker(self._product.container, width=size.width, height=size.height)
        date_picker.set_allow_change_month(allow_change_month)
        date_picker.set_allow_manual_input(allow_manual_input)
        date_picker.set_localization(localization)
        date_picker.set_date_format('%Y-%m-%d')
        date_picker.grid(
            column=col,
            row=row,
            rowspan=rowspan,
            columnspan=colspan,
            pady=(pad.north,pad.south),
            padx=(pad.west, pad.east),
            sticky=sticky
        )
        date_picker.set_date(default)
        self._product.add(key, date_picker)
        return self

    def table(
            self,
            key: str,
            rows: int,
            cols: int,
            row: int,
            col: int,
            values: list[list[str]],
            fontsize: int,
            labels: list[str]=None,
            pad:Padding=Padding.default(),
            rowspan: int=1,
            colspan: int=1,
            typeface: str=Font.TF,
            sticky: str='',
            **kwargs
    ):
        table = CTkTable(
            self._product.container,
            row=rows,
            column=cols,
            values=values,
            font=(typeface, fontsize),
            **kwargs
        )
        if labels:
            table.edit_row(0, labels)
        table.grid(
            column=col,
            row=row,
            rowspan=rowspan,
            columnspan=colspan,
            pady=(pad.north, pad.south),
            padx=(pad.west, pad.east),
            sticky=sticky
        )
        self._product.add(key, table)
        return self

    def spinbox(
            self,
            key: str,
            row: int,
            col: int,
            fontsize: int,
            size: Size=Size(100,32),
            pad: Padding=Padding(0,0,0,0),
            typeface: str=Font.TF,
            sticky: str='nsew',
            rowspan: int=1,
            colspan: int=1,
            **kwargs
    ):
        spin_box = FloatSpinbox(
            self._product.container,
            width=size.width,
            height=size.height,
            font=(typeface, fontsize),
            **kwargs
        )
        spin_box.grid(
            column=col,
            row=row,
            rowspan=rowspan,
            columnspan=colspan,
            pady=(pad.north, pad.south),
            padx=(pad.west, pad.east),
            sticky=sticky
        )
        self._product.add(key, spin_box)
        return self

    def build(self):
        return self._product

    def destroy(self):
        self._product.container.destroy()
        del self._product