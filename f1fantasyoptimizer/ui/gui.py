#!/usr/bin/env python3
import tkinter as tk
import tkinter.font

import f1fantasyoptimizer.data as data
import f1fantasyoptimizer.simulator as simulator
import f1fantasyoptimizer.solver as solver
import f1fantasyoptimizer.ui.cli as cli

WINDOW_TITLE = "F1FantasyOptimizer"

FANTASY_MODE = ("Fantasy", "")


class PickWidget(tk.Frame):
    """
    Widget displaying one picked driver or constructor.
    """
    # Frame width in "M" characters of the largest font
    FRAME_WIDTH_CHARS = 10
    FRAME_HEIGHT = 140
    FRAME_PADDING = 5
    FRAME_RELIEF = tk.RAISED
    FRAME_BORDER_WIDTH = 1
    FRAME_BG_COLOR_DRIVER = "white"
    FRAME_BG_COLOR_CONSTRUCTOR = "#DEDEDE"
    # Padding in terms of the height of the label
    TYPE_PADDING_BOT = 0.3
    # Font size difference relative to the default font size
    NAME_LABEL_SIZE = +1
    TD_LABEL_BG_COLOR = "#ff3333"
    TD_LABEL_TEXT_COLOR = "white"
    TD_LABEL_RELIEF = tk.SUNKEN
    TD_LABEL_BORDER_WIDTH = 1
    TYPE_LABEL_TEXT_CONSTRUCTOR = "Constructor"
    TYPE_LABEL_TEXT_DRIVER = "Driver"
    TD_LABEL_TEXT = "TD"

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, relief=PickWidget.FRAME_RELIEF, borderwidth=PickWidget.FRAME_BORDER_WIDTH,
                          **kwargs)

        self.td_label = tk.Label(self, relief=PickWidget.TD_LABEL_RELIEF, fg=PickWidget.TD_LABEL_TEXT_COLOR)
        td_font = tk.font.Font(font=self.td_label["font"])
        td_font.config(weight=tk.font.BOLD)
        self.td_label.configure(font=td_font)

        self.name_label = tk.Label(self)
        name_font = tk.font.Font(name="name_font", font=self.name_label["font"])
        name_font.config(weight=tk.font.BOLD,
                         size=name_font.actual()["size"] + PickWidget.NAME_LABEL_SIZE)
        self.name_label.configure(font=name_font)

        self.points_label = tk.Label(self)
        points_font = tk.font.Font(font=self.points_label["font"])
        points_font.config(weight=tk.font.BOLD)
        self.points_label.configure(font=points_font)

        self.cost_label = tk.Label(self)
        cost_font = tk.font.Font(font=self.cost_label["font"])
        cost_font.config(weight=tk.font.BOLD)
        self.cost_label.configure(font=cost_font)

        self.type_label = tk.Label(self)
        type_font = tk.font.Font(font=self.type_label["font"])
        self.type_label.configure(font=type_font)

        self.td_label.grid(row=0, column=0, columnspan=2, sticky=tk.N, pady=(PickWidget.FRAME_PADDING, 0))
        self.name_label.grid(row=1, column=0, columnspan=2, sticky=tk.N + tk.W + tk.E, padx=PickWidget.FRAME_PADDING)
        self.type_label.grid(row=2, column=0, columnspan=2, sticky=tk.N + tk.W + tk.E,
                             pady=(0, PickWidget.TYPE_PADDING_BOT * self.type_label.winfo_reqheight()))
        self.points_label.grid(row=3, column=0, sticky=tk.N + tk.W + tk.E)
        self.cost_label.grid(row=3, column=1, sticky=tk.N + tk.W + tk.E)

        # Size of the frame defined by a given amount of "M" characters in the largest font
        frame_width = name_font.measure("M" * PickWidget.FRAME_WIDTH_CHARS) + 2 * PickWidget.FRAME_PADDING

        self.config(width=frame_width, height=PickWidget.FRAME_HEIGHT)

        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def set_pick(self, pick):
        if pick.pick_type == data.Pick.PickType.DRIVER:
            bg_color = PickWidget.FRAME_BG_COLOR_DRIVER
            self.type_label.config(text=PickWidget.TYPE_LABEL_TEXT_DRIVER)
        else:
            bg_color = PickWidget.FRAME_BG_COLOR_CONSTRUCTOR
            self.type_label.config(text=PickWidget.TYPE_LABEL_TEXT_CONSTRUCTOR)
        if pick.td:
            self.td_label.config(text=PickWidget.TD_LABEL_TEXT, borderwidth=PickWidget.TD_LABEL_BORDER_WIDTH,
                                 bg=PickWidget.TD_LABEL_BG_COLOR)
        else:
            self.td_label.config(text="", borderwidth=0, bg=bg_color)
        self.name_label.config(text=pick.name)
        self.points_label.config(text=f"{pick.points} Pts")
        self.cost_label.config(text=f"${pick.cost:.1f}M")
        self.configure(bg=bg_color)
        self.name_label.configure(bg=bg_color)
        self.type_label.configure(bg=bg_color)
        self.points_label.configure(bg=bg_color)
        self.cost_label.configure(bg=bg_color)


class TeamWidget(tk.Frame):
    """
    Widget displaying one team.
    """
    PICKS_COLUMNS_COUNT = 6
    PICK_COLUMN_SPAN = 2
    PICK_PADDING = 5
    TOTAL_PADDING_TOP = 5
    TOTAL_PADDING = 5
    PICK_WIDGET_OPTIONS = dict(padx=PICK_PADDING, pady=PICK_PADDING, sticky=tk.NSEW,
                               columnspan=PICK_COLUMN_SPAN)
    SPACER_FRAME_OPTIONS = dict(sticky=tk.NSEW)
    PICKS_FRAME_OPTIONS = dict(fill=tk.BOTH, expand=True)

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.picks: list[PickWidget] = []

        self.picks_frame = tk.Frame(self, bg=self["bg"])
        self.row3 = tk.Frame(self, bg=self["bg"])

        self.picks.append(PickWidget(self.picks_frame))  # driver 0
        self.picks.append(PickWidget(self.picks_frame))  # driver 1
        self.picks.append(PickWidget(self.picks_frame))  # driver 2
        self.picks.append(PickWidget(self.picks_frame))  # driver 3
        self.picks.append(PickWidget(self.picks_frame))  # driver 4
        self.picks.append(PickWidget(self.picks_frame))  # constructor 0
        self.picks.append(PickWidget(self.picks_frame))  # constructor 1

        self.total_label = tk.Label(self.row3, text="Total:", bg=self["bg"])
        total_font = tk.font.Font(font=self.total_label["font"])
        total_font.config(weight=tk.font.BOLD)
        self.total_label.configure(font=total_font)

        self.total_points = tk.Label(self.row3, bg=self["bg"])
        self.total_points.configure(font=total_font)

        self.total_cost = tk.Label(self.row3, bg=self["bg"])
        self.total_cost.configure(font=total_font)

        row = 0
        col = 1
        for pick_idx in range(0, 1 + 1):
            self.picks[pick_idx].grid(column=col, row=row, **TeamWidget.PICK_WIDGET_OPTIONS)
            col += TeamWidget.PICK_COLUMN_SPAN
        row += 1

        for i, pick_idx in enumerate(range(2, 4 + 1)):
            col = 2 * i
            self.picks[pick_idx].grid(column=col, row=row, **TeamWidget.PICK_WIDGET_OPTIONS)
        row += 1

        col = 1
        for pick_idx in range(5, 6 + 1):
            self.picks[pick_idx].grid(column=col, row=row, **TeamWidget.PICK_WIDGET_OPTIONS)
            col += TeamWidget.PICK_COLUMN_SPAN
        row += 1

        # Set equal weights for all columns
        for i in range(0, TeamWidget.PICKS_COLUMNS_COUNT):
            self.picks_frame.grid_columnconfigure(i, weight=1)

        # Set equal weights for all rows
        for i in range(0, row):
            self.picks_frame.grid_rowconfigure(i, weight=1)

        self.picks_frame.pack(**TeamWidget.PICKS_FRAME_OPTIONS)

        self.total_label.pack(side=tk.LEFT, padx=TeamWidget.TOTAL_PADDING)
        self.total_points.pack(side=tk.LEFT, padx=TeamWidget.TOTAL_PADDING)
        self.total_cost.pack(side=tk.LEFT, padx=TeamWidget.TOTAL_PADDING)
        self.row3.pack(pady=(TeamWidget.TOTAL_PADDING_TOP, 0), fill=tk.Y, expand=False)

    def set_team(self, team: data.Team):
        for i, pick in enumerate(team):
            self.picks[i].set_pick(pick)
        total = simulator.calculate_team_totals(team)
        self.total_points.config(text=f"{total['points']} Pts")
        self.total_cost.config(text=f"${total['cost']:.1f}M")


class MainWindow(tk.Frame):
    PADDING = 5
    WIDGETS_STICKY = tk.NSEW
    # Background color of the OptionMenus. Pass "parent" to use the background color of the parent widget.
    OPTIONMENU_BG = "white"
    # Background color of the OptionMenus when hovered over. Pass "parent" to use the background color of the parent
    # widget.
    OPTIONMENU_BG_ACTIVE = "white"
    # Border color of the OptionMenus. Pass "parent" to use the background color of the parent widget.
    OPTIONMENU_HIGHLIGHTBACKGROUND = "parent"

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        if MainWindow.OPTIONMENU_BG == "parent":
            optionmenu_bg = self["bg"]
        else:
            optionmenu_bg = MainWindow.OPTIONMENU_BG

        if MainWindow.OPTIONMENU_BG_ACTIVE == "parent":
            optionmenu_bg_active = self["bg"]
        else:
            optionmenu_bg_active = MainWindow.OPTIONMENU_BG_ACTIVE

        if MainWindow.OPTIONMENU_HIGHLIGHTBACKGROUND == "parent":
            optionmenu_highlightbackground = self["bg"]
        else:
            optionmenu_highlightbackground = MainWindow.OPTIONMENU_HIGHLIGHTBACKGROUND

        self.options_frame = tk.Frame(self, bg=self["bg"])

        self.event_year = tk.IntVar(self)
        self.event_place = tk.StringVar(self)
        self.event_mode = tk.StringVar(self)

        years = data.download_events_years()
        self.event_year.set(years[0])
        self.yom = tk.OptionMenu(self.options_frame, self.event_year, *years)
        self.event_year.trace("w", lambda name, index, mode: self.update())
        self.yom.config(bg=optionmenu_bg, highlightbackground=optionmenu_highlightbackground,
                        activebackground=optionmenu_bg_active)
        self.yom["menu"].config(bg=optionmenu_bg)

        events = data.download_events(self.event_year.get())
        self.event_place.set(next(iter(events)))
        self.pom = tk.OptionMenu(self.options_frame, self.event_place, *events.keys())
        self.event_place.trace("w", lambda name, index, mode: self.update())
        self.pom.config(bg=optionmenu_bg, highlightbackground=optionmenu_highlightbackground,
                        activebackground=optionmenu_bg_active)
        self.pom["menu"].config(bg=optionmenu_bg)

        self.event_mode.set(FANTASY_MODE[0])
        self.mom = tk.OptionMenu(self.options_frame, self.event_mode, FANTASY_MODE[0])
        self.event_mode.trace("w", lambda name, index, mode: self.update())
        self.mom.config(bg=optionmenu_bg, highlightbackground=optionmenu_highlightbackground,
                        activebackground=optionmenu_bg_active)
        self.mom["menu"].config(bg=optionmenu_bg)

        self.team_widget = TeamWidget(self, bg=self["bg"])

        self.yom.grid(row=0, column=0, sticky=MainWindow.WIDGETS_STICKY)
        self.pom.grid(row=0, column=1, sticky=MainWindow.WIDGETS_STICKY)
        self.mom.grid(row=0, column=2, sticky=MainWindow.WIDGETS_STICKY)

        self.options_frame.columnconfigure(0, weight=2)
        self.options_frame.columnconfigure(1, weight=2)
        self.options_frame.columnconfigure(2, weight=4)
        self.options_frame.pack(fill=tk.X, expand=False)

        self.team_widget.pack(fill=tk.BOTH, expand=True)

        self.pack(padx=MainWindow.PADDING, pady=MainWindow.PADDING, fill=tk.BOTH, expand=True)

        self.update()

    def update(self):
        year = self.event_year.get()
        place = self.event_place.get()
        events = data.download_events(year)
        pick_data = data.download_pick_data()
        modes = {FANTASY_MODE[0]: FANTASY_MODE[1], **data.download_event_modes(events, place=place, year=year)}
        self.mom["menu"].delete("0", tk.END)
        for mode in modes.keys():
            self.mom["menu"].add_command(label=mode, command=tk._setit(self.event_mode, mode))
        mode = modes[self.event_mode.get()]
        if mode:
            data.reset_points(pick_data)
            event_data = data.download_event_data(events, place=place, year=year,
                                                  modes=[mode])
            simulator.simulate(pick_data, event_data[mode])
            cli.print_pick_data(pick_data)

        best_team = sorted(solver.solve(pick_data), key=lambda p: (str(p.pick_type), p.cost), reverse=True)
        self.team_widget.set_team(best_team)


class App(tk.Tk):
    ICON_FILE = "res/icon.png"
    BG_COLOR = "#f8f5f2"

    def __init__(self):
        super().__init__()
        from importlib.resources import files
        icon_file = str(files("f1fantasyoptimizer").joinpath(App.ICON_FILE))
        self.title(WINDOW_TITLE)
        self.iconphoto(True, tk.PhotoImage(file=icon_file))
        self.configure(background=App.BG_COLOR)
        self.mw = MainWindow(self, bg=App.BG_COLOR)
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
