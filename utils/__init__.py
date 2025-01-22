import flet as ft

FIRST_COLOR = "#264653"
SECOND_COLOR = "#2A9D8F"
THRID_COLOR = "#e9c46a"
FOURTH_COLOR = "#f4a261"
FIFTH_COLOR = "#E76F51"

field_style: dict = dict(
    dense=True,
    border_color="#f0f0f6", bgcolor="#f0f0f6",
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=13, font_family="Poppins Medium"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
    capitalization=ft.TextCapitalization.CHARACTERS
)
field_style_2: dict = dict(
    dense=True,
    focused_border_color=FIRST_COLOR,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=13, font_family="Poppins Medium"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
    focused_border_width=1,
    capitalization=ft.TextCapitalization.CHARACTERS
)
login_style: dict = dict(
    dense=True,
    focused_border_color=FIRST_COLOR,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=13, font_family="Poppins Medium"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
    focused_border_width=1,
)
inactive_field_style: dict = dict(
    dense=True, disabled=True,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    border_radius=12, border_width=1,
    capitalization=ft.TextCapitalization.CHARACTERS
)
underline_field_style: dict = dict(
    dense=True, read_only=True,
    border_color="#f0f0f6", bgcolor="#f0f0f6",
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=13, font_family="Poppins Medium"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
    capitalization=ft.TextCapitalization.CHARACTERS
)

date_field_style: dict = dict(
    height=45,
    focused_border_width=2, focused_border_color=FIRST_COLOR,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=13, font_family="Poppins Medium"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
    capitalization=ft.TextCapitalization.CHARACTERS
)

drop_style: dict = dict(
    dense=True, height=45, border_radius=12,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    focused_border_color=FIRST_COLOR, border_width=1,
    focused_border_width=2,
)

radio_style = dict(
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    fill_color=SECOND_COLOR
)
choix_style = dict(
    bgcolor=FIRST_COLOR,
    height=40,
    style=ft.ButtonStyle(
        shape=ft.ContinuousRectangleBorder(radius=16)
    ),
    scale=ft.transform.Scale(1),
    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
    content=ft.Row(
        controls=[
            ft.Icon(ft.icons.CHECK, size=20, color="white"),
            ft.Text("Valider", size=12, font_family="Poppins Medium", color="white")
        ], alignment=ft.MainAxisAlignment.CENTER
    )
)
bt_filtre_style = dict(
    bgcolor=FIRST_COLOR,
    height=40,
    style=ft.ButtonStyle(
        shape=ft.ContinuousRectangleBorder(radius=16)
    ),
    scale=ft.transform.Scale(1),
    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
    content=ft.Row(
        controls=[
            ft.Icon(ft.icons.FILTER_ALT_OUTLINED, size=20, color="white"),
            ft.Text("App. filtres", size=12, font_family="Poppins Medium", color="white")
        ], alignment=ft.MainAxisAlignment.CENTER
    )
)
bt_supp_style = dict(
    bgcolor=FIRST_COLOR,
    height=40,
    style=ft.ButtonStyle(
        shape=ft.ContinuousRectangleBorder(radius=16)
    ),
    scale=ft.transform.Scale(1),
    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
    content=ft.Row(
        controls=[
            ft.Icon(ft.icons.FILTER_ALT_OFF_OUTLINED, size=20, color="white"),
            ft.Text("Supp. filtres", size=12, font_family="Poppins Medium", color="white")
        ], alignment=ft.MainAxisAlignment.CENTER
    )
)

class AnyButton(ft.ElevatedButton):
    def __init__(self, theme_color:str, my_icon: str, title: str, text_color: str, click):
        super().__init__(
            bgcolor=theme_color,
            height=40, width=150, elevation=1,
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(radius=22)
            ),
            scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
            content=ft.Row(
                controls=[
                    ft.Icon(my_icon, color="white", size=16),
                    ft.Text(title, size=12, font_family="Poppins Medium", color=text_color)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8
            ),
            on_click=click, on_hover=self.hover_bt
        )

    def hover_bt(self, e):
        if e.data == "true":
            self.scale = 1.1
            self.update()
        else:
            self.scale = 1
            self.update()


text_title_style = dict(
    size=12, font_family="Poppins Italic", color="grey"
)
details_style = dict(
    # bgcolor="white",
    height=40,
    style=ft.ButtonStyle(
        shape=ft.ContinuousRectangleBorder(radius=16)
    ),
    scale=ft.transform.Scale(1),
    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
    content=ft.Row(
        controls=[
            # ft.Icon(ft.icons.FILTER_ALT_OFF, size=20),
            ft.Text("Détails", size=12, font_family="Poppins Medium")
        ], alignment=ft.MainAxisAlignment.CENTER
    )
)
red_style = dict(
    bgcolor="red",
    height=40,
    style=ft.ButtonStyle(
        shape=ft.ContinuousRectangleBorder(radius=16)
    ),
    scale=ft.transform.Scale(1),
    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
    content=ft.Row(
        controls=[
            ft.Icon(ft.icons.CHECK, size=20, color="white"),
            ft.Text("Confirmer", size=12, font_family="Poppins Medium", color="white")
        ], alignment=ft.MainAxisAlignment.CENTER
    )
)
terminer_style = dict(
    bgcolor="red",
    height=40,
    style=ft.ButtonStyle(
        shape=ft.ContinuousRectangleBorder(radius=16)
    ),
    scale=ft.transform.Scale(1),
    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
    content=ft.Row(
        controls=[
            ft.Icon(ft.icons.CHECK, size=20, color="white"),
            ft.Text("Terminer", size=12, font_family="Poppins Medium", color="white")
        ], alignment=ft.MainAxisAlignment.CENTER
    )
)
blue_style = dict(
    bgcolor=FIRST_COLOR,
    height=40,
    style=ft.ButtonStyle(
        shape=ft.ContinuousRectangleBorder(radius=16)
    ),
    scale=ft.transform.Scale(1),
    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
    content=ft.Row(
        controls=[
            ft.Icon(ft.icons.CLOSE, size=20, color="white"),
            ft.Text("Annuler", size=12, font_family="Poppins Medium", color="white")
        ], alignment=ft.MainAxisAlignment.CENTER
    )
)


class AnyContainerButton(ft.Container):
    def __init__(self, my_icon, my_tooltip: str, my_data, on_click_function, my_color: str):
        super().__init__(
            scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
            on_hover=self.icon_bt_hover,
            on_click=on_click_function,
            tooltip=my_tooltip, data=my_data,
            content=ft.Icon(
                my_icon, scale=1,
                color=my_color,
            )
        )

    def icon_bt_hover(self, e):
        if e.data == 'true':
            self.scale = 1.3
            self.content.update()
            self.update()
        else:
            self.scale = 1
            self.content.update()
            self.update()


