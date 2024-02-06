import curses
from markdownify import markdownify

selected = 0

def set_status_text(status_w: curses.window, text: str):
    status_w.clear()
    status_w.addstr(0, 0, text, curses.A_REVERSE)
    status_w.chgat(-1, curses.A_REVERSE)

def display_menu(menu_items: list[str], window: curses.window, selected: int):
    index = 0
    window.clear()
    window.chgat(-1, curses.A_REVERSE)
    for i in range(selected, len(menu_items)):
        attr = 0
        if i == selected:
            attr = curses.A_REVERSE
        window.addstr(index, 0, menu_items[i].title, attr)
        index += 1


def ui_init(categories: list, total_unread: int):
    global selected

    stdscr = curses.initscr()
    # curses.start_color()
    # curses.can_change_color()
    # curses.use_default_colors()

    stdscr.clear()
    stdscr.nodelay(1)
    curses.noecho()
    stdscr.keypad(1)
    curses.cbreak()
    curses.curs_set(0)

    win_height, win_width = stdscr.getmaxyx()
    status_w = curses.newwin(1, win_width, win_height - 2, 0)

    display_menu(categories, stdscr, selected)
    set_status_text(status_w, f"{categories[selected].unread}")

    stdscr.refresh()
    status_w.refresh()

    while True:
        ch = stdscr.getch()
        if ch == ord('q'):
            exit(0)
        elif ch == ord('j') and selected < len(categories) - 1:
            selected += 1
            display_menu(categories, stdscr, selected)
            set_status_text(status_w, f"{categories[selected].unread}")
            stdscr.refresh()
            status_w.refresh()

        elif ch == ord('k') and selected > 0:
            selected -= 1
            display_menu(categories, stdscr, selected)
            set_status_text(status_w, f"{categories[selected].unread}")
            stdscr.refresh()
            status_w.refresh()

        elif ch == 10 or ch == 13:
            category_ind = selected

            stdscr.clear()
            display_menu(categories[selected].entries, stdscr, selected)
            selected = 0
            set_status_text(status_w, f"there SHOULD BE info about currently selected entry")
            stdscr.refresh()
            status_w.refresh()
            
            while True:
                ch = stdscr.getch()
                if ch == ord('q'):
                    exit(0)
                elif ch == ord('j') and selected < len(categories[category_ind].entries) - 1:
                    selected += 1
                    display_menu(categories[category_ind].entries, stdscr, selected)
                    stdscr.refresh()
                    status_w.refresh()

                elif ch == ord('k') and selected > 0:
                    selected -= 1
                    display_menu(categories[category_ind].entries, stdscr, selected)
                    stdscr.refresh()
                    status_w.refresh()

                elif ch == 10 or ch == 13:
                    stdscr.clear()
                    lines = markdownify(categories[category_ind].entries[selected].content).split("\n")
                    for i in range(len(lines)):
                        if i < win_height:
                            stdscr.addstr(i, 0, lines[i])
                        else: break
                    stdscr.refresh()


    curses.endwin()
