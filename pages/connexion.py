import datetime
from utils import *
from utils import backend as be

user_infos = {"nom": "", "acces": "", "poste": ""}


class Connexion(ft.View):
    def __init__(self, page):
        super(Connexion, self).__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, route="/", bgcolor="white",
            vertical_alignment=ft.MainAxisAlignment.CENTER, padding=0

        )
        self.page = page
        self.login = ft.TextField(
            **login_style, label="Login", prefix_icon=ft.icons.PERSON_OUTLINED, height=45,
        )
        self.password = ft.TextField(
            **login_style, label="Mot de passe", prefix_icon=ft.icons.KEY_OFF_OUTLINED, height=45,
            password=True, can_reveal_password=True
        )
        self.view_pass = ft.IconButton(
            ft.icons.LOCK_OUTLINE_ROUNDED, scale=0.7, icon_color="black", on_click=None
        )
        self.controls = [
            ft.Container(
                expand=True,
                content=ft.Stack(
                    controls=[
                    ft.Image(src="ecole.png", fit=ft.ImageFit.CONTAIN, opacity=0.2),
                    ft.Card(
                        elevation=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        show_border_on_foreground=False, surface_tint_color="white",
                        height=450,
                        content=ft.Container(
                            border_radius=12, width=290, bgcolor="white",
                            padding=ft.padding.only(40, 20, 40, 20),
                            content=ft.Column(
                                controls=[
                                    ft.Text("Connexion".upper(), size=20,
                                            font_family="Poppins ExtraBold"),
                                    ft.Image(src="SP Logo.png", width=80, height=80),
                                    ft.Divider(height=3, color="transparent"),
                                    ft.Column(
                                        controls=[
                                            self.login,
                                            self.password

                                        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.START
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.ElevatedButton(
                                                on_hover=self.bt_hover, **choix_style,
                                                on_click=self.valider, elevation=10
                                            ),
                                            ft.TextButton(
                                                content=ft.Text("Nouvel utlisateur ?", size=10,
                                                                font_family="Poppins Medium",
                                                                color=FIRST_COLOR),
                                                scale=ft.transform.Scale(1),
                                                animate_scale=ft.animation.Animation(300,
                                                                                     ft.AnimationCurve.SLOW_MIDDLE),
                                                on_hover=self.bt_hover,
                                                on_click=self.go_to_new_user
                                            )
                                        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                    )
                                ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ),
                    ),
                ], alignment=ft.alignment.center
                ),
            )
        ]

        self.box = ft.AlertDialog(
            # surface_tint_color="white", bgcolor="white",
            title=ft.Text("", size=16, font_family="Poppins Light"),
            content=ft.Text("", size=12, font_family="Poppins Medium"),
            actions=[
                ft.TextButton(
                    content=ft.Row(
                        [ft.Text("Quitter", size=12, font_family="Poppins Medium", color=FIRST_COLOR)],
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
            e.control.bgcolor = SECOND_COLOR
            e.control.update()

        else:
            e.control.scale = 1
            e.control.bgcolor = FIRST_COLOR
            e.control.update()

    def valider(self, e):
        if be.search_user_state(self.login.value) == "ACTIF":

            if be.user_exists(self.login.value, self.password.value):
                infos = be.search_user_infos(self.login.value)
                user_infos['nom'] = infos[0]
                user_infos['acces'] = infos[1]
                user_infos['poste'] = infos[2]
                last_day = be.find_last_date()

                if datetime.date.today() <= datetime.date(int(last_day[0:4]), int(last_day[5:7]), int(last_day[8::])):
                    self.page.go("/accueil")
                else:
                    self.page.go("/accueil")
                    # self.box.title.value = "Erreur"
                    # self.box.content.value = "La date de la démo est passée"
                    # self.box.open = True
                    # self.box.update()

            else:
                self.box.title.value = "Erreur"
                self.box.content.value = "Mot de passe incorrect"
                self.box.open = True
                self.box.update()

        elif be.search_user_state(self.login.value) == "INACTIF":
            self.box.title.value = "Erreur"
            self.box.content.value = "Compte inactif\nVeuillez contacter votre administrateur"
            self.box.open = True
            self.box.update()

        elif be.search_user_state(self.login.value) == "EN ATTENTE":
            self.box.title.value = "Erreur"
            self.box.content.value = "Ce compte utilisateur est en attente!\nCLiquez sur nouvel utilisateur afin de configurer votre mot de passe"
            self.box.open = True
            self.box.update()

        else:
            self.box.title.value = "Erreur"
            self.box.content.value = "Ce compte n'existe pas"
            self.box.open = True
            self.box.update()

    def close_box(self, e):
        self.box.open = False
        self.box.update()

    def go_to_new_user(self, e):
        self.page.go('/waiting user')

