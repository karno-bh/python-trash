from Tkinter import *
import ttk
from game import flat_matrix
from game import board
FlatMatrix = flat_matrix.FlatMatrix


class UIBoard(object):

    def __init__(self, game_board):
        # type: (board.Board) -> None
        self.game_board = game_board
        self.ui_board_state = FlatMatrix(game_board.state.width, game_board.state.height, initial_val=None)
        pass


class Application(object):

    ui_board = None # type: FlatMatrix
    game_board = None # type: board.Board
    game_canvas = None # type: Canvas

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
        self.red_radio = ttk.Radiobutton(self.game_settings_frame, text="Red", variable = self.playing_for, value="Red")
        self.red_radio.grid(row=0, column=1)
        self.red_radio = ttk.Radiobutton(self.game_settings_frame, text="Yellow", variable=self.playing_for, value="Yellow")
        self.red_radio.grid(row=0, column=2)
        self.playing_for.set("Red")
        self.rows_label = ttk.Label(self.game_settings_frame, text="Rows")
        self.rows_label.grid(row=1, column=0, sticky=W, pady=4, padx=4)
        self.rows_spinner = Spinbox(self.game_settings_frame, from_=5, to=10)
        self.rows_spinner.grid(row=1, column=1, columnspan=2, sticky=W+E)
        self.columns_label = ttk.Label(self.game_settings_frame, text="Columns")
        self.columns_label.grid(row=2, column=0, sticky=W, pady=4, padx=4)
        self.columns_spinner = Spinbox(self.game_settings_frame, from_=5, to=10)
        self.columns_spinner.grid(row=2, column=1, columnspan=2, sticky=W+E)
        self.line_length_label = ttk.Label(self.game_settings_frame, text="Line Length")
        self.line_length_label.grid(row=3, column=0, sticky=W, pady=4, padx=4)
        self.line_length_spinner = Spinbox(self.game_settings_frame, from_=3, to=6)
        self.line_length_spinner.grid(row=3, column=1, columnspan=2, sticky=W+E)
        self.checked_depth_label = ttk.Label(self.game_settings_frame, text="Checked Depth")
        self.checked_depth_label.grid(row=4, column=0, sticky=W, pady=4, padx=4)
        self.checked_depth_spinner = Spinbox(self.game_settings_frame, from_=1, to=6)
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
        self.game_paned_window.add(self.game_canvas)
        self.moves_frame = ttk.Frame(self.game_paned_window)
        self.game_paned_window.add(self.moves_frame)
        self.moves_button_frame = Frame(self.moves_frame)
        self.moves_button_frame.pack(side=TOP, expand=NO, fill=X)
        self.forward_button = ttk.Button(self.moves_button_frame, text="Forward")
        self.forward_button.pack(side=RIGHT)
        self.back_button = ttk.Button(self.moves_button_frame, text="Back")
        self.back_button.pack(side=RIGHT)
        self.moves_list = Listbox(self.moves_frame, height=10)
        self.moves_list.pack(side=BOTTOM, expand=YES, fill=BOTH)
        self.moves_list_scroll = ttk.Scrollbar(self.moves_list, orient=VERTICAL)
        self.moves_list_scroll.pack(side=RIGHT, fill=Y)
        self.moves_list_scroll.config(command=self.moves_list.yview)
        self.moves_list.config(yscrollcommand=self.moves_list_scroll.set)
        for x in range(100):
            self.moves_list.insert(END, str(x))


    def go_on_click(self):
        # print "Event {}".format(event)
        self.game_board = board.Board()
        self.ui_board = FlatMatrix(self.game_board.state.width, self.game_board.state.height, initial_val=None)
        pass

    def canvas_on_size_change(self, event):
        canvas_width = float(event.width)
        canvas_height = float(event.height)
        game_width = 6.0
        game_height = 7.0
        cell_size, start_point = self.__calc_geometry(canvas_width, canvas_height, game_width, game_height)
        pass

    def __calc_geometry(self, canvas_width, canvas_height, board_width, board_height):
        canvas_width = float(canvas_width)
        canvas_height = float(canvas_height)
        canvas_ratio = canvas_width / canvas_height
        board_ratio = board_width / board_height
        if canvas_ratio > board_ratio:
            cell_size = canvas_height / board_height
            start_point = ((canvas_width - board_width * cell_size) / 2, 0)
        else:
            cell_size = canvas_width / board_width
            start_point = (0, 0)
        # print "Cell Size {}, Start Point {}".format(cell_size, start_point)
        return cell_size, start_point

    def __draw_board(self, cell_size, start_point):
        if self.ui_board is None:
            return
        radius = cell_size * 0.95
        x = start_point[0] + cell_size / 2
        y = start_point[1] + cell_size / 2
        for j in range(self.ui_board.height - 1, -1, -1):
            for i in range(self.ui_board.width):
                x += cell_size
            y += cell_size




if __name__ == '__main__':
    root = Tk()
    Application(root)
    root.mainloop()