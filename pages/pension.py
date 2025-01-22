from utils import *
from utils import backend as be
import pandas
import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pages.tranche import Tranches

selection_tranche = {"name": ""}


class Pensions(ft.Container):
    def __init__(self, cp: object):
        super(Pensions, self).__init__(expand=True)
        self.cp = cp

        self.tpr = ft.Text("", size=24, font_family="Poppins Light", color="black")
        self.mt_att = ft.Text("", size=24, font_family="Poppins Light", color="black")
        self.pr = ft.Text("", size=12, font_family="Poppins Medium", color="blue")
        self.rar = ft.Text("", size=24, font_family="Poppins Light", color="black")

        self.classe = ft.Dropdown(**drop_style, prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, width=150, label="Classe")
        self.eleve = ft.TextField(**field_style, width=300, prefix_icon="person_outlined", label="Elève")
        self.statut = ft.Dropdown(
            **drop_style, prefix_icon=ft.icons.SIGNAL_WIFI_STATUSBAR_4_BAR_OUTLINED, width=150, label="Statut",
            options=[ft.dropdown.Option("soldée"),ft.dropdown.Option("en cours")]
        )
        self.cp.fp_extraire_pdf_pensions.on_result = self.imprimer_pdf
        self.cp.fp_extraire_xls_pensions.on_result = self.extraire_excel
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("")),
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("Classe")),
                ft.DataColumn(label=ft.Text("Montant")),
                ft.DataColumn(label=ft.Text("Total")),
                ft.DataColumn(label=ft.Text("Reste")),
                ft.DataColumn(label=ft.Text("Actions")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )
        self.filrtres_frame = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=390, height=465,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                bgcolor="#f0f0f6", padding=20,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=10, bgcolor="white", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Icon(ft.icons.FILTER_ALT_OFF, color="black"),
                                            ft.Text("Filtres".upper(), size=14, font_family="Poppins Medium")
                                        ]
                                    ),
                                    ft.IconButton(
                                        "close", scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                        on_click=self.close_filtres_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),ft.Container(
                            padding=20, bgcolor="white", border_radius=12,
                            content=ft.Column(
                                controls=[
                                    self.classe, self.eleve, self.statut,
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **bt_filtre_style, on_click=self.filter_datas, width=170
                                    ),
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **bt_supp_style, on_click=self.supp_filtres, width=170
                                    )
                                ], spacing=20
                            )
                        )
                    ], spacing=10
                )
            )
        )

        self.main_window = ft.Container(
            padding=ft.padding.only(20, 0, 20, 0), expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        padding=ft.padding.only(30, 15, 30, 15), border_radius=12,
                        content=ft.Column(
                            controls=[
                                ft.Text("Chiffres", size=13, font_family="Poppins Bold", color="black"),
                                ft.Divider(height=1, thickness=1),
                                ft.Row(
                                    controls=[
                                        ft.Column(
                                            [
                                                ft.Text("Mt. attendu", size=11, font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.MONETIZATION_ON_OUTLINED, size=20,
                                                                color="black87"),
                                                        self.mt_att
                                                    ]
                                                ),

                                            ], spacing=3, horizontal_alignment="center",
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("Mt. Perçu", size=12,
                                                        font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.RECEIPT_OUTLINED, size=20,
                                                                color="black87"),

                                                        ft.Row([self.tpr, self.pr], vertical_alignment="end")
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment="center",
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("A percevoir", size=11,
                                                        font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.REAL_ESTATE_AGENT_OUTLINED, size=20,
                                                                color="black87"),

                                                        self.rar
                                                    ]
                                                ),

                                            ], spacing=3, horizontal_alignment="center",
                                        ),
                                    ], spacing=40, vertical_alignment="start"
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
                                        ft.Row(
                                            controls=[
                                                ft.Text("Frais de scolarité", size=14, font_family="Poppins Bold"),
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[
                                                AnyButton(FIRST_COLOR, ft.icons.FILTER_ALT_OUTLINED,
                                                    "Filtrer", "white", self.open_filtres_window,
                                                ),
                                                AnyButton(SECOND_COLOR, ft.icons.FILTER_ALT_OFF_OUTLINED,
                                                          "Supp. Ft.", "white", self.supp_filtres,
                                                ),
                                                AnyButton(
                                                    THRID_COLOR, ft.icons.DISABLED_VISIBLE_OUTLINED,
                                                    "Tranches", "white", self.open_choice_frame
                                                )
                                            ], spacing=15
                                        )
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Divider(height=2, color="transparent"),
                                ft.Column(
                                    expand=True,
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Container(
                                                    border=ft.border.all(1, "grey"),
                                                    border_radius=6, bgcolor="#f0f0f6", padding=5,
                                                    on_click=lambda e: self.cp.fp_extraire_pdf_pensions.save_file(
                                                            allowed_extensions=["pdf"]),
                                                    scale=ft.transform.Scale(1),
                                                    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                                    on_hover=self.icon_bt_hover2,
                                                    tooltip="Imprimer PDF",
                                                    content=ft.Icon(
                                                        ft.icons.PRINT_OUTLINED,
                                                        color=ft.colors.BLACK45,
                                                    )
                                                ),
                                                ft.Container(
                                                    border=ft.border.all(1, "grey"),
                                                    border_radius=6, bgcolor="#f0f0f6", padding=5,
                                                    on_click=lambda e: self.cp.fp_extraire_xls_pensions.save_file(
                                                        allowed_extensions=["xls", "xlsx"]),
                                                    scale=ft.transform.Scale(1),
                                                    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                                    on_hover=self.icon_bt_hover2,
                                                    tooltip="Extraire xls",
                                                    content=ft.Icon(
                                                        ft.icons.FILE_DOWNLOAD_OUTLINED,
                                                        color=ft.colors.BLACK45,
                                                    )
                                                )
                                            ], alignment=ft.MainAxisAlignment.START
                                        ),
                                        ft.Divider(height=2, color="transparent"),
                                        ft.ListView(expand=True, controls=[self.table])
                                    ],
                                )
                            ]
                        )
                    )
                ]
            )
        )

        # details frame
        self.title_details = ft.Text(size=14, font_family="Poppins Bold", color=FIRST_COLOR)
        self.table_details = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Tranche")),
                ft.DataColumn(label=ft.Text("Date de paiement")),
                ft.DataColumn(label=ft.Text("Montant")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            rows=[]
        )
        self.pb = ft.ProgressBar(bgcolor="grey", bar_height=7, width=120, border_radius=8)
        self.pb_label = ft.Text("", size=14, font_family="Poppins Bold", color="white")
        self.icone_t1 = ft.Icon(name=None, size=18)
        self.icone_t2 = ft.Icon(name=None, size=18)
        self.icone_t3 = ft.Icon(name=None, size=18)
        self.details_frame = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=500, height=500, expand=True,
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
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.MONETIZATION_ON, color=SECOND_COLOR),
                                            ft.Text("état Pension".upper(), size=14, font_family="Poppins Medium"),
                                        ]
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                        on_click=self.close_details_frame
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white", expand=True,
                            content=ft.Column(
                                expand=True,
                                controls=[
                                    ft.Column(
                                        controls=[
                                            self.title_details,
                                            ft.Row(
                                                controls=[
                                                    ft.Container(
                                                        bgcolor=FIRST_COLOR, border_radius=10, padding=10,
                                                        content=ft.Row([self.pb_label], alignment=ft.MainAxisAlignment.CENTER)
                                                    ),
                                                    self.pb
                                                ], spacing=50
                                            )
                                        ], spacing=20
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Divider(height=1, thickness=1),
                                            ft.Row(
                                                [ft.Text(value='Tranche 1', size=13, font_family="Poppins Medium"), self.icone_t1],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.Divider(height=1, thickness=1),
                                            ft.Row(
                                                [ft.Text(value='Tranche 2', size=13, font_family="Poppins Medium"), self.icone_t2],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.Divider(height=1, thickness=1),
                                            ft.Row(
                                                [ft.Text(value='Tranche 3', size=13, font_family="Poppins Medium"), self.icone_t3],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.Divider(height=1, thickness=1),
                                        ], spacing=5
                                    ),
                                    ft.Column(
                                        expand=True, scroll=ft.ScrollMode.AUTO,
                                        controls=[self.table_details]
                                    )
                                ], spacing=20
                            )
                        ),

                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )

        # choix frame
        self.choix = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Radio(**radio_style, label="1ère tranche", value="T1"),
                    ft.Radio(**radio_style, label="2eme tranche", value="T2"),
                    ft.Radio(**radio_style, label="3eme tranche", value="T3"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.choice_frame = ft.Card(
            elevation=40, surface_tint_color="#f0f0f6", width=300, height=320,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20, bgcolor="#f0f0f6",
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white",
                            content=ft.Column(
                                controls=[
                                    ft.Text("Sélection tranche", size=14, font_family="Poppins Medium"),
                                    ft.Divider(height=3, thickness=1),
                                    self.choix,
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style, on_click=self.choisir_option, width=170
                                    )
                                ], spacing=20
                            )
                        ),
                    ]
                )
            )
        )

        self.content = ft.Stack(
            controls=[
                self.main_window, self.details_frame, self.choice_frame, self.filrtres_frame
            ], alignment=ft.alignment.center
        )
        self.load_lists()
        self.load_datas()

    @staticmethod
    def icon_bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.2
            e.control.update()
        else:
            e.control.scale = 1
            e.control.update()

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

    def load_lists(self):
        classes = be.show_classes()
        for classe in classes:
            self.classe.options.append(
                ft.dropdown.Option(classe)
            )

    def load_datas(self):
        datas = be.global_pension()

        all_datas = []
        for data in datas:
            dico = {
                'asco': data[0], 'eleve': data[1], 'classe': data[2], 'versé': data[5], 'pension': data[4],
                'reste': data[6], 'statut': data[7],
            }
            all_datas.append(dico)

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in all_datas:
            if data['reste'] == 0:
                color = SECOND_COLOR
                name=ft.icons.CHECK_BOX_OUTLINED
            else:
                color = THRID_COLOR
                name = ft.icons.REAL_ESTATE_AGENT

            self.table.rows.append(
                ft.DataRow(
                    data=data,
                    cells=[
                        ft.DataCell(
                            ft.Icon(name, color=color, size=16)
                        ),
                        ft.DataCell(ft.Text(data['eleve'])),
                        ft.DataCell(ft.Text(data['classe'])),
                        ft.DataCell(ft.Text(be.ajout_separateur_virgule(data['versé']))),
                        ft.DataCell(ft.Text(be.ajout_separateur_virgule(data['pension']))),
                        ft.DataCell(ft.Text(be.ajout_separateur_virgule(data['reste']))),
                        ft.DataCell(
                            ft.Container(
                                scale=ft.transform.Scale(1),
                                animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                on_hover=self.icon_bt_hover2,
                                content=ft.IconButton(
                                    ft.icons.EDIT_OUTLINED, scale=1,
                                    icon_color=FOURTH_COLOR,
                                    on_click=self.open_details_frame, data=data,
                                    tooltip="Supprimer filtres",
                                )
                            ),
                        ),
                    ]
                )
            )

        nb_eleves_inscrits = len(datas)
        total_pension = be.total_pension()
        mt_attendu = nb_eleves_inscrits * total_pension
        self.mt_att.value = f"{be.ajout_separateur_virgule(mt_attendu)}"

        total_pension_recouvre = 0
        for row in datas:
            total_pension_recouvre += row[5]

        self.tpr.value = f"{be.ajout_separateur_virgule(total_pension_recouvre)}"

        if mt_attendu == 0:
            self.pr.value = "0 %"
        else:
            pourcentage_recouvre = (total_pension_recouvre / mt_attendu) * 100
            self.pr.value = f"{pourcentage_recouvre:.2f} %"

        reste_a_recouvrer = mt_attendu - total_pension_recouvre
        self.rar.value = f"{be.ajout_separateur_virgule(reste_a_recouvrer)}"

    def filter_datas(self, e):
        datas = be.global_pension()

        all_datas = []
        for data in datas:
            dico = {
                'asco': data[0], 'eleve': data[1], 'classe': data[2], 'versé': data[5], 'pension': data[4],
                'reste': data[6], 'statut': data[7],
            }
            all_datas.append(dico)

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        classe = self.classe.value if self.classe.value is not None else ""
        statut = self.statut.value if self.statut.value is not None else ""
        eleve = self.eleve.value if self.eleve.value is not None else ""

        filter_data = list(
            filter(lambda x: classe in x['classe'] and eleve in x['eleve'] and statut in x['statut'], all_datas))

        for data in filter_data:
            if data['reste'] == 0:
                color = SECOND_COLOR
                name = ft.icons.CHECK_BOX_OUTLINED
            else:
                color = THRID_COLOR
                name = ft.icons.REAL_ESTATE_AGENT

            self.table.rows.append(
                ft.DataRow(
                    data=data,
                    cells=[
                        ft.DataCell(
                            ft.Icon(name, color=color, size=16)
                        ),
                        ft.DataCell(ft.Text(data['eleve'])),
                        ft.DataCell(ft.Text(data['classe'])),
                        ft.DataCell(ft.Text(be.ajout_separateur_virgule(data['versé']))),
                        ft.DataCell(ft.Text(be.ajout_separateur_virgule(data['pension']))),
                        ft.DataCell(ft.Text(be.ajout_separateur_virgule(data['reste']))),
                        ft.DataCell(
                            ft.Container(
                                scale=ft.transform.Scale(1),
                                animate_scale=ft.animation.Animation(300,
                                                                     ft.AnimationCurve.FAST_OUT_SLOWIN),
                                on_hover=self.icon_bt_hover2,
                                content=ft.IconButton(
                                    ft.icons.EDIT_OUTLINED, scale=1,
                                    icon_color=FOURTH_COLOR,
                                    on_click=self.open_details_frame, data=data,
                                    tooltip="Supprimer filtres",
                                )
                            ),
                        ),
                    ]
                )
            )

        self.table.update()
        self.filrtres_frame.scale = 0
        self.filrtres_frame.update()

    def open_filtres_window(self, e):
        self.filrtres_frame.scale = 1
        self.filrtres_frame.update()

    def close_filtres_window(self, e):
        self.filrtres_frame.scale = 0
        self.filrtres_frame.update()

    def supp_filtres(self, e):
        self.load_datas()
        self.table.update()

        for widget in (self.eleve, self.classe, self.statut):
            widget.value = None
            widget.update()

    def extraire_excel(self, e: ft.FilePickerResultEvent):
        widgets = self.table.rows[:]
        annees = [widget.data['asco'] for widget in widgets]
        noms = [widget.data['eleve'] for widget in widgets]
        classes = [widget.data['classe'] for widget in widgets]
        verses = [widget.data['versé'] for widget in widgets]
        totaux = [widget.data['pension'] for widget in widgets]
        restes = [widget.data['reste'] for widget in widgets]
        statuts = [widget.data['statut'] for widget in widgets]

        data_set = {
            "année scolaire": annees, "élève": noms, "classe": classes, "versé": verses,
            "total pension": totaux, "reste": restes, "statut": statuts
        }
        df = pandas.DataFrame(data_set)
        save_location = f"{e.path}.xlsx"

        if save_location != "None.xlsx":
            excel = pandas.ExcelWriter(save_location)
            df.to_excel(excel, sheet_name="feuil1", index=False)
            excel.close()
            self.cp.box.title.value = "Validé !"
            self.cp.box.content.value = "Fichier créé avec succès"
            self.cp.box.open = True
            self.cp.box.update()
        else:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = f"Pas de chemin choisi"
            self.cp.box.open = True
            self.cp.box.update()

    def imprimer_pdf(self, e: ft.FilePickerResultEvent):
        save_location = f"{e.path}.pdf"
        fichier = os.path.abspath(save_location)
        can = Canvas("{0}".format(fichier), pagesize=A4)

        pdfmetrics.registerFont(TTFont('vinci sans medium', "../assets/fonts/vinci_sans_medium.ttf"))
        pdfmetrics.registerFont(TTFont('vinci sans regular', "../assets/fonts/vinci_sans_regular.ttf"))
        pdfmetrics.registerFont(TTFont('vinci sans bold', "../assets/fonts/vinci_sans_bold.ttf"))
        pdfmetrics.registerFont(TTFont('calibri', "../assets/fonts/calibri.ttf"))
        pdfmetrics.registerFont(TTFont('Poppins Medium', "../assets/fonts/Poppins-Medium.ttf"))
        pdfmetrics.registerFont(TTFont('Poppins Medium', "../assets/fonts/Poppins-Medium.ttf"))
        pdfmetrics.registerFont(TTFont('Poppins Bold', "../assets/fonts/Poppins-Bold.ttf"))
        pdfmetrics.registerFont(TTFont('Poppins SemiBold', "../assets/fonts/Poppins-SemiBold.ttf"))

        asco = be.show_asco_encours()
        widgets = self.table.rows[:]

        # calcul du nombre de lignes
        item = 1
        firts_page_lignes = 19
        others_page_line = 24
        nb_lignes = len(widgets)
        # print(f" total lignes {nb_lignes}")
        reste_lignes = nb_lignes - firts_page_lignes
        print(reste_lignes)

        # Calcul du nombre de pages
        if reste_lignes <= 0:
            nb_pages = 1
        else:
            nb_reste = divmod(reste_lignes, others_page_line)
            pages_supp = nb_reste[0] if nb_reste[1] == 0 else nb_reste[0] + 1
            nb_pages = pages_supp + 1

        # print(f" Total pages {nb_pages}")

        if save_location != "None.pdf":

            if nb_pages == 1:
                gauche, y = 4.25, 28

                # headers à gauche
                def draw_headers():
                    can.setFont("calibri", 12)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(gauche * cm, 28.5 * cm, "République du Cameroun")
                    can.drawCentredString(gauche * cm, 28.0 * cm, "Paix - Travail - Patrie")
                    can.drawCentredString(gauche * cm, 27.5 * cm, "*************")
                    can.drawCentredString(gauche * cm, 27.0 * cm, "Ministère de l'éducation secondaire")
                    can.drawCentredString(gauche * cm, 26.5 * cm, "*************")
                    can.drawCentredString(gauche * cm, 26.0 * cm, "Collège l'excellence")
                    monlogo = "assets/mon logo.png"
                    can.drawImage(monlogo, 16 * cm, 25.5 * cm)

                    # entetes
                    can.setFont("Poppins SemiBold", 12)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(10.5 * cm, (y - 3.5) * cm, f"Etat des pensions".upper())
                    can.setFont("Poppins Medium", 12)
                    can.setFillColorRGB(0, 0, 0)
                    can.drawCentredString(10.5 * cm, (y - 4.2) * cm, f"Global année scolaire {asco - 1}/{asco}")

                    # Pied de page
                    can.setFont("Poppins Medium", 10)
                    can.drawCentredString(10.5 * cm, 1 * cm, "Page 1 de 1")

                draw_headers()

                y = y - 4.2

                # datas
                def draw_entetes():
                    # Lignes horizontales
                    can.line(1 * cm, (y - 1) * cm, 20 * cm, (y - 1) * cm)
                    can.line(1 * cm, (y - 2) * cm, 20 * cm, (y - 2) * cm)

                    # lignes verticales
                    can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 2) * cm)
                    can.line(2 * cm, (y - 1) * cm, 2 * cm, (y - 2) * cm)
                    can.line(13 * cm, (y - 1) * cm, 13 * cm, (y - 2) * cm)
                    can.line(16 * cm, (y - 1) * cm, 16 * cm, (y - 2) * cm)
                    can.line(18 * cm, (y - 1) * cm, 18 * cm, (y - 2) * cm)
                    can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 2) * cm)

                    # draw headers
                    can.setFont("vinci sans bold", 11)
                    can.drawCentredString(1.5 * cm, (y - 1.6) * cm, "N°")
                    can.drawCentredString(7 * cm, (y - 1.6) * cm, "Nom")
                    can.drawCentredString(14.5 * cm, (y - 1.6) * cm, "classe")
                    can.drawCentredString(17 * cm, (y - 1.6) * cm, "versé")
                    can.drawCentredString(19 * cm, (y - 1.6) * cm, "reste")

                draw_entetes()

                # print("cas 1 seule page")
                for widget in widgets:
                    nom = widget.data['eleve']
                    cls = widget.data['classe']
                    verse = widget.data['versé']
                    reste = widget.data['reste']

                    can.setFillColorRGB(0, 0, 0)
                    can.setFont("Poppins Medium", 10)
                    can.drawCentredString(1.5 * cm, (y - 2.6) * cm, f"{item}")
                    can.drawCentredString(7 * cm, (y - 2.6) * cm, f"{nom}")
                    can.drawCentredString(14.5 * cm, (y - 2.6) * cm, f"{cls}")
                    can.drawCentredString(17 * cm, (y - 2.6) * cm, f"{be.ajout_separateur(verse)}")
                    can.drawCentredString(19 * cm, (y - 2.6) * cm, f"{be.ajout_separateur(reste)}")

                    # lignes verticales
                    can.setStrokeColorRGB(0, 0, 0)
                    can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 3) * cm)
                    can.line(2 * cm, (y - 1) * cm, 2 * cm, (y - 3) * cm)
                    can.line(13 * cm, (y - 1) * cm, 13 * cm, (y - 3) * cm)
                    can.line(16 * cm, (y - 1) * cm, 16 * cm, (y - 3) * cm)
                    can.line(18 * cm, (y - 1) * cm, 18 * cm, (y - 3) * cm)
                    can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 3) * cm)

                    can.line(1 * cm, (y - 3) * cm, 20 * cm, (y - 3) * cm)

                    item += 1
                    y -= 1

                can.save()

            # si le nombre de pages est supérieur à 1
            else:
                # print("cas plusieurs pages")
                debut = 0
                fin = firts_page_lignes if firts_page_lignes >= 18 else nb_lignes
                # print(f"début {debut}, fin {fin}")

                for i in range(nb_pages):

                    # Pied de page
                    can.setFont("Poppins Medium", 10)
                    can.drawCentredString(10.5 * cm, 1 * cm, f"Page {i + 1} de {nb_pages}")

                    # print(f"page {i}")
                    if i == 0:
                        # print(f"page {i}, {nb_pages - 1}")
                        gauche, y = 4.25, 28

                        # headers à gauche
                        def draw_headers():
                            can.setFont("calibri", 12)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(gauche * cm, 28.5 * cm, "République du Cameroun")
                            can.drawCentredString(gauche * cm, 28.0 * cm, "Paix - Travail - Patrie")
                            can.drawCentredString(gauche * cm, 27.5 * cm, "*************")
                            can.drawCentredString(gauche * cm, 27.0 * cm, "Ministère de l'éducation secondaire")
                            can.drawCentredString(gauche * cm, 26.5 * cm, "*************")
                            can.drawCentredString(gauche * cm, 26.0 * cm, "Collège l'excellence")
                            monlogo = "assets/mon logo.png"
                            can.drawImage(monlogo, 16 * cm, 25.5 * cm)

                            # entetes
                            can.setFont("Poppins SemiBold", 12)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(10.5 * cm, (y - 3.5) * cm, f"Etat des pensions".upper())
                            can.setFont("Poppins Medium", 12)
                            can.setFillColorRGB(0, 0, 0)
                            can.drawCentredString(10.5 * cm, (y - 4.2) * cm, f"Global année scolaire {asco - 1}/{asco}")

                        draw_headers()

                        y = y - 4.2

                        # datas
                        def draw_entetes():
                            # Lignes horizontales
                            can.line(1 * cm, (y - 1) * cm, 20 * cm, (y - 1) * cm)
                            can.line(1 * cm, (y - 2) * cm, 20 * cm, (y - 2) * cm)

                            # lignes verticales
                            can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 2) * cm)
                            can.line(2 * cm, (y - 1) * cm, 2 * cm, (y - 2) * cm)
                            can.line(13 * cm, (y - 1) * cm, 13 * cm, (y - 2) * cm)
                            can.line(16 * cm, (y - 1) * cm, 16 * cm, (y - 2) * cm)
                            can.line(18 * cm, (y - 1) * cm, 18 * cm, (y - 2) * cm)
                            can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 2) * cm)

                            # draw headers
                            can.setFont("vinci sans bold", 11)
                            can.drawCentredString(1.5 * cm, (y - 1.6) * cm, "N°")
                            can.drawCentredString(7 * cm, (y - 1.6) * cm, "Nom")
                            can.drawCentredString(14.5 * cm, (y - 1.6) * cm, "classe")
                            can.drawCentredString(17 * cm, (y - 1.6) * cm, "versé")
                            can.drawCentredString(19 * cm, (y - 1.6) * cm, "reste")

                        draw_entetes()

                        for nombre in range(debut, fin):
                            nom = widgets[nombre].data['eleve']
                            cls = widgets[nombre].data['classe']
                            verse = widgets[nombre].data['versé']
                            reste = widgets[nombre].data['reste']
                            # print(f"{nombre}, {nom}")

                            can.setFillColorRGB(0, 0, 0)
                            can.setFont("Poppins Medium", 10)
                            can.drawCentredString(1.5 * cm, (y - 2.6) * cm, f"{item}")
                            can.drawCentredString(7 * cm, (y - 2.6) * cm, f"{nom}")
                            can.drawCentredString(14.5 * cm, (y - 2.6) * cm, f"{cls}")
                            can.drawCentredString(17 * cm, (y - 2.6) * cm, f"{be.ajout_separateur(verse)}")
                            can.drawCentredString(19 * cm, (y - 2.6) * cm, f"{be.ajout_separateur(reste)}")

                            # lignes verticales
                            can.setStrokeColorRGB(0, 0, 0)
                            can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 3) * cm)
                            can.line(2 * cm, (y - 1) * cm, 2 * cm, (y - 3) * cm)
                            can.line(13 * cm, (y - 1) * cm, 13 * cm, (y - 3) * cm)
                            can.line(16 * cm, (y - 1) * cm, 16 * cm, (y - 3) * cm)
                            can.line(18 * cm, (y - 1) * cm, 18 * cm, (y - 3) * cm)
                            can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 3) * cm)

                            can.line(1 * cm, (y - 3) * cm, 20 * cm, (y - 3) * cm)

                            item += 1
                            y -= 1

                        debut = fin
                        # print(f"Nouveau debut: {debut}")
                        etape = debut + others_page_line
                        fin = etape if etape <= nb_lignes else nb_lignes
                        # print(f"Nouvelle fin: {fin}")
                        can.showPage()

                    else:
                        y = 28

                        def draw_entetes():
                            # Lignes horizontales
                            can.line(1 * cm, (y - 1) * cm, 20 * cm, (y - 1) * cm)
                            can.line(1 * cm, (y - 2) * cm, 20 * cm, (y - 2) * cm)

                            # lignes verticales
                            can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 2) * cm)
                            can.line(2 * cm, (y - 1) * cm, 2 * cm, (y - 2) * cm)
                            can.line(13 * cm, (y - 1) * cm, 13 * cm, (y - 2) * cm)
                            can.line(16 * cm, (y - 1) * cm, 16 * cm, (y - 2) * cm)
                            can.line(18 * cm, (y - 1) * cm, 18 * cm, (y - 2) * cm)
                            can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 2) * cm)

                            # draw headers
                            can.setFont("vinci sans bold", 11)
                            can.drawCentredString(1.5 * cm, (y - 1.6) * cm, "N°")
                            can.drawCentredString(7 * cm, (y - 1.6) * cm, "Nom")
                            can.drawCentredString(14.5 * cm, (y - 1.6) * cm, "classe")
                            can.drawCentredString(17 * cm, (y - 1.6) * cm, "versé")
                            can.drawCentredString(19 * cm, (y - 1.6) * cm, "reste")

                        draw_entetes()

                        for nombre in range(debut, fin):
                            nom = widgets[nombre].data['eleve']
                            cls = widgets[nombre].data['classe']
                            verse = widgets[nombre].data['versé']
                            reste = widgets[nombre].data['reste']
                            # print(f"{nombre}, {nom}")

                            can.setFillColorRGB(0, 0, 0)
                            can.setFont("Poppins Medium", 10)
                            can.drawCentredString(1.5 * cm, (y - 2.6) * cm, f"{item}")
                            can.drawCentredString(7 * cm, (y - 2.6) * cm, f"{nom}")
                            can.drawCentredString(14.5 * cm, (y - 2.6) * cm, f"{cls}")
                            can.drawCentredString(17 * cm, (y - 2.6) * cm, f"{be.ajout_separateur(verse)}")
                            can.drawCentredString(19 * cm, (y - 2.6) * cm, f"{be.ajout_separateur(reste)}")

                            # lignes verticales
                            can.setStrokeColorRGB(0, 0, 0)
                            can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 3) * cm)
                            can.line(2 * cm, (y - 1) * cm, 2 * cm, (y - 3) * cm)
                            can.line(13 * cm, (y - 1) * cm, 13 * cm, (y - 3) * cm)
                            can.line(16 * cm, (y - 1) * cm, 16 * cm, (y - 3) * cm)
                            can.line(18 * cm, (y - 1) * cm, 18 * cm, (y - 3) * cm)
                            can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 3) * cm)

                            can.line(1 * cm, (y - 3) * cm, 20 * cm, (y - 3) * cm)

                            item += 1
                            y -= 1

                        debut = fin
                        # print(f"Nouveau debut: {debut}")
                        etape = debut + others_page_line
                        fin = etape if etape <= nb_lignes else nb_lignes
                        # print(f"Nouvelle fin: {fin}")

                        if i < nb_pages - 1:
                            can.showPage()
                        else:
                            can.save()

            self.cp.box.title.value = "Validé !"
            self.cp.box.content.value = "Fichier créé avec succès"
            self.cp.box.open = True
            self.cp.box.update()

        else:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = f"Pas de chemin choisi"
            self.cp.box.open = True
            self.cp.box.update()

    def close_details_frame(self, e):
        self.details_frame.scale = 0
        self.details_frame.update()

    def open_details_frame(self, e):
        for row in self.table_details.rows[:]:
            self.table_details.rows.remove(row)

        self.title_details.value = e.control.data['eleve']
        self.title_details.update()
        all_details = be.pension_par_eleve(e.control.data['eleve'])

        # Calcul des versements par tranche ...
        total = 0
        total_t1 = 0
        total_t2 = 0
        total_t3 = 0
        for detail in all_details:

            if detail['tranche'] == 'tranche 1':
                total_t1 += detail['montant']

            elif detail['tranche'] == 'tranche 2':
                total_t2 += detail['montant']

            else:
                total_t3 += detail['montant']

            total += detail['montant']
            self.table_details.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(detail['tranche'].upper())),
                        ft.DataCell(ft.Text(detail['date'])),
                        ft.DataCell(ft.Text(be.ajout_separateur(detail['montant']))),
                    ]
                )
            )

        self.table_details.update()

        if total_t1 == 0:
            self.icone_t1.name = ft.icons.CHECK_BOX_OUTLINE_BLANK_OUTLINED
            self.icone_t1.color = "grey"
        elif total_t1 < be.total_tranche('tranche 1'):
            self.icone_t1.name = ft.icons.INDETERMINATE_CHECK_BOX_OUTLINED
            self.icone_t1.color = FIRST_COLOR
        else:
            self.icone_t1.name = ft.icons.CHECK_BOX_OUTLINED
            self.icone_t1.color = FOURTH_COLOR

        self.icone_t1.update()

        if total_t2 == 0:
            self.icone_t2.name = ft.icons.CHECK_BOX_OUTLINE_BLANK_OUTLINED
            self.icone_t2.color = "grey"
        elif total_t2 < be.total_tranche('tranche 2'):
            self.icone_t2.name = ft.icons.INDETERMINATE_CHECK_BOX_OUTLINED
            self.icone_t2.color = FIRST_COLOR
        else:
            self.icone_t2.name = ft.icons.CHECK_BOX_OUTLINED
            self.icone_t2.color = FOURTH_COLOR

        self.icone_t2.update()

        if total_t3 == 0:
            self.icone_t3.name = ft.icons.CHECK_BOX_OUTLINE_BLANK_OUTLINED
            self.icone_t3.color = "grey"
        elif total_t3 < be.total_tranche('tranche 3'):
            self.icone_t3.name = ft.icons.INDETERMINATE_CHECK_BOX_OUTLINED
            self.icone_t3.color = FIRST_COLOR
        else:
            self.icone_t3.name = ft.icons.CHECK_BOX_OUTLINED
            self.icone_t3.color = FOURTH_COLOR

        self.icone_t3.update()

        self.pb.value = total / be.total_pension()

        if self.pb.value <= 0.33:
            self.pb.color = FOURTH_COLOR
        elif 0.33 < self.pb.value <= 0.66:
            self.pb.color = THRID_COLOR
        else:
            self.pb.color = SECOND_COLOR

        self.pb.update()

        if total * 100 / be.total_pension() != int(total * 100 / be.total_pension()):
            self.pb_label.value = f"{total * 100 / be.total_pension():.2f}%"
        else:
            self.pb_label.value = f"{int(total * 100 / be.total_pension())}%"

        self.pb_label.update()
        self.details_frame.scale = 1
        self.details_frame.update()

    def open_choice_frame(self, e):
        self.choice_frame.scale = 1
        self.choice_frame.update()

    def choisir_option(self, e):
        if self.choix.value == "T1":
            selection_tranche['name'] = "tranche 1"
            for widget in self.cp.contenu.content.controls[:]:
                self.cp.contenu.content.controls.remove(widget)
            self.cp.contenu.content.controls.append(Tranches(self.cp, selection_tranche['name']))
            self.cp.update()

        elif self.choix.value == "T2":
            selection_tranche['name'] = "tranche 2"
            for widget in self.cp.contenu.content.controls[:]:
                self.cp.contenu.content.controls.remove(widget)
            self.cp.contenu.content.controls.append(Tranches(self.cp, selection_tranche['name']))
            self.cp.update()

        elif self.choix.value == "T3":
            selection_tranche['name'] = "tranche 3"
            for widget in self.cp.contenu.content.controls[:]:
                self.cp.contenu.content.controls.remove(widget)
            self.cp.contenu.content.controls.append(Tranches(self.cp, selection_tranche['name']))
            self.cp.update()

        else:
            pass

    @staticmethod
    def bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.2
            e.control.update()
        else:
            e.control.scale = 1
            e.control.update()