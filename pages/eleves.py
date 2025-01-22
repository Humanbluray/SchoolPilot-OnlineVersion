from utils import *
from utils import backend as be
import datetime
import pandas

suscribers_icon_style = dict(size=18, color="")
sex_icon_style = dict(size=22)


class Eleves(ft.Container):
    def __init__(self, cp: object):
        super(Eleves, self).__init__(expand=True)

        self.cp = cp
        self.nom = ft.TextField(
            **field_style, hint_text="Nom élève", width=300, on_change=self.filter_datas,
            prefix_icon=ft.icons.PERSON_OUTLINED
        )
        self.nb_girls = ft.Text(size=24, font_family="Poppins Light")
        self.nb_gars = ft.Text(size=24, font_family="Poppins Light")
        self.nb_total = ft.Text(size=24, font_family="Poppins Light")
        self.pc_gars = ft.Text("", size=12, font_family="Poppins Medium", color=ft.colors.LIGHT_GREEN, visible=False)
        self.pc_filles = ft.Text("", size=12, font_family="Poppins Medium", color="pink", visible=False)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Est inscrit")),
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("Matricule")),
                ft.DataColumn(label=ft.Text("Téléphone")),
                ft.DataColumn(label=ft.Text("")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )
        self.montant = ft.Text("", size=24, font_family="Poppins Light")
        self.cp.fp_print_elev_xls.on_result = self.imprimer_excel

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
                                        ft.Text('BBBB'.upper(), size=13, font_family="Poppins Bold"),
                                        ft.Divider(height=1, thickness=1),
                                    ], spacing=0
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Column(
                                            [
                                                ft.Text("Montant inscriptions".upper(), size=11, font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.MONETIZATION_ON_OUTLINED, size=20,
                                                                color="black87"),
                                                        self.montant
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text('Nb Inscrits'.upper(), size=11, font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.GROUP_OUTLINED, size=20,
                                                                color="black87"),
                                                        self.nb_total
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

                                                        ft.Row([self.nb_girls, self.pc_filles], vertical_alignment=ft.CrossAxisAlignment.END)
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("Garçons".upper(), size=11,
                                                        font_family="Poppins Italic",
                                                        color="grey"),
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.icons.MAN_4_OUTLINED, size=20,
                                                                color="black87"),

                                                        ft.Row([self.nb_gars, self.pc_gars], vertical_alignment=ft.CrossAxisAlignment.END)
                                                    ]
                                                ),
                                            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        )
                                    ], spacing=50,
                                    vertical_alignment=ft.CrossAxisAlignment.START
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        padding=ft.padding.only(30, 15, 30, 15), border_radius=12,
                        bgcolor="white", expand=True,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                ft.Text("Liste des élèves".upper(), size=13, font_family="Poppins Medium", weight=ft.FontWeight.BOLD),
                                ft.Row(
                                    controls=[
                                        self.nom,
                                        ft.Row(
                                            controls=[
                                                AnyButton(FIRST_COLOR, ft.icons.PERSON_ADD_OUTLINED,"élève +","white", self.open_new_elv_frame),
                                                AnyButton(SECOND_COLOR, ft.icons.FILE_DOWNLOAD_OUTLINED,"Ext Excel","white",
                                                    lambda e: self.cp.fp_print_elev_xls.save_file(allowed_extensions=['xls', 'xlsx']),
                                                ),
                                               AnyButton(THRID_COLOR,  ft.icons.CARD_MEMBERSHIP_OUTLINED,"Inscrits",
                                                         "white", self.open_inscrits_frame)
                                            ], spacing=12
                                        )
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.ListView(
                                    expand=True,
                                    controls=[self.table]
                                )
                            ], spacing=20
                        )
                    )
                ]
            )
        )

        # fenetre de modification .............................
        self.edit_id = ft.TextField(**underline_field_style, width=90, label="id", visible=False)
        self.matricule = ft.TextField(**underline_field_style, width=150, label="Matricule", suffix_icon=ft.icons.CREDIT_CARD)
        self.edit_nom = ft.TextField(**underline_field_style, width=450, label="Nom", prefix_icon="person_outlined")
        self.sel_date = ft.TextField(**date_field_style, label="Né le", width=160)
        self.cp.dp_modif_eleve.on_change = self.change_date_edit_elev
        self.edit_bt_select_date = ft.IconButton(
            ft.icons.CALENDAR_MONTH_OUTLINED, scale=0.7, bgcolor="white",
            icon_color="black",
            on_click=lambda _: self.cp.dp_modif_eleve.pick_date(),
        )
        self.edit_lieu = ft.TextField(**field_style_2, label="Né à", width=150, prefix_icon=ft.icons.HOME_OUTLINED)
        self.edit_sexe = ft.TextField(**field_style_2, label="Sexe", width=100)
        self.edit_pere = ft.TextField(**field_style_2, width=350, label="Nom du père", prefix_icon="man_outlined")
        self.edit_mere = ft.TextField(**field_style_2, width=350, label="Nom de la mère", prefix_icon="woman_outlined")
        self.edit_tel = ft.TextField(**field_style_2, width=150, label="Tél", prefix_icon=ft.icons.PHONE_ANDROID_OUTLINED)

        # Fenetre de la discipline ...................................
        self.s_matricule = ft.TextField(**underline_field_style, width=150, label="Matricule", suffix_icon=ft.icons.CREDIT_CARD)
        self.s_nom = ft.TextField(**underline_field_style, width=350, label="Nom", prefix_icon="person")
        self.s_asco = ft.TextField(**underline_field_style, width=90, label="Asco", prefix_icon=ft.icons.EDIT_CALENDAR)
        self.s_sanction = ft.Dropdown(**drop_style, width=200, label="Nature")
        self.s_sequence = ft.Dropdown(**drop_style, width=150, label="Séquence", prefix_icon=ft.icons.CALENDAR_MONTH)
        self.s_nombre = ft.TextField(**field_style_2, width=100, text_align=ft.TextAlign.RIGHT, label="Nombre",
                                     input_filter=ft.NumbersOnlyInputFilter())

        # inscrire un eleve frame ......................................
        self.o_name = ft.TextField(**underline_field_style, width=450, prefix_icon="person_outlined", label="NOM")
        self.o_class = ft.Dropdown(
            **drop_style, prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, width=170, label="CLASSE",
            on_change=self.changement_classe
        )
        self.o_mat = ft.TextField(**underline_field_style, prefix_icon=ft.icons.CREDIT_CARD, width=170,
                                  label="Matricule".upper())
        self.o_effectif = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.BAR_CHART_OUTLINED, width=130,
            text_align=ft.TextAlign.RIGHT, label='effectif'.upper()
        )
        self.o_check = ft.Checkbox(
            label="Cocher si redoublant", label_style=ft.TextStyle(**text_title_style),
            active_color="#f0f0f6", check_color=FIRST_COLOR
        )
        self.o_frais = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED, width=120,
            text_align=ft.TextAlign.RIGHT, label="frais".upper()
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
        self.switch = ft.Switch(
            active_color=SECOND_COLOR, thumb_color=FIRST_COLOR, track_outline_color="black",
            scale=0.7, on_change=self.changement_solde,
        )

        # Nouvel élève .............................................................
        self.n_name = ft.TextField(**field_style_2, width=450, prefix_icon="person_outlined", label="Nom de l'élève")
        self.n_sel_date = ft.TextField(**date_field_style, label="AAAA-MM-JJ", width=160)
        self.cp.dp_new_eleve.on_change = self.change_date_new_elev
        self.bt_select_date = ft.IconButton(
            ft.icons.CALENDAR_MONTH_OUTLINED, scale=0.7, bgcolor="white",
            icon_color="black",
            on_click=lambda _: self.cp.dp_new_eleve.pick_date(), right=3
        )
        self.n_lieu = ft.TextField(**field_style_2, width=200, prefix_icon=ft.icons.LOCATION_ON_OUTLINED,
                                   label="lieu de naissance")
        self.sexe = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(**radio_style, label="Féminin", value="F"),
                    ft.Radio(**radio_style, label="Masculin", value="M"),
                ],
            )
        )
        self.n_pere = ft.TextField(**field_style_2, width=300, prefix_icon=ft.icons.MAN_OUTLINED, label="Nom du Père")
        self.n_mere = ft.TextField(**field_style_2, width=300, prefix_icon=ft.icons.WOMAN_OUTLINED, label="Nom de la mère")
        self.n_contact = ft.TextField(
            **field_style_2, width=150, prefix_icon=ft.icons.PHONE_ANDROID, label="Contact", text_align=ft.TextAlign.RIGHT,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.n_class = ft.Dropdown(
            **drop_style, prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, width=170, on_change=self.changement_classe2,
            label="Classe"
        )
        self.n_mat = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.CREDIT_CARD_OUTLINED, width=170, label="Matricule"
        )
        self.n_effectif = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.STACKED_BAR_CHART_OUTLINED, width=100, text_align=ft.TextAlign.RIGHT,
            label="Effectif"
        )
        self.n_check = ft.Checkbox(
            label="Cocher si redoublant", label_style=ft.TextStyle(**text_title_style),
            active_color="#f0f0f6", check_color=FIRST_COLOR
        )
        self.n_frais = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED, width=120, text_align=ft.TextAlign.RIGHT,
            label="Frais"
        )
        self.n_tranche_1 = ft.TextField(
            **field_style_2, width=150, label="Tranche 1", input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.n_tranche_2 = ft.TextField(
            **field_style_2, width=150, label="Tranche 2", input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.n_tranche_3 = ft.TextField(
            **field_style_2, width=150, label="Tranche 3", input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.n_switch = ft.Switch(
            active_color=ft.colors.GREY, thumb_color=SECOND_COLOR, track_outline_color="black",
            scale=0.7, on_change=self.changement_solde_2,
        )

        self.new_elv_frame = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=600, height=610, expand=True,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20, bgcolor="#f0f0f6",
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=10, bgcolor="white", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.PERSON_ADD_ALT_1, color=SECOND_COLOR),
                                            ft.Text("Inscription nouveau".upper(), size=14,
                                                    font_family="Poppins Medium")
                                        ]
                                    ),
                                    ft.IconButton(
                                        'close', scale=0.7, icon_color="#292f4c", bgcolor="#f0f0f6",
                                        on_click=self.close_new_elv_frame,
                                    )

                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=20, bgcolor="white", border_radius=12, expand=True,
                            content=ft.Column(
                                expand=True, scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Container(
                                        padding=10, content=ft.Column(
                                            controls=[
                                                ft.Column(
                                                    controls=[
                                                        ft.Text("Infos élève".upper(), size=12,
                                                                font_family="Poppins Medium",
                                                                weight=ft.FontWeight.BOLD),
                                                        ft.Divider(height=1, thickness=1),
                                                    ], spacing=0
                                                ),
                                                self.n_name,
                                                ft.Row(
                                                    controls=[ft.Text("Date de naissance".upper(), size=12, font_family="Poppins Medium"),
                                                        ft.Stack(
                                                            controls=[
                                                                self.n_sel_date, self.bt_select_date,
                                                            ], alignment=ft.alignment.center_right
                                                        ),


                                                    ], spacing=10
                                                ),
                                                self.n_lieu,
                                                ft.Row(
                                                    controls=[
                                                        ft.Text("Sexe: ", size=12, font_family="Poppins Medium"),
                                                        self.sexe,
                                                        self.n_contact,
                                                    ], spacing=10
                                                ),
                                                self.n_pere, self.n_mere,
                                                ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                                                ft.Column(
                                                    controls=[
                                                        ft.Text("Inscription".upper(), size=12,
                                                                font_family="Poppins Medium",
                                                                weight=ft.FontWeight.BOLD),
                                                        ft.Divider(height=1, thickness=1),
                                                    ], spacing=0
                                                ),
                                                ft.Row(
                                                    controls=[
                                                        ft.Text("Année scolaire", size=12,
                                                                font_family="Poppins Medium"),
                                                        ft.TextField(
                                                            **underline_field_style,
                                                            prefix_icon=ft.icons.EDIT_CALENDAR_OUTLINED,
                                                            width=90, value=be.show_asco_encours()
                                                        ),
                                                    ]
                                                ),
                                                ft.Row([self.n_class, self.n_effectif,]),
                                                ft.Row([self.n_mat,self.n_frais,]),
                                                self.n_check,
                                                ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                                                ft.Column(
                                                    controls=[
                                                        ft.Text("Frais de scolarité".upper(), size=12, font_family="Poppins Medium", weight=ft.FontWeight.BOLD),
                                                        ft.Divider(height=1, thickness=1),
                                                    ], spacing=0
                                                ),
                                                ft.Row(
                                                    [
                                                        ft.Text("Solder pension".upper(), size=12,
                                                                font_family="Poppins Medium"),
                                                        self.n_switch
                                                    ]
                                                ),
                                                ft.Row(
                                                    controls=[
                                                        self.n_tranche_1, self.n_tranche_2, self.n_tranche_3
                                                    ]
                                                ),
                                                ft.ElevatedButton(
                                                    on_hover=self.bt_hover, **choix_style,
                                                    on_click=self.valider_inscription2,
                                                    width=170,
                                                )
                                            ], spacing=15
                                        )
                                    )
                                ], spacing=20
                            )
                        )
                    ], spacing=15
                )
            )
        )

        # inscrits ........................................................
        self.table_inscrits = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("Matricule")),
                ft.DataColumn(label=ft.Text("classe")),
            ],
            data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
        )
        self.nb_inscrits = ft.Text(size=12, font_family="Poppins Medium")
        self.fil_classe = ft.Dropdown(
            **drop_style, label="Classe", prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, width=170,
            on_change=self.filter_suscribers
        )
        self.cp.fp_print_insc_xls.on_result = self.imprimer_inscrits
        self.inscrits_frame = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=650, height=600, expand=True,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                margin=20, bgcolor="white", border_radius=12, padding=20, expand=True,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.Text("Liste des inscrits".upper(), size=13, font_family="Poppins Medium", weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    "close", scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                    on_click=self.close_inscrits_frame
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Divider(height=1, thickness=1),
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        self.fil_classe,
                                        ft.Container(
                                            border=ft.border.all(1, "grey"),
                                            border_radius=8, bgcolor="#f0f0f6", padding=5,
                                            scale=ft.transform.Scale(1),
                                            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                            on_hover=self.icon_bt_hover,
                                            on_click=self.delete_filter_suscribers,
                                            content=ft.Icon(
                                                ft.icons.FILTER_ALT_OFF_OUTLINED, color="black45",
                                                tooltip="Supprimer filtres"
                                            )
                                        ),
                                        self.nb_inscrits
                                    ], spacing=10,
                                ),
                                ft.Container(
                                    bgcolor=SECOND_COLOR, border_radius=6, padding=10,
                                    border=ft.border.all(1, SECOND_COLOR),
                                    on_click=lambda e: self.cp.fp_print_insc_xls.save_file(
                                        allowed_extensions=['xls', 'xlsx']),
                                    content=ft.Row(
                                        [
                                            ft.Text("Imprimer xls", size=12, color="white",
                                                    font_family="Poppins Medium")
                                        ], alignment=ft.MainAxisAlignment.CENTER
                                    )
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.ListView(
                            expand=True,
                            controls=[self.table_inscrits]
                        )
                    ], spacing=15
                )
            )
        )

        self.new_frame = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6",
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
            content=ft.Container(
                padding=5, bgcolor="#f0f0f6", width=700, height=600,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(10, 5, 10, 5), border_radius=12, bgcolor="white",
                            margin=ft.margin.only(20, 10, 20, 10),
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.LOCK_PERSON_OUTLINED, color=SECOND_COLOR),
                                            ft.Text("Gestion élève".upper(), size=14, font_family="Poppins Bold"),
                                        ]
                                    ),
                                    ft.IconButton(
                                        'close', scale=0.7, bgcolor="#f0f0f6", icon_color="#292f4c",
                                        on_click=self.close_new_frame
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                        ),
                        ft.Tabs(
                            tab_alignment=ft.TabAlignment.START_OFFSET, selected_index=0, expand=True, animation_duration=300,
                            unselected_label_color=ft.colors.GREY, label_color=FIRST_COLOR,
                            indicator_border_radius=30, indicator_border_side=ft.BorderSide(5, SECOND_COLOR),
                            indicator_tab_size=True,
                            tabs=[
                                ft.Tab(
                                    tab_content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.ACCOUNT_BOX, size=20),
                                            ft.Text("Profil".upper(), size=13, font_family="Poppins Medium"),
                                        ]
                                    ),
                                    content=ft.Container(
                                        padding=20, bgcolor="white",
                                    )
                                ),
                                ft.Tab(
                                    tab_content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.ACCOUNT_BALANCE, size=20),
                                            ft.Text("Inscrire".upper(), size=13, font_family="Poppins Medium"),
                                        ]
                                    ),
                                    content=ft.Container(
                                        padding=20, expand=True,
                                        content=ft.Column(
                                            expand=True,
                                            controls=[
                                                ft.Container(
                                                    padding=20, border_radius=12, bgcolor="white", expand=True,
                                                    content=ft.Column(
                                                        expand=True, scroll=ft.ScrollMode.AUTO,
                                                        controls=[
                                                            ft.Column(
                                                                controls=[
                                                                    ft.Text("Infos élève".upper(), size=12,
                                                                            weight=ft.FontWeight.BOLD,
                                                                            font_family="Poppins Medium"),
                                                                    ft.Divider(height=1, thickness=1),
                                                                ], spacing=0
                                                            ),
                                                            self.o_name,
                                                            ft.Row(
                                                                controls=[self.o_class, self.o_effectif, self.o_mat, ]),
                                                            ft.Row(controls=[self.o_frais, self.o_check]),
                                                            ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                                                            ft.Column(
                                                                controls=[
                                                                    ft.Column(
                                                                        controls=[
                                                                            ft.Text("Frais de scolarité".upper(), size=12, weight=ft.FontWeight.BOLD, font_family="Poppins Medium"),
                                                                            ft.Divider(height=1, thickness=1),
                                                                        ], spacing=0
                                                                    ),
                                                                    ft.Row([ft.Text("Solder pension".upper(), size=12,
                                                                                    font_family="Poppins Medium"),
                                                                            self.switch]),
                                                                    ft.Row(
                                                                        controls=[
                                                                            self.tranche_1, self.tranche_2,
                                                                            self.tranche_3
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            ft.ElevatedButton(
                                                                on_hover=self.bt_hover, **choix_style,
                                                                on_click=self.valider_inscription,
                                                                width=170,
                                                            ),
                                                        ], spacing=20
                                                    )
                                                ),

                                            ], spacing=10
                                        )
                                    )
                                ),
                                ft.Tab(
                                    tab_content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.BOOKMARK, size=20),
                                            ft.Text("Discipline".upper(), size=13, font_family="Poppins Medium"),
                                        ]
                                    ),
                                    content=ft.Container(
                                        padding=20, bgcolor="#f0f0f6",
                                        content=ft.Column(
                                            controls=[
                                                ft.Container(
                                                    padding=20, bgcolor="white", border_radius=12,
                                                    content=ft.Column(
                                                        controls=[
                                                            self.s_nom,
                                                            ft.Row([self.s_matricule, self.s_asco]),
                                                            self.s_sequence, self.s_sanction,
                                                            self.s_nombre,
                                                            ft.ElevatedButton(
                                                                on_hover=self.bt_hover, **choix_style,
                                                                on_click=self.create_sanction,
                                                                width=170
                                                            ),
                                                        ],
                                                    )
                                                )
                                            ], spacing=10
                                        )
                                    )
                                ),
                                # Onglet modifier eleve
                                ft.Tab(
                                    tab_content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.EDIT, size=20),
                                            ft.Text("Modifier".upper(), size=13, font_family="Poppins Medium")
                                        ]
                                    ),
                                    content=ft.Container(
                                        padding=20, bgcolor="#f0f0f6",
                                        content=ft.Column(
                                            controls=[
                                                ft.Container(
                                                    padding=20, bgcolor="white", border_radius=12,
                                                    content=ft.Column(
                                                        controls=[
                                                            ft.Container(
                                                                content=ft.Column(
                                                                    controls=[
                                                                        ft.Row(
                                                                            controls=[
                                                                                ft.Container(
                                                                                    height=120, width=120,
                                                                                    content=ft.Stack(
                                                                                        controls=[
                                                                                            ft.Image(
                                                                                                src="assets/silhouette.png",
                                                                                                height=120, width=120,
                                                                                                fit=ft.ImageFit.CONTAIN),
                                                                                            ft.IconButton(
                                                                                                ft.icons.ADD_A_PHOTO_OUTLINED,
                                                                                                bgcolor="#f0f0f6",
                                                                                                opacity=0.7,
                                                                                            )
                                                                                        ],
                                                                                        alignment=ft.alignment.bottom_right
                                                                                    )
                                                                                ),
                                                                                ft.Column(
                                                                                    controls=[
                                                                                        self.edit_id,
                                                                                        self.edit_nom,
                                                                                        ft.Row(
                                                                                            controls=[
                                                                                                ft.Stack(
                                                                                                    controls=[
                                                                                                        self.sel_date,
                                                                                                        self.edit_bt_select_date, ],
                                                                                                    alignment=ft.alignment.center_right
                                                                                                ),
                                                                                                self.edit_lieu,
                                                                                                self.edit_sexe
                                                                                            ]
                                                                                        ),
                                                                                    ]
                                                                                )
                                                                            ]
                                                                        ),

                                                                        ft.Row([self.edit_tel, self.matricule]),
                                                                        self.edit_pere,
                                                                        self.edit_mere,
                                                                        ft.ElevatedButton(
                                                                            on_hover=self.bt_hover, **choix_style,
                                                                            on_click=self.modifier_eleve,
                                                                            width=170
                                                                        )
                                                                    ], spacing=20
                                                                )
                                                            )
                                                        ], spacing=10,
                                                    )
                                                )
                                            ], spacing=10
                                        )
                                    )
                                )
                            ]
                        )
                    ]
                )
            )
        )

        # content == contenu qui sera affiché
        self.content=ft.Stack(
            expand=True, alignment=ft.alignment.center,
            controls=[
                self.main_window, self.new_elv_frame, self.new_frame, self.inscrits_frame
            ]
        )

        self.load_datas()
        self.load_lists()

    @staticmethod
    def afficher_stats():
        total_inscrits = be.nb_inscrits()
        nb_attendus = be.nb_classes() * 40
        taux = f"{(total_inscrits / nb_attendus) * 100:.2f}"
        return total_inscrits, taux

    def imprimer_excel(self, e: ft.FilePickerResultEvent):
        widgets = self.table.rows[:]

        noms = [widget.data['nom'] for widget in widgets]
        dates = [widget.data['date'] for widget in widgets]
        lieux = [widget.data['lieu'] for widget in widgets]
        sexes = [widget.data['sexe'] for widget in widgets]
        peres = [widget.data['pere'] for widget in widgets]
        meres = [widget.data['mere'] for widget in widgets]
        contacts = [widget.data['contact'] for widget in widgets]
        matricules = [widget.data['nom'] for widget in widgets]

        data_set = {
            "noms": noms, "date de naissance": dates, "lieu de naissance": lieux,
            'sexe': sexes, "pere": peres, "mere": meres, "contact": contacts,
            "matricule": matricules
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
            pass

    def imprimer_inscrits(self, e: ft.FilePickerResultEvent):
        widgets = self.table_inscrits.rows[:]

        noms = [widget.data['nom'] for widget in widgets]
        mats = [widget.data['matricule'] for widget in widgets]
        classes = [widget.data['classe'] for widget in widgets]

        data_set = {"nom": noms, "matricule": mats, "classe": classes}
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
            pass

    def open_new_frame(self, e):
        self.edit_id.value = e.control.data['id']
        self.edit_nom.value = e.control.data['nom']
        self.sel_date.value = e.control.data['date']
        self.edit_lieu.value = e.control.data['lieu']
        self.edit_pere.value = e.control.data['pere']
        self.edit_mere.value = e.control.data['mere']
        self.edit_tel.value = e.control.data['contact']
        self.matricule.value = e.control.data['matricule']
        self.edit_sexe.value = e.control.data['sexe']

        self.edit_id.update()
        self.edit_nom.update()
        self.sel_date.update()
        self.edit_lieu.update()
        self.edit_pere.update()
        self.edit_mere.update()
        self.edit_tel.update()
        self.matricule.update()
        self.edit_sexe.update()

        # onglet sanction
        self.s_nom.value = e.control.data['nom']
        self.s_matricule.value = e.control.data['matricule']
        self.s_asco.value = be.show_asco_encours()
        self.s_nom.update()
        self.s_matricule.update()
        self.s_asco.update()

        # onglet inscription
        self.o_name.value = e.control.data['nom']
        self.o_name.update()
        self.o_mat.value = be.search_matricule(e.control.data['nom'])
        self.o_mat.update()

        self.new_frame.scale = 1
        self.new_frame.update()

    def close_new_frame(self, e):
        self.new_frame.scale = 0
        self.new_frame.update()

    @staticmethod
    def icon_bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.2
            e.control.content.color = ft.colors.BLACK
            e.control.content.update()
            e.control.update()
        else:
            e.control.scale = 1
            e.control.content.color = ft.colors.BLACK45
            e.control.content.update()
            e.control.update()

    @staticmethod
    def icon_bt_hover2(e):
        if e.data == 'true':
            e.control.scale = 1.4
            e.control.color = ft.colors.BLACK
            e.control.content.update()
            e.control.update()
        else:
            e.control.scale = 1
            e.control.color = ft.colors.BLACK45
            e.control.content.update()
            e.control.update()

    def load_lists(self):
        classes = be.show_classes()
        for data in classes:
            self.o_class.options.append(
                ft.dropdown.Option(data)
            )
            self.fil_classe.options.append(
                ft.dropdown.Option(data)
            )
            self.n_class.options.append(
                ft.dropdown.Option(data)
            )

        sequences = ['séquence 1', 'séquence 2', 'séquence 3', 'séquence 4', 'séquence 5', 'séquence 6', ]
        for seq in sequences:
            self.s_sequence.options.append(ft.dropdown.Option(seq.upper()))

        sanctions = [
            'ABSENCE NJ.', "ABSENCE JUST.",  "AVERTISSEMENT", 'BLAME', "CONSIGNE",
            "EXCLUSION", "EXCLUSION DEF.", "RETARD"
        ]
        for sanction in sanctions:
            self.s_sanction.options.append(ft.dropdown.Option(sanction.upper()))

    def load_datas(self):
        eleves = be.show_all_elev()
        all_datas = []
        for eleve in eleves:
            all_datas.append(
                {
                    "id": eleve[0],  "nom": eleve[1],  "date": eleve[2],  "lieu": eleve[3],  "sexe": eleve[4],
                    "pere": eleve[5],  "mere": eleve[6],  "contact": eleve[7],  "matricule": eleve[8],
                }
            )

        for item in self.table.rows[:]:
            self.table.rows.remove(item)

        nb_girls = 0
        nb_gars = 0
        for eleve in all_datas:

            if be.is_inscriptions_exists(eleve['nom'], eleve['matricule']):
                suscribers_icon_style['name'] = ft.icons.CHECK_BOX_OUTLINED
                suscribers_icon_style['color'] = FIRST_COLOR
                if eleve['sexe'] == 'M':
                    nb_gars += 1
                else:
                    nb_girls += 1
            else:
                suscribers_icon_style['name'] = ft.icons.CHECK_BOX_OUTLINE_BLANK_OUTLINED
                suscribers_icon_style['color'] = "grey"

            if eleve['sexe'] == "F":
                sex_icon_style['name'] = ft.icons.WOMAN_2_SHARP
                sex_icon_style['color'] = SECOND_COLOR
            else:
                sex_icon_style['name'] = ft.icons.MAN_4_ROUNDED
                sex_icon_style['color'] = THRID_COLOR

            self.table.rows.append(
                ft.DataRow(
                    data=eleve,
                    cells=[
                        ft.DataCell(ft.Icon(**suscribers_icon_style)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.Icon(**sex_icon_style),
                                    ft.Text(eleve['nom'])
                                ]
                            )
                        ),
                        ft.DataCell(ft.Text(eleve['matricule'])),
                        ft.DataCell(ft.Text(eleve['contact'])),
                        ft.DataCell(
                            ft.Container(
                                scale=ft.transform.Scale(1),
                                animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                on_hover=self.icon_bt_hover,
                                content=ft.IconButton(
                                    ft.icons.EDIT_OUTLINED, icon_color="black45",
                                    on_click=self.open_new_frame, data=eleve,
                                    tooltip="Actions"
                                ),
                            )
                        ),
                    ]
                )
            )

        self.nb_gars.value = nb_gars
        self.nb_girls.value = nb_girls
        total = nb_girls + nb_gars
        self.nb_total.value = total
        self.pc_gars.value = f"{(nb_gars * 100 / total):.2f} %" if total > 0 else "0 %"
        self.pc_filles.value = f"{(nb_girls * 100 / total):.2f} %" if total > 0 else "0 %"
        self.montant.value = f"{be.ajout_separateur_virgule(total * be.total_tranche('inscription'))}"

    def close_inscrits_frame(self, e):
        self.inscrits_frame.scale = 0
        self.inscrits_frame.update()

    def open_inscrits_frame(self, e):
        for row in self.table_inscrits.rows[:]:
            self.table_inscrits.rows.remove(row)

        eleves = be.show_all_inscriptions()
        all_datas = []
        self.nb_inscrits.value = f"{len(eleves)} élèves"
        self.nb_inscrits.update()

        for eleve in eleves:
            all_datas.append(
                {
                    "nom": eleve[2], "matricule": eleve[3], "classe": eleve[4]
                }
            )

        for eleve in all_datas:
            self.table_inscrits.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(eleve["nom"])),
                        ft.DataCell(ft.Text(eleve["matricule"])),
                        ft.DataCell(ft.Text(eleve["classe"]))
                    ]
                )
            )

        self.table_inscrits.update()
        self.inscrits_frame.scale = 1
        self.inscrits_frame.update()

    def filter_suscribers(self, e):
        for row in self.table_inscrits.rows[:]:
            self.table_inscrits.rows.remove(row)

        eleves = be.search_insc(self.fil_classe.value)
        all_datas = []
        self.nb_inscrits.value = f"{len(eleves)} élèves"
        self.nb_inscrits.update()

        for eleve in eleves:
            all_datas.append(
                {
                    "nom": eleve[2], "matricule": eleve[3], "classe": eleve[4]
                }
            )

        for eleve in all_datas:
            self.table_inscrits.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(eleve["nom"])),
                        ft.DataCell(ft.Text(eleve["matricule"])),
                        ft.DataCell(ft.Text(eleve["classe"]))
                    ]
                )
            )

        self.table_inscrits.update()

    def delete_filter_suscribers(self, e):
        for row in self.table_inscrits.rows[:]:
            self.table_inscrits.rows.remove(row)

        eleves = be.show_all_inscriptions()
        all_datas = []
        self.nb_inscrits.value = f"{len(eleves)} élèves"
        self.nb_inscrits.update()

        for eleve in eleves:
            all_datas.append(
                {
                    "nom": eleve[2], "matricule": eleve[3], "classe": eleve[4]
                }
            )

        for eleve in all_datas:
            self.table_inscrits.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(eleve["nom"])),
                        ft.DataCell(ft.Text(eleve["matricule"])),
                        ft.DataCell(ft.Text(eleve["classe"]))
                    ]
                )
            )

        self.table_inscrits.update()
        self.fil_classe.value = None
        self.fil_classe.update()

    def filter_datas(self, e):
        eleves = be.show_all_elev()

        for item in self.table.rows[:]:
            self.table.rows.remove(item)

        all_datas = []
        for eleve in eleves:
            all_datas.append(
                {
                    "id": eleve[0],  "nom": eleve[1],  "date": eleve[2],  "lieu": eleve[3],  "sexe": eleve[4],
                    "pere": eleve[5],  "mere": eleve[6],  "contact": eleve[7],  "matricule": eleve[8],
                }
            )

        filter_datas = list(filter(lambda x: self.nom.value in x['nom'], all_datas))
        for eleve in filter_datas:
            if be.is_inscriptions_exists(eleve['nom'], eleve['matricule']):
                suscribers_icon_style['name'] = ft.icons.CHECK_BOX_OUTLINED
                suscribers_icon_style['color'] = FIRST_COLOR
                # if eleve['sexe'] == 'M':
                #     nb_gars += 1
                # else:
                #     nb_girls += 1
            else:
                suscribers_icon_style['name'] = ft.icons.CHECK_BOX_OUTLINE_BLANK_OUTLINED
                suscribers_icon_style['color'] = ft.colors.GREY

            if eleve['sexe'] == "F":
                sex_icon_style['name'] = ft.icons.WOMAN_2_SHARP
                sex_icon_style['color'] = SECOND_COLOR
            else:
                sex_icon_style['name'] = ft.icons.MAN_4_ROUNDED
                sex_icon_style['color'] = THRID_COLOR

            self.table.rows.append(
                ft.DataRow(
                    data=eleve,
                    cells=[
                        ft.DataCell(ft.Icon(**suscribers_icon_style)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.Icon(**sex_icon_style),
                                    ft.Text(eleve['nom'])
                                ]
                            )
                        ),
                        ft.DataCell(
                            ft.Text(eleve['matricule'])
                        ),
                        ft.DataCell(
                            ft.Text(eleve['contact'])
                        ),
                        ft.DataCell(
                            ft.Container(
                                scale=ft.transform.Scale(1),
                                animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                on_hover=self.icon_bt_hover,
                                content=ft.IconButton(
                                    ft.icons.EDIT_OUTLINED, icon_color="black45",
                                    on_click=self.open_new_frame, data=eleve,
                                    tooltip="Actions"
                                ),
                            )
                        ),
                    ]
                )
            )

        self.table.update()

    def change_date_edit_elev(self, e):
        self.sel_date.value = str(self.cp.dp_modif_eleve.value)[0:10]
        self.sel_date.update()

    def change_date_new_elev(self, e):
        self.n_sel_date.value = str(self.cp.dp_new_eleve.value)[0:10]
        self.n_sel_date.update()

    def changement_classe2(self, e):
        self.n_effectif.value = str(be.nb_inscrits_classe(self.n_class.value))
        self.n_effectif.update()
        self.n_frais.value = str(be.frais_inscription())
        self.n_frais.update()

        rs = be.compter_inscrits() + 1

        if 1 <= rs < 10:
            zero = "00"
        elif 10 <= rs < 100:
            zero = "0"
        else:
            zero = ""

        mat = "CBK" + str(be.show_asco_encours()) + zero + str(rs)

        self.n_mat.value = mat
        self.n_mat.update()

    def create_sanction(self, e):
        if be.is_inscriptions_exists(self.s_nom.value, self.s_matricule.value):
            counter = 0
            for widget in (self.s_sanction, self.s_sequence, self.s_nombre):
                if widget.value is None:
                    counter += 1

            if counter == 0:
                nombre = int(self.s_nombre.value)
                be.add_sanction(
                    self.s_asco.value, self.s_nom.value, self.s_matricule.value,
                    self.s_sequence.value.lower(), self.s_sanction.value, nombre
                )

            self.cp.box.title.value = "Validé !"
            self.cp.box.content.value = "Enregistré avec succès"
            self.cp.box.open = True
            self.cp.box.update()

            for widget in (self.s_sanction, self.s_sequence, self.s_nombre):
                widget.value = None
                widget.update()

            self.nom.value = None
            self.nom.update()

        else:
            self.cp.box.title.value = "Action Impossible"
            self.cp.box.content.value = "L'èlève n'est pas encore inscrit pour l'année scolaire en cours"
            self.cp.box.open = True
            self.cp.box.update()

    def modifier_eleve(self, e):
        eleve_id = int(self.edit_id.value)
        be.update_elev(
            self.edit_nom.value, self.sel_date.value, self.edit_lieu.value, self.edit_sexe.value,
            self.edit_pere.value, self.edit_mere.value, self.edit_tel.value, eleve_id
        )
        self.cp.box.title.value = "Validé !"
        self.cp.box.content.value = "élève modifié avec succès avec succès"
        self.cp.box.open = True
        self.cp.box.update()

        self.load_datas()
        self.table.update()
        self.nom.value = None
        self.nom.update()

    def changement_classe(self, e):
        self.o_effectif.value = str(be.nb_inscrits_classe(self.o_class.value))
        self.o_effectif.update()
        self.o_frais.value = str(be.frais_inscription())
        self.o_frais.update()

    def close_new_elv_frame(self, e):
        self.new_elv_frame.scale = 0
        self.new_elv_frame.update()

    def open_new_elv_frame(self, e):
        self.new_elv_frame.scale = 1
        self.new_elv_frame.update()

    def valider_inscription(self, e):
        if be.is_inscriptions_exists(self.o_name.value, self.o_mat.value):
            self.cp.box.title.value = "Action Impossible"
            self.cp.box.content.value = "L'èlève est déja inscrit pour l'année scolaire en cours"
            self.cp.box.open = True
            self.cp.box.update()

        else:
            count = 0
            for widget in (self.o_name, self.o_class):
                if widget.value is None or widget.value == "":
                    count += 1

            if count > 0:
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = "Les champs Nom et Classe sont obligatoires"
                self.cp.box.open = True
                self.cp.box.update()
            else:
                asco = be.show_asco_encours()
                for tranche in (self.tranche_1, self.tranche_2, self.tranche_3):
                    if tranche.value is None or tranche.value == "":
                        pass
                    else:
                        mt = int(tranche.value)
                        if tranche.label == "Tranche 1":
                            name_tranche = 'tranche 1'
                        elif tranche.label == "Tranche 2":
                            name_tranche = 'tranche 2'
                        else:
                            name_tranche = 'tranche 3'

                        be.add_pension(
                            asco,
                            self.o_name.value, name_tranche, mt, datetime.date.today()
                        )

                for tranche in (self.tranche_1, self.tranche_2, self.tranche_3):
                    tranche.value = None
                    tranche.update()

                self.switch.value = False
                self.switch.update()
                statut = "nouveau" if self.o_check.value is False else "redoublant"
                print(statut)
                be.add_inscription(asco, self.o_name.value, self.o_mat.value, self.o_class.value, self.o_frais.value, statut)

                for widget in (self.o_name, self.o_mat, self.o_class, self.o_frais, self.o_effectif):
                    widget.value = None
                    widget.update()

                self.o_check.value = False
                self.o_check.update()

                self.cp.box.title.value = "Validé!"
                self.cp.box.content.value = "Inscription enregistrée avec succès"
                self.cp.box.open = True
                self.cp.box.update()

                self.load_datas()
                self.table.update()
                self.pc_filles.update()
                self.pc_gars.update()
                self.nb_girls.update()
                self.nb_gars.update()
                self.nb_total.update()
                self.montant.update()

    def changement_solde(self, e):
        if self.switch.value:
            self.tranche_3.value = be.total_tranche('tranche 3')
            self.tranche_2.value = be.total_tranche('tranche 2')
            self.tranche_1.value = be.total_tranche('tranche 1')
            self.tranche_3.update()
            self.tranche_2.update()
            self.tranche_1.update()
        else:
            self.tranche_3.value = None
            self.tranche_2.value = None
            self.tranche_1.value = None
            self.tranche_3.update()
            self.tranche_2.update()
            self.tranche_1.update()

    def changement_solde_2(self, e):
        if self.n_switch.value:
            self.n_tranche_3.value = be.total_tranche('tranche 3')
            self.n_tranche_2.value = be.total_tranche('tranche 2')
            self.n_tranche_1.value = be.total_tranche('tranche 1')
            self.n_tranche_3.update()
            self.n_tranche_2.update()
            self.n_tranche_1.update()
        else:
            self.n_tranche_3.value = None
            self.n_tranche_2.value = None
            self.n_tranche_1.value = None
            self.n_tranche_3.update()
            self.n_tranche_2.update()
            self.n_tranche_1.update()

    def valider_inscription2(self, e):
        count = 0
        for widget in (self.n_name, self.n_contact, self.n_class, self.sexe):
            if widget.value is None or widget.value == "":
                count += 1

        if count > 0:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Les champs Nom, Classe, Sexe et Contact sont obligatoires"
            self.cp.box.open = True
            self.cp.box.update()
        else:
            # Ajouter élève
            be.add_eleve(
                self.n_name.value, self.sel_date.value, self.n_lieu.value, self.sexe.value,
                self.n_pere.value, self.n_mere.value, self.n_contact.value, self.n_mat.value
            )

            asco = be.show_asco_encours()

            for tranche in (self.n_tranche_1, self.n_tranche_2, self.n_tranche_3):
                if tranche.value is None or tranche.value == "":
                    pass
                else:
                    mt = int(tranche.value)
                    if tranche.label == "Tranche 1":
                        name_tranche = 'tranche 1'
                    elif tranche.label == "Tranche 2":
                        name_tranche = 'tranche 2'
                    else:
                        name_tranche = 'tranche 3'

                    be.add_pension(
                        asco,
                        self.n_name.value, name_tranche, mt, datetime.date.today()
                    )

            for tranche in (self.tranche_1, self.tranche_2, self.tranche_3):
                tranche.value = None
                tranche.update()

            self.switch.value = False
            self.switch.update()

            statut = "nouveau" if self.o_check.value is False else "redoublant"

            # Ajouter inscription
            be.add_inscription(asco, self.n_name.value.upper(), self.n_mat.value, self.n_class.value,
                               self.n_frais.value, statut)

            for widget in (
                    self.n_name, self.n_contact, self.n_class, self.sexe, self.n_lieu, self.n_mat, self.n_pere,
                    self.n_mere,
                    self.sel_date, self.n_contact, self.n_class, self.n_frais, self.n_effectif, self.n_check
            ):
                widget.value = None
                widget.update()

            self.cp.box.title.value = "Validé!"
            self.cp.box.content.value = "Inscription créée avec succès"
            self.cp.box.open = True
            self.cp.box.update()

            self.load_datas()
            self.table.update()
            self.pc_filles.update()
            self.pc_gars.update()
            self.nb_girls.update()
            self.nb_gars.update()
            self.nb_total.update()
            self.montant.update()

    @staticmethod
    def bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.1
            e.control.update()

        else:
            e.control.scale = 1
            e.control.update()

