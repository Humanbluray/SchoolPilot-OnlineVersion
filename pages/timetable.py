from utils import *
from pages.time_classe import TimeClasse
from pages.time_prof import TimeProf


class TimeTable(ft.Container):
    def __init__(self, cp: object):
        super(TimeTable, self).__init__(
            expand=True
        )
        self.cp = cp

        self.tab_classe = TimeClasse(self)
        self.tab_prof = TimeProf(self)

        self.content = ft.Container(
            padding=ft.padding.only(15, 10, 15, 10), expand=True, border_radius=12,
            margin=ft.margin.only(20, 0, 20, 0),
            content=ft.Tabs(
                tab_alignment=ft.TabAlignment.START, selected_index=0, expand=True, animation_duration=300,
                unselected_label_color=ft.colors.GREY, label_color=FIRST_COLOR,
                indicator_border_radius=30, indicator_border_side=ft.BorderSide(5,SECOND_COLOR),
                indicator_tab_size=True,
                tabs=[self.tab_prof, self.tab_classe],
            )
        )
