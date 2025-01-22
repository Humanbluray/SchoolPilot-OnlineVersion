from utils import *
from utils import backend as be


class Affectation(ft.Container):
    def __init__(self, cp: object, prof: str, classe: str, matiere: str, nb_heures: int, jour: str, creneau: str):
        super(Affectation, self).__init__(
            border_radius=0, bgcolor="white",
            # border=ft.border.all(1, "#e6e6e6"),
            width=190, height=140, padding=10,
            scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),

        )
        self.cp = cp
        self.prof = prof
        self.classe = classe
        self.matiere = matiere
        self.jour = jour
        self.creneau = creneau
        self.nb_heures = nb_heures
        self.nivo = be.look_nivo(self.classe) if self.classe != "" else ""
        self.dim = be.dim_by_nivo(self.nivo, self.matiere) if self.nivo != "" else ""
        self.bt_icon = ""
        self.check = ft.Checkbox(
            active_color="#f0f0f6", check_color=FIRST_COLOR, scale=0.7
        )

        if self.jour == "LUNDI":
            day_color = ft.colors.AMBER_50
        elif self.jour == "MARDI":
            day_color = ft.colors.LIGHT_BLUE_50
        elif self.jour == "MERCREDI":
            day_color = ft.colors.DEEP_PURPLE_50
        elif self.jour == "JEUDI":
            day_color = ft.colors.INDIGO_50
        else:
            day_color = ft.colors.TEAL_50

        if self.matiere != "" or self.matiere is None:
            self.bt_icon = ft.icons.DELETE_OUTLINE_OUTLINED
            icone = ft.icons.DO_NOT_DISTURB_ON_TOTAL_SILENCE_OUTLINED
            couleur = "red"
            text_font = "Poppins Medium"
            text_color = "white"
            bg = day_color.split("50")
            bgcouleur = bg[0] + "700"
        else:
            self.bt_icon = ft.icons.EDIT_OUTLINED
            icone = ft.icons.CHECK_CIRCLE
            couleur = ft.colors.GREEN
            text_font = "Poppins Medium"
            text_color = "black"
            bgcouleur = None

        self.content = ft.Container(
            border_radius=12, bgcolor=day_color, expand=True, padding=ft.padding.only(5, 10, 5, 10),
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=3, bgcolor="white", border_radius=6,
                        content=ft.Row(
                            [
                                ft.Icon(icone, size=16, color=couleur),
                                ft.Text(jour, size=13, font_family="Poppins Regular", color="black"),
                                self.check
                            ], alignment=ft.MainAxisAlignment.SPACE_AROUND
                        )
                    ),
                    ft.Column(
                        controls=[
                            ft.Row(
                                [
                                    ft.Text(self.creneau, size=12, font_family=text_font, color="black"),
                                    ft.Container(
                                        scale=ft.transform.Scale(1), padding=0,
                                        animate_scale=ft.animation.Animation(
                                            300, ft.AnimationCurve.FAST_OUT_SLOWIN
                                        ),
                                        on_hover=self.icon_bt_hover2,
                                        content=ft.IconButton(
                                            self.bt_icon, scale=0.9, on_click=self.open_modif_window,
                                            icon_color=ft.colors.BLACK87,
                                        )
                                    ),
                                ], alignment="center"
                            ),
                            ft.Container(
                                padding=ft.padding.only(5, 2, 5, 2), tooltip=f"Matière: {matiere}\nclasse: {classe}",
                                bgcolor=bgcouleur, border_radius=8, expand=True,
                                content=ft.Row(
                                    [
                                        ft.Text(
                                            f"{self.dim}", size=14, color="white",
                                            font_family="Poppins Light",
                                        ),
                                        ft.Text(
                                            f"{self.classe}", size=14, color="white",
                                            font_family="Poppins Light",
                                        )
                                    ], alignment="center"
                                )
                            ),
                        ], spacing=0
                    )
                ], spacing=2
            )
        )

    def icon_bt_hover2(self, e):
        if e.data == 'true':
            e.control.scale = 1.4
            if self.bt_icon == "edit_outlined":
                e.control.content.icon_color = "#144bb3"
                e.control.tooltip = "Occuper créneau"
            else:
                e.control.content.icon_color = "red"
                e.control.tooltip = "Libérer créneau"
            e.control.content.update()
            e.control.update()
        else:
            e.control.scale = 1
            e.control.content.icon_color = ft.colors.BLACK87
            e.control.content.update()
            e.control.update()

    def open_modif_window(self, e):
        if self.bt_icon == "edit_outlined":
            self.cp.m_jour.value = self.jour
            self.cp.m_matiere.value = self.matiere
            self.cp.m_prof.value = self.cp.search_prof.value
            self.cp.m_creneau.value = self.creneau
            self.cp.m_classe.value = self.classe

            for widget in (
                    self.cp.m_jour, self.cp.m_matiere, self.cp.m_prof, self.cp.m_creneau,
                    self.cp.m_classe
            ):
                widget.update()

            for row in self.cp.m_matiere.options[:]:
                self.cp.m_matiere.options.remove(row)

            self.cp.modif_window.scale = 1
            self.cp.modif_window.update()

        else:
            be.delete_affectation(
                self.prof, self.classe, self.matiere,
                self.jour, self.creneau
            )
            self.cp.refresh_page()
            self.cp.tableau.update()


class TimeProf(ft.Tab):
    def __init__(self, cp: object):
        super(TimeProf, self).__init__(
            tab_content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.ACCOUNT_BOX, size=20),
                    ft.Text("Vue Profs".upper(), size=13, font_family="Poppins Medium")
                ]
            )
        )
        self.cp = cp
        self.multi_affec_bt = AnyButton(FIRST_COLOR, ft.icons.WATCH_LATER_OUTLINED, "Affecter", "white", self.open_multi_window)
        self.nivo = ""
        self.tableau = ft.Row(expand=True, spacing=0, scroll=ft.ScrollMode.AUTO)
        self.time = ft.Column(
            controls=[self.tableau], expand=True, scroll=ft.ScrollMode.AUTO
        )
        self.search_prof = ft.Dropdown(
            **drop_style, label="Professeur", width=300, prefix_icon=ft.icons.PERSON_OUTLINED,
            options=[], on_change=self.filter_datas, bgcolor="#f2f2f2"
        )
        self.mat_enseignees = ft.Text(size=12, font_family="Poppins Italic", color="grey")
        self.main_window = ft.Container(
            padding=ft.padding.only(10, 5, 10, 5), expand=True, border_radius=12,
            margin=ft.margin.only(top=10),
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[self.search_prof, self.mat_enseignees],
                            ),
                            self.multi_affec_bt
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Container(
                        bgcolor="white", border_radius=12, padding=5, expand=True,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                ft.Container(
                                    padding=ft.padding.only(2, 2, 2, 2), expand=True,
                                    content=ft.Row([self.time], alignment=ft.MainAxisAlignment.CENTER)
                                ),
                            ]
                        )
                    ),
                ]
            )
        )

        # edit page
        self.m_prof = ft.TextField(
            **underline_field_style, width=300, label="Prof", prefix_icon=ft.icons.PERSON_OUTLINED
        )
        self.m_classe = ft.Dropdown(
            **drop_style, width=170, prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, label="Classe",
            on_change=self.on_change_classe
        )
        self.m_matiere = ft.Dropdown(
            **drop_style, width=300, prefix_icon="book_outlined", label="Matière"
        )
        self.m_jour = ft.TextField(
            **underline_field_style, width=150, label="Jour", prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED
        )
        self.m_creneau = ft.TextField(
            **underline_field_style, width=170, label="Creneau", prefix_icon=ft.icons.WATCH_LATER_OUTLINED
        )

        self.modif_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=400, height=520,
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
                                            ft.Icon('edit_outlined', color="red"),
                                            ft.Text('Affecter', size=14, font_family="Poppins Medium"),
                                        ]
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                        on_click=self.close_modif_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, bgcolor="white", border_radius=12,
                            content=ft.Column(
                                controls=[
                                    self.m_prof,
                                    self.m_jour,
                                    self.m_creneau,
                                    self.m_classe,
                                    self.m_matiere,
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style, width=150,
                                        on_click=self.create_affectation
                                    ),
                                ], spacing=20
                            )
                        )
                    ]
                )
            )
        )
        # Multi edit page ..................
        self.multi_prof = ft.TextField(
            **underline_field_style, width=300, label="Prof", prefix_icon=ft.icons.PERSON_OUTLINED
        )
        self.multi_classe = ft.Dropdown(
            **drop_style, width=170, prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, label="Classe",
            on_change=self.on_change_multi_classe
        )
        self.multi_matiere = ft.Dropdown(
            **drop_style, width=300, prefix_icon="book_outlined", label="Matière"
        )
        self.multi_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=400, height=400,
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
                                            ft.Icon('edit_outlined', color="red"),
                                            ft.Text('Affecter', size=14, font_family="Poppins Medium"),
                                        ]
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                        on_click=self.close_multi_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=30, bgcolor="white", border_radius=12,
                            content=ft.Column(
                                controls=[
                                    self.multi_prof,
                                    self.multi_classe,
                                    self.multi_matiere,
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style, width=150,
                                        on_click=self.affect_multi
                                    ),
                                ], spacing=20
                            )
                        )
                    ]
                )
            )
        )

        self.content = ft.Stack(
            expand=True,
            controls=[
                self.main_window, self.modif_window, self.multi_window
            ], alignment=ft.alignment.center
        )
        self.load_lists()

    def load_lists(self):
        profs = be.show_nomprof()
        for prof in profs:
            self.search_prof.options.append(
                ft.dropdown.Option(prof)
            )

        classes = be.show_all_classes()
        for classe in classes:
            self.m_classe.options.append(
                ft.dropdown.Option(classe[1])
            )
            self.multi_classe.options.append(
                ft.dropdown.Option(classe[1])
            )

    def filter_datas(self, e):
        self.mat_enseignees.value = be.search_mat_prof(self.search_prof.value)
        self.mat_enseignees.update()

        for row in self.tableau.controls[:]:
            self.tableau.controls.remove(row)

        jours = ['lundi'.upper(), 'mardi'.upper(), 'mercredi'.upper(), 'jeudi'.upper(), 'vendredi'.upper()]
        creneaux = [
            '07:30 - 08:30', '08:30 - 09:30', '09:30 - 10:30', '10:45 - 11:45',
            '11:45 - 12:45', '13:00 - 14:00', '14:00 - 15:00', '1500: - 16:00'
        ]
        lundi, mardi, mercredi, jeudi, vendredi = [], [], [], [], []

        for jour in jours:
            for creneau in creneaux:
                if be.is_creneau_prof_oqp(self.search_prof.value, jour, creneau):
                    oqp = be.is_creneau_prof_oqp2(self.search_prof.value, jour, creneau)
                    une_affec = Affectation(
                        self, oqp[2], oqp[3], oqp[4], oqp[5], oqp[6], oqp[7]
                    )
                    if jour == "LUNDI":
                        lundi.append(une_affec)
                    elif jour == "MARDI":
                        mardi.append(une_affec)
                    elif jour == "MERCREDI":
                        mercredi.append(une_affec)
                    elif jour == "JEUDI":
                        jeudi.append(une_affec)
                    else:
                        vendredi.append(une_affec)
                else:
                    une_affec = Affectation(
                        self, "", "", "", 0, jour, creneau
                    )
                    if jour == "LUNDI":
                        lundi.append(une_affec)
                    elif jour == "MARDI":
                        mardi.append(une_affec)
                    elif jour == "MERCREDI":
                        mercredi.append(une_affec)
                    elif jour == "JEUDI":
                        jeudi.append(une_affec)
                    else:
                        vendredi.append(une_affec)

        elem1 = ft.Column(controls=[item for item in lundi], spacing=0)
        elem2 = ft.Column(controls=[item for item in mardi], spacing=0)
        elem3 = ft.Column(controls=[item for item in mercredi], spacing=0)
        elem4 = ft.Column(controls=[item for item in jeudi], spacing=0)
        elem5 = ft.Column(controls=[item for item in vendredi], spacing=0)

        for colonne in (elem1, elem2, elem3, elem4, elem5):
            self.tableau.controls.append(colonne)

        self.tableau.update()

    def refresh_page(self):
        for row in self.tableau.controls[:]:
            self.tableau.controls.remove(row)

        jours = ['lundi'.upper(), 'mardi'.upper(), 'mercredi'.upper(), 'jeudi'.upper(), 'vendredi'.upper()]
        creneaux = [
            '07:30 - 08:30', '08:30 - 09:30', '09:30 - 10:30', '10:45 - 11:45',
            '11:45 - 12:45', '13:00 - 14:00', '14:00 - 15:00', '1500: - 16:00'
        ]
        lundi, mardi, mercredi, jeudi, vendredi = [], [], [], [], []

        for jour in jours:
            for creneau in creneaux:
                if be.is_creneau_prof_oqp(self.search_prof.value, jour, creneau):
                    oqp = be.is_creneau_prof_oqp2(self.search_prof.value, jour, creneau)
                    une_affec = Affectation(
                        self, oqp[2], oqp[3], oqp[4], oqp[5], oqp[6], oqp[7]
                    )
                    if jour == "LUNDI":
                        lundi.append(une_affec)
                    elif jour == "MARDI":
                        mardi.append(une_affec)
                    elif jour == "MERCREDI":
                        mercredi.append(une_affec)
                    elif jour == "JEUDI":
                        jeudi.append(une_affec)
                    else:
                        vendredi.append(une_affec)
                else:
                    une_affec = Affectation(
                        self, "", "", "", 0, jour, creneau
                    )
                    if jour == "LUNDI":
                        lundi.append(une_affec)
                    elif jour == "MARDI":
                        mardi.append(une_affec)
                    elif jour == "MERCREDI":
                        mercredi.append(une_affec)
                    elif jour == "JEUDI":
                        jeudi.append(une_affec)
                    else:
                        vendredi.append(une_affec)

        elem1 = ft.Column(controls=[item for item in lundi], spacing=0)
        elem2 = ft.Column(controls=[item for item in mardi], spacing=0)
        elem3 = ft.Column(controls=[item for item in mercredi], spacing=0)
        elem4 = ft.Column(controls=[item for item in jeudi], spacing=0)
        elem5 = ft.Column(controls=[item for item in vendredi], spacing=0)

        for colonne in (elem1, elem2, elem3, elem4, elem5):
            self.tableau.controls.append(colonne)

    def close_modif_window(self, e):
        self.modif_window.scale = 0
        self.modif_window.update()

    def create_affectation(self, e):
        counter = 0
        for widget in (self.m_prof, self.m_matiere):
            if widget.value is None:
                counter += 1

        if counter == 0:
            # on vérifie que la classe n'a pas de cours deja à cette heure
            mad_prof = be.is_creneau_classe_oqp(self.m_classe.value, self.m_jour.value, self.m_creneau.value)

            if mad_prof:
                oqp = be.is_creneau_classe_oqp2(self.m_classe.value, self.m_jour.value, self.m_creneau.value)
                self.cp.cp.box.title.value = "Conflit"
                self.cp.cp.box.content.value = f"Ce créneau pour cette classe est déja occupé\n{oqp[3]} - {oqp[4]} - {oqp[6]} - {oqp[7]}"
                self.cp.cp.box.open = True
                self.cp.cp.box.update()

            else:
                nivo = be.look_nivo(self.m_classe.value)
                nb_heures = be.charge_horaire_by_mat_nivo(nivo, self.m_matiere.value)
                all_affec = be.all_affectations_by_annee()
                nb_affec = 0
                for affec in all_affec:
                    if affec['classe'] == self.m_classe.value and affec['matiere'] == self.m_matiere.value:
                        nb_affec += affec['nb_heures']

                if nb_affec == nb_heures:
                    self.cp.cp.box.title.value = "Attention !"
                    self.cp.cp.box.content.value = f"La charge horaire pour cette matière est déjà atteinte dans cette classe"
                    self.cp.cp.box.open = True
                    self.cp.cp.box.update()
                else:
                    be.ajouter_affectation(
                        self.m_prof.value, self.m_matiere.value, self.m_classe.value,
                        self.m_jour.value, self.m_creneau.value
                    )
                    self.cp.cp.box.title.value = "Validé !"
                    self.cp.cp.box.content.value = f"Affectation créée avec succès"
                    self.cp.cp.box.open = True
                    self.cp.cp.box.update()

                    for row in self.m_matiere.options[:]:
                        self.m_matiere.options.remove(row)

                    for widget in (self.m_classe, self.m_prof, self.m_matiere, self.m_jour, self.m_creneau):
                        widget.value = None
                        widget.update()

                    self.refresh_page()
                    self.tableau.update()

        else:
            self.cp.cp.box.title.value = "Erreur !"
            self.cp.cp.box.content.value = f"Tous les champs sont obligatoires"
            self.cp.cp.box.open = True
            self.cp.cp.box.update()

    @staticmethod
    def bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.2
            e.control.update()
        else:
            e.control.scale = 1
            e.control.update()

    def on_change_classe(self, e):
        for row in self.m_matiere.options[:]:
            self.m_matiere.options.remove(row)

        self.nivo = be.look_nivo(self.m_classe.value)

        matieres = be.show_matieres_fn_niv(self.nivo)
        for matiere in matieres:
            self.m_matiere.options.append(ft.dropdown.Option(matiere))

        self.m_matiere.update()

    def on_change_multi_classe(self, e):
        for row in self.multi_matiere.options[:]:
            self.multi_matiere.options.remove(row)

        self.nivo = be.look_nivo(self.multi_classe.value)

        matieres = be.show_matieres_fn_niv(self.nivo)
        for matiere in matieres:
            self.multi_matiere.options.append(ft.dropdown.Option(matiere))

        self.multi_matiere.update()

    def affect_multi(self, e):
        select_creneaux: list = []
        valid_creneaux: list = []

        for widget in self.tableau.controls[:]:
            for sub_widget in widget.controls[:]:
                if sub_widget.check.value:
                    select_creneaux.append(sub_widget)

        counter = 0
        for widget in (self.multi_prof, self.multi_matiere):
            if widget.value is None:
                counter += 1

        if counter == 0:
            print(len(select_creneaux))
            for wid in select_creneaux:
                # on vérifie que la classe n'a pas de cours deja à cette heure
                mad_prof = be.is_creneau_classe_oqp(self.multi_classe.value, wid.jour, wid.creneau)

                if mad_prof:
                    valid_creneaux.append(
                        {
                            "creneau": f"{wid.jour} / {wid.creneau}", "conflit": "Ce créneau pour cette classe est déja occupé",
                            "statut": "Affectation refusée"
                        }
                    )

                else:
                    nivo = be.look_nivo(self.multi_classe.value)
                    nb_heures = be.charge_horaire_by_mat_nivo(nivo, self.multi_matiere.value)
                    all_affec = be.all_affectations_by_annee()
                    nb_affec = 0
                    for affec in all_affec:
                        if affec['classe'] == self.multi_classe.value and affec['matiere'] == self.multi_matiere.value:
                            nb_affec += affec['nb_heures']

                    if nb_affec == nb_heures:
                        valid_creneaux.append(
                            {
                                "creneau": f"{wid.jour} / {wid.creneau}",
                                "conflit": "La charge horaire pour cette matière est déjà atteinte dans cette classe",
                                "statut": "Affectation refusée"
                            }
                        )
                    else:
                        be.ajouter_affectation(
                            self.multi_prof.value, self.multi_matiere.value, self.multi_classe.value,
                            wid.jour, wid.creneau
                        )
                        valid_creneaux.append(
                            {
                                "creneau": f"{wid.jour} / {wid.creneau}",
                                "conflit": "Aucun",
                                "statut": "Affectation validée"
                            }
                        )

            for row in self.multi_matiere.options[:]:
                self.multi_matiere.options.remove(row)

            for widget in (self.multi_classe, self.multi_prof, self.multi_matiere):
                widget.value = None
                widget.update()

            self.refresh_page()
            self.tableau.update()

            self.cp.cp.box.title.value = "Recap !"
            results = ""
            for item in valid_creneaux:
                results = results + f"\n{item['creneau']}\nconflit: {item['conflit']}\nstatut: {item['statut']}\n   "

            self.cp.cp.box.content.value = f"{results}"
            self.cp.cp.box.open = True
            self.cp.cp.box.update()

            self.refresh_page()
            self.tableau.update()

        else:
            self.cp.cp.box.title.value = "Erreur !"
            self.cp.cp.box.content.value = f"Tous les champs sont obligatoires"
            self.cp.cp.box.open = True
            self.cp.cp.box.update()

    def open_multi_window(self, e):
        select_creneaux: list = []
        valid_creneaux: list = []
        for widget in self.tableau.controls[:]:
            for sub_widget in widget.controls[:]:
                if sub_widget.check.value:
                    select_creneaux.append(sub_widget)

        if len(select_creneaux) < 2:
            self.cp.cp.box.title.value = "Erreur !"
            self.cp.cp.box.content.value = f"Il vous faut sélectionner au moins 2 créneaux"
            self.cp.cp.box.open = True
            self.cp.cp.box.update()

        else:
            self.multi_prof.value = self.search_prof.value

            for widget in (
                    self.multi_matiere, self.multi_prof,
                    self.multi_classe
            ):
                widget.update()

            for row in self.multi_matiere.options[:]:
                self.multi_matiere.options.remove(row)

            self.multi_window.scale = 1
            self.multi_window.update()

    def close_multi_window(self,e ):
        self.multi_window.scale = 0
        self.multi_window.update()



