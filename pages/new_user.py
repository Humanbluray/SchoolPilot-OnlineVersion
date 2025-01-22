from utils import *
from utils import backend as be
import time


class NewUser(ft.View):
    def __init__(self, page):
        super(NewUser, self).__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, route='/waiting user',
            vertical_alignment=ft.MainAxisAlignment.CENTER

        )
        self.page = page
        self.login = ft.TextField(
            **field_style_2, label="Login", prefix_icon=ft.icons.PERSON_OUTLINED, height=45,
        )
        self.password = ft.TextField(
            **field_style_2, label="Mot de passe", prefix_icon=ft.icons.KEY_OFF_OUTLINED, height=45,
            password=True, can_reveal_password=True
        )
        self.confirm_pass = ft.TextField(
            **field_style_2, label="Confirmation", prefix_icon=ft.icons.KEY_OFF_OUTLINED, height=45,
            password=True, can_reveal_password=True, on_change=self.on_change_confirm
        )

        self.controls = [
            ft.Container(
                expand=True,
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Card(
                                elevation=10, show_border_on_foreground=False, height=450,
                                content=ft.Container(
                                    border_radius=12, width=290,
                                    padding=ft.padding.only(40, 20, 40, 20),
                                    content=ft.Column(
                                        controls=[
                                            ft.Text("Nouvel Utilisateur".upper(), size=20, font_family="Poppins ExtraBold"),
                                            ft.Divider(height=1, color="transparent"),
                                            ft.Column(
                                                controls=[
                                                    self.login,
                                                    self.password,
                                                    self.confirm_pass

                                                ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.START
                                            ),
                                            ft.Column(
                                                controls=[
                                                    ft.ElevatedButton(
                                                        on_hover=self.bt_hover, **choix_style,
                                                        on_click=self.valider, elevation=10,
                                                    ),
                                                    ft.TextButton(
                                                        content=ft.Text("Retour page de connexion", size=10, font_family="Poppins Medium",
                                                                        color=first_color),
                                                        scale=ft.transform.Scale(1),
                                                        animate_scale=ft.animation.Animation(300, ft.AnimationCurve.SLOW_MIDDLE),
                                                        on_hover=self.bt_hover,
                                                        on_click=self.go_back
                                                    )
                                                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                            )
                                        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        alignment=ft.MainAxisAlignment.CENTER
                                    )
                                )
                            )
                        ),
                        ft.Container(
                            margin=20,
                            content=ft.Row(
                                [
                                    ft.Image(src="ecole.jpg", width=400, height=400)
                                ], alignment=ft.MainAxisAlignment.CENTER
                            )
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND
                )
            )
        ]
        self.box = ft.AlertDialog(
            # surface_tint_color="white", bgcolor="white",
            title=ft.Text("", size=16, font_family="Poppins Light"),
            content=ft.Text("", size=12, font_family="Poppins Medium"),
            actions=[
                ft.TextButton(
                    content=ft.Row(
                        [ft.Text("Quitter", size=12, font_family="Poppins Medium", color=first_color)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ), width=120,
                    on_click=self.close_box
                )
            ]
        )
        self.page.overlay.append(self.box)

    @staticmethod
    def bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.1
            e.control.update()
        else:
            e.control.scale = 1
            e.control.update()

    def valider(self, e):
        if be.search_user_infos(self.login.value) is not None:
            if self.password.value is not None or self.password.value != "":
                if self.password.value == self.confirm_pass.value:
                    be.update_user("ACTIF", be.search_user_infos(self.login.value)[3])
                    be.update_password_new(
                        self.password.value, be.search_user_infos(self.login.value)[3]
                    )
                    for widget in (self.login, self.password, self.confirm_pass):
                        widget.value = None
                        widget.update()

                    self.box.title.value = "Validé"
                    self.box.content.value = "Votre compte est désormais actif"
                    self.box.open = True
                    self.box.update()
                    time.sleep(3)
                    self.page.go('/')
            else:
                self.box.title.value = "erreur"
                self.box.content.value = "Les 2 mots de passe ne sont pas identiques"
                self.box.open = True
                self.box.update()

        else:
            self.box.title.value = "erreur"
            self.box.content.value = "Le login n'existe pas"
            self.box.open = True
            self.box.update()

    def on_change_confirm(self, e):
        if self.password.value is not None or self.password.value != "":
            if self.password.value == self.confirm_pass.value:
                self.password.border_color = "green300"
                self.confirm_pass.border_color = "green300"
                self.password.update()
                self.confirm_pass.update()
            else:
                self.password.border_color = None
                self.confirm_pass.border_color = None
                self.password.update()
                self.confirm_pass.update()
        else:
            self.password.border_color = None
            self.confirm_pass.border_color = None
            self.password.update()
            self.confirm_pass.update()

    def close_box(self, e):
        self.box.open = False
        self.box.update()

    def go_back(self, e):
        self.page.go('/')

