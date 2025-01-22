from utils import *
from utils import backend as be
import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_pdf_fonts():
    pdfmetrics.registerFont(TTFont('vinci sans medium', "assets/fonts/vinci_sans_medium.ttf"))
    pdfmetrics.registerFont(TTFont('vinci sans regular', "assets/fonts/vinci_sans_regular.ttf"))
    pdfmetrics.registerFont(TTFont('vinci sans bold', "assets/fonts/vinci_sans_bold.ttf"))
    pdfmetrics.registerFont(TTFont('calibri', "assets/fonts/calibri.ttf"))
    pdfmetrics.registerFont(TTFont('calibri italic', "assets/fonts/calibrii.ttf"))
    pdfmetrics.registerFont(TTFont('calibri bold', "assets/fonts/calibrib.ttf"))
    pdfmetrics.registerFont(TTFont('calibri z', "assets/fonts/calibriz.ttf"))
    pdfmetrics.registerFont(TTFont('Poppins SemiBold', "assets/fonts/Poppins-SemiBold.ttf"))
    pdfmetrics.registerFont(TTFont('Poppins Bold', "assets/fonts/Poppins-Bold.ttf"))


def trouver_sequence(sequence):
    if sequence.lower() == "séquence 1":
        return "premiere sequence"
    elif sequence.lower() == "séquence 2":
        return "deuxieme sequence"
    elif sequence.lower() == "séquence 3":
        return "troisieme sequence"
    elif sequence.lower() == "séquence 4":
        return "quatrieme sequence"
    elif sequence.lower() == "séquence 1":
        return "cinquieme sequence"
    else:
        return "sixieme sequence"


class BullSeq(ft.Tab):
    def __init__(self, cp: object):
        super(BullSeq, self).__init__(
            tab_content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.FOLDER, size=20),
                    ft.Text("Séquences".upper(), font_family="Poppins Medium", size=12)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.cp = cp  # Conteneur parent
        self.classe = ft.Dropdown(**drop_style, prefix_icon="school_outlined", label="classe", width=150)
        self.sequence = ft.Dropdown(**drop_style, prefix_icon=ft.icons.CALENDAR_MONTH_SHARP, label="Séquence",
                                    width=150)
        self.taux = ft.Text("0", size=12, font_family="Poppins Bold", color="black")
        self.info_classe = ft.Text("-", size=12, font_family="Poppins Bold", color="black")
        self.titus = ft.Text("-", size=12, font_family="Poppins Bold", color="black")
        self.effectif = ft.Text("0", size=12, font_family="Poppins Bold", color="black")
        self.moygen = ft.Text("0", size=12, font_family="Poppins Bold", color="black")
        self.notemin = ft.Text("0", size=12, font_family="Poppins Bold", color="black")
        self.notemax = ft.Text("0", size=12, font_family="Poppins Bold", color="black")

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
                            self.info_classe
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
                            self.titus
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
                            self.effectif
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
                            self.moygen
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
                            self.taux
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
                            self.notemin
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
                            self.notemax
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
        self.moy_eleve = ft.Text(size=12, font_family="Poppins Medium", visible=False, color="amber")
        self.rang_eleve = ft.Text(size=12, font_family="Poppins Medium", visible=False, color="amber")
        self.classe_eleve = ft.Text(size=12, font_family="Poppins Medium", visible=False, color="amber")
        self.seq_eleve = ft.Text(size=12, font_family="Poppins Medium", visible=False, color="amber")
        self.cp.cp.fp_onebull_seq.on_result = self.imprimer_un_bulletin
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
                                                    on_click=lambda e: self.cp.cp.fp_onebull_seq.save_file(
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
        self.sel_classe = ft.Dropdown(
            **drop_style, width=170, label="Classe", prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED
        )
        self.sel_seq = ft.Dropdown(
            **drop_style, width=150, label="Séquence", prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED
        )
        self.progres = ft.Text(size=12, font_family="Poppins Italic", color="grey")
        self.cp.cp.fp_allbull_seq.on_result = self.imprimer_all_bulletins
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
                                    self.sel_classe, self.sel_seq, self.progres, self.pb_bull,
                                    ft.ElevatedButton(
                                        **choix_style, width=170,
                                        on_click=lambda e: self.cp.cp.fp_allbull_seq.save_file(allowed_extensions=['pdf'])
                                    )
                                ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
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
                    padding=ft.padding.only(20, 10, 20, 10), expand=True, bgcolor="white", border_radius=12,
                    margin=ft.margin.only(top=10),
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.Divider(height=2, color="transparent"),
                            ft.Row(
                                controls=[
                                    ft.Text("Bulletins séquence".upper(), size=13, font_family="Poppins Medium"),
                                    AnyButton(SECOND_COLOR, "print_outlined", "Classe", "white", self.open_select_window)
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
                                                                    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
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
                                                                    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                                                    on_hover=self.icon_bt_hover2,
                                                                    tooltip="Supprimer filtres",
                                                                    content=ft.Icon(
                                                                        ft.icons.FILTER_ALT_OFF_OUTLINED,
                                                                        color=ft.colors.BLACK45,
                                                                    )
                                                                ),
                                                            ], spacing=10
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
        classes = be.show_classes_autres()
        for classe in classes:
            self.classe.options.append(ft.dropdown.Option(classe))
            self.sel_classe.options.append(ft.dropdown.Option(classe))

        sequences = ['séquence 1', 'séquence 2', 'séquence 3', 'séquence 4', 'séquence 5', 'séquence 6']
        for sequence in sequences:
            self.sequence.options.append(ft.dropdown.Option(sequence.upper()))
            self.sel_seq.options.append(ft.dropdown.Option(sequence.upper()))

    def filter_datas_seq(self, e):
        datas = be.bull_seq()
        bulls = []

        for data in datas:
            dico = {
                "asco": data[0], "classe": data[1], "sequence": data[3], "nom": data[4],
                "nb_coeff": data[6], "total": data[7], "moyenne": data[8], "rang": data[9]
            }
            bulls.append(dico)

        for row in self.table_seq.rows[:]:
            self.table_seq.rows.remove(row)

        une_classe = self.classe.value if self.classe.value is not None else ""
        une_sequence = self.sequence.value if self.sequence.value is not None else ""

        filter_datas = list(
            filter(lambda x: une_classe in x['classe'] and une_sequence in x['sequence'].upper(), bulls))

        if une_classe == "" or une_sequence == "":
            pass

        else:
            self.info_classe.value = self.classe.value
            self.effectif.value = be.effectif_classe(self.classe.value)
            self.moygen.value = f"{(be.search_moygen(self.classe.value, self.sequence.value.lower())):.2f}"
            self.notemax.value = f"{(be.search_notemax_seq(self.classe.value, self.sequence.value.lower())):.2f}"
            self.notemin.value = f"{(be.search_notemin_seq(self.classe.value, self.sequence.value.lower())):.2f}"
            nb_admis = be.nb_admis_seq(self.classe.value, self.sequence.value.lower())
            taux = nb_admis * 100 / be.effectif_classe(self.classe.value)
            self.taux.value = f"{taux:.2f} %"
            self.titus.value = be.search_titus(self.classe.value)
            for widget in (
                    self.effectif, self.moygen, self.notemax,
                    self.notemin, self.taux, self.titus,
                    self.info_classe
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

        self.info_classe.value = "-"
        self.effectif.value = "0"
        self.moygen.value = "0"
        self.notemax.value = "0"
        self.notemin.value = "0"
        self.taux.value = "0"

        for widget in (
                self.effectif, self.moygen, self.notemax,
                self.notemin, self.taux, self.titus,
                self.info_classe
        ):
            widget.update()

    def view_details(self, e):
        for row in self.table_details.rows[:]:
            self.table_details.rows.remove(row)

        donnees = be.details_notes(e.control.data['classe'], e.control.data['sequence'], e.control.data['nom'])
        details = []

        for data in donnees:
            details.append(
                {
                    'matiere': data[1], 'coeff': data[2], 'note': data[3], 'nc': data[4], 'cote': data[5]
                }
            )

        for data in details:
            self.table_details.rows.append(
                ft.DataRow(
                    data=data,
                    cells=[
                        ft.DataCell(ft.Text(data['matiere'])),
                        ft.DataCell(ft.Text(data['coeff'])),
                        ft.DataCell(ft.Text(data['note'])),
                        ft.DataCell(ft.Text(data['nc'])),
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

                # Si le niveau est 6e ou 5e
                if "6E" in niveau or "5E" in niveau:
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
                        # can.drawCentredString(gauche * cm, 26.9 * cm, "*************")
                        # can.setFont("calibri bold", 10)
                        # can.drawCentredString(gauche * cm, 26.9 * cm, "Delegation régionale du centre".upper())
                        # can.setFont("calibri", 9)
                        # can.drawCentredString(gauche * cm, 26.1 * cm, "*************")
                        can.drawCentredString(gauche * cm, 26.9 * cm, "Delegation departementale du mfoundi".upper())
                        # can.drawCentredString(gauche * cm, 25.3 * cm, "*************")
                        # can.drawCentredString(gauche * cm, 24.9 * cm, "Complexe scolaire THECLA".upper())
                        can.drawCentredString(gauche * cm, 26.5 * cm, "Complexe scolaire THECLA".upper())

                        # A droite
                        # can.setFillColorRGB(0, 0, 0)
                        # can.setFont("calibri bold", 10)
                        # can.drawCentredString(droite * cm, 28.5 * cm, "Republique du Cameroun".upper())
                        # can.setFont("calibri z", 9)
                        # can.drawCentredString(droite * cm, 28.1 * cm, "Paix - Travail - Patrie".upper())
                        # can.setFont("calibri", 9)
                        # can.drawCentredString(droite * cm, 27.7 * cm, "*************")
                        # can.setFont("calibri", 9)
                        # can.drawCentredString(droite * cm, 27.3 * cm, "Ministere des enseignements secondaires".upper())
                        # can.setFont("calibri", 9)
                        # can.drawCentredString(droite * cm, 26.9 * cm, "*************")
                        # can.setFont("calibri bold", 10)
                        # can.drawCentredString(droite * cm, 26.5 * cm, "Delegation régionale du centre".upper())
                        # can.setFont("calibri", 9)
                        # can.drawCentredString(droite * cm, 26.1 * cm, "*************")
                        # can.drawCentredString(droite * cm, 25.7 * cm, "Delegation departementale du mfoundi".upper())
                        # can.drawCentredString(droite * cm, 25.3 * cm, "*************")
                        # can.drawCentredString(droite * cm, 24.9 * cm, "collège bista".upper())

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
                        can.setFont("calibri", 7)
                        can.setFillColorRGB(0, 0, 0)
                        can.drawCentredString(10.5 * cm, 0.5 * cm, pied)
                        can.setFont("calibri", 9)
                        can.drawRightString(20 * cm, 0.5 * cm, "Page 1")

                    draw_headers()

                    # divisions pour les lignes horizontales
                    b1, b2, b3, b4, b5, b6, b7, b8, b9, b10 = 1, 4.5, 10, 11, 12, 13, 14.5, 15.5, 17.5, 20

                    # divisions pour les lignes verticales
                    m1 = (b1 + b2) / 2
                    m2 = (b2 + b3) / 2
                    m3 = (b3 + b4) / 2
                    m4 = (b4 + b5) / 2
                    m5 = (b5 + b6) / 2
                    m6 = (b6 + b7) / 2
                    m7 = (b7 + b8) / 2
                    m8 = (b8 + b9) / 2
                    m9 = (b9 + b10) / 2

                    def draw_entetes():
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)

                        # Lignes horizontales
                        can.line(1 * cm, 19.4 * cm, 20 * cm, 19.4 * cm)
                        can.line(1 * cm, 18 * cm, 20 * cm, 18 * cm)
                        # Matieres
                        can.line(1 * cm, 16 * cm, 20 * cm, 16 * cm)
                        can.line(1 * cm, 13.5 * cm, 20 * cm, 13.5 * cm)
                        can.line(1 * cm, 11.8 * cm, 20 * cm, 11.8 * cm)
                        can.line(1 * cm, 7.5 * cm, 20 * cm, 7.5 * cm)
                        can.line(1 * cm, 4.4 * cm, 20 * cm, 4.4 * cm)
                        can.line(1 * cm, 2.9* cm, 20 * cm, 2.9* cm)

                        # Lignes verticales du menu
                        can.line(b1 * cm, 2.9 * cm, b1 * cm, 19.4 * cm)
                        can.line(b2 * cm, 2.9 * cm, b2 * cm, 19.4 * cm)
                        can.line(b3 * cm, 2.9 * cm, b3 * cm, 19.4 * cm)
                        can.line(b4 * cm, 2.9 * cm, b4 * cm, 19.4 * cm)
                        can.line(b5 * cm, 2.9 * cm, b5 * cm, 19.4 * cm)
                        can.line(b6 * cm, 2.9 * cm, b6 * cm, 19.4 * cm)
                        can.line(b7 * cm, 2.9 * cm, b7 * cm, 19.4 * cm)
                        can.line(b8 * cm, 2.9 * cm, b8 * cm, 19.4 * cm)
                        can.line(b9 * cm, 2.9 * cm, b9 * cm, 19.4 * cm)
                        can.line(b10 * cm, 2.9 * cm, b10 * cm, 19.4 * cm)

                        # Entête
                        can.setFont("calibri bold", 10)
                        can.setFillColorRGB(0, 0, 0)
                        can.drawCentredString(m1 * cm, 19 * cm, f"Matiere")
                        can.drawCentredString(m1 * cm, 18.6 * cm, f"et nom de")
                        can.drawCentredString(m1 * cm, 18.2 * cm, f"l'enseignant")
                        can.drawCentredString(m2 * cm, 18.7 * cm, "Compétences évaluées")
                        can.drawCentredString(m3 * cm, 18.7 * cm, "n/20")
                        can.drawCentredString(m4 * cm, 18.7 * cm, "m/20")
                        can.drawCentredString(m5 * cm, 18.7 * cm, "coef")
                        can.drawCentredString(m6 * cm, 18.8 * cm, f"m x")
                        can.drawCentredString(m6 * cm, 18.4 * cm, f"coef")
                        can.drawCentredString(m7 * cm, 18.7 * cm, "Cote")
                        can.setFillColorRGB(1, 0, 0)
                        can.drawCentredString(m8 * cm, 18.7 * cm, "Min-Max")
                        can.drawCentredString(m9 * cm, 19 * cm, f"Appreciation")
                        can.drawCentredString(m9 * cm, 18.6 * cm, "et visa de")
                        can.drawCentredString(m9 * cm, 18.2 * cm, "l'enseignant")
                        can.setFillColorRGB(0, 0, 0)

                        # Entête des matières ......

                        # Anglais
                        can.setFont("calibri", 8)
                        can.setFillColorRGB(0, 0, 0)
                        can.drawString(1.2 * cm, 17.4 * cm, "ANGLAIS")
                        can.drawString(1.2 * cm, 17 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 16.6*cm, ".......")
                        can.drawCentredString(m2*cm, 17.6*cm, "Use appropriate language skills and resources")
                        can.drawCentredString(m2 * cm, 17.3 * cm, "to talk about oneself, the family, and school")
                        can.drawCentredString(m2 * cm, 17 * cm, "community.")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 16.8 * cm, b4 * cm, 16.8 * cm)
                        can.drawCentredString(m2 * cm, 16.5 * cm, "Use appropriate language skills and resources")
                        can.drawCentredString(m2 * cm, 16.2 * cm, "to buy, sell, and explore jobs and professions.")

                        # informatique
                        can.drawString(1.2 * cm, 15.4 * cm, "INFORMATIQUE")
                        can.drawString(1.2 * cm, 15 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 14.6 * cm, ".......")
                        can.drawCentredString(m2 * cm, 15.7 * cm, "Identifier les éléments matériels, logiciels")
                        can.drawCentredString(m2 * cm, 15.4 * cm, "d’un microordinateur et distinguer les types")
                        can.drawCentredString(m2 * cm, 15.1 * cm, "et rôles des différents utilisateurs.")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 14.9 * cm, b4 * cm, 14.9 * cm)
                        can.drawCentredString(m2 * cm, 14.6 * cm, "Décrire les composants externes à l’unité")
                        can.drawCentredString(m2 * cm, 14.3 * cm, "centrale d’un microordinateur et se")
                        can.drawCentredString(m2 * cm, 14 * cm, "conformer aux attitudes règlementaires dans")
                        can.drawCentredString(m2 * cm, 13.7 * cm, "un laboratoire informatique.")

                        # culture nationale
                        can.drawString(1.2 * cm, 13 * cm, "CULTURES NATIONALES")
                        can.drawString(1.2 * cm, 12.6 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 12.2 * cm, ".......")
                        can.drawCentredString(m2 * cm, 13.2 * cm, "Utiliser correctement les concepts clés de la")
                        can.drawCentredString(m2 * cm, 12.9 * cm, "diversité culturelle camerounaise")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 12.7 * cm, b4 * cm, 12.7 * cm)
                        can.drawCentredString(m2 * cm, 12.4 * cm, "Présenter et localiser les pratiques culturelles")
                        can.drawCentredString(m2 * cm, 12.1 * cm, "dans les aires auxquelles elles appartiennent.")

                        # arts et culture
                        can.drawString(1.2 * cm, 11.3 * cm, "EDUCATION")
                        can.drawString(1.2 * cm, 10.9 * cm, "ARTISTIQUE ET")
                        can.drawString(1.2 * cm, 10.5 * cm, "CULTURELLE")
                        can.drawString(1.2 * cm, 10.1 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 9.7 * cm, ".......")
                        can.drawCentredString(m2 * cm, 11.5 * cm, "Déployer son savoir artistique pour utiliser le")
                        can.drawCentredString(m2 * cm, 11.2 * cm, "matériel et le matériau  (le crayon, le ")
                        can.drawCentredString(m2 * cm, 10.9 * cm, "pinceau, les couleurs, les gouaches etc.) et")
                        can.drawCentredString(m2 * cm, 10.6 * cm, "avoir une  position adéquate vis-à-vis du")
                        can.drawCentredString(m2 * cm, 10.3 * cm, "papier ou du support")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 10.1 * cm, b4 * cm, 10.1 * cm)
                        can.drawCentredString(m2 * cm, 9.8 * cm, "Identifier, écrire et utiliser les notes, les")
                        can.drawCentredString(m2 * cm, 9.5 * cm, "figures de notes, la portée et les silences")
                        can.drawCentredString(m2 * cm, 9.2 * cm, "pour parler de la musique")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 9 * cm, b4 * cm, 9 * cm)
                        can.drawCentredString(m2 * cm, 8.7 * cm, "Produire des gestes, des mimes, mimiques ou")
                        can.drawCentredString(m2 * cm, 8.4 * cm, "grimaces dans la déclamation des poèmes, la")
                        can.drawCentredString(m2 * cm, 8.1 * cm, "mise en scène des contes et l’exécution des")
                        can.drawCentredString(m2 * cm, 7.8 * cm, "berceuses en situation familiale ou en public")

                        # Français
                        can.drawString(1.2 * cm, 7 * cm, "français".upper())
                        can.drawString(1.2 * cm, 6.6 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 6.2 * cm, ".......")
                        can.drawCentredString(m2 * cm, 7.2 * cm, "Orthographier correctement un dialogue et")
                        can.drawCentredString(m2 * cm, 6.9 * cm, "une lettre  privée ou bien y corriger des")
                        can.drawCentredString(m2 * cm, 6.6 * cm, "erreurs volontairement insérées")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 6.4 * cm, b4 * cm, 6.4 * cm)
                        can.drawCentredString(m2 * cm, 6.1 * cm, "Répondre correctement à des questions sur")
                        can.drawCentredString(m2 * cm, 5.8 * cm, "un dialogue et sur une lettre privée")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 5.6 * cm, b4 * cm, 5.6 * cm)
                        can.drawCentredString(m2 * cm, 5.3 * cm, "Produire à l’oral comme à l’écrit, dans une")
                        can.drawCentredString(m2 * cm, 5 * cm, "langue correcte et usuelle, un dialogue et une")
                        can.drawCentredString(m2 * cm, 4.7 * cm, "lettre privée")

                        # Eduation artistique
                        can.drawString(1.2 * cm, 3.9 * cm, "LANGUES NATIONALES")
                        can.drawString(1.2 * cm, 3.5 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 3.1* cm, ".......")
                        can.drawCentredString(m2 * cm, 4.1 * cm, "Parler  de la diversité linguistique")
                        can.drawCentredString(m2 * cm, 3.8 * cm, "camerounaise et placer les  langues ")
                        can.drawCentredString(m2 * cm, 3.5 * cm, "nationales dans les aires linguistiques ")
                        can.drawCentredString(m2 * cm, 3.2 * cm, "auxquelles elles appartiennent")

                        can.showPage()

                        # 2e page

                        # Lignes horizontales
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(1 * cm, 29 * cm, 20 * cm, 29 * cm)
                        can.line(1 * cm, 27.3 * cm, 20 * cm, 27.3 * cm)
                        can.line(1 * cm, 24.9 * cm, 20 * cm, 24.9 * cm)
                        can.line(1 * cm, 23.3 * cm, 20 * cm, 23.3 * cm)
                        can.line(1 * cm, 21.8 * cm, 20 * cm, 21.8 * cm)
                        can.line(1 * cm, 20.2 * cm, 20 * cm, 20.2 * cm)
                        can.line(1 * cm, 17.3 * cm, 20 * cm, 17.3 * cm)
                        can.line(1 * cm, 15.1 * cm, 20 * cm, 15.1 * cm)
                        can.line(1 * cm, 13.1 * cm, 20 * cm, 13.1 * cm)
                        can.line(1 * cm, 10.3 * cm, 20 * cm, 10.3 * cm)

                        can.line(1*cm, 9.3*cm, 20*cm, 9.3*cm)

                        # lignes vertciales
                        can.line(b1 * cm, 9.3 * cm, b1 * cm, 29 * cm)
                        can.line(b2 * cm, 10.3 * cm, b2 * cm, 29 * cm)
                        can.line(b3 * cm, 10.3 * cm, b3 * cm, 29 * cm)
                        can.line(b4 * cm, 10.3 * cm, b4 * cm, 29 * cm)
                        can.line(b5 * cm, 9.3 * cm, b5 * cm, 29 * cm)
                        can.line(b6 * cm, 9.3 * cm, b6 * cm, 29 * cm)
                        can.line(b7 * cm, 9.3 * cm, b7 * cm, 29 * cm)
                        can.line(b8 * cm, 10.3 * cm, b8 * cm, 29 * cm)
                        can.line(b9 * cm, 10.3 * cm, b9 * cm, 29 * cm)
                        can.line(b10 * cm, 9.3 * cm, b10 * cm, 29 * cm)

                        # lettres classiques
                        can.setFont("calibri", 8)
                        can.setFillColorRGB(0, 0, 0)
                        can.drawString(1.2 * cm, 28.5 * cm, "LETTRES CLASSIQUES")
                        can.drawString(1.2 * cm, 28.1 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 27.7 * cm, ".......")
                        can.drawCentredString(m2 * cm, 28.7 * cm, "Lire et écrire le latin, Conjuguer et traduire")
                        can.drawCentredString(m2 * cm, 28.4 * cm, "esse et ses composés à l’infectum indicatif;")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 28.2 * cm, b4 * cm, 28.2 * cm)
                        can.drawCentredString(m2 * cm, 27.9 * cm, "répondre correctement aux questions en")
                        can.drawCentredString(m2 * cm, 27.6 * cm, "s’appuyant sur un texte latin")

                        # ECM
                        can.drawString(1.2 * cm, 26.8 * cm, "éducation à la".upper())
                        can.drawString(1.2 * cm, 26.4 * cm, "citoyenneté et".upper())
                        can.drawString(1.2 * cm, 26. * cm, "à la morale".upper())
                        can.drawString(1.2 * cm, 25.6 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 25.2 * cm, ".......")
                        can.drawCentredString(m2 * cm, 26.3 * cm, "Promouvoir l’intégration à la vie familiale et")
                        can.drawCentredString(m2 * cm, 25.9 * cm, "scolaire.")
                        # can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        # can.line(b3 * cm, 28.2 * cm, b4 * cm, 28.2 * cm)

                        # Géographie
                        can.drawString(1.2 * cm, 24.4* cm, "géographie".upper())
                        can.drawString(1.2 * cm, 24 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 23.6 * cm, ".......")
                        can.drawCentredString(m2 * cm, 24.1 * cm, "S’adapter aux influences cosmiques")

                        # Histoire
                        can.drawString(1.2 * cm, 22.8 * cm, "histoire".upper())
                        can.drawString(1.2 * cm, 22.4 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 22 * cm, ".......")
                        can.drawCentredString(m2 * cm, 23 * cm, "Utiliser les savoirs historiques")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 22.8 * cm, b4 * cm, 22.8 * cm)
                        can.drawCentredString(m2 * cm, 22.5 * cm, "Découvrir les traits culturels")

                        # Mathématiques
                        can.drawString(1.2 * cm, 21.3 * cm, "mathématiques".upper())
                        can.drawString(1.2 * cm, 20.9 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 20.5 * cm, ".......")
                        can.drawCentredString(m2 * cm, 21.5 * cm, "Résoudre des situations problèmes relatives")
                        can.drawCentredString(m2 * cm, 21.2 * cm, "aux nombres (entiers naturels, décimaux")
                        can.drawCentredString(m2 * cm, 20.9 * cm, "arithmétiques, décimaux relatifs), aux droites")
                        can.drawCentredString(m2 * cm, 20.6 * cm, "et segments dans le plan et aux cercles.")

                        # Sciences
                        can.drawString(1.2 * cm, 19.7 * cm, "sciences".upper())
                        can.drawString(1.2 * cm, 19.3 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 18.9 * cm, ".......")
                        can.drawCentredString(m2 * cm, 19.9 * cm, "Résoudre, en utilisant la méthode")
                        can.drawCentredString(m2 * cm, 19.6 * cm, "scientifique, des situations problèmes")
                        can.drawCentredString(m2 * cm, 19.3 * cm, "relatives à l’insuffisance des ressources")
                        can.drawCentredString(m2 * cm, 19 * cm, "comestibles et aux propriétés physiques de la")
                        can.drawCentredString(m2 * cm, 18.7 * cm, "matière")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 18.5 * cm, b4 * cm, 18.5 * cm)
                        can.drawCentredString(m2 * cm, 18.2* cm, "Communiquer oralement ou à l’écrit sur ces")
                        can.drawCentredString(m2 * cm, 17.9 * cm, "thèmes à l’aide du langage et des symboles")
                        can.drawCentredString(m2 * cm, 17.6 * cm, "scientifiques adéquats.")

                        # ESF
                        can.drawString(1.2 * cm, 16.8 * cm, "économie sociale".upper())
                        can.drawString(1.2 * cm, 16.4 * cm, "et familiale (esf)".upper())
                        can.drawString(1.2 * cm, 16 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 15.6 * cm, ".......")
                        can.drawCentredString(m2 * cm, 17 * cm, "Expliquer le rôle de l’Économie Sociale et")
                        can.drawCentredString(m2 * cm, 16.7 * cm, "Familiale dans le cadre du développement")
                        can.drawCentredString(m2 * cm, 16.4 * cm, "personnel")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 16.2 * cm, b4 * cm, 16.2 * cm)
                        can.drawCentredString(m2 * cm, 15.9 * cm, "Faire  l’ourlet et fixer le bouton")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 15.7 * cm, b4 * cm, 15.7 * cm)
                        can.drawCentredString(m2 * cm, 15.4 * cm, "Décorer et ranger")

                        # Sport
                        can.drawString(1.2 * cm, 14.6* cm, "éducation physique".upper())
                        can.drawString(1.2 * cm, 14.2 * cm, "et sportive (eps)".upper())
                        can.drawString(1.2 * cm, 13.8 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 13.4 * cm, ".......")
                        can.drawCentredString(m2 * cm, 14.8 * cm, "Exécuter une course de vitesse et une course")
                        can.drawCentredString(m2 * cm, 14.5 * cm, "d’endurance-vitesse")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 14.3 * cm, b4 * cm, 14.3 * cm)
                        can.drawCentredString(m2 * cm, 14 * cm, "Manipuler et lancer le poids")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 13.8 * cm, b4 * cm, 13.8 * cm)
                        can.drawCentredString(m2 * cm, 13.5 * cm, "Exécuter le saut en hauteur")

                        # TM
                        can.drawString(1.2 * cm, 12.6 * cm, "TRAVAIL manuel".upper())
                        can.drawString(1.2 * cm, 12.2 * cm, "M/Mme")
                        can.drawString(1.2 * cm, 11.8 * cm, ".......")
                        can.drawCentredString(m2 * cm, 12.8 * cm, "Utiliser le matériel, les matériaux et les")
                        can.drawCentredString(m2 * cm, 12.5 * cm, "techniques  pour dessiner le kiosque et")
                        can.drawCentredString(m2 * cm, 12.2 * cm, "autres objets")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 12 * cm, b4 * cm, 12 * cm)
                        can.drawCentredString(m2 * cm, 11.7 * cm, "Utiliser  les outils et le matériel agricole pour")
                        can.drawCentredString(m2 * cm, 11.4 * cm, "produire une pépinière")
                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(b2 * cm, 11.2 * cm, b4 * cm, 11.2 * cm)
                        can.drawCentredString(m2 * cm, 10.9 * cm, "Utiliser le matériel et les matériaux pour")
                        can.drawCentredString(m2 * cm, 10.6 * cm, "monter une ferme et y placer les poussins")

                        # Pied de page
                        can.setFont("calibri", 9)
                        can.drawRightString(20 * cm, 0.5 * cm, "Page 2")

                        # total
                        can.setFont("calibri bold", 10)
                        can.setFillColorRGB(0, 0, 0)
                        can.drawRightString((b5-0.2) * cm, 9.6 * cm, "TOTAL")
                        can.drawString((b7+0.2)* cm, 9.6 * cm, "MOYENNE:")

                    draw_entetes()

                    # Statistiques
                    y = 8.3

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
                        abs_nj = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                          'ABSENCE NJ.')
                        abs_jus = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                           'ABSENCE JUST.')
                        avert = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                         'AVERTISSEMENT')
                        blame = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value, 'BLAME')
                        consigne = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                            'CONSIGNE')
                        exclusion = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                             'EXCLUSION')
                        exclu_def = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                             'EXCLUSION DEF.')
                        retard = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value, 'RETARD')
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
                        # can.drawCentredString(10.05 * cm, (y - 1.375) * cm, f"{be.ecrire_nombre(total_general)}")
                        # can.drawCentredString(10.05 * cm, (y - 2.15) * cm, f"{total_coeff_general}")
                        # can.drawCentredString(10.05 * cm, (y - 2.925) * cm, f"{self.moy_eleve.value:.2f}")
                        # can.drawCentredString(10.05 * cm, (y - 3.7) * cm, f"{be.trouver_cote(self.moy_eleve.value)}")

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
                        can.drawCentredString(18.5 * cm, (y - 1.375) * cm, f"{self.moygen.value}")
                        can.drawCentredString(18.5 * cm, (y - 2.15) * cm,
                                              f"{self.notemin.value} - {self.notemax.value}")
                        can.drawCentredString(18.5 * cm, (y - 2.925) * cm,
                                              f"{be.nb_admis_seq(self.classe_eleve.value, self.seq_eleve.value)}")
                        can.drawCentredString(18.5 * cm, (y - 3.7) * cm, f"{self.taux.value}")

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

                # si le niveau est différent de 6e et de 5e
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
                        # can.drawCentredString(gauche * cm, 26.9 * cm, "*************")
                        # can.setFont("calibri bold", 10)
                        # can.drawCentredString(gauche * cm, 26.9 * cm, "Delegation régionale du centre".upper())
                        # can.setFont("calibri", 9)
                        # can.drawCentredString(gauche * cm, 26.1 * cm, "*************")
                        can.drawCentredString(gauche * cm, 26.9 * cm, "Delegation departementale du mfoundi".upper())
                        # can.drawCentredString(gauche * cm, 25.3 * cm, "*************")
                        # can.drawCentredString(gauche * cm, 24.9 * cm, "Complexe scolaire THECLA".upper())
                        can.drawCentredString(gauche * cm, 26.5 * cm, "Complexe scolaire THECLA".upper())

                        # # A droite
                        # can.setFillColorRGB(0, 0, 0)
                        # can.setFont("calibri bold", 10)
                        # can.drawCentredString(droite * cm, 28.5 * cm, "Republique du Cameroun".upper())
                        # can.setFont("calibri z", 9)
                        # can.drawCentredString(droite * cm, 28.1 * cm, "Paix - Travail - Patrie".upper())
                        # can.setFont("calibri", 9)
                        # can.drawCentredString(droite * cm, 27.7 * cm, "*************")
                        # can.setFont("calibri", 9)
                        # can.drawCentredString(droite * cm, 27.3 * cm, "Ministere des enseignements secondaires".upper())
                        # can.setFont("calibri", 9)
                        # can.drawCentredString(droite * cm, 26.9 * cm, "*************")
                        # can.setFont("calibri bold", 10)
                        # can.drawCentredString(droite * cm, 26.5 * cm, "Delegation régionale du centre".upper())
                        # can.setFont("calibri", 9)
                        # can.drawCentredString(droite * cm, 26.1 * cm, "*************")
                        # can.drawCentredString(droite * cm, 25.7 * cm, "Delegation departementale du mfoundi".upper())
                        # can.drawCentredString(droite * cm, 25.3 * cm, "*************")
                        # can.drawCentredString(droite * cm, 24.9 * cm, "collège bista".upper())

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

                    details_notes = be.details_notes_groupe(
                        self.classe_eleve.value, self.seq_eleve.value.lower(), self.title_details.value
                    )
                    total_general = 0
                    total_coeff_general = 0

                    # eriture des notes en fonction des groupes
                    for data in details_notes:
                        can.setFillColorRGB(0, 0, 0)
                        can.setFont("calibri", 10)
                        can.drawCentredString(m1 * cm, (y - 0.6) * cm, f"{data[0]}")
                        can.drawCentredString(m3 * cm, (y - 0.6) * cm, f"{data[2]}")
                        can.drawCentredString(m4 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data[4])}")

                        if "D" in data[6]:
                            can.setFillColorRGB(1, 0, 0)
                        elif "A" in data[6]:
                            can.setFillColorRGB(0, 0.48, 0.22)
                        else:
                            can.setFillColorRGB(0, 0, 0)

                        can.drawCentredString(m5 * cm, (y - 0.6) * cm, f"{data[6]}")
                        can.drawCentredString(m2 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data[3])}")
                        can.setFillColorRGB(0, 0, 0)
                        note_min = be.note_min_mat_seq(data[0], self.seq_eleve.value, self.classe_eleve.value)
                        note_max = be.note_max_mat_seq(data[0], self.seq_eleve.value, self.classe_eleve.value)
                        can.drawCentredString(m6 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(note_min)} - {be.ecrire_nombre(note_max)}")

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

                        total_coeff_general += data[2]
                        total_general += data[4]

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
                        can.drawCentredString(m3 * cm, (y + 0.4) * cm, f"{total_coeff_general}")
                        can.drawCentredString(m4 * cm, (y + 0.4) * cm, f"{total_general}")
                        can.drawCentredString(m7 * cm, (y + 0.4) * cm, f"{(total_general / total_coeff_general):.2f}")

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
                        abs_nj = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                          'ABSENCE NJ.')
                        abs_jus = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                           'ABSENCE JUST.')
                        avert = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                         'AVERTISSEMENT')
                        blame = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value, 'BLAME')
                        consigne = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                            'CONSIGNE')
                        exclusion = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                             'EXCLUSION')
                        exclu_def = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,
                                                             'EXCLUSION DEF.')
                        retard = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value, 'RETARD')
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
                        can.drawCentredString(10.05 * cm, (y - 2.15) * cm, f"{total_coeff_general}")
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
                        can.drawCentredString(18.5 * cm, (y - 1.375) * cm, f"{self.moygen.value}")
                        can.drawCentredString(18.5 * cm, (y - 2.15) * cm, f"{self.notemin.value} - {self.notemax.value}")
                        can.drawCentredString(18.5 * cm, (y - 2.925) * cm,
                                              f"{be.nb_admis_seq(self.classe_eleve.value, self.seq_eleve.value)}")
                        can.drawCentredString(18.5 * cm, (y - 3.7) * cm, f"{self.taux.value}")

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
                    # can.drawCentredString(gauche * cm, 26.9 * cm, "*************")
                    # can.setFont("calibri bold", 10)
                    # can.drawCentredString(gauche * cm, 26.9 * cm, "Delegation régionale du centre".upper())
                    # can.setFont("calibri", 9)
                    # can.drawCentredString(gauche * cm, 26.1 * cm, "*************")
                    can.drawCentredString(gauche * cm, 26.9 * cm, "Delegation departementale du mfoundi".upper())
                    # can.drawCentredString(gauche * cm, 25.3 * cm, "*************")
                    # can.drawCentredString(gauche * cm, 24.9 * cm, "Complexe scolaire THECLA".upper())
                    can.drawCentredString(gauche * cm, 26.5 * cm, "Complexe scolaire THECLA".upper())

                    # # A droite
                    # can.setFillColorRGB(0, 0, 0)
                    # can.setFont("calibri bold", 10)
                    # can.drawCentredString(droite * cm, 28.5 * cm, "Republique du Cameroun".upper())
                    # can.setFont("calibri z", 9)
                    # can.drawCentredString(droite * cm, 28.1 * cm, "Paix - Travail - Patrie".upper())
                    # can.setFont("calibri", 9)
                    # can.drawCentredString(droite * cm, 27.7 * cm, "*************")
                    # can.setFont("calibri", 9)
                    # can.drawCentredString(droite * cm, 27.3 * cm, "Ministere des enseignements secondaires".upper())
                    # can.setFont("calibri", 9)
                    # can.drawCentredString(droite * cm, 26.9 * cm, "*************")
                    # can.setFont("calibri bold", 10)
                    # can.drawCentredString(droite * cm, 26.5 * cm, "Delegation régionale du centre".upper())
                    # can.setFont("calibri", 9)
                    # can.drawCentredString(droite * cm, 26.1 * cm, "*************")
                    # can.drawCentredString(droite * cm, 25.7 * cm, "Delegation departementale du mfoundi".upper())
                    # can.drawCentredString(droite * cm, 25.3 * cm, "*************")
                    # can.drawCentredString(droite * cm, 24.9 * cm, "collège bista".upper())

                    # Le logo
                    monlogo = "assets/mon logo.png"
                    can.drawImage(monlogo, 9 * cm, 27.6 * cm)

                    # entetes année scolaire et séquence
                    can.setFont("calibri bold", 15)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(10.5 * cm, 25.6 * cm, f"bulletin scolaire {trouver_sequence(self.seq_eleve.value)}".upper())

                    can.setFont("calibri", 12)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(10.5 * cm, 25.1 * cm, f"Année scolaire {asco - 1} / {asco}")

                    # infos sur l'élève ________________________

                    # Lignes horizontales
                    # 1ere ligne
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    can.line(4*cm, 24.6*cm, 20*cm, 24.6*cm)

                    # Lignes du milieu
                    can.line(4*cm, 23.9*cm, 20*cm, 23.9*cm)
                    can.line(4*cm, 23.2*cm, 20*cm, 23.2*cm)
                    can.line(4*cm, 22.5*cm, 16*cm, 22.5*cm)

                    # Dernière ligne
                    can.line(4*cm, 21.3*cm, 20*cm, 21.3*cm)

                    # Lignes verticales
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    # 1ere ligne
                    can.line(4*cm, 24.6*cm, 4*cm, 21.3*cm)

                    can.line(11 * cm, 23.2 * cm, 11 * cm, 22.5 * cm)
                    can.line(13.5 * cm, 23.9 * cm, 13.5 * cm, 23.2 * cm)
                    can.line(16 * cm, 24.6 * cm, 16 * cm, 21.3 * cm)

                    # Dernière ligne
                    can.line(20*cm, 24.6*cm, 20*cm, 21.3*cm)

                    # champs d'informations
                    can.setFont("calibri", 10)
                    can.drawString(4.2*cm, 24.1*cm, "Nom de l'élève:")
                    can.drawString(16.2* cm, 24.1 * cm, "Classe:")
                    can.drawString(4.2*cm, 23.4*cm, "Date et lieu de naissance:")
                    can.drawString(13.8 * cm, 23.4 * cm, "Genre:")
                    can.drawString(16.2 * cm, 23.4 * cm, "Effectif:")
                    can.setFillColorRGB(1, 0, 0)
                    can.drawString(4.2*cm, 22.7*cm, "Identifiant unique:")
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(11.2 * cm, 22.7 * cm, "Redoublant: oui          non")
                    can.drawString(16.2 * cm, 22.7 * cm, "Professeur principal:")
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(4.2*cm, 22*cm, "Noms et contact des parents/tuteurs:")

                    # remplissage des informations
                    can.setFont("calibri bold", 11)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawString(6.7 * cm, 24.1 * cm, f"{self.title_details.value}")

                    infos = be.search_elev_by_nom(self.title_details.value)
                    can.drawString(17.4 * cm, 24.1 * cm, f"{self.classe_eleve.value}")
                    # Date et lieu de naissance
                    can.drawString(8 * cm, 23.4 * cm, f"{infos[2]} à {infos[3]}")
                    # sexe
                    can.drawString(15.2 * cm, 23.4 * cm, f"{infos[4]}")
                    # Effectif
                    can.drawString(17.8 * cm, 23.4 * cm, f"{be.effectif_classe(self.classe_eleve.value)}")
                    # Contact parents
                    can.drawString(4.2 * cm, 21.5 * cm, f"{infos[5]} / {infos[7]}")

                    prof_titus = be.search_titus(self.classe_eleve.value)
                    sep = prof_titus.split(" ")
                    can.drawString(16.2 * cm, 22.3 * cm, f"{sep[0]}")
                    can.drawString(16.2 * cm, 21.9 * cm, f"{sep[1]}")

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
                    can.line(1 * cm, 21 * cm, 20 * cm, 21 * cm)
                    can.line(1 * cm, 20.4 * cm, 20 * cm, 20.4 * cm)

                    # Lignes verticales
                    can.line(b1 * cm, 20.4 * cm, b1 * cm, 21 * cm)
                    can.line(b2 * cm, 20.4 * cm, b2 * cm, 21 * cm)
                    can.line(b3 * cm, 20.4 * cm, b3 * cm, 21 * cm)
                    can.line(b4 * cm, 20.4 * cm, b4 * cm, 21 * cm)
                    can.line(b5 * cm, 20.4 * cm, b5 * cm, 21 * cm)
                    can.line(b6 * cm, 20.4 * cm, b6 * cm, 21 * cm)
                    can.line(b7 * cm, 20.4 * cm, b7 * cm, 21 * cm)
                    can.line(b8 * cm, 20.4 * cm, b8 * cm, 21 * cm)

                    can.setFont("calibri bold", 10)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(m1 * cm, 20.6 * cm, "Matiere")
                    can.drawCentredString(m2 * cm, 20.6 * cm, "M/20")
                    can.drawCentredString(m3 * cm, 20.6 * cm, "Coef")
                    can.drawCentredString(m4 * cm, 20.6 * cm, "M x coef")
                    can.drawCentredString(m5 * cm, 20.6 * cm, "Cote")

                    can.setFillColorRGB(1, 0, 0)
                    can.drawCentredString(m6 * cm, 20.6 * cm, "Min-Max")
                    can.drawCentredString(m7 * cm, 20.6 * cm, "Appreciation")
                    can.setFillColorRGB(0, 0, 0)

                draw_entetes()

                y = 20.6

                details_notes = be.details_notes_groupe(
                    self.classe_eleve.value, self.seq_eleve.value.lower(), self.title_details.value
                )
                groupe2 = []
                groupe1 = []
                total_general = 0
                total_coeff_general = 0

                # Remplissage des matières dans les groupes
                for data in details_notes:

                    if data[5] == "1ER GROUPE":
                        groupe1.append(
                            {"matiere": data[0], "coeff": data[2], "note": data[3], "total": data[4],
                             "cote": data[6]}
                        )
                    else:
                        groupe2.append(
                            {"matiere": data[0], "coeff": data[2], "note": data[3], "total": data[4],
                             "cote": data[6]}
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
                        can.drawCentredString(m3 * cm, (y - 0.6) * cm, f"{data['coeff']}")
                        can.drawCentredString(m4 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data['total'])}")

                        if "D" in data['cote']:
                            can.setFillColorRGB(1, 0, 0)
                        elif "A" in data['cote']:
                            can.setFillColorRGB(0, 0.48, 0.22)
                        else:
                            can.setFillColorRGB(0, 0, 0)

                        can.drawCentredString(m5 * cm, (y-0.6) * cm, f"{data['cote']}")
                        can.drawCentredString(m2 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data['note'])}")
                        can.setFillColorRGB(0, 0, 0)
                        note_min = be.note_min_mat_seq(data['matiere'], self.seq_eleve.value, self.classe_eleve.value)
                        note_max = be.note_max_mat_seq(data['matiere'], self.seq_eleve.value, self.classe_eleve.value)
                        can.drawCentredString(m6 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(note_min)} - {be.ecrire_nombre(note_max)}")

                        can.setStrokeColorRGB(0.3, 0.3, 0.3)
                        can.line(1 * cm, (y-0.8) * cm, 20 * cm, (y-0.8) * cm)
                        total_points += data['total']
                        total_des_coeff += data['coeff']

                        # Lignes verticales
                        can.line(b1 * cm, (y-0.7) * cm, b1 * cm, (y-0) * cm)
                        can.line(b2 * cm, (y-0.7) * cm, b2 * cm, (y-0) * cm)
                        can.line(b3 * cm, (y-0.7) * cm, b3 * cm, (y-0) * cm)
                        can.line(b4 * cm, (y-0.7) * cm, b4 * cm, (y-0) * cm)
                        can.line(b5 * cm, (y-0.7) * cm, b5 * cm, (y-0) * cm)
                        can.line(b6 * cm, (y-0.7) * cm, b6 * cm, (y-0) * cm)
                        can.line(b7 * cm, (y-0.7) * cm, b7 * cm, (y-0) * cm)
                        can.line(b8 * cm, (y-0.7) * cm, b8 * cm, (y-0) * cm)

                        y -= 0.7

                    can.setFont("calibri bold", 10)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(m1* cm, (y - 0.6) * cm, f"Total {groupe['nom']}")

                    can.setFont("calibri bold", 10)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(m3 * cm, (y - 0.6) * cm, f"{total_des_coeff}")
                    can.drawCentredString(m4 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(total_points)}")

                    moyenne = total_points / total_des_coeff
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(m7 * cm, (y - 0.6) * cm, f"{moyenne:.2f}/20")

                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    can.line(1 * cm, (y-0.8) * cm, 20 * cm, (y-0.8) * cm)

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
                    can.line(1 * cm, (y+0.1) * cm, 20 * cm, (y+0.1) * cm)
                    can.line(b1*cm, (y+1)*cm, b1*cm, (y+0.1)*cm)
                    can.line(b3 * cm, (y + 1) * cm, b3 * cm, (y + 0.1) * cm)
                    can.line(b4 * cm, (y + 1) * cm, b4 * cm, (y + 0.1) * cm)
                    can.line(b5 * cm, (y + 1) * cm, b5 * cm, (y + 0.1) * cm)
                    can.line(b7 * cm, (y+1) * cm, b7 * cm, (y+0.1) * cm)
                    can.line(b8 * cm, (y + 1) * cm, b8 * cm, (y + 0.1) * cm)

                    can.setFont("calibri bold", 11)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawRightString((b3 -0.2)*cm, (y + 0.4)*cm, "TOTAL")
                    can.drawRightString((b7 - 0.2) * cm, (y + 0.4) * cm, "MOYENNE")
                    can.drawCentredString(m3*cm, (y + 0.4)*cm, f"{total_coeff_general}")
                    can.drawCentredString(m4 * cm, (y + 0.4) * cm, f"{total_general}")
                    can.drawCentredString(m7 * cm, (y + 0.4) * cm, f"{(total_general / total_coeff_general):.2f}")

                draw_recap()

                # Statistiques
                def draw_cadre_stats():

                    # lignes horizontales
                    can.setFillColorRGB(0.75, 0.75, 0.75)
                    can.line(1 * cm, (y - 0.3) * cm, 20 * cm, (y - 0.3) * cm)
                    can.line(1 * cm, (y - 0.9) * cm, 20 * cm, (y - 0.9) * cm)

                    # Lignes verticales
                    can.line(1 * cm, (y - 0.3) * cm, 1 * cm, (y-0.9) * cm)
                    can.line(7.3 * cm, (y - 0.3) * cm, 7.3 * cm, (y-0.9) * cm)
                    can.line(13.6 * cm, (y - 0.3) * cm, 13.6 * cm, (y-0.9) * cm)
                    can.line(20 * cm, (y - 0.3) * cm,  20 * cm, (y-0.9) * cm)

                    # cadre stats divisons principales
                    can.setStrokeColorRGB(0.3, 0.3, 0.3)
                    can.line(1 * cm, (y - 0.3) * cm, 1 * cm, (y-6) * cm)
                    can.line(7.3 * cm, (y - 0.3) * cm, 7.3 * cm, (y-6) * cm)
                    can.line(13.6 * cm, (y - 0.3) * cm, 13.6 * cm, (y-6) * cm)
                    can.line(20 * cm, (y - 0.3) * cm, 20 * cm, (y-6) * cm)
                    can.line(1 * cm, (y-4) * cm, 20 * cm, (y-4) * cm)
                    can.line(1 * cm, (y-6) * cm, 20 * cm, (y-6) * cm)

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
                    can.drawString(1.2*cm, (y-1.375)*cm, "Abs non J.")
                    can.drawString(1.2 * cm, (y - 1.375) * cm, "Abs non J. (h)")
                    can.drawString(1.2 * cm, (y - 2.15) * cm, "Abs just. (h)")
                    can.drawString(1.2 * cm, (y - 2.925) * cm, "Retards (nb) ")
                    can.drawString(1.2 * cm, (y - 3.7) * cm, "Consignes (h) ")
                    can.drawString(4.21 * cm, (y -1.375) * cm, "Avertissement")
                    can.drawString(4.21 * cm, (y - 2.15) * cm, "Blâme")
                    can.drawString(4.21 * cm, (y - 2.925) * cm, f"Exclusions (j)")
                    can.drawString(4.21 * cm, (y - 3.7) * cm, f"Exclusion (def)")

                    # remplissage sanctions
                    can.setFont("calibri bold", 10)
                    abs_nj = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value, 'ABSENCE NJ.')
                    abs_jus = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value, 'ABSENCE JUST.')
                    avert = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value, 'AVERTISSEMENT')
                    blame = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value, 'BLAME')
                    consigne = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value, 'CONSIGNE')
                    exclusion = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value, 'EXCLUSION')
                    exclu_def = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value,'EXCLUSION DEF.')
                    retard = be.sanction_by_eleve_seq(self.title_details.value, self.seq_eleve.value, 'RETARD')
                    can.drawCentredString(3.65* cm, (y - 1.375) * cm, f"{abs_nj}")
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
                    can.drawCentredString(10.05*cm, (y - 1.375) * cm, f"{be.ecrire_nombre(total_general)}")
                    can.drawCentredString(10.05 * cm, (y - 2.15) * cm, f"{total_des_coeff}")
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
                    can.drawCentredString(18.5 * cm, (y - 1.375) * cm, f"{self.moygen.value}")
                    can.drawCentredString(18.5 * cm, (y - 2.15) * cm, f"{self.notemin.value} - {self.notemax.value}")
                    can.drawCentredString(18.5 * cm, (y - 2.925) * cm, f"{be.nb_admis_seq(self.classe_eleve.value, self.seq_eleve.value)}")
                    can.drawCentredString(18.5 * cm, (y - 3.7) * cm, f"{self.taux.value}")

                draw_cadre_stats()

                # Entêtes des stats
                def draw_stats_entetes():
                    can.setFont("calibri bold", 11)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(4.15 * cm, (y-0.7) * cm, "Discipline")
                    can.drawCentredString(10.45 * cm, (y-0.7) * cm, "Travail de l'èlève")
                    can.drawCentredString(17.3 * cm, (y-0.7) * cm, "Profil de la classe")

                    can.setFont("calibri", 9)
                    can.drawCentredString(4.15*cm, (y-4.4)*cm, "Appréciation du travail de l'élève")
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
        for widget in (self.sel_seq, self.sel_classe):
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
            my_class = self.sel_classe.value
            my_seq = self.sel_seq.value.lower()

            if save_location != "None.pdf":
                # ressortir les bulletins filtrés
                def liste_bulletins():
                    bulletins = be.bull_seq_class_seq(my_class, my_seq)
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
                            can.drawCentredString(gauche * cm, 25.7 * cm, "Delegation departementale du mfoundi".upper())
                            can.drawCentredString(gauche * cm, 25.3 * cm, "*************")
                            can.drawCentredString(gauche * cm, 24.9 * cm, "collège bista".upper())

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
                            can.drawCentredString(droite * cm, 25.7 * cm, "Delegation departementale du mfoundi".upper())
                            can.drawCentredString(droite * cm, 25.3 * cm, "*************")
                            can.drawCentredString(droite * cm, 24.9 * cm, "collège bista".upper())

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

                        details_notes = be.details_notes_groupe(
                            my_class, my_seq, any_bull['nom']
                        )
                        total_general = 0
                        total_coeff_general = 0

                        # eriture des notes en fonction des groupes
                        for data in details_notes:
                            can.setFillColorRGB(0, 0, 0)
                            can.setFont("calibri", 10)
                            can.drawCentredString(m1 * cm, (y - 0.6) * cm, f"{data[0]}")
                            can.drawCentredString(m3 * cm, (y - 0.6) * cm, f"{data[2]}")
                            can.drawCentredString(m4 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data[4])}")

                            if "D" in data[6]:
                                can.setFillColorRGB(1, 0, 0)
                            elif "A" in data[6]:
                                can.setFillColorRGB(0, 0.48, 0.22)
                            else:
                                can.setFillColorRGB(0, 0, 0)

                            can.drawCentredString(m5 * cm, (y - 0.6) * cm, f"{data[6]}")
                            can.drawCentredString(m2 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data[3])}")
                            can.setFillColorRGB(0, 0, 0)
                            note_min = be.note_min_mat_seq(data[0], my_seq, my_class)
                            note_max = be.note_max_mat_seq(data[0], my_seq, my_class)
                            can.drawCentredString(m6 * cm, (y - 0.6) * cm,
                                                  f"{be.ecrire_nombre(note_min)} - {be.ecrire_nombre(note_max)}")

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

                            total_coeff_general += data[2]
                            total_general += data[4]

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
                            can.drawCentredString(m3 * cm, (y + 0.4) * cm, f"{total_coeff_general}")
                            can.drawCentredString(m4 * cm, (y + 0.4) * cm, f"{total_general}")
                            can.drawCentredString(m7 * cm, (y + 0.4) * cm, f"{(total_general / total_coeff_general):.2f}")

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
                            abs_nj = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'ABSENCE NJ.')
                            abs_jus = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(),'ABSENCE JUST.')
                            avert = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(),'AVERTISSEMENT')
                            blame = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), "BLAME")
                            consigne = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'CONSIGNE')
                            exclusion = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'EXCLUSION')
                            exclu_def = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'EXCLUSION DEF.')
                            retard = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'RETARD')

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
                            can.drawCentredString(10.05 * cm, (y - 2.15) * cm, f"{total_coeff_general}")
                            can.drawCentredString(10.05 * cm, (y - 2.925) * cm, f"{any_bull['moyenne']:.2f}")
                            can.drawCentredString(10.05 * cm, (y - 3.7) * cm, f"{be.trouver_cote(any_bull['moyenne'])}")

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
                            moy = be.ecrire_nombre(be.search_moygen(any_bull['classe'], any_bull['sequence']))
                            nmin = be.ecrire_nombre(be.search_notemin_seq(my_class, my_seq))
                            nmax = be.ecrire_nombre(be.search_notemax_seq(my_class, my_seq))
                            nb_admis = be.nb_admis_seq(my_class, my_seq)
                            taux = nb_admis *100 / be.effectif_classe(my_class)
                            can.drawCentredString(18.5 * cm, (y - 1.375) * cm, f"{moy}")
                            can.drawCentredString(18.5 * cm, (y - 2.15) * cm, f"{nmin} - {nmax}")
                            can.drawCentredString(18.5 * cm, (y - 2.925) * cm, f"{nb_admis}")
                            can.drawCentredString(18.5 * cm, (y - 3.7) * cm, f"{be.ecrire_nombre(taux)}%")

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

                # Bulletin des classes du second cycle
                else:
                    decompte = 0

                    for any_bull in all_bulletins:
                        gauche, droite, y = 4.25, 17.25, 28

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
                            can.drawCentredString(gauche * cm, 25.7 * cm, "Delegation departementale du mfoundi".upper())
                            can.drawCentredString(gauche * cm, 25.3 * cm, "*************")
                            can.drawCentredString(gauche * cm, 24.9 * cm, "collège bista".upper())

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
                            can.drawCentredString(droite * cm, 25.7 * cm, "Delegation departementale du mfoundi".upper())
                            can.drawCentredString(droite * cm, 25.3 * cm, "*************")
                            can.drawCentredString(droite * cm, 24.9 * cm, "collège bista".upper())

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

                        details_notes = be.details_notes_groupe(my_class, my_seq.lower(), any_bull['nom'])
                        groupe2 = []
                        groupe1 = []
                        total_general = 0
                        total_coeff_general = 0

                        # Remplissage des matières dans les groupes
                        for data in details_notes:

                            if data[5] == "1ER GROUPE":
                                groupe1.append(
                                    {"matiere": data[0], "coeff": data[2], "note": data[3], "total": data[4],
                                     "cote": data[6]}
                                )
                            else:
                                groupe2.append(
                                    {"matiere": data[0], "coeff": data[2], "note": data[3], "total": data[4],
                                     "cote": data[6]}
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
                                can.drawCentredString(m3 * cm, (y - 0.6) * cm, f"{data['coeff']}")
                                can.drawCentredString(m4 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data['total'])}")

                                if "D" in data['cote']:
                                    can.setFillColorRGB(1, 0, 0)
                                elif "A" in data['cote']:
                                    can.setFillColorRGB(0, 0.48, 0.22)
                                else:
                                    can.setFillColorRGB(0, 0, 0)

                                can.drawCentredString(m5 * cm, (y - 0.6) * cm, f"{data['cote']}")
                                can.drawCentredString(m2 * cm, (y - 0.6) * cm, f"{be.ecrire_nombre(data['note'])}")
                                can.setFillColorRGB(0, 0, 0)
                                note_min = be.ecrire_nombre(be.note_min_mat_seq(data['matiere'], my_seq, my_class))
                                note_max = be.ecrire_nombre(be.note_max_mat_seq(data['matiere'], my_seq, my_class))
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
                            can.drawCentredString(m3 * cm, (y + 0.4) * cm, f"{total_coeff_general}")
                            can.drawCentredString(m4 * cm, (y + 0.4) * cm, f"{total_general}")
                            can.drawCentredString(m7 * cm, (y + 0.4) * cm, f"{(total_general / total_coeff_general):.2f}")

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
                            abs_nj = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'ABSENCE NJ.')
                            abs_jus = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'ABSENCE JUST.')
                            avert = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'AVERTISSEMENT')
                            blame = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'BLAME')
                            consigne = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'CONSIGNE')
                            exclusion = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'EXCLUSION')
                            exclu_def = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'EXCLUSION DEF.')
                            retard = be.sanction_by_eleve_seq(any_bull['nom'], my_seq.upper(), 'RETARD')

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
                            can.drawCentredString(10.05 * cm, (y - 2.15) * cm, f"{total_des_coeff}")
                            can.drawCentredString(10.05 * cm, (y - 2.925) * cm, f"{any_bull['moyenne']:.2f}")
                            can.drawCentredString(10.05 * cm, (y - 3.7) * cm, f"{be.trouver_cote(any_bull['moyenne'])}")

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
                            moy = be.ecrire_nombre(be.search_moygen(any_bull['classe'], any_bull['sequence']))
                            nmin = be.ecrire_nombre(be.search_notemin_seq(my_class, my_seq))
                            nmax = be.ecrire_nombre(be.search_notemax_seq(my_class, my_seq))
                            nb_admis = be.nb_admis_seq(my_class, my_seq)
                            taux = nb_admis * 100 / be.effectif_classe(my_class)

                            can.drawCentredString(18.5 * cm, (y - 1.375) * cm, f"{moy}")
                            can.drawCentredString(18.5 * cm, (y - 2.15) * cm, f"{nmin} - {nmax}")
                            can.drawCentredString(18.5 * cm, (y - 2.925) * cm, f"{nb_admis}")
                            can.drawCentredString(18.5 * cm, (y - 3.7) * cm, f"{be.ecrire_nombre(taux)}%")

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
                    self.cp.cp.box.content.value = f"Bulletins {my_class} pour la {trouver_sequence(my_seq)} créés avec succès"
                    self.cp.cp.box.open = True
                    self.cp.cp.box.update()

            else:
                pass

