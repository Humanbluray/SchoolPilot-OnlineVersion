# from styles.annees_stylesheet import *
from utils import *
from utils import backend as be


class Annees(ft.Container):
    def __init__(self, cp: object):
        super(Annees, self).__init__(
            expand=True
        )
        self.cp = cp
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("")),
                ft.DataColumn(label=ft.Text("Année")),
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("Début")),
                ft.DataColumn(label=ft.Text("Fin")),
                ft.DataColumn(label=ft.Text("Statut")),
                ft.DataColumn(label=ft.Text("Actions")),
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
                        padding=ft.padding.only(30, 15, 30, 15), bgcolor="white", border_radius=12, expand=True,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.icons.WARNING_AMBER, size=36, color="amber"),
                                                ft.Text("Avertissement".upper(), size=16,
                                                        font_family="Poppins SemiBold", color="red"),
                                            ]
                                        ),
                                        ft.Text(
                                            "Les manipulations sur cette fenêtre ne peuvent se réaliser qu'ue seule fois durant une année scolaire".upper(),
                                            size=12, font_family="Poppins Regular", color="grey"),
                                        ft.Text(
                                            "Veuillez alors avant de faire la manipulation que l'année scolaire est complètement bouclée".upper(),
                                            size=12, font_family="Poppins Regular", color="grey"),
                                    ], spacing=3
                                ),
                                ft.Divider(height=3, color=ft.colors.TRANSPARENT),
                                ft.Row([ft.Text("Années".upper(), size=13, font_family="Poppins Medium")]),
                                ft.ListView(
                                    expand=True,
                                    controls=[self.table]
                                )
                            ]
                        )
                    ),
                ], spacing=15
            )
        )

        # Annee scolaire suivante
        self.debut_annee = ft.TextField(
            **underline_field_style, width=145, prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED, label="début"
        )
        self.fin_annee = ft.TextField(
            **underline_field_style, width=145, prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED, label="fin"
        )
        self.name_annee = ft.TextField(
            **underline_field_style, width=100, label="asco", prefix_icon="edit_calendar_outlined"
        )
        self.name_long = ft.TextField(
            **underline_field_style, width=150, label="Nom", prefix_icon=ft.icons.LABEL_OUTLINED
        )

        # Frais de scolarité
        self.inscription = ft.TextField(
            **field_style_2, width=150, label="Inscription", input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.tranche_1 = ft.TextField(
            **field_style_2, width=150, label="Tranche 1", input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.tranche_2 = ft.TextField(
            **field_style_2, width=150, label="Tranche 2", input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.tranche_3 = ft.TextField(
            **field_style_2, width=150, label="Tranche 3", input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.switch_sco = ft.Switch(
            active_color=SECOND_COLOR, thumb_color=FIRST_COLOR, track_outline_color="black",
            scale=0.6, on_change=self.changement_solde
        )
        self.new_scolarite = ft.Container(
            padding=0, border_radius=12, border=ft.border.all(1, "grey"),
            content=ft.Column(
                controls=[
                    ft.Container(
                        bgcolor="white", padding=10,
                        content=ft.Row(
                            controls=[
                                ft.Text("Nouveaux Frais de scolarité".upper(), size=13, font_family="Poppins Medium", color="black", weight=ft.FontWeight.BOLD),
                            ], alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ),
                    ft.Container(
                        padding=10, content=ft.Column(
                            controls=[
                                ft.Row(
                                    [ft.Text("Reconduire".upper(), size=12, font_family="Poppins Italic", color="grey"),
                                     self.switch_sco]),
                                ft.Row(
                                    controls=[self.inscription, self.tranche_1, self.tranche_2, self.tranche_3]
                                )
                            ]
                        )
                    )
                ], spacing=10
            )
        )

        # affectations_professeurs
        self.switch_affec = ft.Switch(
            active_color=SECOND_COLOR, thumb_color=FIRST_COLOR, track_outline_color="black",
            scale=0.6, on_change=None
        )
        self.pb_affec = ft.ProgressBar(bar_height=6, width=100, border_radius=12, color=FOURTH_COLOR, bgcolor="grey")
        self.switch_titus = ft.Switch(
            active_color=SECOND_COLOR, thumb_color=FIRST_COLOR, track_outline_color="black",
            scale=0.6, on_change=None
        )
        self.pb_titus = ft.ProgressBar(bar_height=10, width=200, border_radius=12, color=FOURTH_COLOR, bgcolor="grey", value=0)
        self.pb_affec = ft.ProgressBar(bar_height=10, width=200, border_radius=12, color=FIFTH_COLOR, bgcolor="grey", value=0)
        self.count_affec = ft.Text("Evolution 0 %", size=12, font_family="Poppins Light", color="grey")
        self.count_titus = ft.Text("Evolution 0 %", size=12, font_family="Poppins Light", color="grey")

        self.new_otpions = ft.Container(
            padding=0, border_radius=12, border=ft.border.all(1, "grey"),
            content=ft.Column(
                controls=[
                    ft.Container(
                        bgcolor="white", padding=10,
                        content=ft.Row(
                            controls=[
                                ft.Text("Autres options".upper(), size=13, font_family="Poppins Medium", color="black", weight=ft.FontWeight.BOLD),
                            ], alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ),
                    ft.Container(
                        padding=10,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("Reconduire Affectations".upper(), font_family="Poppins Italic", color="grey", size=12),
                                        self.switch_affec,
                                        ft.Text(f"Si vous activez, les emplois de temps actuels\nseront reportés sur l'année suivante".upper(), size=12, font_family="Poppins Medium")
                                    ]
                                ),
                            ]
                        )
                    )
                ], spacing=10
            )
        )

        # Fenêtre de clôture
        self.fenetre_cloture = ft.Card(
            elevation=30, surface_tint_color="#f0f0f6", shadow_color="black", expand=True,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            width=750, height=620,
            scale=ft.transform.Scale(0), animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20, bgcolor="#f0f0f6", expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            bgcolor="white", padding=10, border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.EDIT_CALENDAR, color=SECOND_COLOR),
                                            ft.Text("Configuration nouvelle année scolaire".upper(), size=14,
                                                    font_family="Poppins Medium"),
                                        ]
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, scale=0.8, bgcolor="#f0f0f6", icon_color=FIRST_COLOR,
                                        on_click=self.close_fenetre_cloture
                                    )
                                ],  alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                        ),
                        ft.Container(
                            bgcolor="white", padding=20, border_radius=12, expand=True,
                            content=ft.Column(
                                expand=True,  # scroll="auto",
                                controls=[
                                    ft.Container(
                                        padding=10, content=ft.Row(
                                            [self.name_annee, self.name_long, self.debut_annee, self.fin_annee]),
                                    ),
                                    self.new_scolarite, self.new_otpions,
                                    ft.Container(
                                        padding=10,
                                        content=ft.ElevatedButton(
                                            on_hover=self.bt_hover, **choix_style, width=150,
                                            on_click=self.open_confirmation_window
                                        ),
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        )

        self.confirmation_window = ft.Card(
            elevation=30, surface_tint_color="#f0f0f6", shadow_color="black", expand=True,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            width=500, height=320,
            scale=ft.transform.Scale(0), animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20, bgcolor="#f0f0f6",
                content=ft.Container(
                    bgcolor="white", border_radius=12, padding=20,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.WORK, color=SECOND_COLOR),
                                    ft.Text("Confirmation".upper(), size=18, font_family="Poppins Medium"),
                                ]
                            ),
                            ft.Divider(height=1, thickness=1),
                            ft.Column(
                                controls=[
                                    ft.Text("Souhaitez-vous poursuivre ?".upper(), size=12, font_family="Poppins Medium"),
                                    ft.Text("L'opération est irréversible".upper(), size=12, font_family="Poppins Medium"),
                                    ft.Text("Vous n'aurez plus accès aux données de l'année scolaire en cours".upper(), size=12, font_family="Poppins Medium"),
                                    ft.Text("Toutefois elles sont sauvegardées dans la base de données".upper(), size=12, font_family="Poppins Medium"),
                                ], spacing=5
                            ),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        **red_style, width=170, on_click=self.cloturer_annee
                                    ),
                                    ft.ElevatedButton(
                                        **blue_style, width=170, on_click=self.close_confirmation_window
                                    ),
                                ]
                            )
                        ], spacing=20
                    )
                )
            )
        )

        self.finish = ft.ElevatedButton(
            **terminer_style, width=170,
            on_click=lambda e: self.cp.page.go("/"), disabled=True
        )

        self.count_window = ft.Card(
            elevation=30, surface_tint_color="#f0f0f6", shadow_color="black", expand=True,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            width=290, height=290,
            scale=ft.transform.Scale(0), animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20, bgcolor="#f0f0f6", expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            bgcolor="white", padding=10, border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.DO_NOT_DISTURB_ON_OUTLINED, color="red"),
                                            ft.Text("Patientez", size=18,
                                                    font_family="Poppins Light"),
                                        ]
                                    ),

                                ],  alignment=ft.MainAxisAlignment.CENTER
                            ),
                        ),
                        ft.Container(
                            bgcolor="white", padding=20, border_radius=12, expand=True,
                            content=ft.Column(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text("génération des affectations", size=12, font_family="Poppins Medium"),
                                            self.count_affec,
                                            self.pb_affec
                                        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    self.finish

                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20
                            )
                        )
                    ]
                )
            )
        )

        self.content = ft.Stack(
            controls=[
                self.main_window, self.fenetre_cloture, self.count_window, self.confirmation_window
            ], alignment=ft.alignment.center
        )
        self.load_datas()

    @staticmethod
    def icon_bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.3
            e.control.update()

        else:
            e.control.scale = 1
            e.control.update()

    def load_datas(self):
        annees = be.all_asco()

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in annees:
            if data[5] == "terminée":
                icone = ft.icons.DO_NOT_DISTURB_ON_OUTLINED
                color = FIRST_COLOR
                visible = False
                b_color = "grey"
            else:
                icone = ft.icons.CHECK_CIRCLE
                color = ft.colors.GREEN
                visible = True
                b_color = ft.colors.BLACK87

            self.table.rows.append(
                ft.DataRow(
                    data=data,
                    cells=[
                        ft.DataCell(ft.Icon(icone, color, 16)),
                        ft.DataCell(ft.Text(data[1])),
                        ft.DataCell(ft.Text(data[2])),
                        ft.DataCell(ft.Text(data[3])),
                        ft.DataCell(ft.Text(data[4])),
                        ft.DataCell(ft.Text(data[5])),
                        ft.DataCell(
                            ft.Container(
                                scale=ft.transform.Scale(1),
                                animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                on_hover=self.icon_bt_hover,
                                content=ft.IconButton(
                                    ft.icons.NEXT_PLAN_OUTLINED, icon_color=ft.colors.BLACK87, scale=0.8,
                                    on_click=self.open_fenetre_cloture, visible=visible,
                                    tooltip="Clôturer année scolaire", data=data
                                ),
                            )
                        ),
                    ]
                )
            )

    def close_fenetre_cloture(self, e):
        self.fenetre_cloture.scale = 0
        self.fenetre_cloture.update()

    def open_fenetre_cloture(self, e):
        self.name_annee.value = be.show_asco_encours() + 1
        self.name_annee.update()
        self.name_long.value = f"{be.show_asco_encours()} - {be.show_asco_encours() + 1}"
        self.name_long.update()
        self.debut_annee.value = f"{be.show_asco_encours()}-08-01"
        self.debut_annee.update()
        self.fin_annee.value = f"{be.show_asco_encours() + 1}-07-31"
        self.fin_annee.update()

        self.fenetre_cloture.scale = 1
        self.fenetre_cloture.update()

    def changement_solde(self, e):
        if self.switch_sco.value:
            self.tranche_3.value = be.total_tranche('tranche 3')
            self.tranche_2.value = be.total_tranche('tranche 2')
            self.tranche_1.value = be.total_tranche('tranche 1')
            self.inscription.value = be.total_tranche('inscription')
            self.tranche_3.read_only = True
            self.tranche_2.read_only = True
            self.tranche_1.read_only = True
            self.inscription.read_only = True
            self.tranche_3.update()
            self.tranche_2.update()
            self.tranche_1.update()
            self.inscription.update()
        else:
            self.tranche_3.read_only = False
            self.tranche_2.read_only = False
            self.tranche_1.read_only = False
            self.inscription.read_only = False
            self.tranche_3.value = None
            self.tranche_2.value = None
            self.tranche_1.value = None
            self.inscription.value = None
            self.tranche_3.update()
            self.tranche_2.update()
            self.tranche_1.update()
            self.inscription.update()

    def cloturer_annee(self, e):

        count_vides = 0
        for widget in (self.tranche_1, self.tranche_2, self.tranche_3, self.inscription):
            if widget.value == "" or widget.value is None:
                count_vides += 1

        if count_vides > 0:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Tous les champs sont obligatoires"
            self.cp.box.open = True
            self.cp.box.update()

        else:
            tranche_1 = int(self.tranche_1.value)
            tranche_2 = int(self.tranche_2.value)
            tranche_3 = int(self.tranche_3.value)
            inscription = int(self.inscription.value)

            be.add_tranche('inscription', inscription, 'non', self.name_annee.value)
            be.add_tranche('tranche 1', tranche_1, 'oui', self.name_annee.value)
            be.add_tranche('tranche 2', tranche_2, 'oui', self.name_annee.value)
            be.add_tranche('tranche 3', tranche_3, 'oui', self.name_annee.value)

            self.fenetre_cloture.scale = 0
            self.fenetre_cloture.update()

            self.confirmation_window.scale = 0
            self.confirmation_window.update()

            self.count_window.scale = 1
            self.count_window.update()

            all_affec = be.all_affectations_by_annee()
            # update asco
            asco = be.show_asco_encours()
            be.update_statut_asco("terminée", asco)

            # créer une nouvelle année
            be.add_asco(self.name_annee.value, self.name_long.value, self.debut_annee.value, self.fin_annee.value, "en cours")

            # creer les affectations
            if self.switch_affec.value:
                total = len(all_affec)
                count = 0
                for affec in all_affec:
                    be.add_affectation(
                        affec['prof'], affec['classe'], affec['matiere'], affec['nb_heures'], affec['jour'], affec['creneau']
                    )
                    count += 1
                    self.pb_affec.value = count / total
                    self.count_affec.value = f"{(count *100 / total):.2f} %"
                    self.pb_affec.update()
                    self.count_affec.update()

            else:
                jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']
                creneaux = ['07:30 - 08:30', '08:30 - 09:30', '09:30 - 10:30', '10:45 - 11:45',
                            '11:45 - 12:45', '13:00 - 14:00', '14:00 - 15:00', '1500: - 16:00']

                all_classes = be.show_classes()
                count = 0
                total = len(jours) * len(creneaux) * len(all_classes)

                for jour in jours:
                    for creneau in creneaux:
                        for classe in be.show_classes():
                            be.add_affectation("", classe, "", 0, jour.upper(), creneau)
                            count += 1
                            self.pb_affec.value = count / total
                            self.count_affec.value = f"{be.ecrire_nombre(count * 100 / total)} %"
                            self.pb_affec.update()
                            self.count_affec.update()

            self.finish.disabled = False
            self.finish.update()
            self.load_datas()
            self.table.update()

    def open_confirmation_window(self, e):
        self.confirmation_window.scale = 1
        self.confirmation_window.update()

    def close_confirmation_window(self, e):
        self.confirmation_window.scale = 0
        self.confirmation_window.update()

    @staticmethod
    def bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.1
            e.control.update()

        else:
            e.control.scale = 1
            e.control.update()



