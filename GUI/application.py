from Tkinter import *
import ttk
from game import flat_matrix
from game import board
from game import affine_2d as a_2d
from game import terminals
from game import players
FlatMatrix = flat_matrix.FlatMatrix


__UI_COLORS__ = {
    board.EMPTY: 'white',
    board.YELLOW: 'yellow',
    board.RED: 'red',
}


class Application(object):

    game_board = None  # type: board.Board
    game_canvas = None  # type: Canvas
    cell_size = 0.  # type: float
    view_port = None  # type: FlatMatrix
    column_ranges = None  # type: list[list[float]]
    canvas_mouse_state = {
        'inside': False,
        'activeColumn': -1,
        'winner': board.EMPTY,
    }
    game_state = None  # type: dict

    def __init__(self, root):
        super(Application, self).__init__()
        # root = Tk()
        self.root = root

        self.control_frame = ttk.Frame(self.root, borderwidth=2, relief=RIDGE)
        self.control_frame.pack(side=RIGHT, expand=NO, fill=Y, ipadx=5, ipady=5)

        self.game_settings_frame = ttk.Labelframe(self.control_frame, text="Game Settings")
        self.game_settings_frame.pack()

        self.playing_for_label = ttk.Label(self.game_settings_frame, text="Playing For")
        self.playing_for_label.grid(row=0, column=0, sticky=W, pady=4, padx=4)
        self.playing_for = StringVar()

        self.red_radio = ttk.Radiobutton(self.game_settings_frame, text="Red", variable=self.playing_for, value="Red")
        self.red_radio.grid(row=0, column=1)
        self.red_radio = ttk.Radiobutton(self.game_settings_frame, text="Yellow", variable=self.playing_for, value="Yellow")
        self.red_radio.grid(row=0, column=2)
        self.playing_for.set("Red")

        self.rows_label = ttk.Label(self.game_settings_frame, text="Rows")
        self.rows_label.grid(row=1, column=0, sticky=W, pady=4, padx=4)

        self.rows_spinner_var = StringVar()
        self.rows_spinner = Spinbox(self.game_settings_frame, from_=5, to=12, textvariable=self.rows_spinner_var)
        self.rows_spinner_var.set("6")
        self.rows_spinner.grid(row=1, column=1, columnspan=2, sticky=W+E)

        self.columns_label = ttk.Label(self.game_settings_frame, text="Columns")
        self.columns_label.grid(row=2, column=0, sticky=W, pady=4, padx=4)

        self.columns_spinner_var = StringVar()
        self.columns_spinner = Spinbox(self.game_settings_frame, from_=5, to=12, textvariable=self.columns_spinner_var)
        self.columns_spinner_var.set("7")
        self.columns_spinner.grid(row=2, column=1, columnspan=2, sticky=W+E)

        self.line_length_label = ttk.Label(self.game_settings_frame, text="Line Length")
        self.line_length_label.grid(row=3, column=0, sticky=W, pady=4, padx=4)

        self.line_length_spinner_var = StringVar()
        self.line_length_spinner = Spinbox(self.game_settings_frame, from_=3, to=7, textvariable=self.line_length_spinner_var)
        self.line_length_spinner_var.set("4")
        self.line_length_spinner.grid(row=3, column=1, columnspan=2, sticky=W+E)

        self.checked_depth_label = ttk.Label(self.game_settings_frame, text="Checked Depth")
        self.checked_depth_label.grid(row=4, column=0, sticky=W, pady=4, padx=4)

        self.checked_depth_spinner_var = StringVar()
        self.checked_depth_spinner = Spinbox(self.game_settings_frame, from_=2, to=7, textvariable=self.checked_depth_spinner_var)
        self.checked_depth_spinner_var.set("3")
        self.checked_depth_spinner.grid(row=4, column=1, columnspan=2, sticky=W+E)

        self.space_frame = ttk.Frame(self.control_frame, height=40)
        self.space_frame.pack()

        self.control_buttons_frame = ttk.Frame(self.control_frame)
        self.control_buttons_frame.pack(fill=X)
        self.control_button_go = ttk.Button(self.control_buttons_frame, text="Go!", command=self.go_on_click)
        self.control_button_go.pack(side=RIGHT)
        # self.control_button_go.bind("<ButtonRelease-1>", self.go_on_click)
        # self.dummy_button = ttk.Button(self.control_frame)
        # self.dummy_button.pack()

        self.game_paned_window = PanedWindow(self.root, orient=VERTICAL)
        self.game_paned_window.pack(expand=YES, fill=BOTH)

        self.game_canvas = Canvas(self.game_paned_window, width=640, height=480, bg="cyan")
        self.game_canvas.bind("<Configure>", self.canvas_on_size_change)
        self.game_canvas.bind("<Motion>", self.canvas_on_motion)
        self.game_canvas.bind("<Enter>", self.canvas_on_enter)
        self.game_canvas.bind("<Leave>", self.canvas_on_leave)
        self.game_canvas.bind("<ButtonRelease-1>", self.canvas_on_button_1_release)

        self.game_paned_window.add(self.game_canvas)
        self.moves_frame = ttk.Frame(self.game_paned_window)
        self.game_paned_window.add(self.moves_frame)
        self.moves_button_frame = Frame(self.moves_frame)
        self.moves_button_frame.pack(side=TOP, expand=NO, fill=X)
        # self.forward_button = ttk.Button(self.moves_button_frame, text="Forward")
        # self.forward_button.pack(side=RIGHT)
        # self.back_button = ttk.Button(self.moves_button_frame, text="Back")
        # self.back_button.pack(side=RIGHT)
        self.moves_list = Listbox(self.moves_frame, height=10)
        self.moves_list.pack(side=BOTTOM, expand=YES, fill=BOTH)
        self.moves_list_scroll = ttk.Scrollbar(self.moves_list, orient=VERTICAL)
        self.moves_list_scroll.pack(side=RIGHT, fill=Y)
        self.moves_list_scroll.config(command=self.moves_list.yview)
        self.moves_list.config(yscrollcommand=self.moves_list_scroll.set)


    def go_on_click(self):
        self.game_board = board.Board(int(self.columns_spinner_var.get()), int(self.rows_spinner_var.get()))
        expected_in_line = int(self.line_length_spinner.get())
        minimax_depth = int(self.checked_depth_spinner.get())
        self.moves_list.delete(0, END)
        if self.playing_for.get() == "Red":
            players_list = [
                players.UIPlayer(board.RED, self.get_active_column),
                players.MiniMaxPlayer(board.YELLOW, terminals.combined_terminal, minimax_depth, expected_in_line),
            ]
        else:
            players_list = [
                players.MiniMaxPlayer(board.RED, terminals.combined_terminal, minimax_depth, expected_in_line),
                players.UIPlayer(board.YELLOW, self.get_active_column),
            ]
        self.game_state = {
            'gameStep': 0,
            'players': players_list,
            'winner': board.EMPTY,
            'expectedInLine': expected_in_line,
        }
        width = self.game_canvas.winfo_width()
        height = self.game_canvas.winfo_height()
        # print "winfo_width = {}, winfo_height = {}".format(width, height)
        self.__calc_geometry(width, height,
                             self.game_board.state.width, self.game_board.state.height)
        self.__draw_board()
        self.update_game_state()

    def canvas_on_size_change(self, event):
        canvas_width = float(event.width)
        canvas_height = float(event.height)
        if not self.game_board:
            return
        self.__calc_geometry(canvas_width, canvas_height,
                             self.game_board.state.width, self.game_board.state.height)
        self.__draw_board()

    def canvas_on_motion(self, event):
        # print "x = {}, y = {}".format(event.x, event.y)
        if not self.column_ranges:
            return
        x = float(event.x)
        # linear search is good enough for such task...
        for i, [left, right] in enumerate(self.column_ranges):
            # print "limits {}".format(limits)
            if left < x <= right:
                # print "column {}".format(i)
                self.canvas_mouse_state['activeColumn'] = i
                return
        self.canvas_mouse_state['activeColumn'] = -1

    def get_active_column(self):
        return self.canvas_mouse_state['activeColumn']

    def update_game_state(self):
        if self.game_state['winner'] != board.EMPTY:
            return
        step = self.game_state['gameStep']
        player = self.game_state['players'][step % 2]
        color = player.color
        column = player.move(self.game_board)
        if column == -1:
            return
        new_state = self.game_board.move(column, color)
        # replace = {
        #     board.EMPTY: '-',
        #     board.RED: 'r',
        #     board.YELLOW: 'y',
        # }
        # print new_state.pretty_log(replace)
        self.game_board = board.Board(state=new_state)
        win, coordinates = terminals.winner(self.game_board, self.game_state['expectedInLine'], return_coordinates=True)

        self.__draw_board()
        self.game_canvas.update()
        if win != board.EMPTY:
            self.moves_list.insert(END, "{} played on column {} and won".format(board.COLOR_NAMES[win], column + 1))
            self.game_state['winner'] = win
            self.game_state['winCoordinates'] = coordinates
            self.__draw_board()
            return
        else:
            self.moves_list.insert(END, "{} played on column {}".format(board.COLOR_NAMES[color], column + 1))
        self.moves_list.see("end")
        # self.moves_list.select_set(self.moves_list.size() - 1, self.moves_list.size() - 1)
        self.game_state['gameStep'] += 1
        self.update_game_state()



    def canvas_on_enter(self, event):
        # print "Entered"
        self.canvas_mouse_state['inside'] = True

    def canvas_on_leave(self, event):
        # print "Left"
        self.canvas_mouse_state['inside'] = False

    def canvas_on_button_1_release(self, event):
        # print "Click"
        # active_column = self.canvas_mouse_state['activeColumn']
        # if self.canvas_mouse_state['inside'] and active_column != -1:
        #     print "Clicked on Column {}".format(active_column)
        self.update_game_state()

    def __calc_geometry(self, canvas_width, canvas_height, board_width, board_height):
        canvas_width = float(canvas_width)
        canvas_height = float(canvas_height)
        board_width = float(board_width)
        board_height = float(board_height)
        # print "width = {}, height = {}".format(canvas_width, canvas_height)
        canvas_ratio = canvas_width / canvas_height
        board_ratio = board_width / board_height
        if canvas_ratio > board_ratio:
            cell_size = canvas_height / board_height
            start_point = [(canvas_width - board_width * cell_size) / 2.0, 0.0]
        else:
            cell_size = canvas_width / board_width
            start_point = [0.0, 0.0]
        # print "Start point {}".format(start_point)
        self.cell_size = cell_size
        self.view_port = a_2d.translate(start_point[0], canvas_height - start_point[1]) * a_2d.scale(1., -1.)

    def __draw_board(self):
        self.game_canvas.delete(ALL)
        if self.game_board is None:
            return
        scale = a_2d.scale(self.cell_size, self.cell_size)
        self.column_ranges = []
        for i in range(self.game_board.state.width):
            if i == 0:
                left_limit = (scale * self.view_port * a_2d.point(float(i), 0.0))[0]
            right_limit = (scale * self.view_port * a_2d.point(float(i + 1), 0.0))[0]
            self.column_ranges.append([left_limit, right_limit])
            left_limit = right_limit
        # print "column ranges = {}".format(self.column_ranges)
        for j in range(self.game_board.state.height):
            for i in range(self.game_board.state.width):
                obj_transform = scale * a_2d.translate(float(i), float(j))
                obj_view_port = obj_transform * self.view_port
                canvas_point = obj_view_port * a_2d.point(0.05, 0.05)
                x = int(canvas_point[0])
                y = int(canvas_point[1])
                second_point = obj_view_port * a_2d.point(0.95, 0.95)
                self.game_canvas.create_oval(x, y, second_point[0], second_point[1],
                                             outline='black', fill=__UI_COLORS__.get(self.game_board.state.get(i,j)),
                                             width=2)
        obj_transform = scale
        obj_view_port = obj_transform * self.view_port
        p1 = obj_view_port * a_2d.point(0,0)
        p2 = obj_view_port * a_2d.point(self.game_board.state.width,self.game_board.state.height)
        # print "p1 = {}, p2 = {}".format(p1, p2)
        self.game_canvas.create_rectangle(p1[0], p1[1], p2[0], p2[1], width=2)

        if self.game_state['winner'] != board.EMPTY:
            coordinates = self.game_state['winCoordinates']
            obj_transform = scale * a_2d.translate(0.5, 0.5)
            obj_view_port = obj_transform * self.view_port
            p1 = obj_view_port * a_2d.point(coordinates[0][0], coordinates[0][1])
            p2 = obj_view_port * a_2d.point(coordinates[-1][0], coordinates[-1][1])
            self.game_canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill='blue', width=4)


def start_app():
    root = Tk()
    Application(root)
    root.mainloop()

if __name__ == '__main__':
    start_app()