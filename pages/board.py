import flet as ft


class Board(ft.Container):
    def __init__(self, cp: object):
        super(Board, self).__init__(
            expand=True
        )
        self.cp = cp
        self.main_window = ft.Container(
            padding=ft.padding.only(20, 0, 20, 0), expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    # ft.Container(
                    #     padding=ft.padding.only(30, 15, 30, 15), border_radius=12, bgcolor="white",
                    #     content=ft.Column(
                    #         controls=[]
                    #     )
                    # ),
                    ft.Container(
                        padding=ft.padding.only(30, 15, 30, 15), bgcolor="white", border_radius=12, expand=True,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                ft.Row([ft.Text("En cours d'élaboration", size=16, font_family="Poppins Light")], alignment="center")
                            ]
                        )
                    ),
                ], spacing=15
            )
        )
        self.content = ft.Stack(
            controls=[
                self.main_window
            ], alignment=ft.alignment.center
        )
