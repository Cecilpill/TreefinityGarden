rom tkinter import Tk, Canvas

def run_achievements():
    root = Tk()
    root.iconbitmap('./sprites/icon.ico')
    root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

    WIDTH = 420
    HEIGHT = 720
    x_coordinate = (root.winfo_screenwidth() - WIDTH) // 2
    y_coordinate = (root.winfo_screenheight() - HEIGHT) // 2

    root.geometry(f'{WIDTH}x{HEIGHT}+{x_coordinate}+{y_coordinate}')
    root.title('Achievements')

    # Creating a canvas for background and achievements
    canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='lightgray')
    canvas.pack()

achievements = [
    "Grew your first tree",
    "Grew your third tree",

]


    num_achievements = 10  # example number of achievements
    for i in achievements enumerate():
        canvas.create_rectangle(50, 30 + i*60, 150, 80 + i*60, fill='darkgrey', outline='black')

    root.mainloop()

