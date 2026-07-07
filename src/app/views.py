import webbrowser
from typing import Literal

from customtkinter import CTkFrame

import reqs, consts
# pandas and numpy only used to format shareholders into a 2d-list.
# TODO: Find a way to isolate this process from the front-end.
import customtkinter
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

from consts import Font
from main import App
from ctkbuilder import CTkProduct, CTkBuilder, Size, Padding
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from abc import ABC, abstractmethod

class BaseView(ABC):
    def __init__(self, app: App, row: int, col: int):
        self._app = app
        self._row = row
        self._col= col
        self._view_product: CTkProduct = None

    @abstractmethod
    def _build(self):
        pass

    def destroy(self):
        if self._view_product:
            for widget in self._view_product.container.winfo_children():
                try:
                    widget.destroy()
                except Exception:
                    pass
            self._view_product.container.destroy()

    def get_widget(self, key: str):
        return self._view_product.get_widget(key)

    @property
    def container(self):
        return self._view_product.container


class LoginView(BaseView):
    def __init__(self, app: App, row, col):
        super().__init__(app, row, col)
        self._build()

    def _build(self):
        entry_w = 300
        entry_h = consts.golden_shrink(entry_w, factor=4)
        button_w = consts.golden_shrink(entry_w, factor=0.7)
        button_h = consts.golden_shrink(button_w, factor=4)
        parent_product = self._app.main_window_product

        self._view_product = (CTkBuilder.frame(
            parent_product,
            self._row,
            self._col,
            "frame",
            6,
            1,
            size=Size(500, 500),
            col_weights=[1],
            row_weights=[1, 1, 1, 1, 1, 1, 1],
            col_minsizes=[700]
            )
            .label("login_label", "Log In To Your ShareTrader", fontsize=Font.H1, row=0, col=0, pad=Padding(50, 0, 20, 0))
            .entry("username_entry", "Username", fontsize=Font.TEXT, width=entry_w, height=entry_h, row=1, col=0, pad=Padding(10, 0, 10, 0))
            .entry("password_entry", "Password", fontsize=Font.TEXT, width=entry_w, height=entry_h, row=2, col=0, show="*", pad=Padding(10, 0, 10, 0))
            .label("alert_label", "", fontsize=Font.SUBTLE, row=3, col=0, pad=Padding(10, 0, 10, 0))
            .button("login_button", "Login", fontsize=Font.BUTTON_TEXT, row=4, col=0, width=button_w, height=button_h, pad=Padding(10, 0, 10, 0), command=self._exec_login)
            .label("register_label", "Not an existing user?", fontsize=Font.TEXT, row=5, col=0, pad=Padding(5, 0, 5, 0))
            .button("register_button", "Register", fontsize=Font.BUTTON_TEXT, row=6, col=0, width=button_w, height=button_h, pad=Padding(10, 0, 50, 0), command=self._exec_register)
            .build()
        )
        parent_product.add("current_view", self._view_product)

    def _exec_login(self):
        alert_label = self._view_product.get_widget("alert_label")
        username = self._view_product.get_widget("username_entry").get()
        password = self._view_product.get_widget("password_entry").get()
        if username and password:
            response = reqs.login_user(username, password)
            status_code = response.status_code
            token = response.json().get("token")
            user = response.json().get("user")
            if status_code == 200:
                alert_label.configure(
                    text="Login successful!",
                    text_color=consts.SUCCESS_MSG_COLOR
                )
                self._app.user_data.save(user, token)
                self._app.user_data.load()
                self._app.trigger_logged_in_view()
            elif status_code == 401:
                alert_label.configure(
                    text="Incorrect username or password!",
                    text_color=consts.ERROR_MSG_COLOR
                )
            else:
                alert_label.configure(
                    text="ERR_500: INTERNAL ERROR!",
                    text_color=consts.ERROR_MSG_COLOR
                )
        else:
            alert_label.configure(
                text="Please enter a username and password!",
                text_color=consts.ERROR_MSG_COLOR
            )

    def _exec_register(self):
        print("Execute Register")
        RegisterViewWindow(self._view_product.container)


class RegisterViewWindow:
    def __init__(self, parent_container):
        entry_w = 300
        entry_h = consts.golden_shrink(entry_w, factor=4)
        button_w = consts.golden_shrink(entry_w, factor=0.7)
        button_h = consts.golden_shrink(button_w, factor=4)

        self._view_product = (CTkBuilder.popUp(
            parent_container,
            "ShareTrader: Register",
            False,
            False,
            8,
            1,
            Size(500, 600)
        )
        .label("register_label", "Register", Font.H1, 0, 0, pad=Padding(50, 0, 20, 0))
        .entry("username_entry", "Username", Font.ENTRY_TEXT, 1, 0, width=entry_w, height=entry_h, pad=Padding(20, 0, 10, 0))
        .entry("password_entry", "Password", Font.ENTRY_TEXT, 2, 0, width=entry_w, height=entry_h, pad=Padding(10, 0, 10, 0), show="*")
        .entry("confirm_password_entry", "Confirm Password", Font.ENTRY_TEXT, 3, 0, width=entry_w, height=entry_h, pad=Padding(10, 0, 10, 0), show="*")
        .entry("email_entry", "Email", Font.ENTRY_TEXT, 4, 0, width=entry_w, height=entry_h, pad=Padding(10, 0, 10, 0))
        .entry("name_entry", "Name", Font.ENTRY_TEXT, 5, 0, width=entry_w, height=entry_h, pad=Padding(10, 0, 10, 0))
        .label("alert_label", "", Font.SUBTLE, 6, 0, pad=Padding(5, 0, 5, 0))
        .button("register_button", "Register", Font.BUTTON_TEXT, 7, 0, width=button_w, height=button_h, pad=Padding(10, 0, 50, 0), command=self._exec_register)
        .build()
        )

    def _exec_register(self):
        alert_label = self._view_product.get_widget("alert_label")
        username = self._view_product.get_widget("username_entry").get()
        password = self._view_product.get_widget("password_entry").get()
        password2 = self._view_product.get_widget("confirm_password_entry").get()
        email = self._view_product.get_widget("email_entry").get()
        name = self._view_product.get_widget("name_entry").get()
        if all([username, password, password2, email, name]):
            if self._input_conditions_satisfied():
                status_code = reqs.register_user(username, password, email, name, "user")
                if status_code == 201:
                    alert_label.configure(
                        text="Registered successfully! You may now return to the login page.",
                        text_color=consts.SUCCESS_MSG_COLOR
                    )
                    CTkBuilder(self._view_product).destroy()
                elif status_code == 400:
                    alert_label.configure(
                        text=f"ERR_{status_code}: Bad request!.",
                        text_color=consts.ERROR_MSG_COLOR
                    )
                else:
                    alert_label.configure(
                        text=f"ERR_{status_code}: Unexpected error occurred!",
                        text_color=consts.ERROR_MSG_COLOR
                    )
        else:
            alert_label.configure(
                text="Please provide all information!",
                text_color=consts.ERROR_MSG_COLOR
            )

    def _input_conditions_satisfied(self):
        alert_label = self._view_product.get_widget("alert_label")
        if not self._passwords_match():
            alert_label.configure(text="Passwords do not match!", text_color=consts.ERROR_MSG_COLOR)
            return False
        return True

    def _valid_username(self):
        # TODO: Enforce valid 8-character username
        raise NotImplementedError("Enforce valid 8-character username")

    def _valid_password(self):
        # TODO: Enforce valid 12-character password with words from the charset [a-zA-z0-9!?@_+$&]
        raise NotImplementedError("Enforce valid 12-character password with words from the charset [a-zA-z0-9!?@_+$&]")

    def _passwords_match(self):
        password = self._view_product.get_widget("password_entry").get()
        password2 = self._view_product.get_widget("confirm_password_entry").get()
        return password == password2

    def _valid_email(self):
        # TODO: Enforce valid email, suffixed by '@<domain>
        raise NotImplementedError("Enforce valid email, suffixed by '@<domain>")

    def _valid_name(self):
        # TODO: Enforce valid name from charset [a-zA-Z], with capital first letter
        raise NotImplementedError("Enforce valid name from charset [a-zA-Z], with capital first letter")


class LoggedInView(BaseView):
    def __init__(self, app: App, row: int, col: int):
        super().__init__(app, row, col)
        self._build()

    def _build(self):
        parent_product = self._app.main_window_product
        segments = ['Dashboard', 'News', 'Stocks', 'Brokers', 'Profile', 'Log Out']
        if self._app.user_data.get('role') == 'admin':
            segments.insert(-1, 'Admin')

        self._current_view = None
        self._nav_product = (
            CTkBuilder.frame(
                parent_product,
                self._row,
                self._col,
                "frame",
                2,
                1,
                sticky="nsew",
                row_minsizes=[50, 0],
                row_weights=[0, 1]
            )
            .segmentedButton("nav_bar", segments, "Dashboard", Font.BUTTON_TEXT, 0, 0, corner_radius=0, sticky="nsew", command=self._seg_button_listener)
            .build()
        )
        parent_product.add("current_view", self._nav_product.container)
        self._exec_dashboard()

    def _seg_button_listener(self, value: str):
        if value == "Dashboard":
            self._exec_dashboard()
        elif value == "News":
            self._exec_news()
        elif value == "Stocks":
            self._exec_stocks()
        elif value == "Brokers":
            self._exec_brokers()
        elif value == "Profile":
            self._exec_profile()
        elif value == "Admin":
            self._exec_admin()
        elif value == "Log Out":
            self._exec_logout()

    def _exec_logout(self):
        reqs.update_user(self._app.user_data.get(), self._app.user_data.get_token())
        self._app.user_data.clear()
        self._new_view()
        self._nav_product.container.destroy()
        self._app.trigger_login_view()

    def _exec_dashboard(self):
        self._new_view()
        self._current_view = DashboardView(self._nav_product, self._app, 1, 0)

    def _exec_news(self):
        self._new_view()
        self._current_view = NewsView(self._nav_product, self._app, 1, 0)

    def _exec_stocks(self):
        self._new_view()
        self._current_view = StocksView(self._nav_product, self._app, 1, 0)

    def _exec_brokers(self):
        self._new_view()
        self._current_view = BrokersView(self._nav_product, self._app, 1, 0)

    def _exec_profile(self):
        self._new_view()
        self._current_view = ProfileView(self._nav_product, self._app, 1, 0)

    def _exec_admin(self):
        self._new_view()
        self._current_view = AdminView(self._nav_product, self._app, 1, 0)

    def _new_view(self):
        if self._current_view:
            self._current_view.destroy()


class DashboardView(BaseView):
    def __init__(self, parent, app: App, row: int, col: int):
        super().__init__(app, row, col)
        self._parent = parent
        self._build()

    def _build(self):
        self._view_product = (CTkBuilder.frame(
            self._parent,
            self._row,
            self._col,
            "scroll",
            2,
            2,
            sticky="nsew",
            row_minsizes=[50, 0],
            row_weights=[0, 1],
            col_minsizes=[0, 150],
            col_weights=[1, 0],
        )
        .label("greeting_label", f"Welcome {self._app.user_data.get('name')}!", Font.H1, 0, 0, colspan=2, sticky="w", pad=Padding(20, 20, 20, 20))
        .build())
        chart_frame = ShareChartView(self._view_product, self._app, 1, 0)
        self._view_product.add("chart_frame", chart_frame)

        chart_range_intervals = list(consts.CHART_RNG_INTERVALS.keys())
        chart_manip_product = (CTkBuilder.frame(
            self._view_product,
            1,
            1,
            "frame",
            5,
            2,
            row_minsizes=[50 for _ in range(5)],
            row_weights=[0 for _ in range(5)],
            col_minsizes=[0, 90],
            col_weights=[1, 0],
            sticky="nsew",
            fg_color="transparent",
            corner_radius=0
        )
        .label("start_date_label", "Start Date:", Font.TEXT, 0, 0, sticky="e", pad=Padding(0, 0, 0, 10))
        .datePicker("start_date_picker", 0, 1, consts.THIRTY_DAYS_AGO_STR, sticky="w", pad=Padding(0, 20, 0, 10), size=Size(90, 32))
        .label("end_date_label", "End Date:", Font.TEXT, 1, 0, sticky="e", pad=Padding(0, 0, 10, 10))
        .datePicker("end_date_picker", 1, 1, consts.TODAY_STR, sticky="w", pad=Padding(10, 20, 10, 10))
        .label("interval_label", "Interval:", Font.TEXT, 2, 0, sticky="e", pad=Padding(10, 0, 10, 10))
        .comboBox("interval_combobox", chart_range_intervals, "1 Day", Font.COMBO_TEXT, 2, 1, sticky="ew", pad=Padding(0, 20, 0, 10))
        .label("threshold_label", "Threshold:", Font.TEXT, 3, 0, sticky="e", pad=Padding(10, 0, 10, 10))
        .spinbox("threshold_spinbox", 3, 1, Font.ENTRY_TEXT, default=self._app.user_data.get("threshold"), step_size=5, pad=Padding(10, 20, 10, 10), sticky = "ew", fg_color="transparent", bg_color="transparent", command=self._exec_load_chart)
        .button("submit_button", "Submit", Font.BUTTON_TEXT, 4, 0, sticky="", pad=Padding(10, 20, 0, 0), colspan=2, command=self._exec_load_chart)
        .build())
        self._view_product.add("chart_manip_product", chart_manip_product)
        self._exec_load_chart()

    def _exec_load_chart(self):
        parent = self._view_product
        chart_manip_product = parent.get_widget("chart_manip_product")
        try:
            start = chart_manip_product.get_widget("start_date_picker").get_date()
            end = chart_manip_product.get_widget("end_date_picker").get_date()
            interval = chart_manip_product.get_widget("interval_combobox").get()
            threshold = chart_manip_product.get_widget("threshold_spinbox").get()
            self._app.user_data.update_cache_property("threshold", threshold)
        except ValueError:
            return
        tickers = self._app.user_data.get("tickers")
        if not tickers:
            return
        res = reqs.get_tickers_history(tickers, start, end, consts.CHART_RNG_INTERVALS[interval], self._app.user_data.get_token())
        if res.status_code == 200:
            parent.get_widget("chart_frame").draw(res.json()['data'], threshold)



class StocksView(BaseView):
    def __init__(self, parent, app: App, row: int, col: int):
        super().__init__(app, row, col)
        self._parent = parent
        self._build()

    def _build(self):
        self._view_product = (CTkBuilder.frame(
            self._parent,
            self._row,
            self._col,
            "frame",
            2,
            2,
            sticky="nsew",
            row_minsizes=[50, 0],
            row_weights=[0, 1],
            col_minsizes=[0, 100],
            col_weights=[1, 0]
        )
        .entry("ticker_entry", "Look Up Stocks Using Trading Codes (E.g,. AAPL For Apple Inc.)", Font.ENTRY_TEXT, 0, 0, height=40, sticky="ew", pad=Padding(20, 10, 0, 50))
        .button("submit_ticker_button", "Find", Font.BUTTON_TEXT, 0, 1, height=30, pad=Padding(20, 50, 0, 10), width=120, sticky="ew", command=self._exec_find)
        .build())
        self._stock_view_product = (CTkBuilder.frame(
            self._view_product,
            1,
            0,
            "scroll",
            9,
            2,
            col_minsizes=[100, 0],
            col_weights=[0, 1],
            pad=Padding(10, 50, 50, 50),
            sticky="nsew",
            colspan=2
        )
        .label("stock_label", "No Stock Has Been Selected", Font.H1, 0, 0, pad=Padding(20, 0, 0, 20), sticky="w")
        .build())

    def _exec_find(self):
        view_product = self._view_product
        svp = self._stock_view_product
        stock_label = svp.get_widget("stock_label")
        for child in svp.container.winfo_children():
            if child != stock_label:
                child.destroy()

        self._ticker_code = view_product.get_widget("ticker_entry").get()
        res = reqs.get_ticker_by_code(self._ticker_code, self._app.user_data.get_token())

        if res.status_code == 200:
            stock = res.json()["share"]
            currency = stock["currency"]
            svp.get_widget("stock_label").configure(text=f"Results For {self._ticker_code}:")
            data = self._get_shareholders_as_2d_list()
            # labels = []
            self._stock_view_product = (CTkBuilder(svp)
                .label("name_label", f"Company Name: {stock["name"]}", Font.TEXT, 1, 0, colspan=2, pad=Padding(20, 0, 5, 20), sticky="w")
                .label("sector_label", f"Sector: {stock["sector"]}", Font.TEXT, 2, 0, colspan=2, pad=Padding(5, 0, 5, 20), sticky="w")
                .label("price_label", f"Current Price: {stock["price"]:,} {currency.upper()}", Font.TEXT, 3, 0, colspan=2, pad=Padding(5, 0, 5, 20), sticky="w")
                .label("shares_label", f"Number of Shares: {stock["nShares"]:,} {currency.upper()}", Font.TEXT, 4, 0, colspan=2, pad=Padding(5, 0, 5, 20), sticky="w")
                .label("market_val_label", f"Market Value: {stock["marketValue"]:,} {currency.upper()}", Font.TEXT, 5, 0, colspan=2, pad=Padding(5, 0, 5, 20), sticky="w")
                .label("country_label", f"Country: {stock["country"]}", Font.TEXT, 6, 0, colspan=2, pad=Padding(5, 0, 20, 20), sticky="w")
                .label("alert_label", "", Font.SUBTLE, 7, 0, colspan=2, pad=Padding(5, 0, 20, 20), sticky="w")
                .button("register_interest_button", "Register Interest",Font.BUTTON_TEXT, 8, 0, pad=Padding(0,0,0,20), sticky="w", command=self._exec_register_interest)
                .button("resign_interest_button", "Resign Interest",Font.BUTTON_TEXT, 8, 1, sticky="w", command=self._exec_resign_interest)
                .table("shareholder_table", len(data), len(data[0]), 9, 0, data, Font.TEXT, pad=Padding(20, 20, 20, 20), sticky="ew", colspan=2, anchor="w", corner_radius=0, command=self._on_shareholder_click)
                .build())

            self._sector = stock["sector"]

    def _exec_register_interest(self):
        alert_label = self._stock_view_product.get_widget("alert_label")
        tickers = self._app.user_data.get("tickers")
        sectors = self._app.user_data.get("sectors")

        if self._ticker_code not in tickers:
            tickers.append(self._ticker_code)
            try:
                self._app.user_data.update_cache_property("tickers", tickers)
                if self._sector not in sectors:
                    sectors.append(self._sector)
                    self._app.user_data.update_cache_property("sectors", sectors)
                alert_label.configure(text=f"Successfully registered interest for {self._ticker_code}!", text_color=consts.SUCCESS_MSG_COLOR)
            except Exception:
                alert_label.configure(text=f"ERROR: Failed to save!", text_color=consts.ERROR_MSG_COLOR)
        else:
            alert_label.configure(text=f"Already watching this stock!", text_color=consts.ERROR_MSG_COLOR)

    def _exec_resign_interest(self):
        alert_label = self._stock_view_product.get_widget("alert_label")
        tickers = self._app.user_data.get("tickers")
        sectors = self._app.user_data.get("sectors")

        if self._ticker_code in tickers:
            tickers.remove(self._ticker_code)
            try:
                self._app.user_data.update_cache_property("tickers", tickers)
                self._try_delete_sector_of_interest(tickers, sectors)
                alert_label.configure(text=f"Successfully resigned interest for {self._ticker_code}!", text_color=consts.SUCCESS_MSG_COLOR)
            except Exception:
                alert_label.configure(text=f"ERROR: Failed to save!", text_color=consts.ERROR_MSG_COLOR)
        else:
            alert_label.configure(text=f"This stock is not registered for interest!", text_color=consts.ERROR_MSG_COLOR)

    def _get_shareholders_as_2d_list(self):
        res = reqs.get_ticker_shareholders(self._ticker_code, self._app.user_data.get_token())
        shareholders = res.json()["shareholders"]
        df = pd.DataFrame(shareholders)[["holder", "pctHeld", "value", "shares", "pctChange", "recency"]]
        return [list(df.columns)] + np.array(df).tolist()

    def _try_delete_sector_of_interest(self, tickers, sectors):
        found = False
        for ticker in tickers:
            sector = reqs.get_ticker_by_code(ticker, self._app.user_data.get_token()).json()["share"]["sector"]
            if sector in sectors and sector == self._sector:
                found = True
                break
        if not found:
            sectors.remove(self._sector)
            self._app.user_data.update_cache_property("sectors", sectors)

    def _on_shareholder_click(self, cell_data: dict):
        if cell_data["row"] == 0:
            return
        table = self._stock_view_product.get_widget("shareholder_table")
        row_values = table.get_row(cell_data["row"])

class AdminView(BaseView):
    def __init__(self, parent, app: App, row: int, col: int):
        super().__init__(app, row, col)
        self._parent = parent
        self._build()

    def _build(self):
        self._view_product = (CTkBuilder.frame(
            self._parent,
            self._row,
            self._col,
            "frame",
            8,
            2,
            sticky="nsew",
            row_minsizes=[75, 75, 75, 75, 75, 75, 20, 75],
            row_weights=[0 for _ in range(8)],
            col_minsizes=[400, 0],
            col_weights=[0, 1]
        )
        .label("admin_tools_label", "Admin Tools", Font.H1, 0, 0, pad=Padding(20, 0, 10, 20), sticky="w")
        .label("new_admin_label", "New Admin", Font.H2, 1, 0, pad=Padding(10, 0, 10, 20), sticky="w")
        .label("existing_users_label", "Existing Users", Font.H2, 1, 1, pad=Padding(10, 0, 10, 20), sticky="w")
        .entry("username_entry", "Username",Font.ENTRY_TEXT, 2,0, width=200, pad=Padding(5,0,5,20), sticky="w")
        .entry("password_entry", "Password", Font.ENTRY_TEXT, 3, 0, width=200, pad=Padding(5,0,5,20), sticky="w", show="*")
        .entry("email_entry", "Email", Font.ENTRY_TEXT, 4, 0, width=200, pad=Padding(5,0,5,20), sticky="w")
        .entry("name_entry", "Name", Font.ENTRY_TEXT, 5, 0, width=200, pad=Padding(5,0,5,20), sticky="w")
        .label("alert_label", "", Font.SUBTLE, 6, 0, sticky="ew", pad=Padding(0,0,0,20))
        .button("submit_button", "Submit", Font.BUTTON_TEXT, 7, 0, pad=Padding(5,0,20,20), sticky="w", command=self._exec_submit)
        .build())
        self._view_product.add("users_table_product", None)
        self._build_user_table()

    def _exec_submit(self):
        alert_label = self._view_product.get_widget("alert_label")
        username = self._view_product.get_widget("username_entry").get()
        password = self._view_product.get_widget("password_entry").get()
        email = self._view_product.get_widget("email_entry").get()
        name = self._view_product.get_widget("name_entry").get()
        if all([username, password, email, name]):
            status_code = reqs.register_user(username, password, email, name, "admin")
            if status_code == 201:
                alert_label.configure(
                    text=f"New administrator registered successfully!",
                    text_color=consts.SUCCESS_MSG_COLOR
                )
                self._build_user_table()
            else:
                alert_label.configure(
                    text=f"ERR_{status_code}: Unexpected error occurred!",
                    text_color=consts.ERROR_MSG_COLOR
                )
        else:
            alert_label.configure(
                text="Please provide all information!",
                text_color=consts.ERROR_MSG_COLOR
            )

    def _build_user_table(self):
        utb = self._view_product.get_widget("users_table_product")
        if utb:
            utb.container.destroy()
        data = self._get_users_as_2d_list()
        table_product = (CTkBuilder.frame(
            self._view_product,
            2,
            1,
            "scroll",
            1,
            1,
            sticky="new",
            pad=Padding(5, 20, 20, 20),
            rowspan=6
        )
        .table("users_table", len(data), len(data[0]), 0, 0, data, fontsize=Font.TEXT, anchor='w', corner_radius=0, sticky="nsew")
        .build())
        self._view_product.add("users_table_product", table_product)

    def _get_users_as_2d_list(self):
        res = reqs.get_all_users(self._app.user_data.get_token())
        if res.status_code == 200:
            users = res.json()["users"]
            df = pd.DataFrame(users)[["uid", "username", "name", "email", "role"]]
            return [list(df.columns)] + np.array(df).tolist()
        else:
            raise Exception(res.status_code)


class ProfileView(BaseView):
    def __init__(self, parent, app: App, row: int, col:int):
        super().__init__(app, row, col)
        self._parent = parent
        self._build()

    def _build(self):
        self._view_product = (CTkBuilder.frame(
            self._parent,
            self._row,
            self._col,
            "frame",
            5,
            2,
            sticky="nsew",
            row_minsizes=[75, 75, 75, 75, 75, 75],
            row_weights=[0, 0, 0, 0, 0, 0],
            col_minsizes=[400, 0],
            col_weights=[0, 1]
        )
        .label("profile_label", f"{self._app.user_data.get("name")}'s Profile", Font.H1, 0, 0, pad=Padding(20, 0, 10, 20), sticky="w")
        .label("username_label", f"Username: {self._app.user_data.get("username")}", Font.TEXT, 1, 0, pad=Padding(5, 0, 5, 20), sticky="w")
        .label("email_label", f"Email: {self._app.user_data.get("email")}", Font.TEXT, 2, 0, pad=Padding(5, 0, 5, 20), sticky="w")
        .label("stocks_label", f"Stocks of Interest: {self._app.user_data.get("tickers")}", Font.TEXT, 3, 0, pad=Padding(5, 0, 5, 20), sticky="w")
        .label("sectors_label", f"Sectors of Interest: {self._app.user_data.get("sectors")}", Font.TEXT, 4, 0, pad=Padding(5, 0, 5, 20), sticky="w")
        .build())


class ShareChartView(BaseView):
    def __init__(self, parent, app: App, row: int, col:int):
        super().__init__(app, row, col)
        self._parent = parent
        self._build()

    def _build(self):
        self._view_product = (CTkBuilder.frame(
            self._parent,
            self._row,
            self._col,
            "frame",
            1, 1,
            sticky="nsew",
            row_weights=[1],
            col_weights=[1],
            pad=Padding(0, 20, 0, 20),
        ).build())
        self._fig = Figure()
        self._ax = self._fig.add_subplot()
        self._fig.set_facecolor("none")
        self._ax.set_facecolor("none")
        self._canvas = FigureCanvasTkAgg(self._fig, master=self._view_product.container)
        fg = self._view_product.container.cget('fg_color')
        bg = fg[0] if customtkinter.get_appearance_mode() == 'Light' else fg[1]
        self._canvas.get_tk_widget().configure(bg=bg)
        self._canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def draw(self, data: dict, threshold: int):
        self._ax.clear()
        self._ax.set_facecolor("none")

        self._ax.axhline(y=threshold, color="red", linestyle="--", linewidth=1)
        for ticker, payload in data.items():
            dates = pd.to_datetime(payload["datetime"], utc=True).tz_convert(None)
            self._ax.plot(dates, payload["High"], label=ticker)

        self._ax.legend()
        locator = mdates.AutoDateLocator()
        self._ax.xaxis.set_major_locator(locator)
        self._ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
        self._ax.tick_params(axis='x', length=10, rotation=45)
        self._fig.tight_layout(pad=0)
        self._canvas.draw()


class BrokersView(BaseView):
    def __init__(self, parent, app: App, row: int, col:int):
        super().__init__(app, row, col)
        self._parent = parent
        self._build()

    def _build(self):
        self._view_product = (CTkBuilder.frame(
            self._parent,
            self._row,
            self._col,
            "frame",
            5, 1,
            sticky="nsew",
            pad=Padding(0, 50, 0, 50),
            row_minsizes=[50, 50, 0, 50, 300],
            row_weights=[0, 0, 1, 0, 0]
            # fg_color=None
        )
        .label("brokers_label", f"Brokers", consts.Font.H1, 0, 0, pad=Padding(20, 0, 20, 0), sticky="w")
        .label("recommendations_label", f"Recommended Brokers Based On Your Interests", consts.Font.H2, 1, 0, pad=Padding(5, 0, 5, 0), sticky="w")
        .label("brokers_table_label", f"Browse Other Brokers", consts.Font.H2, 3, 0, pad=Padding(5, 0, 5, 0), sticky="w")
        .build())
        self._build_recommendations()
        self._build_brokers_table()

    def _build_recommendations(self):
        brokers = reqs.get_brokers_by_domains(
            self._app.user_data.get("sectors"),
            self._app.user_data.get_token()
        ).json()["brokers"]
        self._recommendations_view_product = (CTkBuilder.frame(
            self._view_product,
            2, 0,
            "scroll",
            1, len(brokers),
            orientation="horizontal",
            sticky="nsew",
            row_minsizes=[300],
            row_weights=[0]
        ).build())

        for i in range(len(brokers)):
            recom_broker_product = (CTkBuilder.frame(
                self._recommendations_view_product,
                0, i,
                "frame",
                8, 1,
                sticky="nw",
                pad=Padding(10, 10, 10, 10),
            )
            .label("name_label", f"Name: {brokers[i]['name']}", Font.SUBTLE, 0, 0, sticky="w")
            .label("domain_label", f"Domain: {brokers[i]['domain']}", Font.SUBTLE, 1, 0, sticky="w")
            .label("trades_label", f"Trades Made: {brokers[i]['trading_record']:,}", Font.SUBTLE, 2, 0, sticky="w")
            .label("rating_label", f"Rating: {brokers[i]['rating']}", Font.SUBTLE, 3, 0, sticky="w")
            .label("pricing_label", f"Pricing: £{brokers[i]['price']}", Font.SUBTLE, 4, 0, sticky="w")
            .label("email_label", f"Email: {brokers[i]['email']}", Font.SUBTLE, 6, 0, sticky="w")
            .label("phone_label", f"Phone: {brokers[i]['phone']}", Font.SUBTLE, 7, 0, sticky="w")
            .build())
            self._recommendations_view_product.add(f"recom_broker{i+1}_product", recom_broker_product)


    def _build_brokers_table(self):
        data = self._get_brokers_as_2d_list("others")
        self._table = (CTkBuilder.frame(
            self._view_product,
            4, 0,
            "scroll",
            1, 1,
            sticky="nsew",
            pad=Padding(15, 0, 15, 0),
            fg_color="transparent"
        )
        .table("brokers_table", len(data), len(data[0]), 0, 0, data, fontsize=Font.TEXT, anchor="w", sticky="nsew", corner_radius=0)
        .build())

    def _get_brokers_as_2d_list(self, domain_or_others: Literal["domain", "others"]):
        res = reqs.get_all_brokers_except(self._app.user_data.get("sectors"), self._app.user_data.get_token())
        brokers = res.json()["brokers"]
        df = pd.DataFrame(brokers)[["name","domain","trading_record","rating","price","email","phone"]]
        df["phone"] = df["phone"].fillna("Not Provided")
        return [list(df.columns)] + np.array(df).tolist()


class NewsView(BaseView):
    def __init__(self, parent, app: App, row: int, col: int):
        BaseView.__init__(self, app, row, col)
        self._parent = parent
        self._build()

    def _build(self):
        news = reqs.get_ticker_news(self._app.user_data.get("tickers"), self._app.user_data.get_token()).json()["news"]
        self._view_product = (CTkBuilder.frame(
            self._parent,
            self._row,
            self._col,
            "scroll",
            len(news), 1,
            pad=Padding(20, 50, 20, 50),
            sticky="nsew"
        ).build())

        for i in range(len(news)):
            article_view_product = (CTkBuilder.frame(
                self._view_product,
                i, 0,
                "frame",
                5, 2,
                sticky="nsew",
                pad=Padding(20, 20, 20, 20),
                fg_color="transparent"
            )
            .label("ticker_label", f"{news[i]['ticker']}", Font.SUBTLE, 0, 0, sticky="w", italic=True)
            .label("date_label", f"Date Published: {news[i]['date']}", Font.SUBTLE, 0, 1, sticky="e", italic=True)
            .label("title_label", f"{news[i]['title']}", Font.H2, 1, 0, sticky="ew", colspan=2, bold=True, wraplength=800, justify="left")
            .label("summary_label", f"{news[i]['summary']}", Font.TEXT, 2, 0, sticky="ew", colspan=2, wraplength=800, justify="left")
            .label("url_label", f"Link To Article", Font.TEXT, 3, 0, sticky="w", cursor="hand2", text_color="blue", colspan=2, underline=True)
            .build())

            # Divider
            CTkFrame(article_view_product.container, height=2, fg_color="gray").grid(row=4,column=0,columnspan=2,sticky="ew")

            article_view_product.get_widget("url_label").bind("<Button-1>", lambda e, url=news[i]['url']: webbrowser.open(url))
            self._view_product.add(f"article{i+1}_product", article_view_product)
