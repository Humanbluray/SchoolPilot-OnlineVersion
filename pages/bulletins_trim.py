from utils import *
from utils import backend as be
import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_pdf_fonts():
    pdfmetrics.registerFont(TTFont('vinci sans medium', "../assets/fonts/vinci_sans_medium.ttf"))
    pdfmetrics.registerFont(TTFont('vinci sans regular', "../assets/fonts/vinci_sans_regular.ttf"))
    pdfmetrics.registerFont(TTFont('vinci sans bold', "../assets/fonts/vinci_sans_bold.ttf"))
    pdfmetrics.registerFont(TTFont('calibri', "../assets/fonts/calibri.ttf"))
    pdfmetrics.registerFont(TTFont('calibri italic', "../assets/fonts/calibrii.ttf"))
    pdfmetrics.registerFont(TTFont('calibri bold', "../assets/fonts/calibrib.ttf"))
    pdfmetrics.registerFont(TTFont('calibri z', "../assets/fonts/calibriz.ttf"))
    pdfmetrics.registerFont(TTFont('Poppins SemiBold', "../assets/fonts/Poppins-SemiBold.ttf"))
    pdfmetrics.registerFont(TTFont('Poppins Bold', "../assets/fonts/Poppins-Bold.ttf"))


def trouver_sequence(sequence):
    if sequence.lower() == "trimestre 1":
        return "premiere trimestre"
    elif sequence.lower() == "trimestre 2":
        return "deuxieme trimestre"
    else:
        return "sixieme trimestre"


class BullTrim(ft.Tab):
    def __init__(self, cp: object):
        super(BullTrim, self).__init__(
            tab_content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.FOLDER_SPECIAL, size=20),
                    ft.Text("Trimestres".upper(), font_family="Poppins Medium", size=12)
                ]
            )
        )
        self.cp = cp  # Conteneur parent
        self.classe = ft.Dropdown(**drop_style, prefix_icon="school_outlined", label="classe", width=150)
        self.sequence = ft.Dropdown(**drop_style, prefix_icon=ft.icons.CALENDAR_MONTH_SHARP, label="Trimestre", width=150)
        self.taux_trim = ft.Text("0", size=12, font_family="Poppins Bold", color="black")
        self.info_classe_trim = ft.Text("-", size=12, font_family="Poppins Bold", color="black")
        self.titus_trim = ft.Text("-", size=12, font_family="Poppins Bold", color="black")
        self.effectif_trim = ft.Text("0", size=12, font_family="Poppins Bold", color="black")
        self.moygen_trim = ft.Text("0", size=12, font_family="Poppins Bold", color="black")
        self.notemin_trim = ft.Text("0", size=12, font_family="Poppins Bold", color="black")
        self.notemax_trim = ft.Text("0", size=12, font_family="Poppins Bold", color="black")

        self.info_container = ft.Row(
            visible=False,
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.ACCOUNT_BALANCE_OUTLINED, size=18, color="black"),
                                    ft.Text("Classe", size=11, font_family="Poppins Medium", color="grey"),

                                ]
                            ),
                            self.info_classe_trim
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    visible=False,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Titulaie", size=11, font_family="Poppins Medium", color="grey"),
                                ]
                            ),
                            self.titus_trim
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon('group_outlined', size=18, color="black"),
                                    ft.Text("Effectif", size=11, font_family="Poppins Medium", color="grey"),
                                ]
                            ),
                            self.effectif_trim
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.BAR_CHART_OUTLINED, size=18, color="black"),
                                    ft.Text("Moy générale", size=11, font_family="Poppins Medium", color="grey"),
                                ]
                            ),
                            self.moygen_trim
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.CHECK_BOX_OUTLINED, color="black", size=18),
                                    ft.Text("Taux réussite", size=11, font_family="Poppins Medium", color="grey"),
                                ]
                            ),
                            self.taux_trim
                        ], spacing=3,  horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.ARROW_CIRCLE_UP_OUTLINED, size=18, color="black"),
                                    ft.Text("Note min", size=11, font_family="Poppins Medium", color="grey"),
                                ]
                            ),
                            self.notemin_trim
                        ], spacing=3,  horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.ARROW_CIRCLE_DOWN_OUTLINED, size=18, color="black"),
                                    ft.Text("Note Max", size=11, font_family="Poppins Medium", color="grey"),
                                ]
                            ),
                            self.notemax_trim
                        ], spacing=3,  horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.table_seq = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("")),
                ft.DataColumn(label=ft.Text("CLasse")),
                ft.DataColumn(label=ft.Text("Séquence")),
                ft.DataColumn(label=ft.Text("ELève")),
                ft.DataColumn(label=ft.Text("Moyenne")),
                ft.DataColumn(label=ft.Text("Rang")),
                ft.DataColumn(label=ft.Text("Actions")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )
        self.table_details = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Matière")),
                ft.DataColumn(label=ft.Text("Coeff")),
                ft.DataColumn(label=ft.Text("Note")),
                ft.DataColumn(label=ft.Text("Note * coeff")),
                ft.DataColumn(label=ft.Text("Cote")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )

        # details bulletin un eleve
        self.title_details = ft.Text(size=12, font_family="Poppins Medium", color="black")
        self.moy_eleve = ft.Text(size=12, font_family="Poppins Medium", visible=False, color=ft.colors.AMBER)
        self.rang_eleve = ft.Text(size=12, font_family="Poppins Medium", visible=False, color=ft.colors.AMBER)
        self.classe_eleve = ft.Text(size=12, font_family="Poppins Medium", visible=False, color=ft.colors.AMBER)
        self.seq_eleve = ft.Text(size=12, font_family="Poppins Medium", visible=False, color=ft.colors.AMBER)
        self.cp.cp.fp_onebull_trim.on_result = self.imprimer_un_bulletin
        self.details_window = ft.Card(
            elevation=50, surface_tint_color="#f0f0f6", width=700, height=500,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                expand=True,
                padding=20, bgcolor="#f0f0f6",
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=10, border_radius=12, bgcolor="white",
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Row(
                                                [
                                                    ft.Icon(ft.icons.NOTE_ALT_OUTLINED, color="red"),
                                                    self.title_details
                                                ]
                                            ),
                                            self.moy_eleve, self.rang_eleve, self.classe_eleve, self.seq_eleve,
                                            ft.Container(
                                                scale=ft.transform.Scale(1),
                                                animate_scale=ft.animation.Animation(300,
                                                                                     ft.AnimationCurve.FAST_OUT_SLOWIN),
                                                on_hover=self.icon_bt_hover2,
                                                content=ft.IconButton(
                                                    ft.icons.PRINT_OUTLINED, scale=1,
                                                    icon_color=ft.colors.BLACK45,
                                                    on_click=lambda e: self.cp.cp.fp_onebull_trim.save_file(
                                                        allowed_extensions=["pdf"]),
                                                    tooltip="Supprimer filtres",
                                                )
                                            ),
                                        ]
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, bgcolor="#f0f0f6", icon_color="#292f4c", scale=0.7,
                                        on_click=self.close_details_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white", expand=True, width=700,
                            content=ft.ListView(
                                expand=True,
                                controls=[self.table_details]
                            )
                        )
                    ]
                )
            )
        )

        # fenetre de selections classe et séquence
        self.pb_bull = ft.ProgressBar(
            value=0, bar_height=7, width=200, bgcolor="grey100", color="amber", border_radius=12
        )
        self.sel_classe_trim = ft.Dropdown(
            **drop_style, width=170, label="Classe", prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED
        )
        self.sel_seq_trim = ft.Dropdown(
            **drop_style, width=150, label="Trimestre", prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED
        )
        self.progres = ft.Text(size=12, font_family="Poppins Italic", color="grey")
        self.cp.cp.fp_allbull_trim.on_result = self.imprimer_all_bulletins
        self.select_window = ft.Card(
            elevation=50, surface_tint_color="#f0f0f6", width=300, height=400,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                expand=True,
                padding=20, bgcolor="#f0f0f6",
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=10, bgcolor="white", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Text("Bulletins d'une classe".upper(), size=14, font_family="Poppins Medium"),
                                    ft.IconButton("close", scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                                  on_click=self.close_select_window
                                                  )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, bgcolor="white", border_radius=12, width=300,
                            content=ft.Column(
                                controls=[
                                    self.sel_classe_trim, self.sel_seq_trim, self.progres, self.pb_bull,
                                    ft.ElevatedButton(
                                        **choix_style, width=170,
                                        on_click=lambda e: self.cp.cp.fp_allbull_trim.save_file(
                                            allowed_extensions=['pdf'])
                                    )
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
                ft.Container(
                    padding=ft.padding.only(20, 0, 20, 0), expand=True, bgcolor="white", border_radius=12,
                    margin=ft.margin.only(top=10),
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.Row(
                                []
                            ),
                            ft.Divider(height=2, color="transparent"),
                            ft.Row(
                                controls=[
                                    ft.Text("Bulletins trimestre".upper(), size=14, font_family="Poppins Medium"),
                                    AnyButton(SECOND_COLOR, "print_outlined", "Classe", "white", self.open_select_window),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Container(
                                expand=True, padding=0,
                                content=ft.Column(
                                    expand=True,
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Row(
                                                    controls=[
                                                        ft.Row([self.classe, self.sequence, ],
                                                               spacing=20),
                                                        ft.Row(
                                                            controls=[
                                                                ft.Container(
                                                                    border=ft.border.all(1, "grey"),
                                                                    border_radius=6, bgcolor="#f0f0f6", padding=5,
                                                                    on_click=self.filter_datas_seq,
                                                                    scale=ft.transform.Scale(1),
                                                                    animate_scale=ft.animation.Animation(300,
                                                                                                         ft.AnimationCurve.FAST_OUT_SLOWIN),
                                                                    on_hover=self.icon_bt_hover2,
                                                                    tooltip="filtrer",
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
                                                                    animate_scale=ft.animation.Animation(300,
                                                                                                         ft.AnimationCurve.FAST_OUT_SLOWIN),
                                                                    on_hover=self.icon_bt_hover2,
                                                                    tooltip="Supprimer filtres",
                                                                    content=ft.Icon(
                                                                        ft.icons.FILTER_ALT_OFF_OUTLINED,
                                                                        color=ft.colors.BLACK45,
                                                                    )
                                                                ),
                                                            ]
                                                        )
                                                    ], spacing=20
                                                ),

                                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        ),
                                        ft.ListView(
                                            expand=True,
                                            controls=[self.table_seq]
                                        ),
                                    ]
                                )
                            ),
                            self.info_container,
                        ],
                    )
                ),
                self.details_window, self.select_window
                # autre stack
            ], alignment=ft.alignment.center
        )
        self.load_lists()

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

    @staticmethod
    def icon_bt_hover(e):
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

    def load_lists(self):
        classes = be.show_classes_prim()
        for classe in classes:
            self.classe.options.append(ft.dropdown.Option(classe))
            self.sel_classe_trim.options.append(ft.dropdown.Option(classe))

        sequences = ['trimestre 1', 'trimestre 2', 'trimestre 3']
        for sequence in sequences:
            self.sequence.options.append(ft.dropdown.Option(sequence.upper()))
            self.sel_seq_trim.options.append(ft.dropdown.Option(sequence.upper()))

    def filter_datas_seq(self, e):
        datas = be.bull_trim()
        bulls = []

        for data in datas:
            dico = {
                "asco": data[0], "classe": data[1], "sequence": data[3], "nom": data[4],
                "nb_coeff": data[7], "total": data[6], "moyenne": data[8], "rang": data[9]
            }
            bulls.append(dico)

        for row in self.table_seq.rows[:]:
            self.table_seq.rows.remove(row)

        une_classe = self.classe.value if self.classe.value is not None else ""
        une_sequence = self.sequence.value if self.sequence.value is not None else ""

        # print(bulls)
        filter_datas = []
        for row in bulls:
            if row['classe'] == une_classe and row['sequence'] == une_sequence.lower():
                filter_datas.append(row)

        # print(filter_datas)

        if une_classe == "" or une_sequence == "":
            pass

        else:
            self.info_classe_trim.value = self.classe.value
            self.effectif_trim.value = be.effectif_classe(self.classe.value)
            self.moygen_trim.value = f"{(be.moygen_trim(self.classe.value, self.sequence.value.lower())):.2f}"
            self.notemax_trim.value = f"{(be.notemax_trim(self.classe.value, self.sequence.value.lower())):.2f}"
            self.notemin_trim.value = f"{(be.notemin_trim(self.classe.value, self.sequence.value.lower())):.2f}"
            nb_admis = be.nb_admis_trim(self.classe.value, self.sequence.value.lower())
            taux = nb_admis * 100 / be.effectif_classe(self.classe.value)
            self.taux_trim.value = f"{taux:.2f} %"
            self.titus_trim.value = be.search_titus(self.classe.value)
            for widget in (
                    self.effectif_trim, self.moygen_trim, self.notemax_trim,
                    self.notemin_trim, self.taux_trim, self.titus_trim,
                    self.info_classe_trim
            ):
                widget.update()

            for bull in filter_datas:
                if bull['moyenne'] >= 10:
                    icone = ft.icons.CHECK_BOX_OUTLINED
                    color = "teal"
                else:
                    icone = ft.icons.CLOSE
                    color = "red"

                self.table_seq.rows.append(
                    ft.DataRow(
                        data=bull,
                        cells=[
                            ft.DataCell(ft.Icon(icone, color=color, size=18)),
                            ft.DataCell(ft.Text(bull['classe'])),
                            ft.DataCell(ft.Text(bull['sequence'])),
                            ft.DataCell(ft.Text(bull['nom'])),
                            ft.DataCell(ft.Text(f"{bull['moyenne']:.2f}")),
                            ft.DataCell(ft.Text(bull['rang'])),
                            ft.DataCell(
                                ft.Container(
                                    scale=ft.transform.Scale(1),
                                    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                    on_hover=self.icon_bt_hover2,
                                    content=ft.IconButton(
                                        ft.icons.EDIT_OUTLINED, scale=1,
                                        icon_color=ft.colors.BLACK45,
                                        on_click=self.view_details,
                                        tooltip="Voir details",
                                        data=bull,
                                    )
                                ),
                            ),
                        ]
                    )
                )

            self.table_seq.update()

    def supp_filtres(self, e):
        self.classe.value = None
        self.sequence.value = None
        self.classe.update()
        self.sequence.update()

        for row in self.table_seq.rows[:]:
            self.table_seq.rows.remove(row)

        self.table_seq.update()

        self.info_classe_trim.value = "-"
        self.effectif_trim.value = "0"
        self.moygen_trim.value = "0"
        self.notemax_trim.value = "0"
        self.notemin_trim.value = "0"
        self.taux_trim.value = "0"

        for widget in (
                self.effectif_trim, self.moygen_trim, self.notemax_trim,
                self.notemin_trim, self.taux_trim, self.titus_trim,
                self.info_classe_trim
        ):
            widget.update()

    def view_details(self, e):
        for row in self.table_details.rows[:]:
            self.table_details.rows.remove(row)

        details = be.detail_bull_trim(e.control.data['classe'], e.control.data['sequence'], e.control.data['nom'])
        # details = []
        #
        # for data in donnees:
        #     details.append(
        #         {
        #             'matiere': data[5], 'coeff': be.ecrire_nombre(data[8]), 'note': be.ecrire_nombre(data[7]),
        #             'nc': be.ecrire_nombre(data[9]), 'cote': data[10]
        #         }
        #     )

        for data in details:
            self.table_details.rows.append(
                ft.DataRow(
                    data=data,
                    cells=[
                        ft.DataCell(ft.Text(data['matiere'])),
                        ft.DataCell(ft.Text(data['coeff'])),
                        ft.DataCell(ft.Text(data['note'])),
                        ft.DataCell(ft.Text(data['total'])),
                        ft.DataCell(ft.Text(data['cote'])),
                    ]
                )
            )

        self.table_details.update()

        self.title_details.value = e.control.data['nom']
        self.classe_eleve.value = e.control.data['classe']
        self.rang_eleve.value = e.control.data['rang']
        self.moy_eleve.value = e.control.data['moyenne']
        self.seq_eleve.value = e.control.data['sequence']

        for widget in (
                self.classe_eleve, self.rang_eleve, self.moy_eleve,
                self.seq_eleve, self.title_details
        ):
            widget.update()

        self.details_window.scale = 1
        self.details_window.update()

    def close_details_window(self, e):
        self.details_window.scale = 0
        self.details_window.update()

    def open_select_window(self, e):
        self.select_window.scale = 1
        self.select_window.update()

    def close_select_window(self, e):
        self.select_window.scale = 0
        self.select_window.update()

    def imprimer_un_bulletin(self, e: ft.FilePickerResultEvent):
        save_location = f"{e.path}.pdf"
        fichier = os.path.abspath(save_location)
        can = Canvas("{0}".format(fichier), pagesize=A4)
        create_pdf_fonts()

        asco = be.show_asco_encours()

        if save_location != "None.pdf":
            niveau = be.look_nivo(self.classe_eleve.value)
            cycle = be.cycle_par_niveau(niveau)

            # bulletin des classes du premier cycle
            if cycle == "premier":
                gauche, droite, y = 4.25, 17.25, 28

                # gauche, droite, y = 4.25, 17.75, 28
                def draw_headers():
                    # A gauche
                    can.setFillColorRGB(0, 0, 0)
                    can.setFont("calibri bold", 10)
                    can.drawCentredString(gauche * cm, 28.5 * cm, "Republique du Cameroun".upper())
                    can.setFont("calibri z", 9)
                    can.drawCentredString(gauche * cm, 28.1 * cm, "Paix - Travail - Patrie".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(gauche * cm, 27.7 * cm, "*************")
                    can.setFont("calibri", 9)
                    can.drawCentredString(gauche * cm, 27.3 * cm, "Ministere des enseignements secondaires".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(gauche * cm, 26.9 * cm, "*************")
                    can.setFont("calibri bold", 10)
                    can.drawCentredString(gauche * cm, 26.5 * cm, "Delegation régionale du centre".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(gauche * cm, 26.1 * cm, "*************")
                    can.drawCentredString(gauche * cm, 25.7 * cm, "Délégation departementale du mfoundi".upper())
                    can.drawCentredString(gauche * cm, 25.3 * cm, "*************")
                    can.drawCentredString(gauche * cm, 24.9 * cm, "NOM DU COLLEGE".upper())

                    # A droite
                    can.setFillColorRGB(0, 0, 0)
                    can.setFont("calibri bold", 10)
                    can.drawCentredString(droite * cm, 28.5 * cm, "Republique du Cameroun".upper())
                    can.setFont("calibri z", 9)
                    can.drawCentredString(droite * cm, 28.1 * cm, "Paix - Travail - Patrie".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(droite * cm, 27.7 * cm, "*************")
                    can.setFont("calibri", 9)
                    can.drawCentredString(droite * cm, 27.3 * cm, "Ministere des enseignements secondaires".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(droite * cm, 26.9 * cm, "*************")
                    can.setFont("calibri bold", 10)
                    can.drawCentredString(droite * cm, 26.5 * cm, "Delegation régionale du centre".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(droite * cm, 26.1 * cm, "*************")
                    can.drawCentredString(droite * cm, 25.7 * cm, "Délégation departementale du mfoundi".upper())
                    can.drawCentredString(droite * cm, 25.3 * cm, "*************")
                    can.drawCentredString(droite * cm, 24.9 * cm, "NOM DU COLLEGE".upper())

                    # Le logo
                    monlogo = "assets/mon logo.png"
                    can.drawImage(monlogo, 9 * cm, 26 * cm)

                    # entetes année scolaire et séquence
                    can.setFont("calibri bold", 15)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(10.5 * cm, 24 * cm, f"bulletin scolaire {trouver_sequence(self.seq_eleve.value)}".upper())

                    can.setFont("calibri", 12)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(10.5 * cm, 23.5 * cm, f"Année scolaire {asco - 1} / {asco}")

                    # infos sur l'élève ________________________

                    # Lignes horizontales
                    # 1ere ligne
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    can.line(4 * cm, 23 * cm, 20 * cm, 23 * cm)

                    # Lignes du milieu
                    can.line(4 * cm, 22.3 * cm, 20 * cm, 22.3 * cm)
                    can.line(4 * cm, 21.6 * cm, 20 * cm, 21.6 * cm)
                    can.line(4 * cm, 20.9 * cm, 16 * cm, 20.9 * cm)

                    # Dernière ligne
                    can.line(4 * cm, 19.7 * cm, 20 * cm, 19.7 * cm)

                    # Lignes verticales
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    # 1ere ligne
                    can.line(4 * cm, 23 * cm, 4 * cm, 19.7 * cm)

                    can.line(11 * cm, 21.6 * cm, 11 * cm, 20.9 * cm)
                    can.line(13.5 * cm, 22.3 * cm, 13.5 * cm, 21.6 * cm)
                    can.line(16 * cm, 23 * cm, 16 * cm, 19.7 * cm)

                    # Dernière ligne
                    can.line(20 * cm, 23 * cm, 20 * cm, 19.7 * cm)

                    # champs d'informations
                    can.setFont("calibri", 10)
                    can.drawString(4.2 * cm, 22.5 * cm, "Nom de l'élève:")
                    can.drawString(16.2 * cm, 22.5 * cm, "Classe:")
                    can.drawString(4.2 * cm, 21.8 * cm, "Date et lieu de naissance:")
                    can.drawString(13.8 * cm, 21.8 * cm, "Genre:")
                    can.drawString(16.2 * cm, 21.8 * cm, "Effectif:")
                    can.setFillColorRGB(1, 0, 0)
                    can.drawString(4.2 * cm, 21.1 * cm, "Identifiant unique:")
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(11.2 * cm, 21.1 * cm, "Redoublant: oui          non")
                    can.drawString(16.2 * cm, 21.1 * cm, "Professeur principal:")
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(4.2 * cm, 20.4 * cm, "Noms et contact des parents/tuteurs:")

                    # remplissage des informations
                    can.setFont("calibri bold", 11)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(6.7 * cm, 22.5 * cm, f"{self.title_details.value}")

                    infos = be.search_elev_by_nom(self.title_details.value)
                    can.drawString(17.4 * cm, 22.5 * cm, f"{self.classe_eleve.value}")
                    # Date et lieu de naissance
                    can.drawString(8 * cm, 21.8 * cm, f"{infos[2]} à {infos[3]}")
                    # sexe
                    can.drawString(15.2 * cm, 21.8 * cm, f"{infos[4]}")
                    # Effectif
                    can.drawString(17.8 * cm, 21.8 * cm, f"{be.effectif_classe(self.classe_eleve.value)}")
                    # Contact parents
                    can.drawString(4.2 * cm, 19.9 * cm, f"{infos[5]} / {infos[7]}")

                    prof_titus = be.search_titus(self.classe_eleve.value)
                    sep = prof_titus.split(" ")
                    can.drawString(16.2 * cm, 20.7 * cm, f"{sep[0]}")
                    can.drawString(16.2 * cm, 20.3 * cm, f"{sep[1]}")

                    # Pied de page
                    pied = f"Bulletin / {asco - 1}-{asco} / {self.seq_eleve.value} / {self.classe_eleve.value} / {self.title_details.value}".upper()
                    can.setFont("calibri", 9)
                    can.setFillColorRGB(0.5, 0.5, 0.5)
                    can.drawCentredString(10.5 * cm, 0.5 * cm, pied)

                draw_headers()

                # divisions pour les lignes horizontales
                b1, b2, b3, b4, b5, b6, b7, b8, = 1, 10, 11.5, 12.5, 14, 15, 17, 20

                # divisions pour les lignes verticales
                m1 = (b1 + b2) / 2
                m2 = (b2 + b3) / 2
                m3 = (b3 + b4) / 2
                m4 = (b4 + b5) / 2
                m5 = (b5 + b6) / 2
                m6 = (b6 + b7) / 2
                m7 = (b7 + b8) / 2

                def draw_entetes():
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)

                    # Lignes horizontales
                    can.line(1 * cm, 19.4 * cm, 20 * cm, 19.4 * cm)
                    can.line(1 * cm, 18.8 * cm, 20 * cm, 18.8 * cm)

                    # Lignes verticales
                    can.line(b1 * cm, 18.8 * cm, b1 * cm, 19.4 * cm)
                    can.line(b2 * cm, 18.8 * cm, b2 * cm, 19.4 * cm)
                    can.line(b3 * cm, 18.8 * cm, b3 * cm, 19.4 * cm)
                    can.line(b4 * cm, 18.8 * cm, b4 * cm, 19.4 * cm)
                    can.line(b5 * cm, 18.8 * cm, b5 * cm, 19.4 * cm)
                    can.line(b6 * cm, 18.8 * cm, b6 * cm, 19.4 * cm)
                    can.line(b7 * cm, 18.8 * cm, b7 * cm, 19.4 * cm)
                    can.line(b8 * cm, 18.8 * cm, b8 * cm, 19.4 * cm)

                    can.setFont("calibri bold", 10)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(m1 * cm, 19 * cm, "Matiere")
                    can.drawCentredString(m2 * cm, 19 * cm, "M/20")
                    can.drawCentredString(m3 * cm, 19 * cm, "Coef")
                    can.drawCentredString(m4 * cm, 19 * cm, "M x coef")
                    can.drawCentredString(m5 * cm, 19 * cm, "Cote")

                    can.setFillColorRGB(1, 0, 0)
                    can.drawCentredString(m6 * cm, 19 * cm, "Min-Max")
                    can.drawCentredString(m7 * cm, 19 * cm, "Appreciation")
                    can.setFillColorRGB(0, 0, 0)

                draw_entetes()

                y = 19

                details_notes = be.detail_bull_trim(
                    self.classe_eleve.value, self.seq_eleve.value.lower(), self.title_details.value
                )
                total_general = 0
                total_coeff_general = 0

                # eriture des notes en fonction des groupes
                for data in details_notes:
                    can.setFillColorRGB(0, 0, 0)
                    can.setFont("calibri", 10)
                    can.drawCentredString(m1 * cm, (y - 0.6) * cm, f"{data['matiere']}")  # Matiere

                    if "D" in data['cote']:
                        can.setFillColorRGB(1, 0, 0)
                    elif "A" in data['cote']:
                        can.setFillColorRGB(0, 0.48, 0.22)
                    else:
                        can.setFillColorRGB(0, 0, 0)

                    can.drawCentredString(m2 * cm, (y - 0.6) * cm, f"{data['note']}")  # Note / 20

                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(m3 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data['coeff'])}")  # Coefficient
                    can.drawCentredString(m4 * cm, (y - 0.6) * cm, f"{data['total']}")

                    if "D" in data['cote']:
                        can.setFillColorRGB(1, 0, 0)
                    elif "A" in data['cote']:
                        can.setFillColorRGB(0, 0.48, 0.22)
                    else:
                        can.setFillColorRGB(0, 0, 0)

                    can.drawCentredString(m5 * cm, (y - 0.6) * cm, f"{data['cote']}")

                    can.setFillColorRGB(0, 0, 0)
                    note_min = be.note_min_mat_trim(self.classe_eleve.value, data['matiere'], self.seq_eleve.value)
                    note_max = be.note_max_mat_trim(self.classe_eleve.value, data['matiere'], self.seq_eleve.value)
                    can.drawCentredString(m6 * cm, (y - 0.6) * cm, f"{note_min} - {note_max}")

                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    can.line(1 * cm, (y - 0.8) * cm, 20 * cm, (y - 0.8) * cm)

                    # Lignes verticales
                    can.line(b1 * cm, (y - 0.7) * cm, b1 * cm, (y - 0) * cm)
                    can.line(b2 * cm, (y - 0.7) * cm, b2 * cm, (y - 0) * cm)
                    can.line(b3 * cm, (y - 0.7) * cm, b3 * cm, (y - 0) * cm)
                    can.line(b4 * cm, (y - 0.7) * cm, b4 * cm, (y - 0) * cm)
                    can.line(b5 * cm, (y - 0.7) * cm, b5 * cm, (y - 0) * cm)
                    can.line(b6 * cm, (y - 0.7) * cm, b6 * cm, (y - 0) * cm)
                    can.line(b7 * cm, (y - 0.7) * cm, b7 * cm, (y - 0) * cm)
                    can.line(b8 * cm, (y - 0.7) * cm, b8 * cm, (y - 0) * cm)

                    total_coeff_general += data['coeff']
                    total_general += data['total']

                    y -= 0.7

                y = y - 1

                def draw_recap():
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    can.line(1 * cm, (y + 0.1) * cm, 20 * cm, (y + 0.1) * cm)
                    can.line(b1 * cm, (y + 1) * cm, b1 * cm, (y + 0.1) * cm)
                    can.line(b3 * cm, (y + 1) * cm, b3 * cm, (y + 0.1) * cm)
                    can.line(b4 * cm, (y + 1) * cm, b4 * cm, (y + 0.1) * cm)
                    can.line(b5 * cm, (y + 1) * cm, b5 * cm, (y + 0.1) * cm)
                    can.line(b7 * cm, (y + 1) * cm, b7 * cm, (y + 0.1) * cm)
                    can.line(b8 * cm, (y + 1) * cm, b8 * cm, (y + 0.1) * cm)

                    can.setFont("calibri bold", 11)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawRightString((b3 - 0.2) * cm, (y + 0.4) * cm, "TOTAL")
                    can.drawRightString((b7 - 0.2) * cm, (y + 0.4) * cm, "MOYENNE")
                    can.drawCentredString(m3 * cm, (y + 0.4) * cm, f"{be.ecrire_nombre(total_coeff_general)}")
                    can.drawCentredString(m4 * cm, (y + 0.4) * cm, f"{be.ecrire_nombre(total_general)}")
                    can.drawCentredString(m7 * cm, (y + 0.4) * cm, f"{(be.ecrire_nombre(total_general / total_coeff_general))}")

                draw_recap()

                # Statistiques
                def draw_cadre_stats():

                    # lignes horizontales
                    can.setFillColorRGB(0.75, 0.75, 0.75)
                    can.line(1 * cm, (y - 0.3) * cm, 20 * cm, (y - 0.3) * cm)
                    can.line(1 * cm, (y - 0.9) * cm, 20 * cm, (y - 0.9) * cm)

                    # Lignes verticales
                    can.line(1 * cm, (y - 0.3) * cm, 1 * cm, (y - 0.9) * cm)
                    can.line(7.3 * cm, (y - 0.3) * cm, 7.3 * cm, (y - 0.9) * cm)
                    can.line(13.6 * cm, (y - 0.3) * cm, 13.6 * cm, (y - 0.9) * cm)
                    can.line(20 * cm, (y - 0.3) * cm, 20 * cm, (y - 0.9) * cm)

                    # cadre stats divisons principales
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    can.line(1 * cm, (y - 0.3) * cm, 1 * cm, (y - 6) * cm)
                    can.line(7.3 * cm, (y - 0.3) * cm, 7.3 * cm, (y - 6) * cm)
                    can.line(13.6 * cm, (y - 0.3) * cm, 13.6 * cm, (y - 6) * cm)
                    can.line(20 * cm, (y - 0.3) * cm, 20 * cm, (y - 6) * cm)
                    can.line(1 * cm, (y - 4) * cm, 20 * cm, (y - 4) * cm)
                    can.line(1 * cm, (y - 6) * cm, 20 * cm, (y - 6) * cm)

                    # divisons verticales secondaires
                    # Discipline
                    can.line(3.15 * cm, (y - 0.9) * cm, 3.15 * cm, (y - 4) * cm)
                    can.line(4.15 * cm, (y - 0.9) * cm, 4.15 * cm, (y - 4) * cm)
                    can.line(6.3 * cm, (y - 0.9) * cm, 6.3 * cm, (y - 4) * cm)
                    # Travail de l'élève
                    can.line(9.3 * cm, (y - 0.9) * cm, 9.3 * cm, (y - 4) * cm)
                    can.line(10.8 * cm, (y - 0.9) * cm, 10.8 * cm, (y - 4) * cm)
                    can.line(12.8 * cm, (y - 1.675) * cm, 12.8 * cm, (y - 4) * cm)
                    can.line(12.8 * cm, (y - 1.675) * cm, 12.8 * cm, (y - 4) * cm)
                    # Profil
                    can.line(17 * cm, (y - 0.9) * cm, 17 * cm, (y - 4) * cm)

                    # divisions horizontales secondaire
                    can.line(1 * cm, (y - 1.675) * cm, 20 * cm, (y - 1.675) * cm)
                    can.line(1 * cm, (y - 2.45) * cm, 20 * cm, (y - 2.45) * cm)
                    can.line(1 * cm, (y - 3.225) * cm, 20 * cm, (y - 3.225) * cm)

                    can.line(10.8 * cm, (y - 2.0125) * cm, 13.6 * cm, (y - 2.0125) * cm)
                    can.line(10.8 * cm, (y - 2.7875) * cm, 13.6 * cm, (y - 2.7875) * cm)

                    # divisons horizontales tertiares

                    can.setFont("calibri", 9)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(1.2 * cm, (y - 1.375) * cm, "Abs non J.")
                    can.drawString(1.2 * cm, (y - 1.375) * cm, "Abs non J. (h)")
                    can.drawString(1.2 * cm, (y - 2.15) * cm, "Abs just. (h)")
                    can.drawString(1.2 * cm, (y - 2.925) * cm, "Retards (nb) ")
                    can.drawString(1.2 * cm, (y - 3.7) * cm, "Consignes (h) ")
                    can.drawString(4.21 * cm, (y - 1.375) * cm, "Avertissement")
                    can.drawString(4.21 * cm, (y - 2.15) * cm, "Blâme")
                    can.drawString(4.21 * cm, (y - 2.925) * cm, f"Exclusions (j)")
                    can.drawString(4.21 * cm, (y - 3.7) * cm, f"Exclusion (def)")

                    # remplissage sanctions
                    can.setFont("calibri bold", 10)
                    abs_nj = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value.upper(),
                                                      'ABSENCE NJ.')
                    abs_jus = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value.upper(),
                                                       'ABSENCE JUST.')
                    avert = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value.upper(),
                                                     'AVERTISSEMENT')
                    blame = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value.upper(), 'BLAME')
                    consigne = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value.upper(),
                                                        'CONSIGNE')
                    exclusion = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value.upper(),
                                                         'EXCLUSION')
                    exclu_def = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value.upper(),
                                                         'EXCLUSION DEF.')
                    retard = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value.upper(), 'RETARD')

                    can.drawCentredString(3.65 * cm, (y - 1.375) * cm, f"{abs_nj}")
                    can.drawCentredString(3.65 * cm, (y - 2.15) * cm, f"{abs_jus}")
                    can.drawCentredString(3.65 * cm, (y - 2.925) * cm, f"{retard}")
                    can.drawCentredString(3.65 * cm, (y - 3.7) * cm, f"{consigne}")
                    can.drawCentredString(6.8 * cm, (y - 1.375) * cm, f"{avert}")
                    can.drawCentredString(6.8 * cm, (y - 2.15) * cm, f"{blame}")
                    can.drawCentredString(6.8 * cm, (y - 2.925) * cm, f"{exclusion}")
                    can.drawCentredString(6.8 * cm, (y - 3.7) * cm, f"{exclu_def}")

                    # travail de l'élève
                    can.setFont("calibri", 10)
                    can.drawString(7.5 * cm, (y - 1.375) * cm, "Total Gén.".upper())
                    can.drawString(7.5 * cm, (y - 2.15) * cm, "Coef".upper())
                    can.drawString(7.5 * cm, (y - 2.925) * cm, "Moyenne".upper())
                    can.drawString(7.5 * cm, (y - 3.7) * cm, f"Cote".upper())

                    can.setFont("calibri bold", 10)
                    can.drawString(11 * cm, (y - 1.375) * cm, "appreciations.".upper())
                    can.setFont("calibri", 8)
                    can.drawString(11 * cm, (y - 1.9625) * cm, "CTBA")
                    can.drawString(11 * cm, (y - 2.35) * cm, "CBA")
                    can.drawString(11 * cm, (y - 2.7375) * cm, "CA")
                    can.drawString(11 * cm, (y - 3.125) * cm, "CMA")
                    can.drawString(11 * cm, (y - 3.8125) * cm, "CNA")

                    # Remplissage du travail de l'élève
                    can.setFont("calibri bold", 11)
                    can.drawCentredString(10.05 * cm, (y - 1.375) * cm, f"{be.ecrire_nombre(total_general)}")
                    can.drawCentredString(10.05 * cm, (y - 2.15) * cm, f"{be.ecrire_nombre(total_coeff_general)}")
                    can.drawCentredString(10.05 * cm, (y - 2.925) * cm, f"{be.ecrire_nombre(self.moy_eleve.value)}")
                    can.drawCentredString(10.05 * cm, (y - 3.7) * cm, f"{be.trouver_cote(self.moy_eleve.value)}")

                    # Profil de la classe
                    can.setFont("calibri", 10)
                    can.drawString(13.8 * cm, (y - 1.375) * cm, "Moyenne générale")
                    can.setFillColorRGB(1, 0, 0)
                    can.setFont("calibri bold", 10)
                    can.drawString(13.8 * cm, (y - 2.15) * cm, "[Min-Max]")
                    can.setFont("calibri", 10)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(13.8 * cm, (y - 2.925) * cm, "Nb de moyennes")
                    can.drawString(13.8 * cm, (y - 3.7) * cm, f"Taux de réussite")

                    # Remplissage profil
                    can.setFont("calibri bold", 11)
                    can.drawCentredString(18.5 * cm, (y - 1.375) * cm, f"{self.moygen_trim.value}")
                    can.drawCentredString(18.5 * cm, (y - 2.15) * cm, f"{self.notemin_trim.value} - {self.notemax_trim.value}")
                    can.drawCentredString(18.5 * cm, (y - 2.925) * cm, f"{be.nb_admis_trim(self.classe_eleve.value, self.seq_eleve.value)}")
                    can.drawCentredString(18.5 * cm, (y - 3.7) * cm, f"{self.taux_trim.value}")

                draw_cadre_stats()

                # Entêtes des stats
                def draw_stats_entetes():
                    can.setFont("calibri bold", 11)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(4.15 * cm, (y - 0.7) * cm, "Discipline")
                    can.drawCentredString(10.45 * cm, (y - 0.7) * cm, "Travail de l'èlève")
                    can.drawCentredString(17.3 * cm, (y - 0.7) * cm, "Profil de la classe")

                    can.setFont("calibri", 9)
                    can.drawCentredString(4.15 * cm, (y - 4.4) * cm, "Appréciation du travail de l'élève")
                    can.drawCentredString(4.15 * cm, (y - 4.8) * cm, "(Points forts et points à améliorer)")

                    can.drawCentredString(8.8 * cm, (y - 4.4) * cm, "Visa du parent /")
                    can.drawCentredString(8.8 * cm, (y - 4.8) * cm, "tuteur")

                    can.drawCentredString(11.95 * cm, (y - 4.4) * cm, "Nom et visa du")
                    can.drawCentredString(11.95 * cm, (y - 4.8) * cm, "professeur titulaire")

                    can.drawCentredString(17.3 * cm, (y - 4.4) * cm, "Le chef d'établissement")

                draw_stats_entetes()

                can.save()
                self.cp.cp.box.title.value = "Validé !"
                self.cp.cp.box.content.value = "Bulletin créé avec succès"
                self.cp.cp.box.open = True
                self.cp.cp.box.update()

            # Bulletin des classes du second cycle
            else:
                gauche, droite, y = 4.25, 17.25, 28

                # gauche, droite, y = 4.25, 17.75, 28
                def draw_headers():
                    # A gauche
                    can.setFillColorRGB(0, 0, 0)
                    can.setFont("calibri bold", 10)
                    can.drawCentredString(gauche * cm, 28.5 * cm, "Republique du Cameroun".upper())
                    can.setFont("calibri z", 9)
                    can.drawCentredString(gauche * cm, 28.1 * cm, "Paix - Travail - Patrie".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(gauche * cm, 27.7 * cm, "*************")
                    can.setFont("calibri", 9)
                    can.drawCentredString(gauche * cm, 27.3 * cm, "Ministere des enseignements secondaires".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(gauche * cm, 26.9 * cm, "*************")
                    can.setFont("calibri bold", 10)
                    can.drawCentredString(gauche * cm, 26.5 * cm, "Delegation régionale du centre".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(gauche * cm, 26.1 * cm, "*************")
                    can.drawCentredString(gauche * cm, 25.7 * cm, "Délégation departementale du mfoundi".upper())
                    can.drawCentredString(gauche * cm, 25.3 * cm, "*************")
                    can.drawCentredString(gauche * cm, 24.9 * cm, "NOM DU COLLEGE".upper())

                    # A droite
                    can.setFillColorRGB(0, 0, 0)
                    can.setFont("calibri bold", 10)
                    can.drawCentredString(droite * cm, 28.5 * cm, "Republique du Cameroun".upper())
                    can.setFont("calibri z", 9)
                    can.drawCentredString(droite * cm, 28.1 * cm, "Paix - Travail - Patrie".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(droite * cm, 27.7 * cm, "*************")
                    can.setFont("calibri", 9)
                    can.drawCentredString(droite * cm, 27.3 * cm, "Ministere des enseignements secondaires".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(droite * cm, 26.9 * cm, "*************")
                    can.setFont("calibri bold", 10)
                    can.drawCentredString(droite * cm, 26.5 * cm, "Delegation régionale du centre".upper())
                    can.setFont("calibri", 9)
                    can.drawCentredString(droite * cm, 26.1 * cm, "*************")
                    can.drawCentredString(droite * cm, 25.7 * cm, "Délégation departementale du mfoundi".upper())
                    can.drawCentredString(droite * cm, 25.3 * cm, "*************")
                    can.drawCentredString(droite * cm, 24.9 * cm, "NOM DU COLLEGE".upper())

                    # Le logo
                    monlogo = "assets/mon logo.png"
                    can.drawImage(monlogo, 9 * cm, 26 * cm)

                    # entetes année scolaire et séquence
                    can.setFont("calibri bold", 15)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(10.5 * cm, 24 * cm,
                                          f"bulletin scolaire {trouver_sequence(self.seq_eleve.value)}".upper())

                    can.setFont("calibri", 12)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(10.5 * cm, 23.5 * cm, f"Année scolaire {asco - 1} / {asco}")

                    # infos sur l'élève ________________________

                    # Lignes horizontales
                    # 1ere ligne
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    can.line(4 * cm, 23 * cm, 20 * cm, 23 * cm)

                    # Lignes du milieu
                    can.line(4 * cm, 22.3 * cm, 20 * cm, 22.3 * cm)
                    can.line(4 * cm, 21.6 * cm, 20 * cm, 21.6 * cm)
                    can.line(4 * cm, 20.9 * cm, 16 * cm, 20.9 * cm)

                    # Dernière ligne
                    can.line(4 * cm, 19.7 * cm, 20 * cm, 19.7 * cm)

                    # Lignes verticales
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    # 1ere ligne
                    can.line(4 * cm, 23 * cm, 4 * cm, 19.7 * cm)

                    can.line(11 * cm, 21.6 * cm, 11 * cm, 20.9 * cm)
                    can.line(13.5 * cm, 22.3 * cm, 13.5 * cm, 21.6 * cm)
                    can.line(16 * cm, 23 * cm, 16 * cm, 19.7 * cm)

                    # Dernière ligne
                    can.line(20 * cm, 23 * cm, 20 * cm, 19.7 * cm)

                    # champs d'informations
                    can.setFont("calibri", 10)
                    can.drawString(4.2 * cm, 22.5 * cm, "Nom de l'élève:")
                    can.drawString(16.2 * cm, 22.5 * cm, "Classe:")
                    can.drawString(4.2 * cm, 21.8 * cm, "Date et lieu de naissance:")
                    can.drawString(13.8 * cm, 21.8 * cm, "Genre:")
                    can.drawString(16.2 * cm, 21.8 * cm, "Effectif:")
                    can.setFillColorRGB(1, 0, 0)
                    can.drawString(4.2 * cm, 21.1 * cm, "Identifiant unique:")
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(11.2 * cm, 21.1 * cm, "Redoublant: oui          non")
                    can.drawString(16.2 * cm, 21.1 * cm, "Professeur principal:")
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(4.2 * cm, 20.4 * cm, "Noms et contact des parents/tuteurs:")

                    # remplissage des informations
                    can.setFont("calibri bold", 11)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(6.7 * cm, 22.5 * cm, f"{self.title_details.value}")

                    infos = be.search_elev_by_nom(self.title_details.value)
                    can.drawString(17.4 * cm, 22.5 * cm, f"{self.classe_eleve.value}")
                    # Date et lieu de naissance
                    can.drawString(8 * cm, 21.8 * cm, f"{infos[2]} à {infos[3]}")
                    # sexe
                    can.drawString(15.2 * cm, 21.8 * cm, f"{infos[4]}")
                    # Effectif
                    can.drawString(17.8 * cm, 21.8 * cm, f"{be.effectif_classe(self.classe_eleve.value)}")
                    # Contact parents
                    can.drawString(4.2 * cm, 19.9 * cm, f"{infos[5]} / {infos[7]}")

                    prof_titus = be.search_titus(self.classe_eleve.value)
                    sep = prof_titus.split(" ")
                    can.drawString(16.2 * cm, 20.7 * cm, f"{sep[0]}")
                    can.drawString(16.2 * cm, 20.3 * cm, f"{sep[1]}")

                    # Pied de page
                    pied = f"Bulletin / {asco - 1}-{asco} / {self.seq_eleve.value} / {self.classe_eleve.value} / {self.title_details.value}".upper()
                    can.setFont("calibri", 9)
                    can.setFillColorRGB(0.5, 0.5, 0.5)
                    can.drawCentredString(10.5 * cm, 0.5 * cm, pied)

                draw_headers()

                # divisions pour les lignes horizontales
                b1, b2, b3, b4, b5, b6, b7, b8, = 1, 10, 11.5, 12.5, 14, 15, 17, 20

                # divisions pour les lignes verticales
                m1 = (b1 + b2) / 2
                m2 = (b2 + b3) / 2
                m3 = (b3 + b4) / 2
                m4 = (b4 + b5) / 2
                m5 = (b5 + b6) / 2
                m6 = (b6 + b7) / 2
                m7 = (b7 + b8) / 2

                def draw_entetes():
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)

                    # Lignes horizontales
                    can.line(1 * cm, 19.4 * cm, 20 * cm, 19.4 * cm)
                    can.line(1 * cm, 18.8 * cm, 20 * cm, 18.8 * cm)

                    # Lignes verticales
                    can.line(b1 * cm, 18.8 * cm, b1 * cm, 19.4 * cm)
                    can.line(b2 * cm, 18.8 * cm, b2 * cm, 19.4 * cm)
                    can.line(b3 * cm, 18.8 * cm, b3 * cm, 19.4 * cm)
                    can.line(b4 * cm, 18.8 * cm, b4 * cm, 19.4 * cm)
                    can.line(b5 * cm, 18.8 * cm, b5 * cm, 19.4 * cm)
                    can.line(b6 * cm, 18.8 * cm, b6 * cm, 19.4 * cm)
                    can.line(b7 * cm, 18.8 * cm, b7 * cm, 19.4 * cm)
                    can.line(b8 * cm, 18.8 * cm, b8 * cm, 19.4 * cm)

                    can.setFont("calibri bold", 10)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(m1 * cm, 19 * cm, "Matiere")
                    can.drawCentredString(m2 * cm, 19 * cm, "M/20")
                    can.drawCentredString(m3 * cm, 19 * cm, "Coef")
                    can.drawCentredString(m4 * cm, 19 * cm, "M x coef")
                    can.drawCentredString(m5 * cm, 19 * cm, "Cote")

                    can.setFillColorRGB(1, 0, 0)
                    can.drawCentredString(m6 * cm, 19 * cm, "Min-Max")
                    can.drawCentredString(m7 * cm, 19 * cm, "Appreciation")
                    can.setFillColorRGB(0, 0, 0)

                draw_entetes()

                y = 19

                details_notes = be.detail_bull_trim(
                    self.classe_eleve.value, self.seq_eleve.value.lower(), self.title_details.value
                )
                groupe2 = []
                groupe1 = []
                total_general = 0
                total_coeff_general = 0

                # Remplissage des matières dans les groupes
                for data in details_notes:

                    if data["groupe"] == "1ER GROUPE":
                        groupe1.append(
                            {"matiere": data["matiere"], "coeff": data["coeff"], "note": data["note"], "total": data["total"],
                             "cote": data["cote"]}
                        )
                    else:
                        groupe2.append(
                            {"matiere": data["matiere"], "coeff": data["coeff"], "note": data["note"], "total": data["total"],
                             "cote": data["cote"]}
                        )

                groupes = [{"nom": "1ER GROUPE", "donnees": groupe1}, {"nom": "2E GROUPE", "donnees": groupe2}]

                # eriture des notes en fonction des groupes
                for groupe in groupes:

                    total_des_coeff = 0
                    total_points = 0

                    for data in groupe["donnees"]:
                        can.setFillColorRGB(0, 0, 0)
                        can.setFont("calibri", 10)
                        can.drawCentredString(m1 * cm, (y - 0.6) * cm, f"{data['matiere']}")

                        if "D" in data['cote']:
                            can.setFillColorRGB(1, 0, 0)
                        elif "A" in data['cote']:
                            can.setFillColorRGB(0, 0.48, 0.22)
                        else:
                            can.setFillColorRGB(0, 0, 0)

                        can.drawCentredString(m2 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data['note'])}")

                        can.setFillColorRGB(0, 0, 0)
                        can.drawCentredString(m3 * cm, (y - 0.6) * cm, f"{data['coeff']}")
                        can.drawCentredString(m4 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data['total'])}")

                        if "D" in data['cote']:
                            can.setFillColorRGB(1, 0, 0)
                        elif "A" in data['cote']:
                            can.setFillColorRGB(0, 0.48, 0.22)
                        else:
                            can.setFillColorRGB(0, 0, 0)
                        can.drawCentredString(m5 * cm, (y - 0.6) * cm, f"{data['cote']}")

                        can.setFillColorRGB(0, 0, 0)
                        note_min = be.note_min_mat_trim(self.classe_eleve.value, data['matiere'], self.seq_eleve.value)
                        note_max = be.note_max_mat_trim(self.classe_eleve.value, data['matiere'], self.seq_eleve.value)
                        can.drawCentredString(m6 * cm, (y - 0.6) * cm, f"{note_min} - {note_max}")

                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(1 * cm, (y - 0.8) * cm, 20 * cm, (y - 0.8) * cm)
                        total_points += data['total']
                        total_des_coeff += data['coeff']

                        # Lignes verticales
                        can.line(b1 * cm, (y - 0.7) * cm, b1 * cm, (y - 0) * cm)
                        can.line(b2 * cm, (y - 0.7) * cm, b2 * cm, (y - 0) * cm)
                        can.line(b3 * cm, (y - 0.7) * cm, b3 * cm, (y - 0) * cm)
                        can.line(b4 * cm, (y - 0.7) * cm, b4 * cm, (y - 0) * cm)
                        can.line(b5 * cm, (y - 0.7) * cm, b5 * cm, (y - 0) * cm)
                        can.line(b6 * cm, (y - 0.7) * cm, b6 * cm, (y - 0) * cm)
                        can.line(b7 * cm, (y - 0.7) * cm, b7 * cm, (y - 0) * cm)
                        can.line(b8 * cm, (y - 0.7) * cm, b8 * cm, (y - 0) * cm)

                        y -= 0.7

                    can.setFont("calibri bold", 10)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(m1 * cm, (y - 0.6) * cm, f"Total {groupe['nom']}")

                    can.setFont("calibri bold", 10)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(m3 * cm, (y - 0.6) * cm, f"{total_des_coeff}")
                    can.drawCentredString(m4 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(total_points)}")

                    moyenne = total_points / total_des_coeff
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(m7 * cm, (y - 0.6) * cm, f"{moyenne:.2f}/20")

                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    can.line(1 * cm, (y - 0.8) * cm, 20 * cm, (y - 0.8) * cm)

                    can.line(b1 * cm, (y - 0.8) * cm, b1 * cm, (y - 0) * cm)
                    can.line(b2 * cm, (y - 0.8) * cm, b2 * cm, (y - 0) * cm)
                    can.line(b3 * cm, (y - 0.8) * cm, b3 * cm, (y - 0) * cm)
                    can.line(b4 * cm, (y - 0.8) * cm, b4 * cm, (y - 0) * cm)
                    can.line(b5 * cm, (y - 0.8) * cm, b5 * cm, (y - 0) * cm)
                    can.line(b6 * cm, (y - 0.8) * cm, b6 * cm, (y - 0) * cm)
                    can.line(b7 * cm, (y - 0.8) * cm, b7 * cm, (y - 0) * cm)
                    can.line(b8 * cm, (y - 0.8) * cm, b8 * cm, (y - 0) * cm)

                    total_coeff_general += total_des_coeff
                    total_general += total_points

                    y -= 0.7

                y = y - 1

                def draw_recap():
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    can.line(1 * cm, (y + 0.1) * cm, 20 * cm, (y + 0.1) * cm)
                    can.line(b1 * cm, (y + 1) * cm, b1 * cm, (y + 0.1) * cm)
                    can.line(b3 * cm, (y + 1) * cm, b3 * cm, (y + 0.1) * cm)
                    can.line(b4 * cm, (y + 1) * cm, b4 * cm, (y + 0.1) * cm)
                    can.line(b5 * cm, (y + 1) * cm, b5 * cm, (y + 0.1) * cm)
                    can.line(b7 * cm, (y + 1) * cm, b7 * cm, (y + 0.1) * cm)
                    can.line(b8 * cm, (y + 1) * cm, b8 * cm, (y + 0.1) * cm)

                    can.setFont("calibri bold", 11)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawRightString((b3 - 0.2) * cm, (y + 0.4) * cm, "TOTAL")
                    can.drawRightString((b7 - 0.2) * cm, (y + 0.4) * cm, "MOYENNE")
                    can.drawCentredString(m3 * cm, (y + 0.4) * cm, f"{be.ecrire_nombre(total_coeff_general)}")
                    can.drawCentredString(m4 * cm, (y + 0.4) * cm, f"{be.ecrire_nombre(total_general)}")
                    can.drawCentredString(m7 * cm, (y + 0.4) * cm, f"{be.ecrire_nombre(total_general / total_coeff_general)}")

                draw_recap()

                # Statistiques
                def draw_cadre_stats():

                    # lignes horizontales
                    can.setFillColorRGB(0.75, 0.75, 0.75)
                    can.line(1 * cm, (y - 0.3) * cm, 20 * cm, (y - 0.3) * cm)
                    can.line(1 * cm, (y - 0.9) * cm, 20 * cm, (y - 0.9) * cm)

                    # Lignes verticales
                    can.line(1 * cm, (y - 0.3) * cm, 1 * cm, (y - 0.9) * cm)
                    can.line(7.3 * cm, (y - 0.3) * cm, 7.3 * cm, (y - 0.9) * cm)
                    can.line(13.6 * cm, (y - 0.3) * cm, 13.6 * cm, (y - 0.9) * cm)
                    can.line(20 * cm, (y - 0.3) * cm, 20 * cm, (y - 0.9) * cm)

                    # cadre stats divisons principales
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    can.line(1 * cm, (y - 0.3) * cm, 1 * cm, (y - 6) * cm)
                    can.line(7.3 * cm, (y - 0.3) * cm, 7.3 * cm, (y - 6) * cm)
                    can.line(13.6 * cm, (y - 0.3) * cm, 13.6 * cm, (y - 6) * cm)
                    can.line(20 * cm, (y - 0.3) * cm, 20 * cm, (y - 6) * cm)
                    can.line(1 * cm, (y - 4) * cm, 20 * cm, (y - 4) * cm)
                    can.line(1 * cm, (y - 6) * cm, 20 * cm, (y - 6) * cm)

                    # divisons verticales secondaires
                    # Discipline
                    can.line(3.15 * cm, (y - 0.9) * cm, 3.15 * cm, (y - 4) * cm)
                    can.line(4.15 * cm, (y - 0.9) * cm, 4.15 * cm, (y - 4) * cm)
                    can.line(6.3 * cm, (y - 0.9) * cm, 6.3 * cm, (y - 4) * cm)
                    # Travail de l'élève
                    can.line(9.3 * cm, (y - 0.9) * cm, 9.3 * cm, (y - 4) * cm)
                    can.line(10.8 * cm, (y - 0.9) * cm, 10.8 * cm, (y - 4) * cm)
                    can.line(12.8 * cm, (y - 1.675) * cm, 12.8 * cm, (y - 4) * cm)
                    can.line(12.8 * cm, (y - 1.675) * cm, 12.8 * cm, (y - 4) * cm)
                    # Profil
                    can.line(17 * cm, (y - 0.9) * cm, 17 * cm, (y - 4) * cm)

                    # divisions horizontales secondaire
                    can.line(1 * cm, (y - 1.675) * cm, 20 * cm, (y - 1.675) * cm)
                    can.line(1 * cm, (y - 2.45) * cm, 20 * cm, (y - 2.45) * cm)
                    can.line(1 * cm, (y - 3.225) * cm, 20 * cm, (y - 3.225) * cm)

                    can.line(10.8 * cm, (y - 2.0125) * cm, 13.6 * cm, (y - 2.0125) * cm)
                    can.line(10.8 * cm, (y - 2.7875) * cm, 13.6 * cm, (y - 2.7875) * cm)

                    # divisons horizontales tertiares

                    can.setFont("calibri", 9)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(1.2 * cm, (y - 1.375) * cm, "Abs non J.")
                    can.drawString(1.2 * cm, (y - 1.375) * cm, "Abs non J. (h)")
                    can.drawString(1.2 * cm, (y - 2.15) * cm, "Abs just. (h)")
                    can.drawString(1.2 * cm, (y - 2.925) * cm, "Retards (nb) ")
                    can.drawString(1.2 * cm, (y - 3.7) * cm, "Consignes (h) ")
                    can.drawString(4.21 * cm, (y - 1.375) * cm, "Avertissement")
                    can.drawString(4.21 * cm, (y - 2.15) * cm, "Blâme")
                    can.drawString(4.21 * cm, (y - 2.925) * cm, f"Exclusions (j)")
                    can.drawString(4.21 * cm, (y - 3.7) * cm, f"Exclusion (def)")

                    # remplissage sanctions
                    can.setFont("calibri bold", 10)
                    abs_nj = be.sanction_by_eleve_trim(self.title_details.value, self.seq_eleve.value, 'ABSENCE NJ.')
                    abs_jus = be.sanction_by_eleve_trim(self.title_details.value, self.seq_eleve.value, 'ABSENCE JUST.')
                    avert = be.sanction_by_eleve_trim(self.title_details.value, self.seq_eleve.value, 'AVERTISSEMENT')
                    blame = be.sanction_by_eleve_trim(self.title_details.value, self.seq_eleve.value, 'BLAME')
                    consigne = be.sanction_by_eleve_trim(self.title_details.value, self.seq_eleve.value, 'CONSIGNE')
                    exclusion = be.sanction_by_eleve_trim(self.title_details.value, self.seq_eleve.value, 'EXCLUSION')
                    exclu_def = be.sanction_by_eleve_trim(self.title_details.value, self.seq_eleve.value, 'EXCLUSION DEF.')
                    retard = be.sanction_by_eleve_trim(self.title_details.value, self.seq_eleve.value, 'RETARD')

                    can.drawCentredString(3.65 * cm, (y - 1.375) * cm, f"{abs_nj}")
                    can.drawCentredString(3.65 * cm, (y - 2.15) * cm, f"{abs_jus}")
                    can.drawCentredString(3.65 * cm, (y - 2.925) * cm, f"{retard}")
                    can.drawCentredString(3.65 * cm, (y - 3.7) * cm, f"{consigne}")
                    can.drawCentredString(6.8 * cm, (y - 1.375) * cm, f"{avert}")
                    can.drawCentredString(6.8 * cm, (y - 2.15) * cm, f"{blame}")
                    can.drawCentredString(6.8 * cm, (y - 2.925) * cm, f"{exclusion}")
                    can.drawCentredString(6.8 * cm, (y - 3.7) * cm, f"{exclu_def}")

                    # travail de l'élève
                    can.setFont("calibri", 10)
                    can.drawString(7.5 * cm, (y - 1.375) * cm, "Total Gén.".upper())
                    can.drawString(7.5 * cm, (y - 2.15) * cm, "Coef".upper())
                    can.drawString(7.5 * cm, (y - 2.925) * cm, "Moyenne".upper())
                    can.drawString(7.5 * cm, (y - 3.7) * cm, f"Cote".upper())

                    can.setFont("calibri bold", 10)
                    can.drawString(11 * cm, (y - 1.375) * cm, "appreciations.".upper())
                    can.setFont("calibri", 8)
                    can.drawString(11 * cm, (y - 1.9625) * cm, "CTBA")
                    can.drawString(11 * cm, (y - 2.35) * cm, "CBA")
                    can.drawString(11 * cm, (y - 2.7375) * cm, "CA")
                    can.drawString(11 * cm, (y - 3.125) * cm, "CMA")
                    can.drawString(11 * cm, (y - 3.8125) * cm, "CNA")

                    # Remplissage du travail de l'élève
                    can.setFont("calibri bold", 11)
                    can.drawCentredString(10.05 * cm, (y - 1.375) * cm, f"{be.ecrire_nombre(total_general)}")
                    can.drawCentredString(10.05 * cm, (y - 2.15) * cm, f"{be.ecrire_nombre(total_coeff_general)}")
                    can.drawCentredString(10.05 * cm, (y - 2.925) * cm, f"{self.moy_eleve.value:.2f}")
                    can.drawCentredString(10.05 * cm, (y - 3.7) * cm, f"{be.trouver_cote(self.moy_eleve.value)}")

                    # Profil de la classe
                    can.setFont("calibri", 10)
                    can.drawString(13.8 * cm, (y - 1.375) * cm, "Moyenne générale")
                    can.setFillColorRGB(1, 0, 0)
                    can.setFont("calibri bold", 10)
                    can.drawString(13.8 * cm, (y - 2.15) * cm, "[Min-Max]")
                    can.setFont("calibri", 10)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(13.8 * cm, (y - 2.925) * cm, "Nb de moyennes")
                    can.drawString(13.8 * cm, (y - 3.7) * cm, f"Taux de réussite")

                    # Remplissage profil
                    can.setFont("calibri bold", 11)
                    can.drawCentredString(18.5 * cm, (y - 1.375) * cm, f"{self.moygen_trim.value}")
                    can.drawCentredString(18.5 * cm, (y - 2.15) * cm, f"{self.notemin_trim.value} - {self.notemax_trim.value}")
                    can.drawCentredString(18.5 * cm, (y - 2.925) * cm,
                                          f"{be.nb_admis_trim(self.classe_eleve.value, self.seq_eleve.value)}")
                    can.drawCentredString(18.5 * cm, (y - 3.7) * cm, f"{self.taux_trim.value}")

                draw_cadre_stats()

                # Entêtes des stats
                def draw_stats_entetes():
                    can.setFont("calibri bold", 11)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(4.15 * cm, (y - 0.7) * cm, "Discipline")
                    can.drawCentredString(10.45 * cm, (y - 0.7) * cm, "Travail de l'èlève")
                    can.drawCentredString(17.3 * cm, (y - 0.7) * cm, "Profil de la classe")

                    can.setFont("calibri", 9)
                    can.drawCentredString(4.15 * cm, (y - 4.4) * cm, "Appréciation du travail de l'élève")
                    can.drawCentredString(4.15 * cm, (y - 4.8) * cm, "(Points forts et points à améliorer)")

                    can.drawCentredString(8.8 * cm, (y - 4.4) * cm, "Visa du parent /")
                    can.drawCentredString(8.8 * cm, (y - 4.8) * cm, "tuteur")

                    can.drawCentredString(11.95 * cm, (y - 4.4) * cm, "Nom et visa du")
                    can.drawCentredString(11.95 * cm, (y - 4.8) * cm, "professeur titulaire")

                    can.drawCentredString(17.3 * cm, (y - 4.4) * cm, "Le chef d'établissement")

                draw_stats_entetes()

                can.save()
                self.cp.cp.box.title.value = "Validé !"
                self.cp.cp.box.content.value = "Bulletin créé avec succès"
                self.cp.cp.box.open = True
                self.cp.cp.box.update()

        else:
            pass

    def imprimer_all_bulletins(self, e: ft.FilePickerResultEvent):
        counter = 0
        for widget in (self.sel_seq_trim, self.sel_classe_trim):
            if widget.value is None or widget.value == "":
                counter += 1

        if counter > 0:
            self.cp.cp.box.title.value = "Erreur"
            self.cp.cp.box.content.value = f"Tous les champs sont obligatoires"
            self.cp.cp.box.open = True
            self.cp.cp.box.update()

        else:
            save_location = f"{e.path}.pdf"
            fichier = os.path.abspath(save_location)
            can = Canvas("{0}".format(fichier), pagesize=A4)
            create_pdf_fonts()

            asco = be.show_asco_encours()
            my_class = self.sel_classe_trim.value
            my_seq = self.sel_seq_trim.value.lower()

            if save_location != "None.pdf":
                # ressortir les bulletins filtrés
                def liste_bulletins():
                    bulletins = be.bull_trim_classe_trim(my_class, my_seq)
                    bulls = []

                    for bull in bulletins:
                        dico = {
                            "asco": bull[0], "classe": bull[1], "sequence": bull[3], "nom": bull[4],
                            "nb_coeff": bull[6], "total": bull[7], "moyenne": bull[8], "rang": bull[9]
                        }
                        bulls.append(dico)

                    return bulls

                all_bulletins = liste_bulletins()

                niveau = be.look_nivo(my_class)
                cycle = be.cycle_par_niveau(niveau)

                # bulletin des classes du premier cycle
                if cycle == "premier":
                    decompte = 0

                    for any_bull in all_bulletins:
                        gauche, droite, y = 4.25, 17.25, 28

                        # gauche, droite, y = 4.25, 17.75, 28
                        def draw_headers():
                            # A gauche
                            can.setFillColorRGB(0, 0, 0)
                            can.setFont("calibri bold", 10)
                            can.drawCentredString(gauche * cm, 28.5 * cm, "Republique du Cameroun".upper())
                            can.setFont("calibri z", 9)
                            can.drawCentredString(gauche * cm, 28.1 * cm, "Paix - Travail - Patrie".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(gauche * cm, 27.7 * cm, "*************")
                            can.setFont("calibri", 9)
                            can.drawCentredString(gauche * cm, 27.3 * cm,
                                                  "Ministere des enseignements secondaires".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(gauche * cm, 26.9 * cm, "*************")
                            can.setFont("calibri bold", 10)
                            can.drawCentredString(gauche * cm, 26.5 * cm, "Delegation régionale du centre".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(gauche * cm, 26.1 * cm, "*************")
                            can.drawCentredString(gauche * cm, 25.7 * cm,
                                                  "Délégation departementale du mfoundi".upper())
                            can.drawCentredString(gauche * cm, 25.3 * cm, "*************")
                            can.drawCentredString(gauche * cm, 24.9 * cm, "NOM DU COLLEGE".upper())

                            # A droite
                            can.setFillColorRGB(0, 0, 0)
                            can.setFont("calibri bold", 10)
                            can.drawCentredString(droite * cm, 28.5 * cm, "Republique du Cameroun".upper())
                            can.setFont("calibri z", 9)
                            can.drawCentredString(droite * cm, 28.1 * cm, "Paix - Travail - Patrie".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(droite * cm, 27.7 * cm, "*************")
                            can.setFont("calibri", 9)
                            can.drawCentredString(droite * cm, 27.3 * cm,
                                                  "Ministere des enseignements secondaires".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(droite * cm, 26.9 * cm, "*************")
                            can.setFont("calibri bold", 10)
                            can.drawCentredString(droite * cm, 26.5 * cm, "Delegation régionale du centre".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(droite * cm, 26.1 * cm, "*************")
                            can.drawCentredString(droite * cm, 25.7 * cm,
                                                  "Délégation departementale du mfoundi".upper())
                            can.drawCentredString(droite * cm, 25.3 * cm, "*************")
                            can.drawCentredString(droite * cm, 24.9 * cm, "NOM DU COLLEGE".upper())

                            # Le logo
                            monlogo = "assets/mon logo.png"
                            can.drawImage(monlogo, 9 * cm, 26 * cm)

                            # entetes année scolaire et séquence
                            can.setFont("calibri bold", 15)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(10.5 * cm, 24 * cm, f"bulletin scolaire {trouver_sequence(my_seq)}".upper())

                            can.setFont("calibri", 12)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(10.5 * cm, 23.5 * cm, f"Année scolaire {asco - 1} / {asco}")

                            # infos sur l'élève ________________________

                            # Lignes horizontales
                            # 1ere ligne
                            can.setStrokeColorRGB(0.3, 0.3, 0.3)
                            can.line(4 * cm, 23 * cm, 20 * cm, 23 * cm)

                            # Lignes du milieu
                            can.line(4 * cm, 22.3 * cm, 20 * cm, 22.3 * cm)
                            can.line(4 * cm, 21.6 * cm, 20 * cm, 21.6 * cm)
                            can.line(4 * cm, 20.9 * cm, 16 * cm, 20.9 * cm)

                            # Dernière ligne
                            can.line(4 * cm, 19.7 * cm, 20 * cm, 19.7 * cm)

                            # Lignes verticales
                            can.setStrokeColorRGB(0.3, 0.3, 0.3)
                            # 1ere ligne
                            can.line(4 * cm, 23 * cm, 4 * cm, 19.7 * cm)

                            can.line(11 * cm, 21.6 * cm, 11 * cm, 20.9 * cm)
                            can.line(13.5 * cm, 22.3 * cm, 13.5 * cm, 21.6 * cm)
                            can.line(16 * cm, 23 * cm, 16 * cm, 19.7 * cm)

                            # Dernière ligne
                            can.line(20 * cm, 23 * cm, 20 * cm, 19.7 * cm)

                            # champs d'informations
                            can.setFont("calibri", 10)
                            can.drawString(4.2 * cm, 22.5 * cm, "Nom de l'élève:")
                            can.drawString(16.2 * cm, 22.5 * cm, "Classe:")
                            can.drawString(4.2 * cm, 21.8 * cm, "Date et lieu de naissance:")
                            can.drawString(13.8 * cm, 21.8 * cm, "Genre:")
                            can.drawString(16.2 * cm, 21.8 * cm, "Effectif:")
                            can.setFillColorRGB(1, 0, 0)
                            can.drawString(4.2 * cm, 21.1 * cm, "Identifiant unique:")
                            can.setFillColorRGB(0, 0, 0)
                            can.drawString(11.2 * cm, 21.1 * cm, "Redoublant: oui          non")
                            can.drawString(16.2 * cm, 21.1 * cm, "Professeur principal:")
                            can.setFillColorRGB(0, 0, 0)
                            can.drawString(4.2 * cm, 20.4 * cm, "Noms et contact des parents/tuteurs:")

                            # remplissage des informations
                            can.setFont("calibri bold", 11)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawString(6.7 * cm, 22.5 * cm, f"{any_bull['nom']}")

                            infos = be.search_elev_by_nom(any_bull['nom'])
                            can.drawString(17.4 * cm, 22.5 * cm, f"{my_class}")
                            # Date et lieu de naissance
                            can.drawString(8 * cm, 21.8 * cm, f"{infos[2]} à {infos[3]}")
                            # sexe
                            can.drawString(15.2 * cm, 21.8 * cm, f"{infos[4]}")
                            # Effectif
                            can.drawString(17.8 * cm, 21.8 * cm, f"{be.effectif_classe(my_class)}")
                            # Contact parents
                            can.drawString(4.2 * cm, 19.9 * cm, f"{infos[5]} / {infos[7]}")

                            prof_titus = be.search_titus(my_class)
                            sep = prof_titus.split(" ")
                            can.drawString(16.2 * cm, 20.7 * cm, f"{sep[0]}")
                            can.drawString(16.2 * cm, 20.3 * cm, f"{sep[1]}")

                            # Pied de page
                            pied = f"Bulletin / {asco - 1}-{asco} / {self.seq_eleve.value} / {my_class} / {any_bull['nom']}".upper()
                            can.setFont("calibri", 9)
                            can.setFillColorRGB(0.5, 0.5, 0.5)
                            can.drawCentredString(10.5 * cm, 0.5 * cm, pied)

                        draw_headers()

                        # divisions pour les lignes horizontales
                        b1, b2, b3, b4, b5, b6, b7, b8, = 1, 10, 11.5, 12.5, 14, 15, 17, 20

                        # divisions pour les lignes verticales
                        m1 = (b1 + b2) / 2
                        m2 = (b2 + b3) / 2
                        m3 = (b3 + b4) / 2
                        m4 = (b4 + b5) / 2
                        m5 = (b5 + b6) / 2
                        m6 = (b6 + b7) / 2
                        m7 = (b7 + b8) / 2

                        def draw_entetes():
                            can.setStrokeColorRGB(0.3, 0.3, 0.3)

                            # Lignes horizontales
                            can.line(1 * cm, 19.4 * cm, 20 * cm, 19.4 * cm)
                            can.line(1 * cm, 18.8 * cm, 20 * cm, 18.8 * cm)

                            # Lignes verticales
                            can.line(b1 * cm, 18.8 * cm, b1 * cm, 19.4 * cm)
                            can.line(b2 * cm, 18.8 * cm, b2 * cm, 19.4 * cm)
                            can.line(b3 * cm, 18.8 * cm, b3 * cm, 19.4 * cm)
                            can.line(b4 * cm, 18.8 * cm, b4 * cm, 19.4 * cm)
                            can.line(b5 * cm, 18.8 * cm, b5 * cm, 19.4 * cm)
                            can.line(b6 * cm, 18.8 * cm, b6 * cm, 19.4 * cm)
                            can.line(b7 * cm, 18.8 * cm, b7 * cm, 19.4 * cm)
                            can.line(b8 * cm, 18.8 * cm, b8 * cm, 19.4 * cm)

                            can.setFont("calibri bold", 10)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(m1 * cm, 19 * cm, "Matiere")
                            can.drawCentredString(m2 * cm, 19 * cm, "M/20")
                            can.drawCentredString(m3 * cm, 19 * cm, "Coef")
                            can.drawCentredString(m4 * cm, 19 * cm, "M x coef")
                            can.drawCentredString(m5 * cm, 19 * cm, "Cote")

                            can.setFillColorRGB(1, 0, 0)
                            can.drawCentredString(m6 * cm, 19 * cm, "Min-Max")
                            can.drawCentredString(m7 * cm, 19 * cm, "Appreciation")
                            can.setFillColorRGB(0, 0, 0)

                        draw_entetes()

                        y = 19

                        details_notes = be.detail_bull_trim(
                            my_class, my_seq.lower(), any_bull['nom']
                        )
                        total_general = 0
                        total_coeff_general = 0

                        # ecriture des notes en fonction des groupes
                        for data in details_notes:
                            can.setFillColorRGB(0, 0, 0)
                            can.setFont("calibri", 10)
                            can.drawCentredString(m1 * cm, (y - 0.6) * cm, f"{data['matiere']}")  # Matiere

                            if "D" in data['cote']:
                                can.setFillColorRGB(1, 0, 0)
                            elif "A" in data['cote']:
                                can.setFillColorRGB(0, 0.48, 0.22)
                            else:
                                can.setFillColorRGB(0, 0, 0)

                            can.drawCentredString(m2 * cm, (y - 0.6) * cm, f"{data['note']}")  # Note / 20

                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(m3 * cm, (y - 0.6) * cm,
                                                  f"{be.ecrire_nombre(data['coeff'])}")  # Coefficient
                            can.drawCentredString(m4 * cm, (y - 0.6) * cm, f"{data['total']}")

                            if "D" in data['cote']:
                                can.setFillColorRGB(1, 0, 0)
                            elif "A" in data['cote']:
                                can.setFillColorRGB(0, 0.48, 0.22)
                            else:
                                can.setFillColorRGB(0, 0, 0)

                            can.drawCentredString(m5 * cm, (y - 0.6) * cm, f"{data['cote']}")

                            can.setFillColorRGB(0, 0, 0)
                            note_min = be.note_min_mat_trim(my_class, data['matiere'], my_class)
                            note_max = be.note_max_mat_trim(my_class, data['matiere'], my_class)
                            can.drawCentredString(m6 * cm, (y - 0.6) * cm, f"{note_min} - {note_max}")

                            can.setStrokeColorRGB(0.3, 0.3, 0.3)
                            can.line(1 * cm, (y - 0.8) * cm, 20 * cm, (y - 0.8) * cm)

                            # Lignes verticales
                            can.line(b1 * cm, (y - 0.7) * cm, b1 * cm, (y - 0) * cm)
                            can.line(b2 * cm, (y - 0.7) * cm, b2 * cm, (y - 0) * cm)
                            can.line(b3 * cm, (y - 0.7) * cm, b3 * cm, (y - 0) * cm)
                            can.line(b4 * cm, (y - 0.7) * cm, b4 * cm, (y - 0) * cm)
                            can.line(b5 * cm, (y - 0.7) * cm, b5 * cm, (y - 0) * cm)
                            can.line(b6 * cm, (y - 0.7) * cm, b6 * cm, (y - 0) * cm)
                            can.line(b7 * cm, (y - 0.7) * cm, b7 * cm, (y - 0) * cm)
                            can.line(b8 * cm, (y - 0.7) * cm, b8 * cm, (y - 0) * cm)

                            total_coeff_general += data['coeff']
                            total_general += data['total']

                            y -= 0.7

                        y = y - 1

                        def draw_recap():
                            can.setStrokeColorRGB(0.3, 0.3, 0.3)
                            can.line(1 * cm, (y + 0.1) * cm, 20 * cm, (y + 0.1) * cm)
                            can.line(b1 * cm, (y + 1) * cm, b1 * cm, (y + 0.1) * cm)
                            can.line(b3 * cm, (y + 1) * cm, b3 * cm, (y + 0.1) * cm)
                            can.line(b4 * cm, (y + 1) * cm, b4 * cm, (y + 0.1) * cm)
                            can.line(b5 * cm, (y + 1) * cm, b5 * cm, (y + 0.1) * cm)
                            can.line(b7 * cm, (y + 1) * cm, b7 * cm, (y + 0.1) * cm)
                            can.line(b8 * cm, (y + 1) * cm, b8 * cm, (y + 0.1) * cm)

                            can.setFont("calibri bold", 11)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawRightString((b3 - 0.2) * cm, (y + 0.4) * cm, "TOTAL")
                            can.drawRightString((b7 - 0.2) * cm, (y + 0.4) * cm, "MOYENNE")
                            can.drawCentredString(m3 * cm, (y + 0.4) * cm, f"{be.ecrire_nombre(total_coeff_general)}")
                            can.drawCentredString(m4 * cm, (y + 0.4) * cm, f"{be.ecrire_nombre(total_general)}")
                            can.drawCentredString(m7 * cm, (y + 0.4) * cm,
                                                  f"{(be.ecrire_nombre(total_general / total_coeff_general))}")

                        draw_recap()

                        # Statistiques
                        def draw_cadre_stats():

                            # lignes horizontales
                            can.setFillColorRGB(0.75, 0.75, 0.75)
                            can.line(1 * cm, (y - 0.3) * cm, 20 * cm, (y - 0.3) * cm)
                            can.line(1 * cm, (y - 0.9) * cm, 20 * cm, (y - 0.9) * cm)

                            # Lignes verticales
                            can.line(1 * cm, (y - 0.3) * cm, 1 * cm, (y - 0.9) * cm)
                            can.line(7.3 * cm, (y - 0.3) * cm, 7.3 * cm, (y - 0.9) * cm)
                            can.line(13.6 * cm, (y - 0.3) * cm, 13.6 * cm, (y - 0.9) * cm)
                            can.line(20 * cm, (y - 0.3) * cm, 20 * cm, (y - 0.9) * cm)

                            # cadre stats divisons principales
                            can.setStrokeColorRGB(0.3, 0.3, 0.3)
                            can.line(1 * cm, (y - 0.3) * cm, 1 * cm, (y - 6) * cm)
                            can.line(7.3 * cm, (y - 0.3) * cm, 7.3 * cm, (y - 6) * cm)
                            can.line(13.6 * cm, (y - 0.3) * cm, 13.6 * cm, (y - 6) * cm)
                            can.line(20 * cm, (y - 0.3) * cm, 20 * cm, (y - 6) * cm)
                            can.line(1 * cm, (y - 4) * cm, 20 * cm, (y - 4) * cm)
                            can.line(1 * cm, (y - 6) * cm, 20 * cm, (y - 6) * cm)

                            # divisons verticales secondaires
                            # Discipline
                            can.line(3.15 * cm, (y - 0.9) * cm, 3.15 * cm, (y - 4) * cm)
                            can.line(4.15 * cm, (y - 0.9) * cm, 4.15 * cm, (y - 4) * cm)
                            can.line(6.3 * cm, (y - 0.9) * cm, 6.3 * cm, (y - 4) * cm)
                            # Travail de l'élève
                            can.line(9.3 * cm, (y - 0.9) * cm, 9.3 * cm, (y - 4) * cm)
                            can.line(10.8 * cm, (y - 0.9) * cm, 10.8 * cm, (y - 4) * cm)
                            can.line(12.8 * cm, (y - 1.675) * cm, 12.8 * cm, (y - 4) * cm)
                            can.line(12.8 * cm, (y - 1.675) * cm, 12.8 * cm, (y - 4) * cm)
                            # Profil
                            can.line(17 * cm, (y - 0.9) * cm, 17 * cm, (y - 4) * cm)

                            # divisions horizontales secondaire
                            can.line(1 * cm, (y - 1.675) * cm, 20 * cm, (y - 1.675) * cm)
                            can.line(1 * cm, (y - 2.45) * cm, 20 * cm, (y - 2.45) * cm)
                            can.line(1 * cm, (y - 3.225) * cm, 20 * cm, (y - 3.225) * cm)

                            can.line(10.8 * cm, (y - 2.0125) * cm, 13.6 * cm, (y - 2.0125) * cm)
                            can.line(10.8 * cm, (y - 2.7875) * cm, 13.6 * cm, (y - 2.7875) * cm)

                            # divisons horizontales tertiares

                            can.setFont("calibri", 9)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawString(1.2 * cm, (y - 1.375) * cm, "Abs non J.")
                            can.drawString(1.2 * cm, (y - 1.375) * cm, "Abs non J. (h)")
                            can.drawString(1.2 * cm, (y - 2.15) * cm, "Abs just. (h)")
                            can.drawString(1.2 * cm, (y - 2.925) * cm, "Retards (nb) ")
                            can.drawString(1.2 * cm, (y - 3.7) * cm, "Consignes (h) ")
                            can.drawString(4.21 * cm, (y - 1.375) * cm, "Avertissement")
                            can.drawString(4.21 * cm, (y - 2.15) * cm, "Blâme")
                            can.drawString(4.21 * cm, (y - 2.925) * cm, f"Exclusions (j)")
                            can.drawString(4.21 * cm, (y - 3.7) * cm, f"Exclusion (def)")

                            # remplissage sanctions
                            can.setFont("calibri bold", 10)
                            abs_nj = be.sanction_by_eleve_trim(any_bull['nom'], my_seq.upper(), 'ABSENCE NJ.')
                            abs_jus = be.sanction_by_eleve_trim(any_bull['nom'], my_seq.upper(), 'ABSENCE JUST.')
                            avert = be.sanction_by_eleve_trim(any_bull['nom'], my_seq.upper(), 'AVERTISSEMENT')
                            blame = be.sanction_by_eleve_trim(any_bull['nom'], my_seq.upper(), 'BLAME')
                            consigne = be.sanction_by_eleve_trim(any_bull['nom'], my_seq.upper(), 'CONSIGNE')
                            exclusion = be.sanction_by_eleve_trim(any_bull['nom'], my_seq.upper(), 'EXCLUSION')
                            exclu_def = be.sanction_by_eleve_trim(any_bull['nom'], my_seq.upper(), 'EXCLUSION DEF.')
                            retard = be.sanction_by_eleve_trim(any_bull['nom'], my_seq.upper(), 'RETARD')

                            can.drawCentredString(3.65 * cm, (y - 1.375) * cm, f"{abs_nj}")
                            can.drawCentredString(3.65 * cm, (y - 2.15) * cm, f"{abs_jus}")
                            can.drawCentredString(3.65 * cm, (y - 2.925) * cm, f"{retard}")
                            can.drawCentredString(3.65 * cm, (y - 3.7) * cm, f"{consigne}")
                            can.drawCentredString(6.8 * cm, (y - 1.375) * cm, f"{avert}")
                            can.drawCentredString(6.8 * cm, (y - 2.15) * cm, f"{blame}")
                            can.drawCentredString(6.8 * cm, (y - 2.925) * cm, f"{exclusion}")
                            can.drawCentredString(6.8 * cm, (y - 3.7) * cm, f"{exclu_def}")

                            # travail de l'élève
                            can.setFont("calibri", 10)
                            can.drawString(7.5 * cm, (y - 1.375) * cm, "Total Gén.".upper())
                            can.drawString(7.5 * cm, (y - 2.15) * cm, "Coef".upper())
                            can.drawString(7.5 * cm, (y - 2.925) * cm, "Moyenne".upper())
                            can.drawString(7.5 * cm, (y - 3.7) * cm, f"Cote".upper())

                            can.setFont("calibri bold", 10)
                            can.drawString(11 * cm, (y - 1.375) * cm, "appreciations.".upper())
                            can.setFont("calibri", 8)
                            can.drawString(11 * cm, (y - 1.9625) * cm, "CTBA")
                            can.drawString(11 * cm, (y - 2.35) * cm, "CBA")
                            can.drawString(11 * cm, (y - 2.7375) * cm, "CA")
                            can.drawString(11 * cm, (y - 3.125) * cm, "CMA")
                            can.drawString(11 * cm, (y - 3.8125) * cm, "CNA")

                            # Remplissage du travail de l'élève
                            can.setFont("calibri bold", 11)
                            can.drawCentredString(10.05 * cm, (y - 1.375) * cm, f"{be.ecrire_nombre(total_general)}")
                            can.drawCentredString(10.05 * cm, (y - 2.15) * cm,
                                                  f"{be.ecrire_nombre(total_coeff_general)}")
                            can.drawCentredString(10.05 * cm, (y - 2.925) * cm,
                                                  f"{be.ecrire_nombre(self.moy_eleve.value)}")
                            can.drawCentredString(10.05 * cm, (y - 3.7) * cm,
                                                  f"{be.trouver_cote(self.moy_eleve.value)}")

                            # Profil de la classe
                            can.setFont("calibri", 10)
                            can.drawString(13.8 * cm, (y - 1.375) * cm, "Moyenne générale")
                            can.setFillColorRGB(1, 0, 0)
                            can.setFont("calibri bold", 10)
                            can.drawString(13.8 * cm, (y - 2.15) * cm, "[Min-Max]")
                            can.setFont("calibri", 10)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawString(13.8 * cm, (y - 2.925) * cm, "Nb de moyennes")
                            can.drawString(13.8 * cm, (y - 3.7) * cm, f"Taux de réussite")

                            # Remplissage profil
                            can.setFont("calibri bold", 11)
                            moygen = be.ecrire_nombre(be.moygen_trim(my_class, my_seq.lower()))
                            nmin = be.ecrire_nombre(be.notemin_trim(my_class, my_seq.lower()))
                            nmax = be.ecrire_nombre(be.notemax_trim(my_class, my_seq.lower()))
                            nb_admis = be.nb_admis_trim(my_class, my_seq.lower())
                            taux = be.ecrire_nombre(nb_admis * 100 / be.effectif_classe(my_class))

                            can.drawCentredString(18.5 * cm, (y - 1.375) * cm, f"{moygen}")
                            can.drawCentredString(18.5 * cm, (y - 2.15) * cm,
                                                  f"{nmin} - {nmax}")
                            can.drawCentredString(18.5 * cm, (y - 2.925) * cm,
                                                  f"{nb_admis}")
                            can.drawCentredString(18.5 * cm, (y - 3.7) * cm, f"{taux} %")

                        draw_cadre_stats()

                        # Entêtes des stats
                        def draw_stats_entetes():
                            can.setFont("calibri bold", 11)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(4.15 * cm, (y - 0.7) * cm, "Discipline")
                            can.drawCentredString(10.45 * cm, (y - 0.7) * cm, "Travail de l'èlève")
                            can.drawCentredString(17.3 * cm, (y - 0.7) * cm, "Profil de la classe")

                            can.setFont("calibri", 9)
                            can.drawCentredString(4.15 * cm, (y - 4.4) * cm, "Appréciation du travail de l'élève")
                            can.drawCentredString(4.15 * cm, (y - 4.8) * cm, "(Points forts et points à améliorer)")

                            can.drawCentredString(8.8 * cm, (y - 4.4) * cm, "Visa du parent /")
                            can.drawCentredString(8.8 * cm, (y - 4.8) * cm, "tuteur")

                            can.drawCentredString(11.95 * cm, (y - 4.4) * cm, "Nom et visa du")
                            can.drawCentredString(11.95 * cm, (y - 4.8) * cm, "professeur titulaire")

                            can.drawCentredString(17.3 * cm, (y - 4.4) * cm, "Le chef d'établissement")

                        draw_stats_entetes()

                        can.showPage()
                        decompte += 1
                        self.pb_bull.value = decompte / len(all_bulletins)
                        self.pb_bull.update()
                        self.progres.value = f"{be.ecrire_nombre(decompte * 100 / len(all_bulletins))}%"
                        self.progres.update()

                    can.save()
                    self.cp.cp.box.title.value = "Validé !"
                    self.cp.cp.box.content.value = f"Bulletins de {my_class} pour la {trouver_sequence(my_seq)} créés avec succès"
                    self.cp.cp.box.open = True
                    self.cp.cp.box.update()

                # cas des buletins du second cycle
                else:
                    decompte = 0

                    for any_bull in all_bulletins:
                        gauche, droite, y = 4.25, 17.25, 28

                        # gauche, droite, y = 4.25, 17.75, 28
                        def draw_headers():
                            # A gauche
                            can.setFillColorRGB(0, 0, 0)
                            can.setFont("calibri bold", 10)
                            can.drawCentredString(gauche * cm, 28.5 * cm, "Republique du Cameroun".upper())
                            can.setFont("calibri z", 9)
                            can.drawCentredString(gauche * cm, 28.1 * cm, "Paix - Travail - Patrie".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(gauche * cm, 27.7 * cm, "*************")
                            can.setFont("calibri", 9)
                            can.drawCentredString(gauche * cm, 27.3 * cm,
                                                  "Ministere des enseignements secondaires".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(gauche * cm, 26.9 * cm, "*************")
                            can.setFont("calibri bold", 10)
                            can.drawCentredString(gauche * cm, 26.5 * cm, "Delegation régionale du centre".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(gauche * cm, 26.1 * cm, "*************")
                            can.drawCentredString(gauche * cm, 25.7 * cm,
                                                  "Délégation departementale du mfoundi".upper())
                            can.drawCentredString(gauche * cm, 25.3 * cm, "*************")
                            can.drawCentredString(gauche * cm, 24.9 * cm, "NOM DU COLLEGE".upper())

                            # A droite
                            can.setFillColorRGB(0, 0, 0)
                            can.setFont("calibri bold", 10)
                            can.drawCentredString(droite * cm, 28.5 * cm, "Republique du Cameroun".upper())
                            can.setFont("calibri z", 9)
                            can.drawCentredString(droite * cm, 28.1 * cm, "Paix - Travail - Patrie".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(droite * cm, 27.7 * cm, "*************")
                            can.setFont("calibri", 9)
                            can.drawCentredString(droite * cm, 27.3 * cm,
                                                  "Ministere des enseignements secondaires".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(droite * cm, 26.9 * cm, "*************")
                            can.setFont("calibri bold", 10)
                            can.drawCentredString(droite * cm, 26.5 * cm, "Delegation régionale du centre".upper())
                            can.setFont("calibri", 9)
                            can.drawCentredString(droite * cm, 26.1 * cm, "*************")
                            can.drawCentredString(droite * cm, 25.7 * cm,
                                                  "Délégation departementale du mfoundi".upper())
                            can.drawCentredString(droite * cm, 25.3 * cm, "*************")
                            can.drawCentredString(droite * cm, 24.9 * cm, "NOM DU COLLEGE".upper())

                            # Le logo
                            monlogo = "assets/mon logo.png"
                            can.drawImage(monlogo, 9 * cm, 26 * cm)

                            # entetes année scolaire et séquence
                            can.setFont("calibri bold", 15)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(10.5 * cm, 24 * cm,
                                                  f"bulletin scolaire {trouver_sequence(my_seq)}".upper())

                            can.setFont("calibri", 12)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(10.5 * cm, 23.5 * cm, f"Année scolaire {asco - 1} / {asco}")

                            # infos sur l'élève ________________________

                            # Lignes horizontales
                            # 1ere ligne
                            can.setStrokeColorRGB(0.3, 0.3, 0.3)
                            can.line(4 * cm, 23 * cm, 20 * cm, 23 * cm)

                            # Lignes du milieu
                            can.line(4 * cm, 22.3 * cm, 20 * cm, 22.3 * cm)
                            can.line(4 * cm, 21.6 * cm, 20 * cm, 21.6 * cm)
                            can.line(4 * cm, 20.9 * cm, 16 * cm, 20.9 * cm)

                            # Dernière ligne
                            can.line(4 * cm, 19.7 * cm, 20 * cm, 19.7 * cm)

                            # Lignes verticales
                            can.setStrokeColorRGB(0.3, 0.3, 0.3)
                            # 1ere ligne
                            can.line(4 * cm, 23 * cm, 4 * cm, 19.7 * cm)

                            can.line(11 * cm, 21.6 * cm, 11 * cm, 20.9 * cm)
                            can.line(13.5 * cm, 22.3 * cm, 13.5 * cm, 21.6 * cm)
                            can.line(16 * cm, 23 * cm, 16 * cm, 19.7 * cm)

                            # Dernière ligne
                            can.line(20 * cm, 23 * cm, 20 * cm, 19.7 * cm)

                            # champs d'informations
                            can.setFont("calibri", 10)
                            can.drawString(4.2 * cm, 22.5 * cm, "Nom de l'élève:")
                            can.drawString(16.2 * cm, 22.5 * cm, "Classe:")
                            can.drawString(4.2 * cm, 21.8 * cm, "Date et lieu de naissance:")
                            can.drawString(13.8 * cm, 21.8 * cm, "Genre:")
                            can.drawString(16.2 * cm, 21.8 * cm, "Effectif:")
                            can.setFillColorRGB(1, 0, 0)
                            can.drawString(4.2 * cm, 21.1 * cm, "Identifiant unique:")
                            can.setFillColorRGB(0, 0, 0)
                            can.drawString(11.2 * cm, 21.1 * cm, "Redoublant: oui          non")
                            can.drawString(16.2 * cm, 21.1 * cm, "Professeur principal:")
                            can.setFillColorRGB(0, 0, 0)
                            can.drawString(4.2 * cm, 20.4 * cm, "Noms et contact des parents/tuteurs:")

                            # remplissage des informations
                            can.setFont("calibri bold", 11)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawString(6.7 * cm, 22.5 * cm, f"{any_bull['nom']}")

                            infos = be.search_elev_by_nom(any_bull['nom'])
                            can.drawString(17.4 * cm, 22.5 * cm, f"{my_class}")
                            # Date et lieu de naissance
                            can.drawString(8 * cm, 21.8 * cm, f"{infos[2]} à {infos[3]}")
                            # sexe
                            can.drawString(15.2 * cm, 21.8 * cm, f"{infos[4]}")
                            # Effectif
                            can.drawString(17.8 * cm, 21.8 * cm, f"{be.effectif_classe(my_class)}")
                            # Contact parents
                            can.drawString(4.2 * cm, 19.9 * cm, f"{infos[5]} / {infos[7]}")

                            prof_titus = be.search_titus(my_class)
                            sep = prof_titus.split(" ")
                            can.drawString(16.2 * cm, 20.7 * cm, f"{sep[0]}")
                            can.drawString(16.2 * cm, 20.3 * cm, f"{sep[1]}")

                            # Pied de page
                            pied = f"Bulletin / {asco - 1}-{asco} / {my_seq} / {my_class} / {any_bull['nom']}".upper()
                            can.setFont("calibri", 9)
                            can.setFillColorRGB(0.5, 0.5, 0.5)
                            can.drawCentredString(10.5 * cm, 0.5 * cm, pied)

                        draw_headers()

                        # divisions pour les lignes horizontales
                        b1, b2, b3, b4, b5, b6, b7, b8, = 1, 10, 11.5, 12.5, 14, 15, 17, 20

                        # divisions pour les lignes verticales
                        m1 = (b1 + b2) / 2
                        m2 = (b2 + b3) / 2
                        m3 = (b3 + b4) / 2
                        m4 = (b4 + b5) / 2
                        m5 = (b5 + b6) / 2
                        m6 = (b6 + b7) / 2
                        m7 = (b7 + b8) / 2

                        def draw_entetes():
                            can.setStrokeColorRGB(0.3, 0.3, 0.3)

                            # Lignes horizontales
                            can.line(1 * cm, 19.4 * cm, 20 * cm, 19.4 * cm)
                            can.line(1 * cm, 18.8 * cm, 20 * cm, 18.8 * cm)

                            # Lignes verticales
                            can.line(b1 * cm, 18.8 * cm, b1 * cm, 19.4 * cm)
                            can.line(b2 * cm, 18.8 * cm, b2 * cm, 19.4 * cm)
                            can.line(b3 * cm, 18.8 * cm, b3 * cm, 19.4 * cm)
                            can.line(b4 * cm, 18.8 * cm, b4 * cm, 19.4 * cm)
                            can.line(b5 * cm, 18.8 * cm, b5 * cm, 19.4 * cm)
                            can.line(b6 * cm, 18.8 * cm, b6 * cm, 19.4 * cm)
                            can.line(b7 * cm, 18.8 * cm, b7 * cm, 19.4 * cm)
                            can.line(b8 * cm, 18.8 * cm, b8 * cm, 19.4 * cm)

                            can.setFont("calibri bold", 10)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(m1 * cm, 19 * cm, "Matiere")
                            can.drawCentredString(m2 * cm, 19 * cm, "M/20")
                            can.drawCentredString(m3 * cm, 19 * cm, "Coef")
                            can.drawCentredString(m4 * cm, 19 * cm, "M x coef")
                            can.drawCentredString(m5 * cm, 19 * cm, "Cote")

                            can.setFillColorRGB(1, 0, 0)
                            can.drawCentredString(m6 * cm, 19 * cm, "Min-Max")
                            can.drawCentredString(m7 * cm, 19 * cm, "Appreciation")
                            can.setFillColorRGB(0, 0, 0)

                        draw_entetes()

                        y = 19

                        details_notes = be.detail_bull_trim(
                            my_class, my_seq.lower(), any_bull['nom']
                        )
                        groupe2 = []
                        groupe1 = []
                        total_general = 0
                        total_coeff_general = 0

                        # Remplissage des matières dans les groupes
                        for data in details_notes:

                            if data["groupe"] == "1ER GROUPE":
                                groupe1.append(
                                    {"matiere": data["matiere"], "coeff": data["coeff"], "note": data["note"],
                                     "total": data["total"],
                                     "cote": data["cote"]}
                                )
                            else:
                                groupe2.append(
                                    {"matiere": data["matiere"], "coeff": data["coeff"], "note": data["note"],
                                     "total": data["total"],
                                     "cote": data["cote"]}
                                )

                        groupes = [{"nom": "1ER GROUPE", "donnees": groupe1}, {"nom": "2E GROUPE", "donnees": groupe2}]

                        # eriture des notes en fonction des groupes
                        for groupe in groupes:

                            total_des_coeff = 0
                            total_points = 0

                            for data in groupe["donnees"]:
                                can.setFillColorRGB(0, 0, 0)
                                can.setFont("calibri", 10)
                                can.drawCentredString(m1 * cm, (y - 0.6) * cm, f"{data['matiere']}")

                                if "D" in data['cote']:
                                    can.setFillColorRGB(1, 0, 0)
                                elif "A" in data['cote']:
                                    can.setFillColorRGB(0, 0.48, 0.22)
                                else:
                                    can.setFillColorRGB(0, 0, 0)

                                can.drawCentredString(m2 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data['note'])}")

                                can.setFillColorRGB(0, 0, 0)
                                can.drawCentredString(m3 * cm, (y - 0.6) * cm, f"{data['coeff']}")
                                can.drawCentredString(m4 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data['total'])}")

                                if "D" in data['cote']:
                                    can.setFillColorRGB(1, 0, 0)
                                elif "A" in data['cote']:
                                    can.setFillColorRGB(0, 0.48, 0.22)
                                else:
                                    can.setFillColorRGB(0, 0, 0)
                                can.drawCentredString(m5 * cm, (y - 0.6) * cm, f"{data['cote']}")

                                can.setFillColorRGB(0, 0, 0)
                                note_min = be.note_min_mat_trim(my_class, data['matiere'],
                                                                my_seq)
                                note_max = be.note_max_mat_trim(my_class, data['matiere'],
                                                                my_seq)
                                can.drawCentredString(m6 * cm, (y - 0.6) * cm, f"{note_min} - {note_max}")

                                can.setStrokeColorRGB(0.3, 0.3, 0.3)
                                can.line(1 * cm, (y - 0.8) * cm, 20 * cm, (y - 0.8) * cm)
                                total_points += data['total']
                                total_des_coeff += data['coeff']

                                # Lignes verticales
                                can.line(b1 * cm, (y - 0.7) * cm, b1 * cm, (y - 0) * cm)
                                can.line(b2 * cm, (y - 0.7) * cm, b2 * cm, (y - 0) * cm)
                                can.line(b3 * cm, (y - 0.7) * cm, b3 * cm, (y - 0) * cm)
                                can.line(b4 * cm, (y - 0.7) * cm, b4 * cm, (y - 0) * cm)
                                can.line(b5 * cm, (y - 0.7) * cm, b5 * cm, (y - 0) * cm)
                                can.line(b6 * cm, (y - 0.7) * cm, b6 * cm, (y - 0) * cm)
                                can.line(b7 * cm, (y - 0.7) * cm, b7 * cm, (y - 0) * cm)
                                can.line(b8 * cm, (y - 0.7) * cm, b8 * cm, (y - 0) * cm)

                                y -= 0.7

                            can.setFont("calibri bold", 10)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(m1 * cm, (y - 0.6) * cm, f"Total {groupe['nom']}")

                            can.setFont("calibri bold", 10)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(m3 * cm, (y - 0.6) * cm, f"{total_des_coeff}")
                            can.drawCentredString(m4 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(total_points)}")

                            moyenne = total_points / total_des_coeff
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(m7 * cm, (y - 0.6) * cm, f"{moyenne:.2f}/20")

                            can.setStrokeColorRGB(0.3, 0.3, 0.3)
                            can.line(1 * cm, (y - 0.8) * cm, 20 * cm, (y - 0.8) * cm)

                            can.line(b1 * cm, (y - 0.8) * cm, b1 * cm, (y - 0) * cm)
                            can.line(b2 * cm, (y - 0.8) * cm, b2 * cm, (y - 0) * cm)
                            can.line(b3 * cm, (y - 0.8) * cm, b3 * cm, (y - 0) * cm)
                            can.line(b4 * cm, (y - 0.8) * cm, b4 * cm, (y - 0) * cm)
                            can.line(b5 * cm, (y - 0.8) * cm, b5 * cm, (y - 0) * cm)
                            can.line(b6 * cm, (y - 0.8) * cm, b6 * cm, (y - 0) * cm)
                            can.line(b7 * cm, (y - 0.8) * cm, b7 * cm, (y - 0) * cm)
                            can.line(b8 * cm, (y - 0.8) * cm, b8 * cm, (y - 0) * cm)

                            total_coeff_general += total_des_coeff
                            total_general += total_points

                            y -= 0.7

                        y = y - 1

                        def draw_recap():
                            can.setStrokeColorRGB(0.3, 0.3, 0.3)
                            can.line(1 * cm, (y + 0.1) * cm, 20 * cm, (y + 0.1) * cm)
                            can.line(b1 * cm, (y + 1) * cm, b1 * cm, (y + 0.1) * cm)
                            can.line(b3 * cm, (y + 1) * cm, b3 * cm, (y + 0.1) * cm)
                            can.line(b4 * cm, (y + 1) * cm, b4 * cm, (y + 0.1) * cm)
                            can.line(b5 * cm, (y + 1) * cm, b5 * cm, (y + 0.1) * cm)
                            can.line(b7 * cm, (y + 1) * cm, b7 * cm, (y + 0.1) * cm)
                            can.line(b8 * cm, (y + 1) * cm, b8 * cm, (y + 0.1) * cm)

                            can.setFont("calibri bold", 11)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawRightString((b3 - 0.2) * cm, (y + 0.4) * cm, "TOTAL")
                            can.drawRightString((b7 - 0.2) * cm, (y + 0.4) * cm, "MOYENNE")
                            can.drawCentredString(m3 * cm, (y + 0.4) * cm, f"{be.ecrire_nombre(total_coeff_general)}")
                            can.drawCentredString(m4 * cm, (y + 0.4) * cm, f"{be.ecrire_nombre(total_general)}")
                            can.drawCentredString(m7 * cm, (y + 0.4) * cm,
                                                  f"{be.ecrire_nombre(total_general / total_coeff_general)}")

                        draw_recap()

                        # Statistiques
                        def draw_cadre_stats():

                            # lignes horizontales
                            can.setFillColorRGB(0.75, 0.75, 0.75)
                            can.line(1 * cm, (y - 0.3) * cm, 20 * cm, (y - 0.3) * cm)
                            can.line(1 * cm, (y - 0.9) * cm, 20 * cm, (y - 0.9) * cm)

                            # Lignes verticales
                            can.line(1 * cm, (y - 0.3) * cm, 1 * cm, (y - 0.9) * cm)
                            can.line(7.3 * cm, (y - 0.3) * cm, 7.3 * cm, (y - 0.9) * cm)
                            can.line(13.6 * cm, (y - 0.3) * cm, 13.6 * cm, (y - 0.9) * cm)
                            can.line(20 * cm, (y - 0.3) * cm, 20 * cm, (y - 0.9) * cm)

                            # cadre stats divisons principales
                            can.setStrokeColorRGB(0.3, 0.3, 0.3)
                            can.line(1 * cm, (y - 0.3) * cm, 1 * cm, (y - 6) * cm)
                            can.line(7.3 * cm, (y - 0.3) * cm, 7.3 * cm, (y - 6) * cm)
                            can.line(13.6 * cm, (y - 0.3) * cm, 13.6 * cm, (y - 6) * cm)
                            can.line(20 * cm, (y - 0.3) * cm, 20 * cm, (y - 6) * cm)
                            can.line(1 * cm, (y - 4) * cm, 20 * cm, (y - 4) * cm)
                            can.line(1 * cm, (y - 6) * cm, 20 * cm, (y - 6) * cm)

                            # divisons verticales secondaires
                            # Discipline
                            can.line(3.15 * cm, (y - 0.9) * cm, 3.15 * cm, (y - 4) * cm)
                            can.line(4.15 * cm, (y - 0.9) * cm, 4.15 * cm, (y - 4) * cm)
                            can.line(6.3 * cm, (y - 0.9) * cm, 6.3 * cm, (y - 4) * cm)
                            # Travail de l'élève
                            can.line(9.3 * cm, (y - 0.9) * cm, 9.3 * cm, (y - 4) * cm)
                            can.line(10.8 * cm, (y - 0.9) * cm, 10.8 * cm, (y - 4) * cm)
                            can.line(12.8 * cm, (y - 1.675) * cm, 12.8 * cm, (y - 4) * cm)
                            can.line(12.8 * cm, (y - 1.675) * cm, 12.8 * cm, (y - 4) * cm)
                            # Profil
                            can.line(17 * cm, (y - 0.9) * cm, 17 * cm, (y - 4) * cm)

                            # divisions horizontales secondaire
                            can.line(1 * cm, (y - 1.675) * cm, 20 * cm, (y - 1.675) * cm)
                            can.line(1 * cm, (y - 2.45) * cm, 20 * cm, (y - 2.45) * cm)
                            can.line(1 * cm, (y - 3.225) * cm, 20 * cm, (y - 3.225) * cm)

                            can.line(10.8 * cm, (y - 2.0125) * cm, 13.6 * cm, (y - 2.0125) * cm)
                            can.line(10.8 * cm, (y - 2.7875) * cm, 13.6 * cm, (y - 2.7875) * cm)

                            # divisons horizontales tertiares

                            can.setFont("calibri", 9)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawString(1.2 * cm, (y - 1.375) * cm, "Abs non J.")
                            can.drawString(1.2 * cm, (y - 1.375) * cm, "Abs non J. (h)")
                            can.drawString(1.2 * cm, (y - 2.15) * cm, "Abs just. (h)")
                            can.drawString(1.2 * cm, (y - 2.925) * cm, "Retards (nb) ")
                            can.drawString(1.2 * cm, (y - 3.7) * cm, "Consignes (h) ")
                            can.drawString(4.21 * cm, (y - 1.375) * cm, "Avertissement")
                            can.drawString(4.21 * cm, (y - 2.15) * cm, "Blâme")
                            can.drawString(4.21 * cm, (y - 2.925) * cm, f"Exclusions (j)")
                            can.drawString(4.21 * cm, (y - 3.7) * cm, f"Exclusion (def)")

                            # remplissage sanctions
                            can.setFont("calibri bold", 10)
                            abs_nj = be.sanction_by_eleve_trim(any_bull['nom'], my_seq,
                                                               'ABSENCE NJ.')
                            abs_jus = be.sanction_by_eleve_trim(any_bull['nom'], my_seq,
                                                                'ABSENCE JUST.')
                            avert = be.sanction_by_eleve_trim(any_bull['nom'], my_seq,
                                                              'AVERTISSEMENT')
                            blame = be.sanction_by_eleve_trim(any_bull['nom'], my_seq, 'BLAME')
                            consigne = be.sanction_by_eleve_trim(any_bull['nom'], my_seq,
                                                                 'CONSIGNE')
                            exclusion = be.sanction_by_eleve_trim(any_bull['nom'], my_seq,
                                                                  'EXCLUSION')
                            exclu_def = be.sanction_by_eleve_trim(any_bull['nom'], my_seq,
                                                                  'EXCLUSION DEF.')
                            retard = be.sanction_by_eleve_trim(any_bull['nom'], my_seq, 'RETARD')

                            can.drawCentredString(3.65 * cm, (y - 1.375) * cm, f"{abs_nj}")
                            can.drawCentredString(3.65 * cm, (y - 2.15) * cm, f"{abs_jus}")
                            can.drawCentredString(3.65 * cm, (y - 2.925) * cm, f"{retard}")
                            can.drawCentredString(3.65 * cm, (y - 3.7) * cm, f"{consigne}")
                            can.drawCentredString(6.8 * cm, (y - 1.375) * cm, f"{avert}")
                            can.drawCentredString(6.8 * cm, (y - 2.15) * cm, f"{blame}")
                            can.drawCentredString(6.8 * cm, (y - 2.925) * cm, f"{exclusion}")
                            can.drawCentredString(6.8 * cm, (y - 3.7) * cm, f"{exclu_def}")

                            # travail de l'élève
                            can.setFont("calibri", 10)
                            can.drawString(7.5 * cm, (y - 1.375) * cm, "Total Gén.".upper())
                            can.drawString(7.5 * cm, (y - 2.15) * cm, "Coef".upper())
                            can.drawString(7.5 * cm, (y - 2.925) * cm, "Moyenne".upper())
                            can.drawString(7.5 * cm, (y - 3.7) * cm, f"Cote".upper())

                            can.setFont("calibri bold", 10)
                            can.drawString(11 * cm, (y - 1.375) * cm, "appreciations.".upper())
                            can.setFont("calibri", 8)
                            can.drawString(11 * cm, (y - 1.9625) * cm, "CTBA")
                            can.drawString(11 * cm, (y - 2.35) * cm, "CBA")
                            can.drawString(11 * cm, (y - 2.7375) * cm, "CA")
                            can.drawString(11 * cm, (y - 3.125) * cm, "CMA")
                            can.drawString(11 * cm, (y - 3.8125) * cm, "CNA")

                            # Remplissage du travail de l'élève
                            can.setFont("calibri bold", 11)
                            can.drawCentredString(10.05 * cm, (y - 1.375) * cm, f"{be.ecrire_nombre(total_general)}")
                            can.drawCentredString(10.05 * cm, (y - 2.15) * cm,
                                                  f"{be.ecrire_nombre(total_coeff_general)}")
                            can.drawCentredString(10.05 * cm, (y - 2.925) * cm, f"{any_bull['moyenne']:.2f}")
                            can.drawCentredString(10.05 * cm, (y - 3.7) * cm,
                                                  f"{be.trouver_cote(any_bull['moyenne'])}")

                            # Profil de la classe
                            can.setFont("calibri", 10)
                            can.drawString(13.8 * cm, (y - 1.375) * cm, "Moyenne générale")
                            can.setFillColorRGB(1, 0, 0)
                            can.setFont("calibri bold", 10)
                            can.drawString(13.8 * cm, (y - 2.15) * cm, "[Min-Max]")
                            can.setFont("calibri", 10)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawString(13.8 * cm, (y - 2.925) * cm, "Nb de moyennes")
                            can.drawString(13.8 * cm, (y - 3.7) * cm, f"Taux de réussite")

                            # Remplissage profil
                            can.setFont("calibri bold", 11)
                            moygen = be.ecrire_nombre(be.moygen_trim(my_class, my_seq.lower()))
                            nmin = be.ecrire_nombre(be.notemin_trim(my_class, my_seq.lower()))
                            nmax = be.ecrire_nombre(be.notemax_trim(my_class, my_seq.lower()))
                            nb_admis = be.nb_admis_trim(my_class, my_seq.lower())
                            taux = be.ecrire_nombre(nb_admis * 100 / be.effectif_classe(my_class))

                            can.drawCentredString(18.5 * cm, (y - 1.375) * cm, f"{moygen}")
                            can.drawCentredString(18.5 * cm, (y - 2.15) * cm,
                                                  f"{nmin} - {nmax}")
                            can.drawCentredString(18.5 * cm, (y - 2.925) * cm,
                                                  f"{nb_admis}")
                            can.drawCentredString(18.5 * cm, (y - 3.7) * cm, f"{taux} %")

                        draw_cadre_stats()

                        # Entêtes des stats
                        def draw_stats_entetes():
                            can.setFont("calibri bold", 11)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(4.15 * cm, (y - 0.7) * cm, "Discipline")
                            can.drawCentredString(10.45 * cm, (y - 0.7) * cm, "Travail de l'èlève")
                            can.drawCentredString(17.3 * cm, (y - 0.7) * cm, "Profil de la classe")

                            can.setFont("calibri", 9)
                            can.drawCentredString(4.15 * cm, (y - 4.4) * cm, "Appréciation du travail de l'élève")
                            can.drawCentredString(4.15 * cm, (y - 4.8) * cm, "(Points forts et points à améliorer)")

                            can.drawCentredString(8.8 * cm, (y - 4.4) * cm, "Visa du parent /")
                            can.drawCentredString(8.8 * cm, (y - 4.8) * cm, "tuteur")

                            can.drawCentredString(11.95 * cm, (y - 4.4) * cm, "Nom et visa du")
                            can.drawCentredString(11.95 * cm, (y - 4.8) * cm, "professeur titulaire")

                            can.drawCentredString(17.3 * cm, (y - 4.4) * cm, "Le chef d'établissement")

                        draw_stats_entetes()

                        can.showPage()
                        decompte += 1
                        self.pb_bull.value = decompte / len(all_bulletins)
                        self.pb_bull.update()
                        self.progres.value = f"{be.ecrire_nombre(decompte * 100 / len(all_bulletins))}%"
                        self.progres.update()

                    can.save()
                    self.cp.cp.box.title.value = "Validé !"
                    self.cp.cp.box.content.value = f"Bulletins de {my_class} pour la {trouver_sequence(my_seq)} créés avec succès"
                    self.cp.cp.box.open = True
                    self.cp.cp.box.update()

            else:
                pass

