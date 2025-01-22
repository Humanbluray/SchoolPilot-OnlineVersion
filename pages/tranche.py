from utils import *
from utils import backend as be
import pandas
import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class Tranches(ft.Container):
    def __init__(self, cp: object, tranche_name: str):
        super(Tranches, self).__init__(
            expand=True
        )
        self.cp = cp
        self.tranche_name = tranche_name

        if self.tranche_name == "tranche 1":
            my_text = "1ere tranche"
        elif self.tranche_name == "tranche 2":
            my_text = "2e tranche"
        else:
            my_text = "3e tranche"

        self.tpr = ft.Text("", size=24, font_family="Poppins Light", color="black")
        self.mt_att = ft.Text("", size=24, font_family="Poppins Light", color="black")
        self.pr = ft.Text("", size=12, font_family="Poppins Medium", color="blue")
        self.rar = ft.Text("", size=24, font_family="Poppins Light", color="black")

        self.classe = ft.Dropdown(**drop_style, prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, width=150, label="Classe")
        self.eleve = ft.TextField(**field_style, width=300, prefix_icon="person_outlined", label="Elève")
        self.statut = ft.Dropdown(
            **drop_style, prefix_icon=ft.icons.SIGNAL_WIFI_STATUSBAR_4_BAR_OUTLINED, width=150, label="Statut",
            options=[
                ft.dropdown.Option("soldée"),
                ft.dropdown.Option("en cours"),
            ]
        )
        self.cp.fp_extraire_pdf_tranches.on_result = self.imprimer_pdf
        self.cp.fp_extraire_xls_tranches.on_result = self.extraire_excel
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("")),
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("Classe")),
                ft.DataColumn(label=ft.Text("Montant")),
                ft.DataColumn(label=ft.Text("Total")),
                ft.DataColumn(label=ft.Text("Reste")),
                ft.DataColumn(label=ft.Text("Statut")),
            ],
            data_text_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black54"),
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

                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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

                                                        ft.Row([self.tpr, self.pr], vertical_alignment=ft.CrossAxisAlignment.END)
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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

                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                    ], spacing=40, vertical_alignment=ft.CrossAxisAlignment.START
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
                                                ft.Text(f"{my_text}", size=15, font_family="Poppins Bold"),
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
                                                    THRID_COLOR, ft.icons.ADD_CARD_OUTLINED, "Paiement +", "white",
                                                    self.open_paiement_frame,
                                                )
                                            ]
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
                                                    border_radius=6, bgcolor="#f0f0f6",
                                                    scale=ft.transform.Scale(1),
                                                    animate_scale=ft.animation.Animation(300,
                                                                                         ft.AnimationCurve.FAST_OUT_SLOWIN),
                                                    on_hover=self.icon_bt_hover2,
                                                    content=ft.IconButton(
                                                        ft.icons.PRINT_OUTLINED, scale=1, tooltip="Imprimer PDF",
                                                        icon_color=ft.colors.BLACK45,
                                                        on_click=lambda e: self.cp.fp_extraire_pdf_pensions.save_file(
                                                            allowed_extensions=["pdf"]),
                                                    )
                                                ),
                                                ft.Container(
                                                    border=ft.border.all(1, "grey"),
                                                    border_radius=6, bgcolor="#f0f0f6",
                                                    scale=ft.transform.Scale(1),
                                                    animate_scale=ft.animation.Animation(300,
                                                                                         ft.AnimationCurve.FAST_OUT_SLOWIN),
                                                    on_hover=self.icon_bt_hover2,
                                                    content=ft.IconButton(
                                                        ft.icons.FILE_DOWNLOAD_OUTLINED, scale=1,
                                                        tooltip="Extarction axcel",
                                                        icon_color=ft.colors.BLACK45,
                                                        on_click=lambda e: self.cp.fp_extraire_xls_pensions.save_file(
                                                            allowed_extensions=["xls", "xlsx"]),
                                                    )
                                                )
                                            ], alignment=ft.MainAxisAlignment.START
                                        ),
                                        ft.Divider(height=3, color=ft.colors.TRANSPARENT),
                                        ft.ListView(expand=True, controls=[self.table])
                                    ], spacing=1
                                )
                            ]
                        )
                    )
                ]
            )
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
                                            ft.Icon(ft.icons.FILTER_ALT_OFF, color=SECOND_COLOR),
                                            ft.Text("Filtres".upper(), size=14, font_family="Poppins Medium")
                                        ]
                                    ),
                                    ft.IconButton(
                                        "close", scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                        on_click=self.close_filtres_window
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ), ft.Container(
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

        self.table_eleves = ft.DataTable(
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=12, font_family="Poppins ExtraBold"),
            columns=[
                ft.DataColumn(
                    ft.Text("Nom")
                )
            ], rows=[]
        )
        self.nom_elv = ft.TextField(**field_style, width=400, prefix_icon="person_outlined",
                                    hint_text="Chercher élève...", on_change=self.changement_name)
        self.nom_elv2 = ft.TextField(**underline_field_style, prefix_icon=ft.icons.PERSON_OUTLINED, label="Nom",
                                     width=500)
        self.tranche_payee = ft.TextField(**underline_field_style, prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
                                          label="Tranche", value=self.tranche_name, width=120)
        self.versement_total = ft.Checkbox(
            label="Solder la tranche", label_style=ft.TextStyle(**text_title_style),
            active_color="#fe9500", check_color="#292f4c", on_change=self.changement_versement
        )
        self.avance = ft.TextField(**underline_field_style, label="Avance", width=120, text_align="right")
        self.montant_paye = ft.TextField(**field_style_2, label="Montant", width=120, input_filter=ft.NumbersOnlyInputFilter(), text_align="right")
        self.sel_date = ft.TextField(**underline_field_style, label="Date", width=120)
        self.cp.dp_paiement_tranche.on_change = self.change_date
        self.bt_select_date = ft.IconButton(
            ft.icons.EDIT_CALENDAR_OUTLINED,
            icon_size=18, bgcolor="#f0f0f06", icon_color="black",
            on_click=lambda _: self.cp.dp_paiement_tranche.pick_date(),
        )
        self.paiement_frame = ft.Card(
            elevation=40, surface_tint_color="#f0f0f6", width=550, height=650,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20, bgcolor="#f0f0f6", expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=10, border_radius=12, bgcolor="white",
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.MONETIZATION_ON, color=SECOND_COLOR),
                                            ft.Text("Versement".upper(), size=14, font_family="Poppins Medium"),
                                        ]
                                    ),
                                    ft.IconButton(
                                        ft.icons.CLOSE, scale=0.7, icon_color="#292f4c", bgcolor='#f0f0f6',
                                        on_click=self.close_paiement_frame
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, border_radius=12, bgcolor="white", expand=True,
                            content=ft.Column(
                                expand=True,
                                controls=[
                                    self.nom_elv,
                                    ft.Container(
                                        border_radius=12, border=ft.border.all(1, "#f0f0f6"), padding=10, expand=True,
                                        height=700,
                                        content=ft.Column(
                                            expand=True, scroll=ft.ScrollMode.AUTO, height=200,
                                            controls=[self.table_eleves]
                                        )
                                    ),
                                    self.nom_elv2,
                                    ft.Row(controls=[self.tranche_payee, ft.Row([self.bt_select_date, self.sel_date])],
                                           spacing=40),
                                    ft.Row([self.avance, self.versement_total, self.montant_paye], spacing=40),
                                    ft.ElevatedButton(
                                        on_hover=self.bt_hover, **choix_style, on_click=self.valider_paiement,
                                        width=170
                                    ),
                                ], spacing=20
                            )
                        )
                    ], spacing=15
                )
            )
        )

        self.content = ft.Stack(
            controls=[
                self.main_window, self.paiement_frame, self.filrtres_frame
            ], alignment=ft.alignment.center
        )
        self.load_lists()
        self.load_datas()

    @staticmethod
    def icon_bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.4
            e.control.update()
        else:
            e.control.scale = 1
            e.control.update()

    @staticmethod
    def icon_bt_hover2(e):
        if e.data == 'true':
            e.control.scale = 1.4
            e.control.update()
        else:
            e.control.scale = 1
            e.control.update()

    def open_filtres_window(self, e):
        self.filrtres_frame.scale = 1
        self.filrtres_frame.update()

    def close_filtres_window(self, e):
        self.filrtres_frame.scale = 0
        self.filrtres_frame.update()

    def load_lists(self):
        classes = be.show_classes()
        for classe in classes:
            self.classe.options.append(
                ft.dropdown.Option(classe)
            )
        eleves = be.tranche_non_soldee(self.tranche_name)
        for eleve in eleves:
            self.table_eleves.rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(eleve))],
                    on_select_changed=lambda e: self.select_person(e.control.cells[0].content.value)
                )
            )

    def load_datas(self):
        datas = be.search_pension_tranche(self.tranche_name)
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
                name = ft.icons.CHECK_BOX_OUTLINED
                border_color = ft.colors.GREEN
                bgcolor = ft.colors.GREEN_50
            else:
                color = THRID_COLOR
                name = ft.icons.REAL_ESTATE_AGENT
                border_color = ft.colors.RED
                bgcolor = ft.colors.RED_50

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
                                padding=7, border_radius=10, border=ft.border.all(1, border_color), bgcolor=bgcolor,
                                content=ft.Row([ft.Text(data['statut'], color=border_color)],
                                               alignment=ft.MainAxisAlignment.CENTER)
                            )
                        ),
                    ]
                )
            )

        nb_eleves_inscrits = len(datas)
        total_pension = be.total_tranche(self.tranche_name)
        mt_attendu = nb_eleves_inscrits * total_pension
        self.mt_att.value = f"{be.ajout_separateur_virgule(mt_attendu)}"

        total_pension_recouvre = 0
        for row in datas:
            total_pension_recouvre += row[5]

        self.tpr.value = f"{be.ajout_separateur_virgule(total_pension_recouvre)}"

        if mt_attendu == 0:
            self.pr.value = f"0%"
        else:
            pourcentage_recouvre = (total_pension_recouvre / mt_attendu) * 100
            self.pr.value = f"{pourcentage_recouvre:.2f} %"

        reste_a_recouvrer = mt_attendu - total_pension_recouvre
        self.rar.value = f"{be.ajout_separateur_virgule(reste_a_recouvrer)}"

    def filter_datas(self, e):
        datas = be.search_pension_tranche(self.tranche_name)

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
                border_color = ft.colors.GREEN
                bgcolor = ft.colors.GREEN_50
            else:
                color = THRID_COLOR
                name = ft.icons.REAL_ESTATE_AGENT
                border_color = ft.colors.RED
                bgcolor = ft.colors.RED_50

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
                                padding=7, border_radius=10, border=ft.border.all(1, border_color), bgcolor=bgcolor,
                                content=ft.Row([ft.Text(data['statut'], color=border_color)], alignment=ft.MainAxisAlignment.CENTER)
                            )
                        ),
                    ]
                )
            )

        self.table.update()

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

    def open_paiement_frame(self, e):
        self.paiement_frame.scale = 1
        self.paiement_frame.update()

    def changement_name(self, e):
        datas = be.tranche_non_soldee(self.tranche_name)
        eleves = []

        for data in datas:
            dico = {"name": data}
            eleves.append(dico)

        eleve = self.nom_elv.value
        filter_data = list(filter(lambda x: eleve in x['name'], eleves))

        for row in self.table_eleves.rows[:]:
            self.table_eleves.rows.remove(row)

        if eleve is not None or eleve != "":
            for data in filter_data:
                self.table_eleves.rows.append(
                    ft.DataRow(
                        cells=[ft.DataCell(ft.Text(data['name']))],
                        on_select_changed=lambda e: self.select_person(e.control.cells[0].content.value)
                    )
                )

            self.table_eleves.update()

    def select_person(self, e):
        self.nom_elv2.value = e
        self.nom_elv2.update()

        self.avance.value = be.mt_verse_par_tranche_par_eleve(self.tranche_name, self.nom_elv2.value)
        self.avance.update()

    def changement_versement(self, e):
        if self.versement_total.value is True:
            self.montant_paye.value = str(int(be.total_tranche(self.tranche_name)) - int(self.avance.value))
            self.montant_paye.update()
        else:
            self.montant_paye.value = None
            self.montant_paye.update()

    def close_paiement_frame(self, e):
        self.paiement_frame.scale = 0
        self.paiement_frame.update()

    def change_date(self, e):
        self.sel_date.value = str(self.cp.dp_paiement_tranche.value)[0:10]
        self.sel_date.update()

    def valider_paiement(self, e):
        counter = 0
        for widget in (self.nom_elv2, self.montant_paye, self.sel_date):
            if widget.value is None or widget.value == "":
                counter += 1

        if counter > 0:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "les champs 'Nom de l'élève', 'Montant' et 'date' sont obligatoires"
            self.cp.box.open = True
            self.cp.box.update()

        else:
            montant = int(self.montant_paye.value)
            avance = int(self.avance.value)

            if montant + avance > be.mt_tranche(self.tranche_name):
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = "Le total du versement + l'avance ne peut pas être supérieur au montant total de la tranche"
                self.cp.box.open = True
                self.cp.box.update()
            else:
                be.add_pension(be.show_asco_encours(), self.nom_elv2.value, self.tranche_payee.value, montant,
                               self.sel_date.value)
                # boite de dialogue
                self.cp.box.title.value = "Validé !"
                self.cp.box.content.value = "Paiement effectué avec succès"
                self.cp.box.open = True
                self.cp.box.update()

                for widget in (self.nom_elv2, self.nom_elv, self.montant_paye):
                    widget.value = None
                    widget.update()

                self.versement_total.value = False
                self.versement_total.update()

                for row in self.table_eleves.rows[:]:
                    self.table_eleves.rows.remove(row)

                eleves = be.tranche_non_soldee(self.tranche_name)
                for eleve in eleves:
                    self.table_eleves.rows.append(
                        ft.DataRow(
                            cells=[ft.DataCell(ft.Text(eleve))],
                            on_select_changed=lambda e: self.select_person(e.control.cells[0].content.value)
                        )
                    )
                self.table_eleves.update()

    @staticmethod
    def bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.1
            e.control.update()
        else:
            e.control.scale = 1
            e.control.update()
