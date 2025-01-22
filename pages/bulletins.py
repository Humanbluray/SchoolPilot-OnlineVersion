from utils import *
from pages.bulletins_seq import BullSeq
from pages.bulletins_trim import BullTrim
from pages.bull_ann import BullAnn


class Bulletins(ft.Container):
    def __init__(self, cp: object):
        super(Bulletins, self).__init__(
            expand=True
        )
        self.cp = cp

        self.tab_seq = BullSeq(self)

        # onglet trimestre
        self.tab_trim = BullTrim(self)

        # onglet annuel
        self.tab_ann = BullAnn(self)

        self.content = ft.Container(
            padding=ft.padding.only(20, 10, 20, 10), expand=True, border_radius=12, bgcolor="#f0f0f6",
            content=ft.Tabs(
                tab_alignment=ft.TabAlignment.START, selected_index=0, expand=True, animation_duration=300,
                unselected_label_color=ft.colors.GREY, label_color=FIRST_COLOR,
                indicator_border_radius=30, indicator_border_side=ft.BorderSide(5, SECOND_COLOR),
                indicator_tab_size=True,
                tabs=[self.tab_seq, self.tab_trim, self.tab_ann],
            )
        )

