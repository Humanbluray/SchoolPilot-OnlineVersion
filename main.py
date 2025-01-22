import flet as ft
from pages.accueil import Accueil
from pages.connexion import Connexion
from pages.new_user import NewUser
import os

# Définir des constantes pour les routes
ROUTE_ACCUEIL = "/accueil"
ROUTE_CONNEXION = "/"
ROUTE_WAITING_USER = "/waiting-user"


def main(page: ft.Page):
    # Charger les polices personnalisées
    page.fonts = {
        "Poppins Regular": "fonts/Poppins-Regular.ttf",
        "Poppins Bold": "fonts/Poppins-Bold.ttf",
        "Poppins SemiBold": "fonts/Poppins-SemiBold.ttf",
        "Poppins Black": "fonts/Poppins-Black.ttf",
        "Poppins Italic": "fonts/Poppins-Italic.ttf",
        "Poppins Medium": "fonts/Poppins-Medium.ttf",
        "Poppins ExtraBold": "fonts/Poppins-ExtraBold.ttf",
        "Poppins Light": "fonts/Poppins-Light.ttf",
    }

    page.theme_mode = ft.ThemeMode.LIGHT

    # Dictionnaire pour mapper les routes aux vues
    route_views = {
        ROUTE_CONNEXION: Connexion,
        ROUTE_ACCUEIL: Accueil,
        ROUTE_WAITING_USER: NewUser,
    }

    # Gérer les changements de route
    def route_change(event: ft.RouteChangeEvent):
        page.views.clear()  # Réinitialiser les vues
        current_route = event.route  # Récupérer la route depuis l'événement
        if current_route in route_views:
            page.views.append(route_views[current_route](page))
        else:
            # Rediriger vers une route par défaut si la route est inconnue
            page.views.append(Connexion(page))
        page.update()

    # Gérer la navigation "retour"
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Assignation des callbacks
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Naviguer vers la route initiale
    page.go(page.route)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, assets_dir="assets", route_url_strategy="default",)
