#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Saylenty'

import numpy
from time import sleep
from tkinter import Tk, Canvas, Button, Frame, BOTH, TclError

cont_flag = True
cell_size = 20


class Visual(object):
    def __init__(self, win_width, win_height, board):
        self.__win_width = win_width
        self.__win_height = win_height
        self.__root = Tk()
        self.__root.wm_title("Game of Life")
        self.__config_string = "{0}x{1}".format(win_width + 5, win_height + 32)
        self.__root.geometry(self.__config_string)
        self.__add_canvas()
        self.__add_frame()
        self._add_buttons(board)

    def __add_canvas(self):
        self.__canvas = Canvas(self.__root, height=self.__win_height)
        self.__canvas.pack(fill=BOTH)

    def __add_frame(self):
        self.__frame = Frame(self.__root)
        self.__frame.pack(side='bottom')

    def _add_buttons(self, board):
        Button(self.__frame, text='Step', command=lambda: step(self, board)).pack(side='left')
        Button(self.__frame, text='Start', command=lambda: start(lambda: auto_step(self, board))).pack(side='left')
        Button(self.__frame, text='Stop', command=lambda: stop()).pack(side='left')
        Button(self.__frame, text='Clear', command=self.clear).pack(side='right')

    def run(self):
        self.__root.mainloop()

    def draw_grid(self):
        for i in range(cell_size, self.__win_height + 1, cell_size):
            line = self.__canvas.create_line(0, i, self.__win_width, i, fill="grey")
            self.__canvas.itemconfig(line, tags='grid')
        for i in range(cell_size, self.__win_width + 1, cell_size):
            line = self.__canvas.create_line(i, 0, i, self.__win_height, fill="grey")
            self.__canvas.itemconfig(line, tags='grid')

    def draw_matrix(self, matrix, color='blue'):
        for i in range(matrix.shape[0]):  # row
            for j in range(matrix.shape[1]):  # coll
                if matrix[i, j]:
                    live_elem = self.__canvas.create_rectangle(j * cell_size + 2, i * cell_size + 2,
                                                               cell_size + cell_size * j - 2,
                                                               cell_size + cell_size * i - 2, fill=color)
                    self.__canvas.itemconfig(live_elem, tags='live_elem')

    def draw_list(self, lst, color='blue'):
        for i, j in lst:
            live_elem = self.__canvas.create_rectangle(j * cell_size + 2, i * cell_size + 2,
                                                       cell_size + cell_size * j - 2,
                                                       cell_size + cell_size * i - 2, fill=color)
            self.__canvas.itemconfig(live_elem, tags='live_elem')

    def clear(self, item='live_elem'):
        self.__canvas.delete(item)

    def canvas_update(self):
        self.__canvas.update()


def get_neighbors(cell):  # Функция возвращает массив координат соседей для точки
    x, y = cell
    neighbors = [(x + i, y + j)
                 for i in range(-1, 2)
                 for j in range(-1, 2)
                 if not i == j == 0]
    return neighbors


def count_alive_neighbors(board, dot):
    return len(
        tuple(filter(lambda x: x if is_correct_con(board.shape[0], x) and board[x] else False, get_neighbors(dot))))


def fill_board(board, alive_cons):
    for i in alive_cons:
        board[i] = 1


def is_correct_con(size, con):
    x, y = con
    return all(0 <= coord <= size - 1 for coord in [x, y])


def generate_new_generation(board):
    die, born = [], []
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] and (count_alive_neighbors(board, (i, j)) < 2
                                or count_alive_neighbors(board, (i, j)) > 3):  # Если живая клетка
                die.append((i, j))  # Умрет в следующем поколении
            elif not board[i, j] and count_alive_neighbors(board, (i, j)) == 3:  # Если мертвая клетка
                born.append((i, j))  # Рождается в следующем поколении
    for i in die: board[i] = 0
    for i in born: board[i] = 1
    return die, born


def glue_matrix_v(top_matrix, bottom_matrix):
    for i in range(bottom_matrix[0].size):
        if bottom_matrix[0, i] == 1 and top_matrix[1, i] != 1:
            top_matrix[top_matrix.shape[1] - 1, i] = 1
    return numpy.concatenate((top_matrix, bottom_matrix[1:]))


def step(visual, board, color='blue'):
    dead, born = generate_new_generation(board)
    visual.clear()
    visual.draw_matrix(board, color)
    #visual.draw_list(dead, 'red')
    #visual.draw_list(born, 'green')
    visual.canvas_update()


def stop():
    global cont_flag
    cont_flag = False


def start(func):
    global cont_flag
    cont_flag = True
    func()


def auto_step(visual, board, color='blue', time=0.05):
    try:
        while cont_flag:
            step(visual, board, color)
            sleep(time)
    except TclError:
        pass


def main():
    size = 38  # Размер игрового поля
    board = numpy.matrix([numpy.zeros(size, dtype=int) for i in range(size)], dtype=int)  # Инициализуем игровое поле
    # -------------------Начальные конфигурации------------------------
    alive_cells = [  # Glider gun (size => 38)
                     (5, 1), (5, 2), (6, 1), (6, 2),
                     (5, 11), (6, 11), (7, 11), (4, 12), (8, 12), (3, 13), (9, 13), (3, 14), (9, 14), (6, 15), (4, 16),
                     (8, 16),
                     (5, 17), (6, 17), (7, 17), (6, 18),
                     (3, 21), (4, 21), (5, 21), (3, 22), (4, 22), (5, 22), (2, 23), (6, 23), (1, 25), (2, 25), (6, 25),
                     (7, 25),
                     (3, 35), (4, 35), (3, 36), (4, 36)
    ]
    #alive_cells = [(i, j) for i in range(25) for j in range(1, 25) if i % 3 and j % 3]  # Virus  - generate main board
    #alive_cells.append((12, 11))  # Virus (size = 25) - put the virus inside
    #size = 25
    #alive_cells = [(1, 2), (2, 3), (3, 1), (3, 2), (4, 0)]  # Умирают
    #alive_cells = [(2, 1), (2, 2), (2, 3)]  # Бесконечно (крест)
    #alive_cells = [(1, 2), (2, 1), (2, 3), (3, 2), (1,6), (1,7), (2,6), (2,7)]  # Не изменяются (ромб + куб)
    # -----------------------------------------------------------------
    fill_board(board, alive_cells)

    win_width = cell_size * size if cell_size * size < 1260 else 1260
    win_height = cell_size * size if cell_size * size < 660 else 660

    v = Visual(win_width, win_height, board)
    v.draw_grid()
    v.draw_matrix(board)
    #v.draw_list([(12, 11)], color='red')
    v.canvas_update()
    v.run()

if __name__ == '__main__':
    main()
