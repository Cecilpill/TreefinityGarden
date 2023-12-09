from tkinter import *
from objects.tree import Tree
import random


class Garden:
    def __init__(self, canvas):
        self.canvas = canvas

        self.canvas.bind('<Motion>', self.draw_hit_box)
        self.canvas.bind('<Button-1>', self.choose_tree)


        self.trees_pos = [(1/6, 57/63), (2/6, 59/63), (3/6, 61/63), (4/6, 59/63), (5/6, 57/63)]
        self.max_number_trees = 5
        self.trees = [None] * 5

        self.day_counter = 0
        self.day_label = None

        self.cur_season = 0
        self.days_in_season = 5
        self.seasons = ['Summer', 'Autumn', 'Winter', 'Spring']
        self.season_label = None

        self.index_cur_tree = 2

    def draw_day_counter(self):
        if self.day_label is not None:
            self.day_label.destroy()

        self.day_label = Label(self.canvas, text='Day:   ' + str(self.day_counter), font=32)
        self.day_label.place(x=self.canvas.winfo_reqwidth() - self.day_label.winfo_reqwidth() - 30, y=10)

    def draw_season(self):
        if self.season_label is not None:
            self.season_label.destroy()

        self.season_label = Label(self.canvas, text=str(self.seasons[self.cur_season]), font=32)
        self.season_label.place(x=self.canvas.winfo_reqwidth() / 2 - self.season_label.winfo_reqwidth(), y=10)

    def add_tree(self, tree):
        position = self.get_first_free_position()
        if position != -1:
            tree.pos = self.trees_pos[position]
            tree.update_hit_box()
            self.trees[position] = tree
        self.draw()
        self.next_day()

    def add_random_tree(self):
        tree = Tree(canvas=self.canvas)
        tree.load_tree_from_json('tree' + str(random.randint(1, 8)))
        self.add_tree(tree)

    def set_tree_on_position(self, tree, positon):
        if self.trees[positon] is None:
            tree.pos = self.trees_pos[positon]
            tree.update_hit_box()
            self.trees[positon] = tree
            self.draw()

    def draw(self):
        self.clean_garden()
        for tree in self.trees:
            if tree is not None:
                tree.draw()
        self.draw_day_counter()
        self.draw_season()

    def action(self, command):
        # only one manipulation with a tree in one day
        command(self.trees[self.index_cur_tree])
        self.next_day()

    def next_day(self):
        self.day_counter += 1
        if self.day_counter % self.days_in_season == 0:
            self.cur_season = (self.cur_season + 1) % len(self.seasons)
        self.draw()

    def clean_garden(self):
        # delete all stuff except background
        background = self.canvas.find_withtag('bg')
        if background:
            background_id = background[0]

            for item in self.canvas.find_all():
                if item != background_id:
                    self.canvas.delete(item)
        else:
            self.canvas.delete('all')

    def draw_hit_box(self, event):
        mouse_pos = (self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(),
                     self.canvas.winfo_pointery() - self.canvas.winfo_rooty())
        for i, tree in enumerate(self.trees):
            if tree is not None:
                if tree.check_overlapping_hix_box(mouse_pos[0], mouse_pos[1]):
                    self.canvas.create_rectangle(tree.hit_box[0], tree.hit_box[1], tree.hit_box[2],
                                             tree.hit_box[3], width=2, tags='tree_' + str(i))
                else:
                    self.canvas.delete('tree_' + str(i))

    def choose_tree(self, event):
        mouse_pos = (self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(),
                     self.canvas.winfo_pointery() - self.canvas.winfo_rooty())

        for i, tree in enumerate(self.trees):
            if tree is not None and tree.check_overlapping_hix_box(mouse_pos[0], mouse_pos[1]):
                self.index_cur_tree = i

    def get_first_free_position(self) -> int:
        for pos in range(self.max_number_trees):
            if self.trees[pos] is None:
                return pos
        return -1