from utils import *
from utils import backend as be


class Users(ft.Container):
    def __init__(self, cp: object):
        super(Users, self).__init__(expand=True)
        self.cp = cp

        self.nom = ft.TextField(
            **field_style, prefix_icon="person_outlined", width=300, label="username",
            on_change=self.filter_datas
        )
        self.table = self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("")),
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("Accès")),
                ft.DataColumn(label=ft.Text("Login")),
                ft.DataColumn(label=ft.Text("Etat")),
                ft.DataColumn(label=ft.Text("Action")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )

        self.nb_users = ft.Text(size=24, font_family="Poppins Light", color="black")
        self.actifs = ft.Text(size=24, font_family="Poppins Light", color="black")
        self.inactifs = ft.Text(size=24, font_family="Poppins Light", color="black")
        self.attente = ft.Text(size=24, font_family="Poppins Light", color="black")

        self.main_window = ft.Container(
            padding=ft.padding.only(20, 0, 20, 0), expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        padding=ft.padding.only(30, 15, 30, 15), border_radius=12,  # bgcolor="white",
                        content=ft.Column(
                            controls=[
                                ft.Text("Chiffres", size=13, font_family="Poppins Bold", color="black"),
                                ft.Divider(height=1, thickness=1),
                                ft.Row(
                                    controls=[
                                        ft.Column(
                                            [
                                                ft.Text("Total utilisateurs", size=11,
                                                        font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.MANAGE_ACCOUNTS_OUTLINED, size=20,
                                                                color="black87"),

                                                        self.nb_users
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("Comptes actifs", size=11,
                                                        font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.PERSON_OUTLINE_OUTLINED, size=20,
                                                                color="black87"),
                                                        self.actifs
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("Comptes inactifs", size=12,
                                                        font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.PERSON_OFF_OUTLINED, size=20,
                                                                color="black87"),
                                                        self.inactifs
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("Comptes en attente", size=11,
                                                        font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.WATCH_OFF_OUTLINED, size=20,
                                                                color="black87"),
                                                        self.attente
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                    ], spacing=70, vertical_alignment=ft.CrossAxisAlignment.START
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        padding=ft.padding.only(30, 15, 30, 15), bgcolor="white", border_radius=12, expand=True,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("Utilisateurs", size=14, font_family="Poppins Bold"),
                                        AnyButton(
                                            FIRST_COLOR, ft.icons.PERSON_ADD_OUTLINED, "utilisateur + ", "white",
                                            self.open_new_user_window
                                        ),
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                self.nom,
                                ft.ListView(
                                    expand=True,
                                    controls=[self.table]
                                )
                            ]
                        )
                    )
                ]
            )
        )

        # New user window
        self.user_name = ft.TextField(
            **field_style_2, prefix_icon="person_outlined", label="Nom utilisteur", width=300,
            on_change=self.changement_nom
        )
        self.poste = ft.Dropdown(
            **drop_style, width=170, prefix_icon=ft.icons.SCHOOL, label="poste", on_change=self.post_change
        )
        self.acces = ft.TextField(
            **underline_field_style, width=170, prefix_icon=ft.icons.PRIVACY_TIP_OUTLINED, label="Niveau accès"
        )
        self.login = ft.TextField(
            **underline_field_style, width=300, prefix_icon=ft.icons.SWITCH_ACCOUNT_OUTLINED, label="login"
        )
        self.etat = ft.TextField(
            **underline_field_style, width=170, prefix_icon=ft.icons.CODE_OUTLINED, label="Etat"
        )
        self.new_user_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=400, height=510,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                bgcolor="#f0f0f6", padding=20,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=10, border_radius=12, bgcolor="white",
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Icon(ft.icons.SWITCH_ACCOUNT, color=FIRST_COLOR),
                                            ft.Text("Nouvel utilisateur".upper(), size=14, font_family="Poppins Medium")
                                        ]
                                    ),
                                    ft.IconButton(
                                        "close", scale=0.7, bgcolor="#f0f0f6", icon_color=FIRST_COLOR,
                                        on_click=self.close_new_user_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white",
                            content=ft.Column(
                                controls=[
                                    self.user_name, self.poste, self.acces, self.login, self.etat,
                                    AnyButton(
                                        FIRST_COLOR, ft.icons.CHECK, "Valider", "white",
                                        self.creer_user
                                    ),
                                ], spacing=20
                            )
                        )
                    ]
                )
            )
        )

        # fenetre modifier
        self.m_user_id = ft.TextField(
            **underline_field_style, prefix_icon="person_outlined", label="Nom utilisteur", width=300,
            visible=False
        )
        self.m_user = ft.TextField(
            **underline_field_style, prefix_icon="person_outlined", label="Nom utilisteur", width=300,
        )
        self.m_etat = ft.Dropdown(
            **drop_style, label="Etat", width=170, prefix_icon=ft.icons.CODE_OUTLINED,
            options=[
                ft.dropdown.Option("ACTIF"),
                ft.dropdown.Option("INACTIF"),
            ]
        )
        self.modif_user_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=400, height=330,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                bgcolor="#f0f0f6", padding=20,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=10, border_radius=12, bgcolor="white",
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Icon(ft.icons.EDIT, color=FIRST_COLOR),
                                            ft.Text("Modifier utilisateur", size=14, font_family="Poppins Medium")
                                        ]
                                    ),
                                    ft.IconButton(
                                        "close", scale=0.7, bgcolor="#f0f0f6", icon_color=FIRST_COLOR,
                                        on_click=self.close_modif_user_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white",
                            content=ft.Column(
                                controls=[
                                    self.m_user_id, self.m_user, self.m_etat,
                                    AnyButton(
                                        FIRST_COLOR, ft.icons.CHECK, "Valider", "white",
                                        self.modifier_user
                                    ),
                                ], spacing=20
                            )
                        )
                    ]
                )
            )
        )

        self.content = ft.Stack(
            controls=[
                self.main_window, self.new_user_window, self.modif_user_window
            ], alignment=ft.alignment.center
        )
        self.load_datas()
        self.load_lists()

    @staticmethod
    def icon_bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.4
            e.control.content.update()
            e.control.update()
        else:
            e.control.scale = 1
            e.control.content.update()
            e.control.update()

    def load_lists(self):
        postes = be.all_postes()
        for poste in postes:
            self.poste.options.append(
                ft.dropdown.Option(poste)
            )

    def post_change(self, e):
        self.acces.value = be.acces_by_poste(self.poste.value)
        self.acces.update()
        self.etat.value = "EN ATTENTE"
        self.etat.update()

    @staticmethod
    def icon_bt_hover_red(e):
        if e.data == 'true':
            e.control.bgcolor = "#FFDDDD"
            e.control.update()
        else:
            e.control.bgcolor = "white"
            e.control.update()

    def load_datas(self):
        datas = be.all_users()
        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        all_datas = []
        for data in datas:
            all_datas.append(
                {
                    "nom": data[1], "poste": data[2], "acces": data[3], "login": data[4], "password": data[5],
                    "etat": data[6], "id": data[0]
                }
            )

        actifs = 0
        inactifs = 0
        attente = 0
        total = 0

        for user_data in all_datas:
            if user_data['etat'] == "EN ATTENTE":
                color = "teal"
                icone = ft.icons.NEW_LABEL_OUTLINED
                attente += 1

            elif user_data['etat'] == "ACTIF":
                color = None
                icone = None
                actifs += 1
            else:
                color = None
                icone = None
                inactifs += 1

            total += 1

            if user_data['acces'] == "administrateur".upper():
                icone_acces = ft.icons.PRIVACY_TIP_OUTLINED
                color_acces = "red"
            else:
                icone_acces = None
                color_acces = None

            self.table.rows.append(
                ft.DataRow(
                    data=user_data,
                    cells=[
                        ft.DataCell(
                            ft.Icon(
                                icone, color=color, size=16
                            )
                        ),
                        ft.DataCell(ft.Text(user_data['nom'])),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.Icon(icone_acces, size=16, color=color_acces),
                                    ft.Text(user_data['acces'].upper())
                                ]
                            )
                        ),
                        ft.DataCell(ft.Text(user_data['login'])),
                        ft.DataCell(ft.Text(user_data['etat'])),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        scale=ft.transform.Scale(1),
                                        animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                        on_hover=self.icon_bt_hover2,
                                        content=ft.IconButton(
                                            ft.icons.EDIT_OUTLINED, scale=1,
                                            icon_color=FOURTH_COLOR,
                                            on_click=self.open_modif_user_window, data=user_data,
                                            tooltip="Supprimer filtres",
                                        )
                                    ),
                                    ft.Container(
                                        scale=ft.transform.Scale(1),
                                        animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                        on_hover=self.icon_bt_hover2,
                                        content=ft.IconButton(
                                            ft.icons.DELETE_OUTLINED, scale=1,
                                            icon_color=FIFTH_COLOR,
                                            on_click=self.supprimer_user, data=user_data,
                                            tooltip="Supprimer filtres",
                                        )
                                    ),
                                ], spacing=0
                            )
                        )
                    ]
                )
            )

        self.nb_users.value = total
        self.actifs.value = actifs
        self.inactifs.value = inactifs
        self.attente.value = attente

    def filter_datas(self, e):
        datas = be.all_users()
        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        all_datas = []
        for data in datas:
            all_datas.append(
                {
                    "nom": data[1], "poste": data[2], "acces": data[3], "login": data[4], "password": data[5],
                    "etat": data[6], "id": data[0]
                }
            )

        filter_datas = list(filter(lambda x: self.nom.value in x['nom'], all_datas))

        for user_data in filter_datas:
            if user_data['etat'] == "EN ATTENTE":
                color = "teal"
                icone = ft.icons.NEW_LABEL_OUTLINED
            else:
                color = None
                icone = None

            if user_data['acces'] == "administrateur".upper():
                icone_acces = ft.icons.PRIVACY_TIP_OUTLINED
                color_acces = "red"
            else:
                icone_acces = None
                color_acces = None

            self.table.rows.append(
                ft.DataRow(
                    data=user_data,
                    cells=[
                        ft.DataCell(
                            ft.Icon(
                                icone, color=color, size=16
                            )
                        ),
                        ft.DataCell(ft.Text(user_data['nom'])),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.Icon(icone_acces, size=16, color=color_acces),
                                    ft.Text(user_data['acces'].upper())
                                ]
                            )
                        ),
                        ft.DataCell(ft.Text(user_data['login'])),
                        ft.DataCell(ft.Text(user_data['etat'])),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        scale=ft.transform.Scale(1),
                                        animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                        on_hover=self.icon_bt_hover,
                                        content=ft.IconButton(
                                            ft.icons.EDIT, scale=1,
                                            icon_color="#144bb3",
                                            on_click=self.open_modif_user_window,
                                            tooltip="Modifier", data=user_data
                                        )
                                    ),
                                    ft.Container(
                                        scale=ft.transform.Scale(1),
                                        animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                        on_hover=self.icon_bt_hover,
                                        content=ft.IconButton(
                                            ft.icons.DELETE, scale=1,
                                            icon_color="red",
                                            on_click=self.supprimer_user,
                                            tooltip="Supprimer", data=user_data
                                        )
                                    )
                                ], spacing=0
                            )
                        )
                    ]
                )
            )

        self.table.update()

    def open_new_user_window(self, e):
        self.new_user_window.scale = 1
        self.new_user_window.update()

    def close_new_user_window(self, e):
        self.new_user_window.scale = 0
        self.new_user_window.update()

    def changement_nom(self, e):
        if " " in self.user_name.value:
            nom = self.user_name.value
            names = nom.split(" ")
            user_name = names[0]
            user_surname = names[1]
            self.login.value = f"{user_name.lower()}.{user_surname.lower()[0:2]}"
            self.login.update()

    def creer_user(self, e):
        count = 0
        for widget in (self.user_name, self.poste):
            if widget.value is None or widget.value == "":
                count += 1

        if count == 0:
            be.add_user(self.user_name.value, self.poste.value, self.acces.value, self.login.value)

            self.cp.box.title.value = "Validé !"
            self.cp.box.content.value = "Nouvel utlisateur créé"
            self.cp.box.open = True
            self.cp.box.update()

            for widget in (self.user_name, self.poste, self.acces, self.login, self.etat):
                widget.value = None
                widget.update()

            self.load_datas()
            self.table.update()
            self.nb_users.update()
            self.actifs.update()
            self.inactifs.update()
            self.attente.update()

        else:
            self.cp.box.title.value = "Erreur !"
            self.cp.box.content.value = "Tous les champs sont obligatoires"
            self.cp.box.open = True
            self.cp.box.update()

    def supprimer_user(self, e):
        be.delete_user(e.control.data['id'])
        self.load_datas()
        self.table.update()
        self.nb_users.update()
        self.actifs.update()
        self.inactifs.update()
        self.attente.update()

        self.load_datas()
        self.table.update()

        self.cp.box.title.value = "Validé !"
        self.cp.box.content.value = "Utilisateur supprimé"
        self.cp.box.open = True
        self.cp.box.update()

    def open_modif_user_window(self, e):
        self.m_user_id.value = e.control.data['id']
        self.m_user.value = e.control.data['nom']
        self.m_etat.value = e.control.data['etat']
        self.m_etat.update()
        self.m_user.update()
        self.m_user_id.update()
        self.modif_user_window.scale = 1
        self.modif_user_window.update()

    def close_modif_user_window(self, e):
        self.modif_user_window.scale = 0
        self.modif_user_window.update()

    def modifier_user(self, e):
        be.update_user(self.m_etat.value, self.m_user_id.value)
        self.modif_user_window.scale = 0
        self.modif_user_window.update()
        self.cp.box.title.value = "Validé !"
        self.cp.box.content.value = "Utilisateur modifié"

        self.load_datas()
        self.table.update()

        self.cp.box.open = True
        self.cp.box.update()
        self.nb_users.update()
        self.actifs.update()
        self.inactifs.update()
        self.attente.update()

    @staticmethod
    def bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.1
            e.control.update()
        else:
            e.control.scale = 1
            e.control.update()

    @staticmethod
    def icon_bt_hover2(e):
        if e.data == 'true':
            e.control.scale = 1.2
            e.control.update()
        else:
            e.control.scale = 1
            e.control.update()
