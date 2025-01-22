import flet as ft
from utils import backend as be


class DashBoard(ft.Container):
    def __init__(self, cp: object):
        super().__init__()
        self.students_chart = ft.PieChart(
            sections_space=5, center_space_radius=40, on_chart_event=self.on_chart_event
        )
        self.cp = cp
        self.content = ft.Container(
            padding=ft.padding.only(20, 0, 20, 0), expand=True,
            content=ft.Column(
                controls=[
                ]
            )
        )
        self.nb_suscribers()

    def nb_suscribers(self):
        # total = be.nb_inscrits()
        girls = {"section": "filles", "quantity": be.nb_inscrits_sexe("F"), "color": "red"}
        boys = {"section": "garçons", "quantity": be.nb_inscrits_sexe("M"), "color": "amber"}
        for item in (girls, boys):
            self.students_chart.sections.append(
                ft.PieChartSection(
                    value=item['quantity'],
                    title=item['section'],
                    color=item['color'],
                    radius=40,
                )
            )

    def on_chart_event(self, e: ft.PieChartEvent):
        for idx, section in enumerate(self.students_chart.sections):
            if idx == e.section_index:
                section.radius = 50
                section.title_style = ft.TextStyle(size=12, font_family="Poppins ExtraBold")
            else:
                section.radius = 40
                section.title_style = ft.TextStyle(size=12, font_family="Poppins Medium")

        self.students_chart.update()
