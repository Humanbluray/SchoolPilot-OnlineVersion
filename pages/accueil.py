from utils.lateral_menu import *
from utils import FIRST_COLOR


class Accueil(ft.View):
    def __init__(self, page):
        super(Accueil, self).__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, route="/accueil", bgcolor="#f2f2f2"
        )
        self.page = page

        self.menu = Menu(self, page)
        self.barre = ft.Container(
            content=ft.Column(
                controls=[
                    self.menu
                ]
            ),
            border_radius=12, width=180,
        )
        self.contenu = ft.Container(
            border_radius=0, padding=0,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        expand=True,
                        controls=[
                            ft.Image(src="logo noir.png", height=325, width=325, opacity=0.2)
                        ], alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
            )
        )
        # Dialog box
        self.box = ft.AlertDialog(
            surface_tint_color="white",
            title=ft.Text("", size=20, font_family="Poppins Light"),
            content=ft.Text("", size=12, font_family="Poppins Medium"),
            actions=[
                ft.TextButton(
                    content=ft.Row(
                        [ft.Text("Quitter", size=12, font_family="Poppins Medium", color=FIRST_COLOR)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ), width=120,
                    on_click=self.close_box
                )
            ]
        )
        self.dp_modif_eleve = ft.DatePicker()
        self.dp_new_eleve = ft.DatePicker()
        self.fp_insc_pdf = ft.FilePicker()
        self.fp_insc_xls = ft.FilePicker()
        self.fp_export_modele_note = ft.FilePicker()
        self.fp_importer_note = ft.FilePicker()
        self.fp_extraire_pdf_pensions = ft.FilePicker()
        self.fp_extraire_xls_pensions = ft.FilePicker()
        self.fp_extraire_pdf_tranches = ft.FilePicker()
        self.fp_extraire_xls_tranches = ft.FilePicker()
        self.dp_paiement_tranche = ft.DatePicker()
        self.fp_onebull_seq = ft.FilePicker()
        self.fp_onebull_trim = ft.FilePicker()
        self.fp_onebull_ann = ft.FilePicker()
        self.fp_allbull_seq = ft.FilePicker()
        self.fp_allbull_trim = ft.FilePicker()
        self.fp_allbull_ann = ft.FilePicker()
        self.fp_print_elev_xls = ft.FilePicker()
        self.fp_print_insc_xls = ft.FilePicker()

        widgets = [
            self.box, self.dp_modif_eleve, self.dp_new_eleve, self.fp_insc_pdf, self.fp_insc_xls,
            self.fp_export_modele_note, self.fp_importer_note, self.fp_extraire_pdf_pensions, self.fp_extraire_xls_pensions,
            self.fp_extraire_pdf_tranches, self.fp_extraire_xls_tranches, self.dp_paiement_tranche,
            self.fp_onebull_seq, self.fp_allbull_seq, self.fp_onebull_trim, self.fp_allbull_trim,
            self.fp_onebull_ann, self.fp_allbull_ann, self.fp_print_elev_xls, self.fp_print_insc_xls
        ]
        # Overlays _________________________________________________________

        for widget in widgets:
            self.page.overlay.append(widget)

        self.controls = [
            ft.Container(
                expand=True, margin=5,
                content=ft.Row(
                    # expand=True,
                    controls=[
                        self.barre,
                        self.contenu
                    ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.START,
                )
            )
        ]

    def close_box(self, e):
        self.box.open = False
        self.box.update()










