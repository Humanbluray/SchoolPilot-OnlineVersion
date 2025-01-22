from utils import *
from utils import backend as be


class Affectation(ft.Container):
    def __init__(self, cp: object, prof: str, classe: str, matiere: str, nb_heures: int, jour: str, creneau: str):
        super(Affectation, self).__init__(
            border_radius=8, bgcolor="white", border=ft.border.all(1, "#ebebeb"),
            width=100, height=100, padding=10
        )
        self.cp = cp
        self.prof = prof
        self.classe = classe
        self.matiere = matiere
        self.jour = jour
        self.creneau = creneau
        self.nb_heures = nb_heures

        if self.matiere != "" or self.matiere is None:
            icone = ft.icons.DO_NOT_DISTURB_ON
            couleur = "red"
        else:
            icone = ft.icons.CHECK_BOX
            couleur = "lightgreen"

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icone, color=couleur, size=16),
                        ft.Text(self.jour, size=12, font_family="Poppins Medium")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.icons.WATCH_LATER_OUTLINED, size=16, color="black"),
                                ft.Text(self.creneau, size=12, font_family="Poppins Medium")
                            ], spacing=1
                        ),
                        ft.Text(self.matiere, size=11, font_family="Poppins Regular"),
                        ft.Text(self.prof, size=10, font_family="Poppins Regular")
                    ]
                )
            ]
        )

    @staticmethod
    def icon_bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.2
            e.control.update()
        else:
            e.control.scale = 1
            e.control.update()


class Classes(ft.Container):
    def __init__(self, cp: object):
        super(Classes, self).__init__(
            expand=True
        )
        self.cp = cp
        self.level = ft.Dropdown(
            **drop_style, prefix_icon=ft.icons.CANDLESTICK_CHART_SHARP, width=170, label="Niveau", on_change=self.filter_datas
        )

        self.nb_classes = ft.Text(size=24, font_family="Poppins Light", color="black87")
        self.tdr_global = ft.Text(size=24, font_family="Poppins Light", color="black87")
        self.cap_global = ft.Text(size=24, font_family="Poppins Light", color="black87")
        self.effectif_global = ft.Text(size=24, font_family="Poppins Light", color="black87")

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Statut")),
                ft.DataColumn(label=ft.Text("Code")),
                ft.DataColumn(label=ft.Text("Niveau")),
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("effectif")),
                ft.DataColumn(label=ft.Text("capacité")),
                ft.DataColumn(label=ft.Text("Actions")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )
        self.table_details = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Ann sco.")),
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("Matricule")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )

        self.main_window = ft.Container(
            padding=ft.padding.only(20, 0, 20, 0), expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        padding=ft.padding.only(30, 15, 30, 15), border_radius=12,  # bgcolor="white",
                        content=ft.Column(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text("Chiffres".upper(), size=13, font_family="Poppins Medium",
                                                color="black", weight=ft.FontWeight.BOLD),
                                        ft.Divider(height=1, thickness=1),
                                    ], spacing=0
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Column(
                                            [
                                                ft.Text("Nb classes".upper(), size=11, font_family="Poppins Italic",color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.ACCOUNT_BALANCE_OUTLINED, size=20,
                                                                color="black87"),
                                                        self.nb_classes
                                                    ]
                                                ),

                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("Capacité Globale".upper(), size=12,
                                                        font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.HOURGLASS_EMPTY_SHARP, size=20,
                                                                color="black87"),
                                                        self.cap_global
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("Effectif Total".upper(), size=11, font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.GROUP_OUTLINED, size=20,
                                                                color="black87"),
                                                        self.effectif_global
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("TDR global".upper(), size=11,
                                                        font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.PERCENT_OUTLINED, size=20,
                                                                color="black87"),
                                                        self.tdr_global
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
                                ft.Text("Classes".upper(), size=13, font_family="Poppins Medium", weight=ft.FontWeight.BOLD),
                                ft.Row(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                self.level,
                                                ft.Container(
                                                    border=ft.border.all(1, "grey"),
                                                    border_radius=6, bgcolor="#f0f0f6", padding=5,
                                                    on_click=self.supp_filtres,
                                                    scale=ft.transform.Scale(1),
                                                    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                                    on_hover=self.icon_bt_hover2,
                                                    tooltip="Supprimer filtres",
                                                    content=ft.Icon(
                                                        ft.icons.FILTER_ALT_OFF_OUTLINED,
                                                        color=ft.colors.BLACK45,
                                                    )
                                                ),
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Row(
                                                    controls=[
                                                        AnyButton(
                                                            FIRST_COLOR, ft.icons.ADD_HOME_OUTLINED, "Classe + ", "white", self.open_new_class_window
                                                        ),
                                                        AnyButton(
                                                            SECOND_COLOR, ft.icons.ADDCHART_OUTLINED, "Niveau +", "white", self.open_new_palier_window
                                                        ),
                                                        AnyButton(
                                                            THRID_COLOR, ft.icons.LIBRARY_ADD_OUTLINED, "Matieres +", "white", None
                                                        ),
                                                    ], spacing=8
                                                )
                                            ]
                                        )

                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.ListView(
                                    expand=True,
                                    controls=[self.table]
                                )
                            ], spacing=15
                        )
                    ),
                ], spacing=15
            )
        )

        # fenetre des details dde la classe
        self.palier = ft.Dropdown(
            **drop_style, width=185, label="palier", prefix_icon=ft.icons.DISCOUNT_OUTLINED,
        )
        self.nom_long = ft.TextField(
            **field_style_2, width=300, label="Nom classe", prefix_icon=ft.icons.LABEL_IMPORTANT_OUTLINE_ROUNDED
        )
        self.nom_classe = ft.TextField(
            **field_style_2, width=170, label="classe", prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED
        )
        self.capacite = ft.TextField(**field_style_2, width=120, label="Capacité", text_align=ft.TextAlign.RIGHT)

        self.section = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(**radio_style, label="francophone", value="francophone"),
                    ft.Radio(**radio_style, label="anglophone", value="anglophone"),
                ]
            )
        )
        self.cycle = ft.Dropdown(
            **drop_style, width=185, label="Cycle", prefix_icon=ft.icons.LANGUAGE_OUTLINED,
            options=[
                ft.dropdown.Option('premier'),
                ft.dropdown.Option('second'),
            ], on_change=self.on_change_cycle
        )
        self.pb_class = ft.ProgressBar(
            bgcolor="grey", color=SECOND_COLOR, bar_height=8, border_radius=12, value=0
        )
        self.new_class_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=410, height=630,
            variant=ft.CardVariant.ELEVATED,
            clip_behavior=ft.ClipBehavior.HARD_EDGE, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                expand=True, bgcolor="#f0f0f6",
                padding=15,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(20, 10, 20, 10), border_radius=12, bgcolor="white",
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.ACCOUNT_BALANCE_OUTLINED, color=SECOND_COLOR),
                                            ft.Text("Ajouter Classe".upper(), size=14, font_family="Poppins Medium")
                                        ]
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, scale=0.7, bgcolor="#f0f0f6", icon_color="black87",
                                        on_click=self.close_new_class_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white", width=380,
                            content=ft.Column(
                                controls=[
                                    self.section,
                                    ft.Divider(height=1, thickness=1),
                                    self.cycle,
                                    self.palier,
                                    ft.Divider(height=1, thickness=1),
                                    self.nom_classe, self.nom_long, self.capacite,
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style, width=150, on_click=self.nouvelle_classe,
                                    ),
                                    self.pb_class
                                ],spacing=20
                            )
                        )
                    ]
                )
            )
        )

        # fenetre ajout palier
        self.section_2 = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(**radio_style, label="francophone", value="francophone"),
                    ft.Radio(**radio_style, label="anglophone", value="anglophone"),
                ]
            )
        )
        self.cycle_2 = ft.Dropdown(
            **drop_style, width=185, label="Cycle", prefix_icon=ft.icons.LANGUAGE_OUTLINED,
            options=[
                ft.dropdown.Option('premier'),
                ft.dropdown.Option('second'),
            ]
        )
        self.nom_palier = ft.TextField(
            **field_style_2, width=170, label="Code", prefix_icon=ft.icons.DISCOUNT_OUTLINED
        )
        self.palier_long = ft.TextField(
            **field_style_2, width=300, label="Nom palier", prefix_icon=ft.icons.LABEL_OUTLINE_ROUNDED
        )
        self.new_palier_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=410, height=460,
            variant=ft.CardVariant.ELEVATED,
            clip_behavior=ft.ClipBehavior.HARD_EDGE, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                expand=True, bgcolor="#f0f0f6",
                padding=15,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(20, 10, 20, 10), border_radius=12, bgcolor="white",
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.ACCOUNT_BALANCE_OUTLINED, color=SECOND_COLOR),
                                            ft.Text("Ajouter Palier".upper(), size=14, font_family="Poppins Medium")
                                        ]
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, scale=0.7, bgcolor="#f0f0f6", icon_color="black87",
                                        on_click=self.close_new_palier_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white", width=380,
                            content=ft.Column(
                                controls=[
                                    self.section_2,
                                    self.cycle_2,
                                    ft.Divider(height=1, thickness=1),
                                    self.nom_palier, self.palier_long,
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style, width=150,
                                        on_click=self.nouveau_palier,
                                    ),
                                ], spacing=20
                            )
                        )
                    ]
                )
            )
        )

        # affecations de la classe
        self.table_affec = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Statut")),
                ft.DataColumn(label=ft.Text("professeur")),
                ft.DataColumn(label=ft.Text("Matière")),
                ft.DataColumn(label=ft.Text("Jour")),
                ft.DataColumn(label=ft.Text("Créneau")),
                ft.DataColumn(label=ft.Text("Modifier")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )
        self.title_affec = ft.Text("", size=13, font_family="Poppins Bold", color="black")
        self.titus_affec = ft.Text(size=12, font_family="Poppins Medium", color=FIRST_COLOR)
        self.affec_eff = ft.Text("", size=13, font_family="Poppins Light", color=SECOND_COLOR)
        self.search_affec = ft.Dropdown(
            **drop_style, label="Jour", width=150, prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED,
            options=[
                ft.dropdown.Option("LUNDI"), ft.dropdown.Option("MARDI"), ft.dropdown.Option("MERCREDI"),
                ft.dropdown.Option("JEUDI"), ft.dropdown.Option("VENDREDI"),
            ],
            on_change=self.filtre_affectations
        )
        self.affec_capacite = ft.Text("", size=13, font_family="Poppins Light", color=FIRST_COLOR)
        self.affec_tdr = ft.Text("", size=13, font_family="Poppins Light", color="deeppurple")
        self.details_affec = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=900, height=600,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN),
            content=ft.Container(
                expand=True, bgcolor="#f0f0f6",
                padding=20,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(10, 5, 10, 5), bgcolor="white", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.ACCOUNT_BALANCE_OUTLINED, color=SECOND_COLOR),
                                            self.title_affec,
                                        ]
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, scale=0.7, bgcolor="#f0f0f6",
                                        icon_color="#292f4c",
                                        on_click=self.close_details_affec
                                    ),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, bgcolor="white", border_radius=12, expand=True,
                            content=ft.Column(
                                expand=True,
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text("Affectations".upper(), size=13, font_family="Poppins Medium", weight=ft.FontWeight.BOLD),
                                            AnyButton(SECOND_COLOR, ft.icons.PERSON_ADD_OUTLINED, "Titulaire +", "white", self.open_window_titus)
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.Row(
                                        [
                                            ft.Row(
                                                controls=[
                                                    self.search_affec,
                                                    ft.Container(
                                                        border=ft.border.all(1, "grey"),
                                                        border_radius=8, bgcolor="#f0f0f6", padding=5,
                                                        scale=ft.transform.Scale(1),
                                                        animate_scale=ft.animation.Animation(300,ft.AnimationCurve.FAST_OUT_SLOWIN),
                                                        on_hover=self.icon_bt_hover2, on_click=self.supp_filtres_affec,
                                                        tooltip="Supprimer filtres",
                                                        content=ft.Icon(
                                                            ft.icons.FILTER_ALT_OFF_OUTLINED,
                                                            color=ft.colors.BLACK45,
                                                        )
                                                    ),
                                                ]
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Text("Titulaire", size=11, font_family="Poppins Italic",
                                                            color="grey"),
                                                    self.titus_affec
                                                ], spacing=50
                                            ),

                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.ListView(
                                        expand=True,
                                        controls=[self.table_affec]
                                    )
                                ]
                            )
                        )
                    ], spacing=10
                )
            )
        )

        # Ecran update affectation
        self.m_classe = ft.TextField(
            **underline_field_style, width=170, prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, label="Classe"
        )
        self.m_niveau = ft.Text("", visible=False)
        self.m_matiere = ft.Dropdown(
            **drop_style, width=300, prefix_icon=ft.icons.BOOK_OUTLINED, label="matiere"
        )
        self.m_prof = ft.Dropdown(
            **drop_style, width=300, prefix_icon=ft.icons.PERSON_OUTLINED, label="Professeur"
        )
        self.m_creneau = ft.TextField(
            **underline_field_style, width=150, prefix_icon=ft.icons.WATCH_LATER_OUTLINED, label="Classe"
        )
        self.m_jour = ft.TextField(
            **underline_field_style, width=150, prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED, label="Classe"
        )
        self.modif_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=390, height=520,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN),
            content=ft.Container(
                expand=True, bgcolor="#f0f0f6",
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=10, bgcolor="white", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Icon(ft.icons.WATCH_LATER, size=24, color=SECOND_COLOR),
                                            ft.Text("Modifier affectation".upper(), size=14, font_family="POppins Medium"),
                                        ]
                                    ),
                                    ft.IconButton(
                                        "close", scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                        on_click=self.close_modif_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, bgcolor="white", border_radius=12,
                            content=ft.Column(
                                controls=[
                                    self.m_classe, self.m_jour, self.m_creneau,
                                    self.m_niveau, self.m_matiere, self.m_prof,
                                    ft.ElevatedButton(
                                        **choix_style, width=150,
                                        on_click=self.valider_modif_affec, on_hover=self.bt_hover
                                    )
                                ], spacing=20
                            )
                        )
                    ]
                )
            )
        )

        # affecter titus
        self.t_prof = ft.Dropdown(
            **drop_style, label="Professeur titulaire", width=350, prefix_icon="person_outlined",
        )
        self.t_classe = ft.TextField(
            **underline_field_style, label="Classe", width=150,
            prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED
        )
        self.window_titus = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=400, height=380,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20, bgcolor="#f0f0f6",
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=10, bgcolor="white", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Text('Titulariser', size=14, font_family="Poppins Medium"),
                                    ft.IconButton(
                                        ft.icons.CLOSE, scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                        on_click=self.close_window_titus
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, bgcolor="white", border_radius=12,
                            content=ft.Column(
                                controls=[
                                    ft.TextField(
                                        **underline_field_style, label="Asco", value=be.show_asco_encours(),
                                        width=100, prefix_icon=ft.icons.EDIT_CALENDAR_OUTLINED
                                    ),
                                    self.t_classe,
                                    self.t_prof,
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style, width=150,
                                        on_click=self.affecter_titus,
                                    ),
                                ], spacing=20
                            )
                        )
                    ], spacing=10
                )
            )
        )

        self.content = ft.Stack(
            expand=True, alignment=ft.alignment.center,
            controls=[
                self.main_window, self.new_class_window, self.new_palier_window, self.details_affec,
                self.modif_window, self.window_titus
            ]
        )
        self.load_lists()
        self.load_datas()

    @staticmethod
    def icon_bt_hover2(e):
        if e.data == 'true':
            e.control.scale = 1.2
            e.control.content.color = "black"
            e.control.content.update()
            e.control.update()
        else:
            e.control.scale = 1
            e.control.content.color = "black45"
            e.control.content.update()
            e.control.update()

    @staticmethod
    def icon_bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.4
            e.control.content.color = "black"
            e.control.content.update()
            e.control.update()
        else:
            e.control.scale = 1
            e.control.content.color = "black45"
            e.control.content.update()
            e.control.update()

    def load_lists(self):
        datas = be.niveaux()
        for niveau in datas:
            self.level.options.append(
                ft.dropdown.Option(niveau)
            )

        paliers = be.niveaux()
        for palier in paliers:
            self.palier.options.append(
                ft.dropdown.Option(palier)
            )

        profs = be.show_nomprof()
        for prof in profs:
            self.m_prof.options.append(ft.dropdown.Option(prof))

        for prof in profs:
            self.t_prof.options.append(ft.dropdown.Option(prof))

    def load_datas(self):
        classes = be.show_all_classes()

        datas = []
        for classe in classes:
            dico = {'code': classe[1], 'niveau': classe[2], 'nom': classe[3], 'effectif': classe[4],
                    "capacite": classe[5]}
            datas.append(dico)

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        cap_totale = 0
        eff_global = 0
        nb_classe = 0

        for data in datas:
            capacite = data['capacite']
            effectif = data['effectif']

            cap_totale += capacite
            eff_global += effectif
            nb_classe += 1

            if effectif < capacite:
                icone = ft.icons.HOURGLASS_BOTTOM_ROUNDED
                couleur = SECOND_COLOR
            else:
                icone = ft.icons.HOURGLASS_FULL
                couleur = THRID_COLOR

            self.table.rows.append(
                ft.DataRow(
                    data=data,
                    cells=[
                        ft.DataCell(ft.Icon(icone, color=couleur, size=16)),
                        ft.DataCell(ft.Text(data['code'].upper())),
                        ft.DataCell(ft.Text(data['niveau'].upper())),
                        ft.DataCell(ft.Text(data['nom'].upper())),
                        ft.DataCell(ft.Text(data['effectif'])),
                        ft.DataCell(ft.Text(data['capacite'])),
                        ft.DataCell(
                            ft.Container(
                                scale=ft.transform.Scale(1),
                                animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                on_hover=self.icon_bt_hover,
                                content=ft.IconButton(
                                    ft.icons.WATCH_LATER_OUTLINED, icon_color=ft.colors.BLACK45,
                                    on_click=self.view_affec,
                                    tooltip="Voir affectations", data=data
                                ),
                            )
                        )
                    ]
                )
            )

        self.cap_global.value = cap_totale
        self.effectif_global.value = eff_global
        self.nb_classes.value = nb_classe
        taux = eff_global * 100 / cap_totale
        self.tdr_global.value = f"{taux:.2f} %"

    def filter_datas(self, e):
        level = self.level.value
        classes = be.show_all_classes()

        datas = []
        for classe in classes:
            dico = {'code': classe[1], 'niveau': classe[2], 'nom': classe[3], 'effectif': classe[4],
                    "capacite": classe[5]}
            datas.append(dico)

        filter_datas = list(filter(lambda x: level in x['niveau'], datas))

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in filter_datas:
            capacite = data['capacite']
            effectif = data['effectif']
            if effectif < capacite:
                icone = ft.icons.HOURGLASS_BOTTOM_ROUNDED
                couleur = SECOND_COLOR
            else:
                icone = ft.icons.HOURGLASS_FULL
                couleur = THRID_COLOR

            self.table.rows.append(
                ft.DataRow(
                    data=data,
                    cells=[
                        ft.DataCell(ft.Icon(icone, color=couleur, size=16)),
                        ft.DataCell(ft.Text(data['code'].upper())),
                        ft.DataCell(ft.Text(data['niveau'].upper())),
                        ft.DataCell(ft.Text(data['nom'].upper())),
                        ft.DataCell(ft.Text(data['effectif'])),
                        ft.DataCell(ft.Text(data['capacite'])),
                        ft.DataCell(
                            ft.Container(
                                scale=ft.transform.Scale(1),
                                animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                on_hover=self.icon_bt_hover,
                                content=ft.IconButton(
                                    ft.icons.WATCH_LATER_OUTLINED, icon_color=ft.colors.BLACK45,
                                    on_click=self.view_affec,
                                    tooltip="Voir affectations", data=data
                                ),
                            )
                        )
                    ]
                )
            )

        self.table.update()

    def supp_filtres(self, e):
        self.level.value = None
        self.level.update()
        self.load_datas()
        self.table.update()

    def on_change_cycle(self,e ):
        for row in self.palier.options[:]:
            self.palier.options.remove(row)

        if self.section.value is None:
            pass
        else:
            for palier in be.all_niveaux_by_section_cyle(self.section.value, self.cycle.value):
                self.palier.options.append(ft.dropdown.Option(palier))

        self.palier.update()

    def close_new_class_window(self, e):
        for widget in (self.nom_classe, self.capacite, self.palier, self.nom_long):
            widget.value = None
            widget.update()

        self.new_class_window.scale = 0
        self.new_class_window.update()

    def nouvelle_classe(self, e):
        count = 0
        for widget in (self.nom_classe, self.capacite, self.palier, self.nom_long):
            if widget.value is None or widget.value == "":
                count += 1

        if count == 0:
            if self.nom_classe.value in be.show_classes():
                self.cp.box.open = True
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = "La classe existe déjà"
                self.cp.box.update()
            else:
                be.add_class(self.nom_classe.value, self.palier.value, self.nom_long.value, self.capacite.value)

                jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']
                creneaux = ['07:30 - 08:30', '08:30 - 09:30', '09:30 - 10:30', '10:45 - 11:45', '11:45 - 12:45',
                            '13:00 - 14:00', '14:00 - 15:00', '1500: - 16:00']

                hour_counter = 0
                for jour in jours:
                    for creneau in creneaux:
                        be.add_affectation('', self.nom_classe.value, '', 0, jour.upper(), creneau)
                        hour_counter += 1
                        total = len(jours) * len(creneaux)
                        self.pb_class.value = hour_counter / total
                        self.pb_class.update()

                for widget in (self.nom_classe, self.capacite, self.palier, self.nom_long):
                    widget.value = None
                    widget.update()

                self.cp.box.open = True
                self.cp.box.title.value = "Confirmé !"
                self.cp.box.content.value = "Nouvelle classe créée"
                self.cp.box.update()

                self.load_datas()
                self.table.update()
                self.tdr_global.update()
                self.cap_global.update()
                self.effectif_global.update()
                self.nb_classes.update()

        else:
            self.cp.box.open = True
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Tous les champs sont obligatoires"
            self.cp.box.update()

    def open_new_class_window(self, e):
        self.new_class_window.scale = 1
        self.new_class_window.update()

    def open_new_palier_window(self, e):
        self.new_palier_window.scale = 1
        self.new_palier_window.update()

    def close_new_palier_window(self, e):
        for widget in (self.section_2, self.cycle_2, self.palier_long, self.nom_palier):
            widget.value = None
            widget.update()

        self.new_palier_window.scale = 0
        self.new_palier_window.update()

    def nouveau_palier(self, e):
        count = 0
        for widget in (self.section_2, self.cycle_2, self.palier_long, self.nom_palier):
            if widget.value is None or widget.value == "":
                count += 1

        if count == 0:
            if self.nom_palier in be.niveaux():
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = f"Ce palier existe déjà"
                self.cp.box.open = True
                self.cp.box.update()

            else:
                be.add_niveau(self.nom_palier.value, "", "", "", self.palier_long.value, self.cycle_2.value, self.section_2.value)
                self.cp.box.open = True
                self.cp.box.title.value = "Confirmé !"
                self.cp.box.content.value = "Nouveau palier créé"
                self.cp.box.update()

            for widget in (self.section_2, self.cycle_2, self.palier_long, self.nom_palier):
                widget.value = None
                widget.update()

        else:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = f"Tous les champs sont obligatoires"
            self.cp.box.open = True
            self.cp.box.update()

    def close_details_affec(self, e):
        self.details_affec.scale = 0
        self.details_affec.update()

    def close_window_titus(self, e):
        self.window_titus.scale = 0
        self.window_titus.update()

    def open_window_titus(self, e):
        if self.titus_affec.value is None or self.titus_affec.value == "":
            self.t_classe.value = self.title_affec.value
            self.t_classe.update()
            self.window_titus.scale = 1
            self.window_titus.update()
        else:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = f"un professeurtitulaire a déjà été affecté"
            self.cp.box.open = True
            self.cp.box.update()

    def affecter_titus(self, e):
        if self.t_prof.value is None or self.t_prof.value == "":
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = f"Champ professeur obligatoire"
            self.cp.box.open = True
            self.cp.box.update()

        else:
            be.add_titus(self.t_prof.value, self.t_classe.value, be.show_asco_encours())
            self.cp.box.title.value = "Confirmé"
            self.cp.box.content.value = f"Opération réussie"
            self.cp.box.open = True
            self.cp.box.update()
            self.window_titus.scale = 0
            self.window_titus.update()

    def filtre_affectations(self, e):
        all_affec = be.all_affectations_by_class(self.title_affec.value)
        datas = []

        if self.search_affec.value is None or self.search_affec.value == "":
            for data in all_affec:
                datas.append(
                    {
                        "asco": data[1], "prof": data[2], "matiere": data[4], "classe": data[3],
                        "jour": data[6], 'creneau': data[7]
                    }
                )

            for row in self.table_affec.rows[:]:
                self.table_affec.rows.remove(row)

            for affectation in all_affec:
                if affectation['prof'] == "" and affectation['matiere'] == "":
                    icone = ft.icons.CHECK_BOX
                    color = FIRST_COLOR
                else:
                    icone = ft.icons.DO_NOT_DISTURB_ON
                    color = SECOND_COLOR

                self.table_affec.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Icon(icone, color=color, size=18)
                            ),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Icon("person_outined", size=16, color="black"),
                                        ft.Text(affectation['prof'])
                                    ]
                                )
                            ),
                            ft.DataCell(ft.Text(affectation['matiere'])),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.CALENDAR_MONTH_OUTLINED, size=18, color="black"),
                                        ft.Text(affectation['jour'])
                                    ]
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.WATCH_LATER_OUTLINED, size=18, color="black"),
                                        ft.Text(affectation['creneau'])
                                    ]
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        AnyContainerButton(
                                            ft.icons.EDIT_OUTLINED, "Modifier", affectation, self.open_modif_window,
                                            FOURTH_COLOR
                                        ),
                                        AnyContainerButton(
                                            ft.icons.DELETE_OUTLINED, "Supprimer", affectation, self.delete_affec,
                                            FIFTH_COLOR
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )

            self.table_affec.update()

        else:
            for data in all_affec:
                datas.append(
                    {
                        "asco": data[1], "prof": data[2], "matiere": data[4], "classe": data[3],
                        "jour": data[6], 'creneau': data[7]
                    }
                )
            filter_datas = list(
                filter(lambda x: self.search_affec.value in x['jour'], datas)
            )
            for row in self.table_affec.rows[:]:
                self.table_affec.rows.remove(row)

            for affectation in filter_datas:
                if affectation['prof'] == "" and affectation['matiere'] == "":
                    icone = ft.icons.CHECK_BOX
                    color = FIRST_COLOR
                else:
                    icone = ft.icons.DO_NOT_DISTURB_ON
                    color = SECOND_COLOR

                self.table_affec.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Icon(icone, color=color, size=18)
                            ),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Icon("person_outined", size=16, color="black"),
                                        ft.Text(affectation['prof'])
                                    ]
                                )
                            ),
                            ft.DataCell(ft.Text(affectation['matiere'])),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.CALENDAR_MONTH_OUTLINED, size=18, color="black"),
                                        ft.Text(affectation['jour'])
                                    ]
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.WATCH_LATER_OUTLINED, size=18, color="black"),
                                        ft.Text(affectation['creneau'])
                                    ]
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        AnyContainerButton(
                                            ft.icons.EDIT_OUTLINED, "Modifier", affectation, self.open_modif_window,
                                            FOURTH_COLOR
                                        ),
                                        AnyContainerButton(
                                            ft.icons.DELETE_OUTLINED, "Supprimer", affectation, self.delete_affec,
                                            FIFTH_COLOR
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )

            self.table_affec.update()

    def supp_filtres_affec(self, e):
        self.search_affec.value = None
        self.search_affec.update()

        all_affec = be.all_affectations_by_class(self.title_affec.value)
        datas = []

        for data in all_affec:
            datas.append(
                {
                    "asco": data[1], "prof": data[2], "matiere": data[4], "classe": data[3],
                    "jour": data[6], 'creneau': data[7]
                }
            )

        for row in self.table_affec.rows[:]:
            self.table_affec.rows.remove(row)

        for affectation in datas:
            if affectation['prof'] == "" and affectation['matiere'] == "":
                icone = ft.icons.CHECK_BOX
                color = FIRST_COLOR
            else:
                icone = ft.icons.DO_NOT_DISTURB_ON
                color = SECOND_COLOR

            self.table_affec.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Icon(icone, color=color, size=18)
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Icon("person_outined", size=16, color="black"),
                                    ft.Text(affectation['prof'])
                                ]
                            )
                        ),
                        ft.DataCell(ft.Text(affectation['matiere'])),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.CALENDAR_MONTH_OUTLINED, size=18, color="black"),
                                    ft.Text(affectation['jour'])
                                ]
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.WATCH_LATER_OUTLINED, size=18, color="black"),
                                    ft.Text(affectation['creneau'])
                                ]
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    AnyContainerButton(
                                        ft.icons.EDIT_OUTLINED, "Modifier", affectation, self.open_modif_window,
                                        FOURTH_COLOR
                                    ),
                                    AnyContainerButton(
                                        ft.icons.DELETE_OUTLINED, "Supprimer", affectation, self.delete_affec,
                                        FIFTH_COLOR
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        self.table_affec.update()

    def view_affec(self, e):
        self.title_affec.value = e.control.data['code']
        self.title_affec.update()

        self.titus_affec.value = be.search_titus(e.control.data['code']).upper()
        self.titus_affec.update()

        # self.affec_eff.value = be.effectif_classe(e.control.data['code'])
        # self.affec_eff.update()
        #
        # self.affec_capacite.value = be.capacite_une_classes(e.control.data['code'])
        # self.affec_capacite.update()

        # eff = be.effectif_classe(e.control.data['code'])
        # cap = be.capacite_une_classes(e.control.data['code'])
        # self.affec_tdr.value = f"{(eff * 100 / cap):.2f} %"
        # self.affec_tdr.update()

        all_affec = be.all_affectations_by_class(e.control.data['code'])
        datas = []
        for data in all_affec:
            datas.append(
                {
                    "asco": data[1], "prof": data[2], "matiere": data[4], "classe": data[3],
                    "jour": data[6], 'creneau': data[7]
                }
            )

        for row in self.table_affec.rows[:]:
            self.table_affec.rows.remove(row)

        for affectation in datas:
            if affectation['prof'] == "" and affectation['matiere'] == "":
                icone = ft.icons.CHECK_BOX
                color = FIRST_COLOR
            else:
                icone = ft.icons.DO_NOT_DISTURB_ON
                color = SECOND_COLOR

            self.table_affec.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Icon(icone, color=color, size=18)
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Icon("person_outined", size=16, color="black"),
                                    ft.Text(affectation['prof'])
                                ]
                            )
                        ),
                        ft.DataCell(ft.Text(affectation['matiere'])),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.CALENDAR_MONTH_OUTLINED, size=18, color="black"),
                                    ft.Text(affectation['jour'])
                                ]
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.WATCH_LATER_OUTLINED, size=18, color="black"),
                                    ft.Text(affectation['creneau'])
                                ]
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    AnyContainerButton(
                                        ft.icons.EDIT_OUTLINED, "Modifier", affectation, self.open_modif_window,
                                        FOURTH_COLOR
                                    ),
                                    AnyContainerButton(
                                        ft.icons.DELETE_OUTLINED, "Supprimer", affectation, self.delete_affec,
                                        FIFTH_COLOR
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        self.table_affec.update()
        # self.title_affec.value = e.control.data['code']
        # self.title_affec.update()
        self.details_affec.scale = 1
        self.details_affec.update()

    def open_modif_window(self, e):

        if e.control.data['matiere'] == "" or e.control.data['matiere'] is None:
            self.m_classe.value = self.title_affec.value
            self.m_classe.update()
            self.m_jour.value = e.control.data['jour']
            self.m_jour.update()
            self.m_creneau.value = e.control.data['creneau']
            self.m_creneau.update()
            self.m_niveau.value = be.look_nivo(self.m_classe.value)
            self.m_niveau.update()
            self.m_matiere.value = e.control.data['matiere']
            self.m_matiere.update()

            matieres = be.mat_by_class(self.m_niveau.value)
            for row in self.m_matiere.options[:]:
                self.m_matiere.options.remove(row)

            for matiere in matieres:
                self.m_matiere.options.append(ft.dropdown.Option(matiere))

            self.m_matiere.update()

            self.modif_window.scale = 1
            self.modif_window.update()

        else:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = f"le créneau horaire est déjà occupé\nPour le modifer vous devez dabord supprimer l'affectation"
            self.cp.box.open = True
            self.cp.box.update()

    def close_modif_window(self, e):

        for row in self.m_matiere.options[:]:
            self.m_matiere.options.remove(row)

        self.m_matiere.update()

        self.modif_window.scale = 0
        self.modif_window.update()

    def delete_affec(self, e):
        if e.control.data['matiere'] is not None or e.control.data['matiere'] != "":
            be.delete_affectation(
                e.control.data['prof'], self.title_affec.value, e.control.data['matiere'],
                e.control.data['jour'], e.control.data['creneau']
            )

            all_affec = be.all_affectations_by_class(self.title_affec.value)
            datas = []
            for data in all_affec:
                datas.append(
                    {
                        "asco": data[1], "prof": data[2], "matiere": data[4], "classe": data[3],
                        "jour": data[6], 'creneau': data[7]
                    }
                )

            for row in self.table_affec.rows[:]:
                self.table_affec.rows.remove(row)

            for affectation in datas:
                if affectation['prof'] == "" and affectation['matiere'] == "":
                    icone = ft.icons.CHECK_BOX
                    color = FIRST_COLOR
                else:
                    icone = ft.icons.DO_NOT_DISTURB_ON
                    color = SECOND_COLOR

                self.table_affec.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Icon(icone, color=color, size=18)
                            ),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Icon("person_outined", size=16, color="black"),
                                        ft.Text(affectation['prof'])
                                    ]
                                )
                            ),
                            ft.DataCell(ft.Text(affectation['matiere'])),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.CALENDAR_MONTH_OUTLINED, size=18, color="black"),
                                        ft.Text(affectation['jour'])
                                    ]
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.WATCH_LATER_OUTLINED, size=18, color="black"),
                                        ft.Text(affectation['creneau'])
                                    ]
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        AnyContainerButton(
                                            ft.icons.EDIT_OUTLINED, "Modifier", affectation, self.open_modif_window,
                                            FOURTH_COLOR
                                        ),
                                        AnyContainerButton(
                                            ft.icons.DELETE_OUTLINED, "Supprimer", affectation, self.delete_affec,
                                            FIFTH_COLOR
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )

            self.table_affec.update()
            self.search_affec.value = None
            self.search_affec.update()

    def valider_modif_affec(self, e):
        if be.is_creneau_prof_oqp(self.m_prof.value, self.m_jour.value, self.m_creneau.value):
            self.cp.box.title.value = "Erreur!"
            self.cp.box.content.value = f"Le professeur est déja occupé pour ce créneau"
            self.cp.box.open = True
            self.cp.box.update()
        else:
            nivo = be.look_nivo(self.m_classe.value)
            nb_heures = be.charge_horaire_by_mat_nivo(nivo, self.m_matiere.value)
            all_affec = be.all_affectations_by_annee()
            nb_affec = 0
            for affec in all_affec:
                if affec['classe'] == self.m_classe.value and affec['matiere'] == self.m_matiere.value:
                    nb_affec += affec['nb_heures']

            if nb_affec == nb_heures:
                self.cp.box.title.value = "Attention !"
                self.cp.box.content.value = f"La charge horaire pour cette matière est déjà atteinte dans cette classe"
                self.cp.box.open = True
                self.cp.box.update()
            else:
                be.ajouter_affectation(
                    self.m_prof.value, self.m_matiere.value, self.m_classe.value,
                    self.m_jour.value, self.m_creneau.value
                )
                self.cp.box.title.value = "Validé !"
                self.cp.box.content.value = f"Affectation modifiée avec succès"
                self.cp.box.open = True
                self.cp.box.update()

                all_affec = be.all_affectations_by_class(self.title_affec.value)
                datas = []
                for data in all_affec:
                    datas.append(
                        {
                            "asco": data[1], "prof": data[2], "matiere": data[4], "classe": data[3],
                            "jour": data[6], 'creneau': data[7]
                        }
                    )

                for row in self.table_affec.rows[:]:
                    self.table_affec.rows.remove(row)

                for affectation in datas:
                    if affectation['prof'] == "" and affectation['matiere'] == "":
                        icone = ft.icons.CHECK_BOX
                        color = FIRST_COLOR
                    else:
                        icone = ft.icons.DO_NOT_DISTURB_ON
                        color = SECOND_COLOR

                    self.table_affec.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(
                                    ft.Icon(icone, color=color, size=18)
                                ),
                                ft.DataCell(
                                    ft.Row(
                                        [
                                            ft.Icon("person_outined", size=16, color="black"),
                                            ft.Text(affectation['prof'])
                                        ]
                                    )
                                ),
                                ft.DataCell(ft.Text(affectation['matiere'])),
                                ft.DataCell(
                                    ft.Row(
                                        [
                                            ft.Icon(ft.icons.CALENDAR_MONTH_OUTLINED, size=18, color="black"),
                                            ft.Text(affectation['jour'])
                                        ]
                                    )
                                ),
                                ft.DataCell(
                                    ft.Row(
                                        [
                                            ft.Icon(ft.icons.WATCH_LATER_OUTLINED, size=18, color="black"),
                                            ft.Text(affectation['creneau'])
                                        ]
                                    )
                                ),
                                ft.DataCell(
                                    ft.Row(
                                        controls=[
                                            AnyContainerButton(
                                                ft.icons.EDIT_OUTLINED, "Modifier", affectation,
                                                self.open_modif_window,
                                                FOURTH_COLOR
                                            ),
                                            AnyContainerButton(
                                                ft.icons.DELETE_OUTLINED, "Supprimer", affectation, self.delete_affec,
                                                FIFTH_COLOR
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    )

                self.table_affec.update()
                self.search_affec.value = None
                self.search_affec.update()
                self.search_affec.value = None
                self.search_affec.update()

                self.modif_window.scale = 0
                self.modif_window.update()

    @staticmethod
    def bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.1
            e.control.update()

        else:
            e.control.scale = 1
            e.control.update()
