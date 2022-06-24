# -*- coding: utf-8 -*-
"""
23 Jun 2022

@author: prslvtsv
"""
import apart_solver as solver


from textual import events

# from textual.app import App
# from textual.widgets import ScrollView
# from rich.table import Table


# class MyApp(App):
#     """An example of a very simple Textual App"""

#     async def on_load(self, event: events.Load) -> None:
#         await self.bind("q", "quit", "Quit")

#     async def on_mount(self, event: events.Mount) -> None:

#         self.body = body = ScrollView(auto_width=True)

#         await self.view.dock(body)

#         async def add_content():
#             table = Table(title="Demo")

#             for i in range(20):
#                 table.add_column(f"Col {i + 1}", style="magenta")
#             for i in range(100):
#                 table.add_row(*[f"cell {i},{j}" for j in range(20)])
#             await body.update(table)

# await self.call_later(add_content)


def main():
    solution = solver.run_test()

    for s in solution:
        print(s)


if __name__ == "__main__":
    pass
    # main()
    # MyApp.run(title="Simple App", log="textual.log")
