import flet as ft

from utils import FIRST_COLOR, SECOND_COLOR
from pages.notes_autres import NotesAutres
from pages.notes_prim import NotesPrim


class Notes(ft.Container):
    def __init__(self, cp: object):
        super(Notes, self).__init__(
            expand=True, padding=ft.padding.only(10, 10, 10, 0), bgcolor="#f2f2f2"
        )
        self.cp = cp

        self.tab_autre = NotesAutres(self)
        self.tab_prim = NotesPrim(self)

        self.content = ft.Container(
            padding=ft.padding.only(10, 10, 10, 10), expand=True, border_radius=12, bgcolor="#f2f2f2",
            content=ft.Tabs(
                tab_alignment=ft.TabAlignment.START_OFFSET,
                selected_index=0, expand=True, animation_duration=300,
                unselected_label_color=ft.colors.GREY, label_color=FIRST_COLOR,
                indicator_border_radius=30, indicator_border_side=ft.BorderSide(5, SECOND_COLOR),
                indicator_tab_size=True,
                tabs=[self.tab_autre],
            )
        )


