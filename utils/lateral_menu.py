import flet as ft
from utils import backend as be, FIRST_COLOR
from pages.eleves import Eleves
from pages.classes import Classes
from pages.profs import Profs
from pages.notes import Notes
from pages.pension import Pensions
from pages.users import Users
from pages.timetable import TimeTable
from pages.bulletins import Bulletins
from pages.asco import Annees
from pages.connexion import user_infos
from pages.dashboard import DashBoard
from utils import THRID_COLOR, SECOND_COLOR
from utils.couleurs import first_color

_icon_color_dark = ft.colors.WHITE70
_icon_color_light = ft.colors.BLACK38
_text_color_dark = ft.colors.WHITE70
_text_color_light = ft.colors.BLACK87


class ItemMenu(ft.Container):
    def __init__(self, title: str, my_icon: str, selected_icon_color: str, selected_text_color: str):
        super(ItemMenu, self).__init__(
            on_hover=self.hover_ct,
            shape=ft.BoxShape.RECTANGLE,
            padding=ft.padding.only(10, 9, 0, 9),
            border_radius=0,
            scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN)
        )
        self.title = title
        self.my_icon = my_icon
        self.is_clicked = False
        self.selected_icon_color = selected_icon_color
        self.selected_text_color = selected_text_color

        self.visuel = ft.Icon(my_icon, size=18, color=selected_icon_color)
        self.name = ft.Text(title, size=12, font_family="Poppins Medium", color=selected_text_color)

        self.content = ft.Row(controls=[self.visuel, self.name], alignment=ft.MainAxisAlignment.START)

    def hover_ct(self, e):
        if e.data == "true":
            e.control.scale = 1.15
            e.control.visuel.color = FIRST_COLOR
            e.control.name.color = FIRST_COLOR

            e.control.name.font_family = "Poppins Medium"
            e.control.visuel.update()
            e.control.name.update()
            e.control.update()
        else:
            if self.is_clicked:
                self.visuel.color = THRID_COLOR
                self.name.font_family = "Poppins Bold"
                self.name.color = FIRST_COLOR
                self.border = ft.border.only(right=ft.BorderSide(4, THRID_COLOR))
                self.visuel.update()
                self.name.update()
                self.update()
            else:
                self.visuel.color = self.selected_icon_color
                self.name.font_family = "Poppins Medium"
                self.name.color = self.selected_text_color
                self.border = None
                self.visuel.update()
                self.name.update()
                self.update()

            e.control.scale = 1
            e.control.update()

    def set_is_clicked_true(self):
        self.is_clicked = True
        self.visuel.color = THRID_COLOR
        self.name.font_family = "Poppins Bold"
        self.name.color = FIRST_COLOR
        self.border = ft.border.only(right=ft.BorderSide(4, THRID_COLOR))
        self.visuel.update()
        self.name.update()
        self.update()

    def set_is_clicked_false(self):
        self.is_clicked = False
        self.visuel.color = self.selected_icon_color
        self.border = None
        self.name.font_family = "Poppins Medium"
        self.name.color = self.selected_text_color
        self.bgcolor = None
        self.visuel.update()
        self.name.update()
        self.update()


class Menu(ft.Card):
    def __init__(self, cp: object, page: ft.Page):
        super(Menu, self).__init__(
            elevation=0,
            expand=True,
        )
        self.page = page
        self.cp = cp  # Conteneur parent

        if self.cp.page.theme_mode == ft.ThemeMode.DARK:
            color_icon = _icon_color_dark
            color_text = _text_color_dark
            card_color = None

        else:
            color_icon = _icon_color_light
            color_text = _text_color_light
            card_color = "white"

        self.eleves = ItemMenu("élèves".upper(), ft.icons.PERSON_OUTLINED, color_icon, color_text)
        self.timetable = ItemMenu("Time table".upper(), ft.icons.FILTER_TILT_SHIFT_OUTLINED, color_icon, color_text)
        self.classes = ItemMenu("Classes".upper(), ft.icons.ACCOUNT_BALANCE_OUTLINED, color_icon, color_text)
        self.professeurs = ItemMenu('profs'.upper(), ft.icons.GROUP_OUTLINED, color_icon, color_text)
        self.pensions = ItemMenu('scolarité'.upper(), ft.icons.MONETIZATION_ON_OUTLINED, color_icon, color_text)
        self.notes= ItemMenu("Notes".upper(), ft.icons.NOTES_OUTLINED, color_icon, color_text)
        self.bull_prim = ItemMenu("Bulls 6e/5e".upper(), ft.icons.SCHOOL_OUTLINED, color_icon, color_text)
        self.bull_second = ItemMenu("Bulls autres".upper(), ft.icons.SCHOOL_OUTLINED, color_icon, color_text)
        self.users = ItemMenu("Utilisateurs".upper(), ft.icons.GROUPS_OUTLINED, color_icon, color_text)
        self.annees = ItemMenu("Années sco.".upper(), ft.icons.EDIT_CALENDAR_OUTLINED, color_icon, color_text)

        if user_infos['acces'] == "PROFESSEUR":
            self.eleves.visible = False
            self.timetable.visible = False
            self.classes.visible = False
            self.professeurs.visible = False
            self.pensions.visible = False
            self.notes.visible = True
            self.bull_prim.visible = True
            self.bull_second.visible = True
            self.annees.visible = False
            self.users.visible = False

        elif user_infos['acces'] == "OPERATEUR":
            self.eleves.visible = True
            self.timetable.visible = False
            self.classes.visible = True
            self.professeurs.visible = True
            self.pensions.visible = True
            self.notes.visible = True
            self.bull_prim.visible = True
            self.bull_second.visible = True
            self.annees.visible = False
            self.users.visible = False

        elif user_infos['acces'] == "CONSULTANT":
            self.eleves.visible = True
            self.timetable.visible = True
            self.classes.visible = True
            self.professeurs.visible = True
            self.pensions.visible = True
            self.notes.visible = True
            self.bull_prim.visible = True
            self.bull_second.visible = True
            self.annees.visible = False
            self.users.visible = False

        elif user_infos['acces'] == "ADMINISTRATEUR":
            self.eleves.visible = True
            self.timetable.visible = True
            self.classes.visible = True
            self.professeurs.visible = True
            self.pensions.visible = True
            self.notes.visible = True
            self.bull_prim.visible = True
            self.bull_second.visible = True
            self.annees.visible = False
            self.users.visible = True

        elif user_infos['acces'] == "SUPER ADMIN":
            self.eleves.visible = True
            self.timetable.visible = True
            self.classes.visible = True
            self.professeurs.visible = True
            self.pensions.visible = True
            self.notes.visible = True
            self.bull_prim.visible = True
            self.bull_second.visible = True
            self.annees.visible = True
            self.users.visible = True

        self.children = [
            self.eleves, self.timetable, self.classes, self.professeurs,
            self.pensions, self.notes, self.bull_prim, self.bull_second,
            self.annees, self.users,
        ]

        for item in self.children:
            item.on_click = self.cliquer_menu

        self.content = ft.Container(
            padding=ft.padding.only(20, 15, 20, 15),
            border_radius=8, bgcolor=card_color,
            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text(f"{user_infos['nom']}", size=12, font_family="Poppins Bold"),
                                            ft.Text(f"{user_infos['poste']}", size=11, font_family="Poppins Regular",
                                                    color="grey")
                                        ], spacing=2
                                    ),
                                    ft.IconButton(
                                        ft.icons.EXIT_TO_APP_OUTLINED, scale=0.7, icon_color="black87",
                                        on_click=lambda e: self.cp.page.go('/')
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Divider(height=1, thickness=1),
                            ft.Divider(height=2, color="transparent"),
                            ft.Column(
                                controls=[
                                    self.eleves, self.classes, self.professeurs, self.timetable,
                                    self.pensions, self.notes, self.bull_prim, self.bull_second, self.users,
                                    self.annees
                                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Divider(height=1, thickness=1),
                            ft.Column(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                f"Année scolaire".upper(),
                                                size=11, font_family="Poppins Medium"),
                                            ft.Text(
                                                f"{be.show_asco_encours()} - {int(be.show_asco_encours()) + 1}",
                                                size=11, font_family="Poppins Medium"),
                                        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    ft.Text("SCHOOL PILOT V1.0", size=10),
                                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ], spacing=30,  horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

    def cliquer_menu(self, e):
        for item in self.children:
            item.set_is_clicked_false()

        e.control.set_is_clicked_true()
        e.control.update()

        for row in self.cp.contenu.content.controls[:]:
            self.cp.contenu.content.controls.remove(row)

        if e.control.name.value == "élèves".upper():
            self.cp.contenu.content.controls.append(Eleves(self.cp))
            self.cp.update()

        if e.control.name.value == "time table".upper():
            self.cp.contenu.content.controls.append(TimeTable(self.cp))
            self.cp.update()

        if e.control.name.value == "classes".upper():
            self.cp.contenu.content.controls.append(Classes(self.cp))
            self.cp.update()

        if e.control.name.value == "profs".upper():
            self.cp.contenu.content.controls.append(Profs(self.cp))
            self.cp.update()

        if e.control.name.value == "notes".upper():
            self.cp.contenu.content.controls.append(Notes(self.cp))
            self.cp.update()

        if e.control.name.value == "scolarité".upper():
            self.cp.contenu.content.controls.append(Pensions(self.cp))
            self.cp.update()

        if e.control.name.value == "utilisateurs".upper():
            self.cp.contenu.content.controls.append(Users(self.cp))
            self.cp.update()

        if e.control.name.value == "board".upper():
            self.cp.contenu.content.controls.append(DashBoard(self.cp))
            self.cp.update()

        if e.control.name.value == "bulls autres".upper():
            self.cp.contenu.content.controls.append(Bulletins(self.cp))
            self.cp.update()

        if e.control.name.value == "bulls 6e/5e".upper():
            pass

        if e.control.name.value == "années sco.".upper():
            self.cp.contenu.content.controls.append(Annees(self.cp))
            self.cp.update()


