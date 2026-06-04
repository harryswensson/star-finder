import flet as ft
from star_info import GALAXY_DATA

def main(page: ft.Page):

    #Get a list of all stars
    all_stars = set()
    view_stars = set()
    for starlist in GALAXY_DATA.values():
        for star in starlist.keys():
            all_stars.add(star.lower())
            view_stars.add(star)
    l_all_stars = []
    l_view_stars = list(view_stars)
    l_view_stars.sort()

    for star in l_view_stars:
        l_all_stars.append(star.lower())

    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.padding = ft.Padding.only(top=50, left=20, right=20)

    title = ft.Text(
        value="Star Finder",
        size=60,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_ACCENT,
        text_align=ft.TextAlign.CENTER
    )

    def on_search_submit(e):
        page.update()

    def select_item(i):
        search_bar.value = l_all_stars[i]
        results_list.visible = False
        show_star_information(l_view_stars[i])
        page.update()

    def show_star_information(star):
        star_list.visible = True
        star_list.controls.clear()
        star_list.controls.append(ft.Text(f"Galaxies where {star} is found:", color=ft.Colors.WHITE_70, text_align=ft.TextAlign.CENTER, size=20))
        star_list.controls.append(
            ft.Text(f"Sorted from highest to lowest chance", color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER,
                    size=10))
        appearing_galaxies = []
        for galaxy in GALAXY_DATA.keys():
            for star_1 in GALAXY_DATA[galaxy].keys():
                if star_1 == star:
                    appearing_galaxies.append((galaxy, GALAXY_DATA[galaxy][star_1]))

        appearing_galaxies.sort(key=lambda x: x[1])

        star_list.controls.append(ft.Container(height=20))
        for galaxy in appearing_galaxies:
            star_list.controls.append(ft.Container(
                width=400,
                padding=5,
                #bgcolor=ft.Colors.SURFACE_VARIANT,
                border_radius = 5,
                border = ft.Border.all(1, ft.Colors.OUTLINE),

                content = ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text(value=galaxy[0], size=20,weight=ft.FontWeight.BOLD,
                        color=ft.Colors.PRIMARY),
                        ft.Text(value="1 in {:,}".format(galaxy[1]), color=ft.Colors.GREY_500, italic=True, size=15)
                    ]
                )
            ))

        page.update()

    def clear_search(e):
        search_bar.value = ""
        view_results(None)
        filter_search(None)
        star_list.visible = False
        page.update()


    def filter_search(e):
        query = search_bar.value.lower()

        results_list.controls.clear()

        for i, item in enumerate(l_all_stars):
            if query in item:
                results_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(l_view_stars[i]),
                        leading=ft.Icons.LABEL_OUTLINED,
                        on_click=lambda x, i=i: select_item(i)
                    )
                )
        if not results_list.controls:
            results_list.controls.append(
                ft.Text("No results found.", color=ft.Colors.GREY_500, italic=True)
            )
        page.update()

    def view_results(e):
        filter_search(None)
        results_list.visible = True
        star_list.visible = False
        page.update()


    search_bar = ft.TextField(
        hint_text="Search for stars...",
        prefix_icon=ft.Icons.SEARCH,
        width=400,
        on_change=filter_search,
        on_click=view_results,

        suffix = ft.Container(
            content=ft.GestureDetector(
                content=ft.Icon(
                    ft.Icons.CLEAR,
                    size=16,
                    color=ft.Colors.GREY_500,
                ),
                mouse_cursor=ft.MouseCursor.CLICK,
                on_tap=clear_search
            ),
            alignment=ft.Alignment.CENTER,
            width = 30
        )
    )



    results_list = ft.Column(width=400, spacing=5)

    star_list = ft.Column(width=400, spacing=5,alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                          controls = [])

    filter_search(None)

    page.add(
        title,
        ft.Container(height=20),
        search_bar,
        results_list,
        ft.Container(height=10),
        star_list
        )

ft.run(main)
