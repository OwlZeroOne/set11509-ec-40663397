import customtkinter, cache

from views import *


class App:
    user_data = cache.CacheSingleton()

    def __init__(self):
        customtkinter.set_appearance_mode("light")
        self.user_data.load()

        self.main_window_product = self._build_main_window()
        self.tool_bar = self._build_tool_bar()

        if self.user_data.is_valid():
            self.current_view = LoggedInView(self, 1, 0)
        else:
            if self.user_data.get():
                reqs.update_user(self.user_data.get(), self.user_data.get_token())
                self.user_data.clear()
            self.current_view = LoginView(self, 1, 0)

        self.main_window_product.container.mainloop()

    @staticmethod
    def _build_main_window():
        window_width = 1200
        window_height = 700
        return CTkBuilder.window(
            "ShareTrader",
            True, True,
            2, 1,
            Size(window_width, window_height),
            row_minsizes=[50,0],
            row_weights=[0,1]
        ).build()

    @staticmethod
    def _theme_combo_triggered(theme: str):
        customtkinter.set_appearance_mode(theme.lower().split(" ")[0])

    def _build_tool_bar(self):
        return (CTkBuilder.frame(
            self.main_window_product,0, 0,
            "frame", 1, 2,
            col_weights=[1, 0],
            row_minsizes=[50],
            row_weights=[1],
            sticky="ew",
            corner_radius=0,
            fg_color="gray")
                .comboBox("theme_combo",["Light Mode", "Dark Mode"], "Light Mode", Font.COMBO_TEXT  , 0, 1, pad=Padding(0, 20, 0, 20), width=150, command=self._theme_combo_triggered)
                .build())

    def _new_view(self):
        if self.current_view:
            self.current_view.destroy()

    def trigger_logged_in_view(self):
        self._new_view()
        self.current_view = LoggedInView(self, 1, 0)

    def trigger_login_view(self):
        self._new_view()
        self.current_view = LoginView(self, 1, 0)


if __name__ == "__main__":
    App()