# from styles.profs_stylesheet import *
from utils import *
from utils import backend as be

icon_style = {'size': 18, 'color': '#fe9500'}
icon_style_2 = {'size': 18, 'color': '#fe9500'}


class Profs(ft.Container):
    def __init__(self, cp: object):
        super(Profs, self).__init__(
            expand=True
        )
        self.cp = cp
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("")),
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("Sexe")),
                ft.DataColumn(label=ft.Text("Matières enseignées")),
                ft.DataColumn(label=ft.Text("Contact")),
                ft.DataColumn(label=ft.Text("Taux horaire")),
                ft.DataColumn(label=ft.Text("Actions")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )
        self.nom = ft.TextField(
            **field_style, hint_text="Nom professeur", width=350, height=45, on_change=self.filter_datas,
            prefix_icon=ft.icons.PERSON_OUTLINED
        )
        self.nb_profs = ft.Text("", size=24, font_family="Poppins Light", color="black")
        self.hommes = ft.Text("", size=24, font_family="Poppins Light", color="black")
        self.femmes = ft.Text("", size=24, font_family="Poppins Light", color="black")
        self.pch = ft.Text("", size=12, font_family="Poppins Medium", color="#144bb3", visible=False)
        self.pcf= ft.Text("", size=12, font_family="Poppins Medium", color="pink", visible=False)

        self.main_window = ft.Container(
            padding=ft.padding.only(20, 0, 20, 0), expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.padding.only(30, 15, 30, 15), border_radius=12,
                        content=ft.Column(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text("Chiffres".upper(), size=13, font_family="Poppins Bold", color="black"),
                                        ft.Divider(height=1, thickness=1),
                                    ], spacing=0
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Column(
                                            [
                                                ft.Text("Nb profs".upper(), size=11, font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.GROUP_OUTLINED, size=20,
                                                                color="black87"),

                                                        self.nb_profs
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("Femmes".upper(), size=12,
                                                        font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.WOMAN_2_OUTLINED, size=20,
                                                                color="black87"),

                                                        ft.Row([self.femmes, self.pcf], vertical_alignment=ft.CrossAxisAlignment.END)
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("Hommes".upper(), size=11,
                                                        font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.MAN_4_OUTLINED, size=20,
                                                                color="black87"),

                                                        ft.Row([self.hommes, self.pch], vertical_alignment=ft.CrossAxisAlignment.END)
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        )
                                    ], spacing=70, vertical_alignment=ft.CrossAxisAlignment.START
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        padding=ft.padding.only(30, 15, 30, 15), border_radius=12, bgcolor="white", expand=True,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("Liste des Professeurs".upper(), size=14, font_family="Poppins Medium", weight=ft.FontWeight.BOLD),
                                        AnyButton(FIRST_COLOR, ft.icons.PERSON_ADD_OUTLINED, "prof +", "white", self.open_new_prof_window),
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Column(
                                    expand=True,
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                self.nom,
                                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        ),
                                        ft.ListView(expand=True, controls=[self.table])
                                    ]
                                ),
                            ], spacing=15
                        )
                    )
                ]
            )
        )

        # new prof window
        self.new_prof = ft.TextField(**field_style_2, width=350, prefix_icon="person_outlined", label="Nom")
        self.new_sex = ft.Dropdown(
            **drop_style, width=100, label="Sexe",
            options=[
                ft.dropdown.Option("M"),
                ft.dropdown.Option("F"),
            ]
        )
        self.new_tel = ft.TextField(**field_style_2, width=200, label="Contact", prefix_icon=ft.icons.PHONE_ANDROID)
        self.new_matiere = ft.Dropdown(**drop_style, prefix_icon="book_outlined", width=350, label="matiere")
        self.new_taux = ft.TextField(
            **field_style_2, width=150, label="Taux", text_align="right", prefix_icon="monetization_on_outlined",
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.new_prof_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=400, height=450,
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
                                    ft.Row(
                                        controls=[
                                            ft.Icon("person", color=SECOND_COLOR),
                                            ft.Text(
                                                "Nouveau prof".upper(), size=14,
                                                font_family="Poppins Medium"
                                            )
                                        ]
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                        on_click=self.close_new_prof_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                        ),
                        ft.Container(
                            padding=20, bgcolor="white", border_radius=12,
                            content=ft.Column(
                                controls=[
                                    self.new_prof,
                                    ft.Row([self.new_tel, self.new_sex]),
                                    self.new_matiere,
                                    self.new_taux,
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style, on_click=self.ajouter_professeur,
                                        width=170
                                    ),
                                ], spacing=20
                            )
                        )
                    ], spacing=10
                )
            )
        )

        # fenetre des affectations
        self.details_prof = ft.Text(size=18, font_family="Poppins Light", color=FIRST_COLOR)
        self.heures_hebdo = ft.Text(size=18, font_family="Poppins Light", color=SECOND_COLOR)
        self.taux_horaire = ft.Text(size=18, font_family="Poppins Light", color=THRID_COLOR)
        self.table_affec = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Classe")),
                ft.DataColumn(label=ft.Text("Matière")),
                ft.DataColumn(label=ft.Text("Jour")),
                ft.DataColumn(label=ft.Text("Creneau")),
                ft.DataColumn(label=ft.Text("PP")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )
        self.affectations_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=720, height=550,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black", expand=True,
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20, expand=True, bgcolor="#f0f0f6",
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Container(
                                                padding=20, bgcolor="white", border_radius=12,
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Icon(ft.icons.PERSON_OUTLINED, size=24, color="black"),
                                                        ft.Text("Professeur", size=12, font_family="Poppins Italic"),
                                                        self.details_prof
                                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                                ),
                                            ),
                                            ft.Container(
                                                padding=20, bgcolor="white", border_radius=12,
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Icon(ft.icons.WATCH_LATER_OUTLINED, size=24, color="black"),
                                                        ft.Text("Charge Horaire", size=12,
                                                                font_family="Poppins Italic"),
                                                        self.heures_hebdo
                                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                                ),
                                            ),
                                            ft.Container(
                                                padding=20, bgcolor="white", border_radius=12,
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Icon(ft.icons.MONETIZATION_ON_OUTLINED, size=24,
                                                                color="black"),
                                                        ft.Text("Taux Horaire", size=12, font_family="Poppins Italic"),
                                                        self.taux_horaire
                                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                                )
                                            ),
                                        ]
                                    ),
                                    ft.IconButton(
                                        "close", scale=0.7, bgcolor="#f0f0f6", icon_color="black",
                                        on_click=self.close_affectations_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white", expand=True,
                            content=ft.Column(
                                expand=True,
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text("Affectations", size=14, font_family="Poppins Bold"),
                                            ft.Row(
                                                controls=[
                                                    AnyButton(
                                                        SECOND_COLOR, ft.icons.ADD_LOCATION_OUTLINED, "Affect. +", "white",
                                                        self.open_new_affectation_window,
                                                    ),
                                                ]
                                            )
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.ListView(
                                        expand=True,
                                        controls=[self.table_affec]
                                    )
                                ], spacing=15
                            )
                        )
                    ], spacing=15
                )
            )
        )

        # New affectation window
        self.naf_prof = ft.TextField(**underline_field_style, width=350, prefix_icon="person_outlined", label="Nom professeur")
        self.naf_classe = ft.Dropdown(
            **drop_style, width=150, prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, label="Classe",
            on_change=self.changement_classe
        )
        self.naf_jour = ft.Dropdown(
            **drop_style, width=150, prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED, label="Jour",
            options=[
                ft.dropdown.Option("LUNDI"), ft.dropdown.Option("MARDI"), ft.dropdown.Option("MERCREDI"),
                ft.dropdown.Option("JEUDI"), ft.dropdown.Option("VENDREDI"),
            ]
        )
        self.naf_creneau = ft.Dropdown(
            **drop_style, width=150, prefix_icon=ft.icons.WATCH_LATER_OUTLINED, label="Créneau",
            options=[]
        )
        self.naf_nivo = ft.TextField(
            **underline_field_style, width=150, prefix_icon=ft.icons.CANDLESTICK_CHART_SHARP, label="niveau"
        )
        self.naf_matiere = ft.Dropdown(**drop_style, width=350, prefix_icon="book_outlined", label="Matière",)
        self.new_affectation_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=470, height=550,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20, bgcolor="#f0f0f6",
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=10, border_radius=12, bgcolor="white",
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.ADD_LOCATION, color=SECOND_COLOR),
                                            ft.Text(
                                                "Créer affectation".upper(), size=14,
                                                font_family="Poppins Medium"
                                            )
                                        ],
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                        on_click=self.close_new_affectation_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                        ),
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white",
                            content=ft.Column(
                                controls=[
                                    self.naf_prof,
                                    ft.Row(controls=[self.naf_classe, self.naf_nivo]),self.naf_matiere,
                                    self.naf_jour, self.naf_creneau,
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style, on_click=self.create_affectation,
                                        width=170
                                    ),
                                ],spacing=20
                            )
                        ),
                    ], spacing=15,
                )
            )
        )

        self.content = ft.Stack(
            expand=True, alignment=ft.alignment.center,
            controls=[
                self.main_window, self.new_prof_window, self.affectations_window, self.new_affectation_window
            ]
        )
        self.load_datas()
        self.load_lists()

    @staticmethod
    def icon_bt_hover2(e):
        if e.data == 'true':
            e.control.scale = 1.4
            e.control.update()
        else:
            e.control.scale = 1
            e.control.content.update()
            e.control.update()

    def load_lists(self):
        types = be.show_typemat()
        for typp in types:
            self.new_matiere.options.append(ft.dropdown.Option(typp))

        classes = be.show_classes()
        for classe in classes:
            self.naf_classe.options.append(ft.dropdown.Option(classe))

        creneaux = ['07:30 - 08:30', '08:30 - 09:30', '09:30 - 10:30', '10:45 - 11:45',
                    '11:45 - 12:45', '13:00 - 14:00', '14:00 - 15:00', '1500: - 16:00']
        for creneau in creneaux:
            self.naf_creneau.options.append(
                ft.dropdown.Option(creneau)
            )

    def load_datas(self):
        datas = be.show_all_profs()
        all_datas = []

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in datas:
            all_datas.append({"nom": data[1], "sexe": data[2], "contact": data[3], "matiere": data[4], 'taux': data[5]})

        hommes = 0
        femmes = 0
        total = 0

        for data in all_datas:
            if be.is_titus(data['nom']):
                icone = ft.icons.ASSIGNMENT_IND_SHARP
                color = FIRST_COLOR
            else:
                icone = None
                color = None

            if data['sexe'] == "M":
                sex_icon = "man"
                sex_color = SECOND_COLOR
                hommes += 1
            else:
                sex_icon = "woman"
                sex_color = THRID_COLOR
                femmes += 1

            total += 1

            self.table.rows.append(
                ft.DataRow(
                    data=data,
                    cells=[
                        ft.DataCell(ft.Icon(icone, color=color, size=18)),
                        ft.DataCell(ft.Text(data['nom'])),
                        ft.DataCell(ft.Icon(sex_icon, color=sex_color, size=18)),
                        ft.DataCell(ft.Text(data['matiere'])),
                        ft.DataCell(ft.Text(data['contact'])),
                        ft.DataCell(ft.Text(data['taux'])),
                        ft.DataCell(
                            ft.Container(
                                scale=ft.transform.Scale(1),
                                animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                on_hover=self.icon_bt_hover2,
                                content=ft.IconButton(
                                    ft.icons.EDIT_OUTLINED, scale=1, data=data,
                                    icon_color=FOURTH_COLOR, on_click=self.open_affec_window
                                )
                            )
                        )
                    ]
                )
            )

        self.hommes.value = hommes
        self.femmes.value = femmes
        self.nb_profs.value = total
        self.pcf.value = f"{(femmes * 100 / total):.2f} %"
        self.pch.value = f"{(hommes * 100 / total):.2f} %"

    def filter_datas(self, e):
        datas = be.show_all_profs()
        all_datas = []

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in datas:
            all_datas.append({"nom": data[1], "sexe": data[2], "contact": data[3], "matiere": data[4], 'taux': data[5]})

        filtre = self.nom.value
        filter_datas = list(filter(lambda x: filtre in x['nom'], all_datas))

        for data in filter_datas:
            if be.is_titus(data['nom']):
                icone = ft.icons.ASSIGNMENT_IND_SHARP
                color = FIRST_COLOR
            else:
                icone = None
                color = None

            if data['sexe'] == "M":
                sex_icon = "man"
                sex_color = SECOND_COLOR
            else:
                sex_icon = "woman"
                sex_color = THRID_COLOR

            self.table.rows.append(
                ft.DataRow(
                    data=data,
                    cells=[
                        ft.DataCell(ft.Icon(icone, color=color, size=18)),
                        ft.DataCell(ft.Text(data['nom'])),
                        ft.DataCell(ft.Icon(sex_icon, color=sex_color, size=18)),
                        ft.DataCell(ft.Text(data['matiere'])),
                        ft.DataCell(ft.Text(data['contact'])),
                        ft.DataCell(ft.Text(data['taux'])),
                        ft.DataCell(
                            ft.Container(
                                scale=ft.transform.Scale(1),
                                animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                on_hover=self.icon_bt_hover2,
                                content=ft.IconButton(
                                    ft.icons.EDIT_OUTLINED, scale=1, data=data,
                                    icon_color=FOURTH_COLOR, on_click=self.open_affec_window
                                )
                            )
                        )
                    ]
                )
            )

        self.table.update()

    def open_new_prof_window(self, e):
        self.new_prof_window.scale = 1
        self.new_prof_window.update()

    def close_new_prof_window(self, e):
        for widget in (self.new_sex, self.new_matiere, self.new_prof, self.new_tel, self.new_taux):
            widget.value = None
            widget.update()

        self.new_prof_window.scale = 0
        self.new_prof_window.update()

    def ajouter_professeur(self, e):
        counter = 0

        for widget in (self.new_sex, self.new_matiere, self.new_prof, self.new_tel, self.new_taux):
            if widget.value is None:
                counter += 1

        if counter > 0:
            self.cp.box.title.value = "Erreur !"
            self.cp.box.content.value = f"Tous les champs sont obligatoires"
            self.cp.box.open = True
            self.cp.box.update()
        else:
            taux = int(self.new_taux.value)
            be.add_prof(self.new_prof.value, self.new_sex.value, self.new_tel.value, self.new_matiere.value, taux)

            self.cp.box.title.value = "Confirmé !"
            self.cp.box.content.value = f"Nouveau professeur ajouté"
            self.cp.box.open = True
            self.cp.box.update()

            for widget in (self.new_sex, self.new_matiere, self.new_prof, self.new_tel, self.new_taux):
                widget.value = None
                widget.update()

            self.load_datas()
            self.table.update()
            self.hommes.update()
            self.femmes.update()
            self.nb_profs.update()
            self.pcf.update()
            self.pch.update()

    def close_affectations_window(self, e):
        self.affectations_window.scale = 0
        self.affectations_window.update()

    def open_affec_window(self, e):
        self.details_prof.value = f"{e.control.data['nom']}".upper()
        self.details_prof.update()
        self.taux_horaire.value = f"{be.ajout_separateur(e.control.data['taux'])}"
        self.taux_horaire.update()

        for row in self.table_affec.rows[:]:
            self.table_affec.rows.remove(row)

        datas = be.show_affectation_by_prof(e.control.data['nom'])

        total_heures = 0
        for data in datas:
            hours = data[5] if data[5] is not None else 0
            total_heures += hours

            # if be.is_titus(e.control.data['nom']):
            #     icone = "star"
            #     color = "amber"
            # else:
            #     icone = None
            #     color = None

            if be.look_classprof_titus(e.control.data['nom']) == data[3]:
                icone = ft.icons.ASSIGNMENT_IND_SHARP
                color = FOURTH_COLOR
            else:
                icone = None
                color = None

            self.table_affec.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data[3])),
                        ft.DataCell(ft.Text(data[4])),
                        ft.DataCell(ft.Text(data[6])),
                        ft.DataCell(ft.Text(data[7])),
                        ft.DataCell(ft.Icon(icone, color=color, size=18))
                    ]
                )
            )

        self.table_affec.update()

        self.affectations_window.scale = 1
        self.affectations_window.update()
        self.heures_hebdo.value = f"{total_heures}"
        self.heures_hebdo.update()

    def changement_classe(self, e):
        for row in self.naf_matiere.options[:]:
            self.naf_matiere.options.remove(row)

        self.naf_nivo.value = be.look_nivo(self.naf_classe.value)
        self.naf_nivo.update()

        matieres = be.mat_by_class(self.naf_nivo.value)

        for matiere in matieres:
            self.naf_matiere.options.append(ft.dropdown.Option(matiere))

        self.naf_matiere.update()

    def create_affectation(self, e):
        counter = 0
        for widget in (self.naf_classe, self.naf_nivo, self.naf_prof, self.naf_matiere):
            if widget.value is None:
                counter += 1

        if counter == 0:

            # on vérifie que le professeur n'est pas affecté à ce créneau
            mad_prof = be.is_creneau_prof_oqp(self.naf_prof.value, self.naf_jour.value, self.naf_creneau.value)

            if mad_prof:
                oqp = be.is_creneau_prof_oqp2(self.naf_prof.value, self.naf_jour.value, self.naf_creneau.value)

                self.cp.box.title.value = "Conflit"
                self.cp.box.content.value = f"Ce professeur est déjà affecté pour ce créneau\n{oqp[3]} - {oqp[4]} - {oqp[6]} - {oqp[7]}"
                self.cp.box.open = True
                self.cp.box.update()

            else:
                # on vérifie si la classe n'a pas un autre cours à cette heure
                if be.is_creneau_classe_oqp(self.naf_classe.value, self.naf_jour.value, self.naf_creneau.value):

                    oqp = be.is_creneau_classe_oqp2(self.naf_classe.value, self.naf_jour.value, self.naf_creneau.value)
                    self.cp.box.title.value = "Conflit"
                    self.cp.box.content.value = f"Ce créneau est déjà occupé pour cette classe\n{oqp[2]} - {oqp[4]}"
                    self.cp.box.open = True
                    self.cp.box.update()

                else:
                    nivo = be.look_nivo(self.naf_classe.value)
                    nb_heures = be.charge_horaire_by_mat_nivo(nivo, self.naf_matiere.value)
                    all_affec = be.all_affectations_by_annee()
                    nb_affec = 0
                    for affec in all_affec:
                        if affec['classe'] == self.naf_classe.value and affec['matiere'] == self.naf_matiere.value:
                            nb_affec += affec['nb_heures']

                    if nb_affec == nb_heures:
                        self.cp.box.title.value = "Attention !"
                        self.cp.box.content.value = f"La charge horaire pour cette matière est déjà atteinte dans cette classe"
                        self.cp.box.open = True
                        self.cp.box.update()
                    else:
                        be.ajouter_affectation(
                            self.naf_prof.value, self.naf_matiere.value, self.naf_classe.value,
                            self.naf_jour.value, self.naf_creneau.value
                        )
                        self.cp.box.title.value = "Validé !"
                        self.cp.box.content.value = f"Affectation créée avec succès"
                        self.cp.box.open = True
                        self.cp.box.update()

                        for row in self.naf_matiere.options[:]:
                            self.naf_matiere.options.remove(row)

                        for widget in (self.naf_classe, self.naf_nivo, self.naf_prof, self.naf_matiere, self.naf_jour, self.naf_creneau):
                            widget.value = None
                            widget.update()

                        self.table_affec.update()

                        self.actualiser_affec_window()
                        self.table_affec.update()
                        self.heures_hebdo.update()

        else:
            self.cp.box.title.value = "Erreur !"
            self.cp.box.content.value = f"Tous les champs sont obligatoires"
            self.cp.box.open = True
            self.cp.box.update()

    def actualiser_affec_window(self):
        datas = be.show_all_profs()
        all_datas = []

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in datas:
            all_datas.append({"nom": data[1], "sexe": data[2], "contact": data[3], "matiere": data[4], 'taux': data[5]})

        filter_datas = list(filter(lambda x: self.details_prof.value in x['nom'], all_datas))

        self.taux_horaire.value = f"{be.ajout_separateur(filter_datas[0]['taux'])}"
        self.taux_horaire.update()

        for row in self.table_affec.rows[:]:
            self.table_affec.rows.remove(row)

        datas = be.show_affectation_by_prof(self.details_prof.value)

        total_heures = 0
        for data in datas:
            hours = data[5] if data[5] is not None else 0
            total_heures += hours

            if be.look_classprof_titus(self.details_prof.value) == data[3]:
                icone = "star"
                color = FOURTH_COLOR
            else:
                icone = None
                color = None

            self.table_affec.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data[3])),
                        ft.DataCell(ft.Text(data[4])),
                        ft.DataCell(ft.Text(data[6])),
                        ft.DataCell(ft.Text(data[7])),
                        ft.DataCell(ft.Icon(icone, color=color, size=18))
                    ]
                )
            )

        self.heures_hebdo.value = f"{total_heures}"

    def close_new_affectation_window(self, e):
        self.new_affectation_window.scale = 0
        self.new_affectation_window.update()

    def open_new_affectation_window(self, e):
        self.naf_prof.value = self.details_prof.value
        self.naf_prof.update()
        self.new_affectation_window.scale = 1
        self.new_affectation_window.update()

    @staticmethod
    def bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.1
            e.control.update()

        else:
            e.control.scale = 1
            e.control.update()

