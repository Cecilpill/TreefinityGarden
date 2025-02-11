from tkinter import *
import tkinter.ttk as ttk

from objects.tree import Tree
from objects.window import Window
from objects.garden import Garden
from utilities.color import COLORINGS
from utilities.json import set_tree_to_file


def create_slider(parent, update_callback, minimum, maximum, pos, initial_value, label_text, ratio=1) -> Scale:
    label = Label(parent, text=label_text)
    label.place(x=pos[0], y=pos[1] + 40)

    slider = Scale(parent, from_=minimum, to=maximum, orient='horizontal', command=update_callback,
                   variable=DoubleVar(value=initial_value), resolution=ratio, length=200)

    slider.place(x=pos[0], y=pos[1])
    return slider


def update_trunk_length(value):
    tree.trunk_length = int(value)
    garden.draw()


def update_branch_length_coefficient(value):
    tree.branch_length_coefficient = float(value)
    garden.draw()


def update_max_recursion_depth(value):
    tree.max_recursion_depth = int(value)
    garden.draw()


def update_branch_angle1(value):
    tree.branch_angle = (int(value), tree.branch_angle[1])
    garden.draw()


def update_branch_angle2(value):
    tree.branch_angle = (tree.branch_angle[0], int(value))
    garden.draw()


def update_max_branch_thickness(value):
    tree.max_branch_thickness = int(value)
    garden.draw()


def update_color_function_name(pos):
    tree.color_function_name = str(pos)
    garden.draw()


def create_file(window, name):
    cur_tree = {'branch_length_coefficient': tree.branch_length_coefficient, 'branch_angle': tree.branch_angle,
                'max_branch_thickness': tree.max_branch_thickness, 'color_function_name': tree.color_function_name}

    set_tree_to_file(cur_tree, './trees/' + name + '.txt')

    window.destroy()


def load_file(window, name):
    tree.load_tree_from_json(name)
    garden.draw()

    window.destroy()


def enter_tree_name(root):
    enter_window = Toplevel(root)
    enter_window.resizable(False, False)
    enter_window.title('Save tree')
    enter_window.iconbitmap('./sprites/icon.ico')

    x_coordinate = (root.winfo_screenwidth() - WIDTH // 3) // 2
    y_coordinate = (root.winfo_screenheight() - HEIGHT // 3) // 2
    enter_window.geometry(f'{WIDTH // 3}x{HEIGHT // 3}+{x_coordinate}+{y_coordinate}')

    entry = Entry(enter_window, font=('Arial', 12))
    entry.place(x=WIDTH / 18, y=HEIGHT / 9, width=WIDTH * 2 / 9, height=HEIGHT / 25)

    button_create = Button(enter_window, text='Save tree', command=lambda: create_file(enter_window, entry.get()))
    button_create.place(x=WIDTH / 9, y=HEIGHT * 2 / 9, width=WIDTH / 9, height=HEIGHT / 22)


def load_tree(root):
    enter_window = Toplevel(root)
    enter_window.resizable(False, False)
    enter_window.title('Load tree')
    enter_window.iconbitmap('./sprites/icon.ico')

    x_coordinate = (root.winfo_screenwidth() - WIDTH // 3) // 2
    y_coordinate = (root.winfo_screenheight() - HEIGHT // 3) // 2
    enter_window.geometry(f'{WIDTH // 3}x{HEIGHT // 3}+{x_coordinate}+{y_coordinate}')

    entry = Entry(enter_window, font=('Arial', 12))
    entry.place(x=WIDTH / 18, y=HEIGHT / 9, width=WIDTH * 2 / 9, height=HEIGHT / 25)

    button_create = Button(enter_window, text='Load tree', command=lambda: load_file(enter_window, entry.get()))
    button_create.place(x=WIDTH / 9, y=HEIGHT * 2 / 9, width=WIDTH / 9, height=HEIGHT / 22)


def change_tree_position(pos):
    position = int(pos)
    tree.pos = garden.trees_pos[position]
    garden.trees[garden.index_cur_tree], garden.trees[pos] = garden.trees[pos], garden.trees[garden.index_cur_tree]
    garden.index_cur_tree = pos
    garden.draw()


def change_season(season):
    garden.cur_season = season
    garden.draw()


def open_tool_window():
    tool_window = Toplevel(root)
    tool_window.resizable(False, False)
    tool_window.title('Tool Window')
    tool_window.iconbitmap('./sprites/icon.ico')

    x_coordinate = (root.winfo_screenwidth() - WIDTH // 2) // 2
    y_coordinate = (root.winfo_screenheight() - HEIGHT // 2) // 2
    tool_window.geometry(f'{WIDTH // 3 + 30}x{HEIGHT // 2}+{x_coordinate}+{y_coordinate}')

    slider_pos = (10, 0)
    slider_trunk_length = create_slider(parent=tool_window, minimum=0, maximum=300,
                                        update_callback=update_trunk_length, pos=(slider_pos[0], slider_pos[1]),
                                        label_text='trunk_length', initial_value=tree.trunk_length)

    slider_branch_length_coefficient = create_slider(parent=tool_window, minimum=0, maximum=1,
                                                     update_callback=update_branch_length_coefficient,
                                                     pos=(slider_pos[0], slider_pos[1] + 60),
                                                     ratio=0.005, label_text='branch_length_coefficient',
                                                     initial_value=tree.branch_length_coefficient)

    slider_max_recursion_depth = create_slider(parent=tool_window, minimum=2, maximum=15,
                                               update_callback=update_max_recursion_depth,
                                               pos=(slider_pos[0], slider_pos[1] + 120),
                                               label_text='max_recursion_depth', initial_value=tree.max_recursion_depth)

    slider_branch_angle1 = create_slider(parent=tool_window, minimum=-90, maximum=90,
                                         update_callback=update_branch_angle1, pos=(slider_pos[0], slider_pos[1] + 180),
                                         label_text='max_trunk_angle1', initial_value=tree.branch_angle[0])

    slider_branch_angle2 = create_slider(parent=tool_window, minimum=-90, maximum=90,
                                         update_callback=update_branch_angle2, pos=(slider_pos[0], slider_pos[1] + 240),
                                         label_text='max_trunk_angle1', initial_value=tree.branch_angle[1])

    slider_max_branch_thickness = create_slider(parent=tool_window, minimum=1, maximum=20,
                                                update_callback=update_max_branch_thickness,
                                                pos=(slider_pos[0], slider_pos[1] + 300),
                                                label_text='max_trunk_angle1', initial_value=tree.max_branch_thickness)

    combobox_color_pos = (250, 25)
    combobox_color = ttk.Combobox(tool_window, values=list(COLORINGS.keys()))
    combobox_color.set(tree.color_function_name)
    combobox_color.place(x=combobox_color_pos[0], y=combobox_color_pos[1])
    combobox_color.bind('<<ComboboxSelected>>', lambda event: update_color_function_name(combobox_color.get()))
    label_combobox_color = Label(tool_window, text='combobox_color')
    label_combobox_color.place(x=combobox_color_pos[0], y=combobox_color_pos[1] - 25)

    cur_tree_pos = IntVar()
    radiobutton_tree_pos = (250, 60)
    r_position_0 = Radiobutton(tool_window, text='Position 0', variable=cur_tree_pos, value=0,
                               command=lambda: change_tree_position(cur_tree_pos.get()))
    r_position_0.place(x=radiobutton_tree_pos[0], y=radiobutton_tree_pos[1])

    r_position_1 = Radiobutton(tool_window, text='Position 1', variable=cur_tree_pos, value=1,
                               command=lambda: change_tree_position(cur_tree_pos.get()))
    r_position_1.place(x=radiobutton_tree_pos[0], y=radiobutton_tree_pos[1] + 30)

    r_position_2 = Radiobutton(tool_window, text='Position 2', variable=cur_tree_pos, value=2,
                               command=lambda: change_tree_position(cur_tree_pos.get()))
    r_position_2.place(x=radiobutton_tree_pos[0], y=radiobutton_tree_pos[1] + 60)

    r_position_3 = Radiobutton(tool_window, text='Position 3', variable=cur_tree_pos, value=3,
                               command=lambda: change_tree_position(cur_tree_pos.get()))
    r_position_3.place(x=radiobutton_tree_pos[0], y=radiobutton_tree_pos[1] + 90)

    r_position_4 = Radiobutton(tool_window, text='Position 4', variable=cur_tree_pos, value=4,
                               command=lambda: change_tree_position(cur_tree_pos.get()))
    r_position_4.place(x=radiobutton_tree_pos[0], y=radiobutton_tree_pos[1] + 120)

    match garden.index_cur_tree:
        case 0:
            r_position_0.select()
        case 1:
            r_position_1.select()
        case 2:
            r_position_2.select()
        case 3:
            r_position_3.select()
        case 4:
            r_position_4.select()

    cur_season = IntVar()
    radiobutton_season = (350, 60)
    r_summer = Radiobutton(tool_window, text='Summer', variable=cur_season, value=0,
                           command=lambda: change_season(cur_season.get()))
    r_summer.place(x=radiobutton_season[0], y=radiobutton_season[1])

    r_autumn = Radiobutton(tool_window, text='Autumn', variable=cur_season, value=1,
                           command=lambda: change_season(cur_season.get()))
    r_autumn.place(x=radiobutton_season[0], y=radiobutton_season[1] + 30)

    r_winter = Radiobutton(tool_window, text='Winter', variable=cur_season, value=2,
                           command=lambda: change_season(cur_season.get()))
    r_winter.place(x=radiobutton_season[0], y=radiobutton_season[1] + 60)

    r_spring = Radiobutton(tool_window, text='Spring', variable=cur_season, value=3,
                           command=lambda: change_season(cur_season.get()))
    r_spring.place(x=radiobutton_season[0], y=radiobutton_season[1] + 90)

    match garden.cur_season:
        case 0:
            r_summer.select()
        case 1:
            r_autumn.select()
        case 2:
            r_winter.select()
        case 3:
            r_spring.select()


root = Tk()
root.resizable(False, False)
root.iconbitmap('./sprites/icon.ico')
root.title('DEV APP')
WIDTH = 1280
HEIGHT = 720

window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT],
                path_background_img='./sprites/backgrounds/window_background.png',
                canvases=[{'name': 'garden',
                           'coords': (WIDTH / 64, WIDTH / 64, WIDTH - WIDTH / 64, HEIGHT - HEIGHT / 8),
                           'bg': 'blue',
                           'bg_picture': './sprites/backgrounds/summer_background.png'}])

garden = Garden(canvas=window.inner_canvases['garden'])

tree = Tree(canvas=window.inner_canvases['garden'],
            pos=(0, 0),
            trunk_length=100, trunk_angle=90, branch_angle=(30, 60), branch_length_coefficient=0.7,
            max_recursion_depth=7, min_branch_thickness=1,
            max_branch_thickness=4, color_function_name='natural_coloring')

garden.set_tree_on_position(tree, 2)
garden.index_cur_tree = 2
garden.draw()

buttons_pos = (320, 666)
save_button = Button(window.canvas, text='save tree', command=lambda: enter_tree_name(root))
save_button.place(x=buttons_pos[0] - WIDTH * 5 / 64, y=buttons_pos[1], width=WIDTH * 5 / 32, height=HEIGHT / 17)
save_button.config(font=("Arial", 14))

load_button = Button(window.canvas, text='load tree', command=lambda: load_tree(root))
load_button.place(x=buttons_pos[0] - WIDTH * 5 / 64 + 320, y=buttons_pos[1], width=WIDTH * 5 / 32, height=HEIGHT / 17)
load_button.config(font=("Arial", 14))

open_tool_window_button = Button(window.canvas, text='open tool window', command=lambda: open_tool_window())
open_tool_window_button.place(x=buttons_pos[0] - WIDTH * 5 / 64 + 640, y=buttons_pos[1], width=WIDTH * 5 / 32,
                              height=HEIGHT / 17)
open_tool_window_button.config(font=("Arial", 14))

window.canvas.pack()
root.mainloop()
