import time
from utils import *
from utils import backend as be
import pandas
import os
import openpyxl
from pages.connexion import user_infos


class NotesAutres(ft.Tab):
    def __init__(self, cp: object):
        super(NotesAutres, self).__init__(
            tab_content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.NOTE_ALT_ROUNDED, size=20),
                    ft.Text("Autres niveaux".upper(), font_family="Poppins Medium", size=12)
                ]
            )
        )
        self.cp = cp
        self.eleve = ft.TextField(**field_style, prefix_icon="person_outlined", label="Elève", width=200)
        self.classe = ft.Dropdown(**drop_style, prefix_icon="school_outlined", label="classe", width=150,
                                  on_change=self.on_change_classe)
        self.matiere = ft.Dropdown(**drop_style, prefix_icon=ft.icons.BOOK_OUTLINED, label="Matière", width=250)
        self.sequence = ft.Dropdown(**drop_style, prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED, label="Séquence",
                                    width=150)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Séquence")),
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("Classe")),
                ft.DataColumn(label=ft.Text("Matiere")),
                ft.DataColumn(label=ft.Text("Coeff")),
                ft.DataColumn(label=ft.Text("Note")),
                ft.DataColumn(label=ft.Text("Action")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )
        self.main_window = ft.Container(
            padding=ft.padding.only(20, 20, 20, 20), expand=True, bgcolor="white", border_radius=12,
            margin=ft.margin.only(top=10),
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.padding.only(30, 15, 30, 15), border_radius=12, bgcolor="white", expand=True,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("Notes (de 4e à Tle)".upper(), size=13, font_family="Poppins Medium"),
                                        ft.Row(
                                            controls=[
                                                AnyButton(
                                                    FIRST_COLOR, ft.icons.NOTE_ADD_OUTLINED, "Ajouter note", "white", self.open_note_window
                                                ),
                                                AnyButton(
                                                    SECOND_COLOR, ft.icons.FILE_UPLOAD_OUTLINED, "Fichier type", "white",
                                                    self.open_imp_file_windows
                                                ),
                                                AnyButton(
                                                   THRID_COLOR, ft.icons.FILE_DOWNLOAD_OUTLINED, "importer",
                                                    "white",
                                                    lambda _: self.cp.cp.fp_importer_note.pick_files(
                                                        allowed_extensions=['xls', 'xlsx']),
                                                )
                                            ]
                                        )
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Divider(height=4, color="transparent"),
                                ft.Row(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                self.eleve, self.classe, self.matiere, self.sequence,
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Container(
                                                    border=ft.border.all(1, "grey"),
                                                    border_radius=6, bgcolor="#f0f0f6", padding=5,
                                                    on_click=self.filter_datas,
                                                    scale=ft.transform.Scale(1),
                                                    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                                    on_hover=self.icon_bt_hover2,
                                                    tooltip="Filtrer",
                                                    content=ft.Icon(
                                                        ft.icons.FILTER_ALT_OUTLINED,
                                                        color=ft.colors.BLACK45,
                                                    )
                                                ),
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
                                        )
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Divider(height=2, color="transparent"),
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

        # file type import window __________________________________________
        self.imp_eleve = ft.TextField(**field_style_2, prefix_icon="person_outlined", label="Elève", width=250)
        self.imp_classe = ft.Dropdown(
            **drop_style, prefix_icon="school_outlined", label="classe", width=150,
            on_change=self.on_change_imp_classe
        )
        self.imp_matiere = ft.Dropdown(
            **drop_style, prefix_icon=ft.icons.SUBJECT_OUTLINED, label="Matière", width=300,
            on_change=self.on_change_imp_matiere
        )
        self.imp_coeff = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.PIN_OUTLINED, width=100,
            label="Coeff", text_align=ft.TextAlign.RIGHT
        )
        self.imp_sequence = ft.Dropdown(
            **drop_style, prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED, label="Séquence",
            width=150
        )
        self.cp.cp.fp_export_modele_note.on_result = self.exporter_fichier_type
        self.imp_file_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=500, height=370,
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
                                    ft.Text("Fichier type import".upper(), size=14, font_family="Poppins Medium",
                                            color="#292f4c"),
                                    ft.IconButton(
                                        ft.icons.CLOSE, bgcolor="#f0f0f6", icon_color=FIRST_COLOR, scale=0.7,
                                        on_click=self.close_print_window,
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                        ),
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white",
                            content=ft.Column(
                                controls=[
                                    ft.Text(**text_title_style, value="F i l t r e s".upper()),
                                    ft.Row(
                                        controls=[
                                            ft.TextField(
                                                **underline_field_style, width=100,
                                                value=be.show_asco_encours(),
                                                prefix_icon=ft.icons.EDIT_CALENDAR_OUTLINED, label="Asco"
                                            ),
                                            self.imp_classe, self.imp_sequence
                                        ]
                                    ),
                                    ft.Row([self.imp_matiere, self.imp_coeff]),
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style,
                                        on_click=lambda e: self.cp.cp.fp_export_modele_note.save_file(
                                            allowed_extensions=['xls', 'xlsx']),
                                        width=170
                                    ),
                                ], spacing=20
                            )
                        )
                    ],
                )
            )
        )

        self.new_classe = ft.Dropdown(**drop_style, prefix_icon="school", label="classe", width=150,
                                      on_change=self.on_change_new_classe)
        self.new_matiere = ft.Dropdown(**drop_style, prefix_icon=ft.icons.BOOK_OUTLINED, label="Matière", width=300,
                                       on_change=self.on_change_matiere)
        self.new_sequence = ft.Dropdown(**drop_style, prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED, label="Séquence",
                                        width=150)
        self.asco = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.EDIT_CALENDAR_OUTLINED,
            width=90, label="asco", value=be.show_asco_encours()
        )
        self.new_coeff = ft.TextField(**inactive_field_style, prefix_icon=ft.icons.PIN_OUTLINED, width=100,
                                      label="Coeff", text_align=ft.TextAlign.RIGHT)
        self.new_note = ft.TextField(
            **field_style, prefix_icon=ft.icons.EDIT_NOTE, width=100, label="Note", text_align=ft.TextAlign.RIGHT,
            input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]", replacement_string="")
        )
        self.new_eleve = ft.Dropdown(**drop_style, prefix_icon="person", width=300, label="Elève")
        self.figer = ft.IconButton(ft.icons.PUSH_PIN_OUTLINED, icon_color="#292f4c", icon_size=20, bgcolor="#f0f0f6",
                                   on_click=self.epingler_filtres)
        self.indic = ft.Text("Cliquez pour figer les filtres ci-dessus", size=12, font_family="Poppins Medium",
                             color=FIRST_COLOR)
        self.new_note_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6",
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black", width=520, height=505,
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
                                    ft.Text("Ajouter note".upper(), size=16, font_family="Poppins Medium"),
                                    ft.IconButton(
                                        ft.icons.CLOSE, bgcolor="#f0f0f6", icon_color=FIRST_COLOR, scale=0.7,
                                        on_click=self.close_note_window,
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white",
                            content=ft.Column(
                                controls=[
                                    ft.Text(**text_title_style, value="F I L T R E S"),
                                    ft.Row(controls=[self.asco, self.new_classe, self.new_sequence], spacing=20),
                                    ft.Row(controls=[self.new_matiere, self.new_coeff], spacing=20),
                                    ft.Row(controls=[self.figer, self.indic]),
                                    ft.Row(controls=[self.new_eleve, self.new_note, ], spacing=20),
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style, on_click=self.valider_note, width=170
                                    )
                                ], spacing=20
                            )
                        ),
                    ], spacing=10,
                )
            )
        )

        # Fenetre de modification d'une note _________________________________
        self.edit_id_note = ft.TextField(**underline_field_style, label="id", width=100, visible=False)
        self.edit_classe = ft.TextField(**underline_field_style, prefix_icon="school", label="classe", width=150)
        self.edit_matiere = ft.TextField(**underline_field_style, prefix_icon=ft.icons.BOOK_OUTLINED, label="Matière",
                                         width=300)
        self.edit_sequence = ft.TextField(**underline_field_style, prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED,
                                          label="Séquence", width=150)
        self.edit_asco = ft.TextField(**underline_field_style, prefix_icon=ft.icons.EDIT_CALENDAR_OUTLINED, width=90,
                                      label="asco", value=be.show_asco_encours())
        self.edit_coeff = ft.TextField(**underline_field_style, prefix_icon=ft.icons.PIN_OUTLINED, width=100,
                                       label="Coeff", text_align=ft.TextAlign.RIGHT)
        self.edit_note = ft.TextField(
            **field_style_2, prefix_icon=ft.icons.EDIT_NOTE, width=100, label="Note", text_align=ft.TextAlign.RIGHT,
            input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]", replacement_string="")
        )
        self.edit_eleve = ft.TextField(**underline_field_style, prefix_icon="person", width=300, label="Elève")
        self.edit_note_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=500, height=500,
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
                                            ft.Icon("edit_outlined", color="black"),
                                            ft.Text("Modifier note".upper(), size=16, font_family="Poppins Medium"),
                                        ]
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, bgcolor="#f0f0f6", icon_color=FIRST_COLOR, scale=0.7,
                                        on_click=self.close_edit_note_window,
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                        ),
                        ft.Container(
                            padding=20, bgcolor="white", border_radius=12,
                            content=ft.Column(
                                controls=[
                                    ft.Row([self.edit_id_note, self.asco]),
                                    ft.Row([self.edit_classe, self.edit_sequence]),
                                    ft.Row([self.edit_matiere, self.edit_coeff]),
                                    ft.Row([self.edit_eleve]),
                                    ft.Row(
                                        controls=[
                                            ft.Text("*", size=18, color="red"),
                                            self.edit_note,
                                        ]
                                    ),
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style, on_click=self.modifier_note, width=170
                                    ),
                                ], spacing=20
                            )
                        )

                    ], spacing=10,
                )
            )
        )

        # fenetre d'importation des notes
        self.import_result_title = ft.Text(size=13, font_family="Poppins Bold")
        self.import_bar = ft.ProgressBar(
            value=0, bgcolor=FIRST_COLOR, color=SECOND_COLOR, width=200, bar_height=10,
            border_radius=12
        )
        self.progres = ft.Text("", size=12, font_family="Poppins Medium")
        self.table_erreurs = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Ligne")),
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("Séquence")),
                ft.DataColumn(label=ft.Text("Matiere")),
                ft.DataColumn(label=ft.Text("Note")),
                ft.DataColumn(label=ft.Text("Observation")),
            ],
            data_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
            heading_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
        )
        self.nb_erreurs = ft.Text("0", size=12, font_family="Poppins Bold", color="red")
        self.nb_succes = ft.Text("0", size=12, font_family="Poppins Bold", color="green")
        self.cp.cp.fp_importer_note.on_result = self.importer_notes
        self.importer_notes_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", expand=True, width=900, height=700,
            clip_behavior=ft.ClipBehavior.HARD_EDGE, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                expand=True, bgcolor="#f0f0f6",
                padding=20,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=10, bgcolor="white", border_radius=16,
                            content=ft.Row(
                                controls=[
                                    ft.Text("Importation des notes via excel".upper(), size=14,
                                            font_family="Poppins Bold"),
                                    ft.IconButton(
                                        "close", scale=0.7, bgcolor="#f0f0f6", icon_color=FIRST_COLOR,
                                        on_click=self.close_importer_notes_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, expand=True, bgcolor="white", border_radius=16,
                            content=ft.Column(
                                controls=[
                                    ft.Column(
                                        [
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(ft.icons.WARNING_AMBER_OUTLINED, color="red"),
                                                    ft.Text(
                                                        "NB: Aucune ligne n'est importée s'il y au moins une erreur dans le fichier".upper(),
                                                        size=13, font_family="Poppins Bold", color="red"
                                                    ),
                                                ]
                                            )
                                        ], spacing=10
                                    ),
                                    ft.Divider(height=1, thickness=1),
                                    ft.Column(
                                        [
                                            ft.Row([self.progres, self.import_bar], spacing=10),
                                            ft.Row(
                                                controls=[
                                                    ft.Row(
                                                        [
                                                            ft.Text("Nombre d'erreurs", size=12,
                                                                    font_family="Poppins Italic", color="grey"),
                                                            self.nb_erreurs
                                                        ]
                                                    ),
                                                    ft.Divider(height=1, thickness=1),
                                                    ft.Row(
                                                        [
                                                            ft.Text("Nombre de succès", size=12,
                                                                    font_family="Poppins Italic", color="grey"),
                                                            self.nb_succes
                                                        ]
                                                    ),

                                                ]
                                            ),
                                            self.import_result_title,
                                            ft.Divider(height=1, thickness=1),
                                        ], spacing=10
                                    ),
                                    ft.Text("Tables des erreurs / succès", size=13, font_family="Poppins Bold"),
                                    ft.ListView(
                                        expand=True,
                                        controls=[self.table_erreurs, ]
                                    ),
                                ], spacing=20
                            )
                        ),

                    ], spacing=15
                )
            )
        )

        self.content = ft.Stack(
            controls=[
                self.main_window, self.imp_file_window, self.new_note_window, self.edit_note_window,
                self.importer_notes_window
            ], alignment=ft.alignment.center
        )
        self.load_lists()

    @staticmethod
    def icon_bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.2
            e.control.content.icon_color = "black"
            e.control.content.update()
            e.control.update()
        else:
            e.control.scale = 1
            e.control.content.icon_color = ft.colors.BLACK45
            e.control.content.update()
            e.control.update()

    @staticmethod
    def icon_bt_hover2(e):
        if e.data == 'true':
            e.control.scale = 1.4
            e.control.content.icon_color = "black"
            e.control.content.update()
            e.control.update()
        else:
            e.control.scale = 1
            e.control.content.icon_color = ft.colors.BLACK45
            e.control.content.update()
            e.control.update()

    def filter_datas(self, e):
        datas = be.show_all_notes()

        notes = []
        for data in datas:
            dico = {
                'eleve': data[1], 'asco': data[2], 'sequence': data[3], 'classe': data[4],
                'matiere': data[5], 'coeff': data[6], 'note': data[7], 'id': data[0]
            }
            notes.append(dico)

        eleve = self.eleve.value if self.eleve.value is not None else ""
        classe = self.classe.value if self.classe.value is not None else ""
        sequence = self.sequence.value.lower() if self.sequence.value is not None else ""
        matiere = self.matiere.value.lower() if self.matiere.value is not None else ""

        filter_datas = list(
            filter(
                lambda x: eleve in x['eleve'] and classe in x['classe'] and sequence in x[
                    'sequence'].lower() and matiere in x['matiere'].lower(), notes
            )
        )

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for note in filter_datas:
            self.table.rows.append(
                ft.DataRow(
                    data=note,
                    cells=[
                        ft.DataCell(ft.Text(note['sequence'])),
                        ft.DataCell(ft.Text(note['eleve'])),
                        ft.DataCell(ft.Text(note['classe'])),
                        ft.DataCell(ft.Text(note['matiere'])),
                        ft.DataCell(ft.Text(note['coeff'])),
                        ft.DataCell(ft.Text(note['note'])),
                        ft.DataCell(
                            ft.Container(
                                scale=ft.transform.Scale(1),
                                animate_scale=ft.animation.Animation(300,
                                                                     ft.AnimationCurve.FAST_OUT_SLOWIN),
                                on_hover=self.icon_bt_hover2,
                                content=ft.IconButton(
                                    ft.icons.EDIT_OUTLINED, scale=1,
                                    icon_color=ft.colors.BLACK45,
                                    on_click=self.open_edit_window, data=note,
                                    tooltip="Supprimer filtres",
                                )
                            ),
                        ),
                    ]
                )
            )

        self.table.update()

    def supp_filtres(self, e):
        for data in self.matiere.options[:]:
            self.matiere.options.remove(data)

        for widget in (self.eleve, self.matiere, self.sequence, self.classe):
            widget.value = None
            widget.update()

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        self.table.update()

    def load_lists(self):
        classes = be.show_classes_autres()
        for classe in classes:
            self.classe.options.append(ft.dropdown.Option(classe))
            self.imp_classe.options.append(ft.dropdown.Option(classe))
            self.new_classe.options.append(ft.dropdown.Option(classe))

        sequences = ['séquence 1', 'séquence 2', 'séquence 3', 'séquence 4', 'séquence 5', 'séquence 6']
        for sequence in sequences:
            self.sequence.options.append(ft.dropdown.Option(sequence.upper()))
            self.imp_sequence.options.append(ft.dropdown.Option(sequence.upper()))
            self.new_sequence.options.append(ft.dropdown.Option(sequence.upper()))

    def on_change_classe(self, e):
        classe = self.classe.value if self.classe.value is not None else ""

        if classe == "":
            pass
        else:
            niveau = be.niv_fn_classe(self.classe.value)
            matieres = be.show_matieres_fn_niv(niveau)

            for matiere in self.matiere.options[:]:
                self.matiere.options.remove(matiere)

            for matiere in matieres:
                self.matiere.options.append(
                    ft.dropdown.Option(matiere.upper())
                )

            self.matiere.update()

    def on_change_imp_classe(self, e):
        classe = self.imp_classe.value if self.imp_classe.value is not None else ""

        if classe == "":
            pass
        else:
            niveau = be.niv_fn_classe(self.imp_classe.value)
            matieres = be.show_matieres_fn_niv(niveau)

            for matiere in self.imp_matiere.options[:]:
                self.imp_matiere.options.remove(matiere)

            for matiere in matieres:
                self.imp_matiere.options.append(
                    ft.dropdown.Option(matiere.upper())
                )

            self.imp_matiere.update()

    def open_imp_file_windows(self, e):
        self.imp_file_window.scale = 1
        self.imp_file_window.update()

    def on_change_imp_matiere(self, e):
        niveau = be.look_nivo(self.imp_classe.value)
        coeff = be.coef_fn_mat_niv(self.imp_matiere.value, niveau)
        self.imp_coeff.value = coeff
        self.imp_coeff.update()

    def close_print_window(self, e):
        self.imp_file_window.scale = 0
        self.imp_file_window.update()

    def exporter_fichier_type(self, e: ft.FilePickerResultEvent):
        counter = 0
        for widget in (self.imp_classe, self.imp_matiere, self.imp_sequence):
            if widget.value is None:
                counter += 1

        if counter > 0:
            pass
        else:
            datas = be.show_det_insc(self.imp_classe.value)
            eleves = [data[2] for data in datas]
            asco = [be.show_asco_encours() for data in datas]
            sequence = [self.imp_sequence.value.lower() for data in datas]
            classe = [self.imp_classe.value for data in datas]
            matiere = [self.imp_matiere.value for data in datas]
            coefficients = [self.imp_coeff.value for data in datas]
            notes = ["" for data in datas]

            all_notes = {
                "eleve": eleves, "asco": asco, "sequence": sequence, "classe": classe, "matiere": matiere,
                "coefficient": coefficients, "note": notes
            }
            df = pandas.DataFrame(all_notes)
            save_location = f"{e.path}.xlsx"

            if save_location != "None.xlsx" or save_location != "None.xls":
                excel = pandas.ExcelWriter(save_location)
                df.to_excel(excel, sheet_name="feuil1", index=False)
                excel.close()
                self.cp.cp.box.title.value = "Validé !"
                self.cp.cp.box.content.value = f"Fichier créé avec succès"
                self.cp.cp.box.open = True
                self.cp.cp.box.update()
            else:
                self.cp.cp.box.title.value = "Erreur"
                self.cp.cp.box.content.value = f"Pas de chemin choisi"
                self.cp.cp.box.open = True
                self.cp.cp.box.update()

    def on_change_new_classe(self, e):
        classe = self.new_classe.value if self.new_classe.value is not None else ""

        if classe == "":
            pass
        else:
            niveau = be.niv_fn_classe(self.new_classe.value)
            matieres = be.show_matieres_fn_niv(niveau)

            for matiere in self.new_matiere.options[:]:
                self.new_matiere.options.remove(matiere)

            for matiere in matieres:
                self.new_matiere.options.append(
                    ft.dropdown.Option(matiere.upper())
                )

            self.new_matiere.update()

    def on_change_matiere(self, e):
        for data in self.new_eleve.options[:]:
            self.new_eleve.options.remove(data)

        eleves = be.eleves_sans_note(
            self.new_classe.value, self.new_sequence.value.lower(), self.new_matiere.value, self.new_classe.value
        )
        for eleve in eleves:
            self.new_eleve.options.append(
                ft.dropdown.Option(eleve)
            )
        self.new_eleve.update()

        niveau = be.look_nivo(self.new_classe.value)
        coeff = be.coef_fn_mat_niv(self.new_matiere.value, niveau)
        self.new_coeff.value = coeff
        self.new_coeff.update()

    def epingler_filtres(self, e):
        if self.figer.icon == ft.icons.PUSH_PIN_OUTLINED:
            self.figer.icon = ft.icons.PUSH_PIN
            self.figer.update()
            self.indic.value = "Cliquez pour libérer les filtres ci-dessus"
            self.indic.color = "red"
            self.indic.update()
            for widget in (self.new_sequence, self.new_classe, self.new_matiere):
                widget.disabled = True
                widget.update()
        else:
            self.figer.icon = ft.icons.PUSH_PIN_OUTLINED
            self.figer.update()
            self.indic.value = "Cliquez pour figer les filtres ci-dessus"
            self.indic.color = "#292f4c"
            self.indic.update()
            for widget in (self.new_sequence, self.new_classe, self.new_matiere):
                widget.disabled = False
                widget.update()

    def valider_note(self, e):
        counter = 0
        for widget in (self.new_eleve, self.new_sequence, self.new_classe, self.new_matiere, self.new_note):
            if widget.value is None or widget.value == "":
                counter += 1

        if counter > 0:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Tous les champs sont obligatoires"
            self.cp.box.open = True
            self.cp.box.update()

        else:
            asco = be.show_asco_encours()
            note = float(self.new_note.value)
            coeff = int(self.new_coeff.value)

            if note <= 20:
                be.add_notes(
                    self.new_eleve.value, asco, self.new_sequence.value.lower(), self.new_classe.value,
                    self.new_matiere.value,
                    coeff, note, ""  # self.user_infos['name']
                )
                self.cp.cp.box.title.value = "Validé !"
                self.cp.cp.box.content.value = "Note enregistrée avec succès"
                self.cp.cp.box.open = True
                self.cp.cp.box.update()

                if self.figer.icon == ft.icons.PUSH_PIN:
                    for widget in (self.new_sequence, self.new_classe, self.new_matiere):
                        widget.disabled = True
                        widget.update()

                    for widget in (self.new_eleve, self.new_note):
                        widget.value = None
                        widget.update()

                    for data in self.new_eleve.options[:]:
                        self.new_eleve.options.remove(data)

                    eleves = be.eleves_sans_note(
                        self.new_classe.value, self.new_sequence.value.lower(), self.new_matiere.value,
                        self.new_classe.value
                    )
                    for eleve in eleves:
                        self.new_eleve.options.append(
                            ft.dropdown.Option(eleve)
                        )
                    self.new_eleve.update()

                else:
                    for widget in (self.new_sequence, self.new_classe, self.new_matiere, self.new_eleve):
                        widget.disabled = False
                        widget.value = None
                        widget.update()

                    self.new_coeff.value = None
                    self.new_coeff.update()

                    for widget in (self.new_eleve, self.new_note):
                        widget.value = None
                        widget.update()

                    for data in self.new_eleve.options[:]:
                        self.new_eleve.options.remove(data)

                    eleves = be.eleves_sans_note(
                        self.new_classe.value, self.new_sequence.value.lower(), self.new_matiere.value,
                        self.new_classe.value
                    )
                    for eleve in eleves:
                        self.new_eleve.options.append(
                            ft.dropdown.Option(eleve)
                        )
                    self.new_eleve.update()

            else:
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = "La note doit être comprise entre 0 et 20"
                self.cp.box.open = True
                self.cp.box.update()

    def close_note_window(self, e):
        self.new_note_window.scale = 0
        self.new_note_window.update()

    def open_note_window(self, e):
        self.new_note_window.scale = 1
        self.new_note_window.update()

    def close_edit_note_window(self, e):
        self.edit_note_window.scale = 0
        self.edit_note_window.update()

    def modifier_note(self, e):
        if user_infos['nom'] == be.search_prof_affec(self.edit_classe.value, self.edit_matiere.value):
            nouvelle_note = float(self.edit_note.value)
            id_note = int(self.edit_id_note.value)
            if nouvelle_note <= 20:
                be.update_notes(nouvelle_note, id_note, "")  # self.user_infos['name'])
                self.cp.box.title.value = "Validé !"
                self.cp.box.content.value = "Note modifiée avec succès"
                self.cp.box.open = True
                self.cp.box.update()
                self.edit_note_window.scale = 0
                self.edit_note_window.update()
            else:
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = "La note doit être comprise entre 0 et 20"
                self.cp.box.open = True
                self.cp.box.update()
        else:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Vous n'avez pas les droits pour cette action"
            self.cp.box.open = True
            self.cp.box.update()

    def open_edit_window(self, e):
        self.edit_asco.value = e.control.data['asco']
        self.edit_eleve.value = e.control.data['eleve']
        self.edit_sequence.value = e.control.data['sequence']
        self.edit_classe.value = e.control.data['classe']
        self.edit_matiere.value = e.control.data['matiere']
        self.edit_coeff.value = e.control.data['coeff']
        self.edit_note.value = e.control.data['note']

        for widget in (self.edit_id_note, self.asco, self.edit_classe,
                       self.edit_sequence,
                       self.edit_matiere, self.edit_coeff, self.edit_eleve,
                       self.edit_note
                       ):
            widget.update()

        self.edit_id_note.value = e.control.data['id']
        self.edit_id_note.update()
        self.edit_note_window.scale = 1
        self.edit_note_window.update()

    def close_importer_notes_window(self, e):
        self.nb_erreurs.value = "0"
        self.nb_succes.value = "0"
        self.nb_erreurs.update()
        self.nb_succes.update()
        self.import_result_title.value = ""
        self.import_result_title.update()
        self.import_bar.value = 0
        self.import_bar.update()

        for row in self.table_erreurs.rows[:]:
            self.table_erreurs.rows.remove(row)

        self.table_erreurs.update()

        self.importer_notes_window.scale = 0
        self.importer_notes_window.update()

    def importer_notes(self, e: ft.FilePickerResultEvent):
        # on met toutes les données du fichier excel dans une liste
        file = e.files[0]
        absolute_path = os.path.abspath(file.path)
        workbook = openpyxl.load_workbook(absolute_path)
        sheet = workbook.active
        valeurs = list(sheet.values)
        header = valeurs[0]
        valeurs.remove(header)
        erreurs = []
        bons = []

        # On ouvre la fenêtre
        self.importer_notes_window.scale = 1
        self.importer_notes_window.update()
        time.sleep(3)

        # on initialise les variables
        counter_verif = 0
        counter_import = 0
        nb_erreurs = 0
        nb_succes = 0

        for item in valeurs:
            exist = be.search_id_note_import(item[0], item[1], item[2], item[3], item[4], item[5])

            # on met dans les différentes listes les natures d'erreurs
            if item[6] == "" or item[6] is None:
                erreurs.append(
                    {"numero": valeurs.index(item) + 1, "details": item, "nature erreur": "La note doit être un nombre"})
                nb_erreurs += 1
                self.nb_erreurs.value = f"{nb_erreurs}"
                self.nb_erreurs.update()
                counter_verif += 1

            elif exist != 'introuvable':
                erreurs.append({"numero": valeurs.index(item) + 1, "details": item, "nature erreur": "existe déja"})
                nb_erreurs += 1
                self.nb_erreurs.value = f"{nb_erreurs}"
                self.nb_erreurs.update()
                counter_verif += 1

            elif item[6] > 20:
                erreurs.append({"numero": valeurs.index(item) + 1, "details": item, "nature erreur": "note > 20"})
                nb_erreurs += 1
                self.nb_erreurs.value = f"{nb_erreurs}"
                self.nb_erreurs.update()
                counter_verif += 1

            else:
                bons.append({"numero": valeurs.index(item) + 1, "details": item, "nature erreur": "OK"})
                nb_succes += 1
                self.nb_succes.value = f"{nb_succes}"
                self.nb_succes.update()
                counter_verif += 1

        if len(erreurs) > 0:
            for row in self.table_erreurs.rows[:]:
                self.table_erreurs.rows.remove(row)

            self.import_result_title.value = f"{len(erreurs)} Erreurs dans le fichier. Corrigez puis reimportez"
            self.import_result_title.color = "red"
            self.import_result_title.update()

            for erreur in erreurs:
                self.table_erreurs.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(erreur['numero'])),
                            ft.DataCell(ft.Text(erreur['details'][0])),
                            ft.DataCell(ft.Text(erreur['details'][2])),
                            ft.DataCell(ft.Text(erreur['details'][4])),
                            ft.DataCell(ft.Text(erreur['details'][6])),
                            ft.DataCell(ft.Text(erreur['nature erreur'], color="red")),
                        ]
                    )
                )
            self.table_erreurs.update()

        else:
            for row in self.table_erreurs.rows[:]:
                self.table_erreurs.rows.remove(row)

            for note in bons:
                be.add_notes(
                    note['details'][0], note['details'][1], note['details'][2], note['details'][3],
                    note['details'][4], note['details'][5], note['details'][6], user_infos['nom']
                )
                counter_import += 1
                self.import_bar.value = counter_import / len(bons)
                self.import_bar.update()
                self.progres.value = f"{be.ecrire_nombre(counter_import * 100 / len(valeurs))} %"
                self.progres.update()

            self.import_result_title.value = f"{len(bons)} lignes importées avec succès"
            self.import_result_title.color = "green"
            self.import_result_title.update()

            for erreur in bons:
                self.table_erreurs.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(erreur['numero'])),
                            ft.DataCell(ft.Text(erreur['details'][0])),
                            ft.DataCell(ft.Text(erreur['details'][2])),
                            ft.DataCell(ft.Text(erreur['details'][4])),
                            ft.DataCell(ft.Text(erreur['details'][6])),
                            ft.DataCell(ft.Text(erreur['nature erreur'], color="green")),
                        ]
                    )
                )
            self.table_erreurs.update()

    @staticmethod
    def bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.1
            e.control.update()
        else:
            e.control.scale = 1
            e.control.update()