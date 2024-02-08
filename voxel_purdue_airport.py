import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

class InteractiveGrid:
    def __init__(self, image_path, grid_size=10):
        self.root = tk.Tk()
        self.grid_size = grid_size
        self.original_image = Image.open(image_path)
        self.image = self.original_image.copy()
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self.root, width=self.image.width, height=self.image.height)
        self.canvas.pack()
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.click_grid)

    def draw_grid(self):
        for x in range(0, self.image.width, self.grid_size):
            for y in range(0, self.image.height, self.grid_size):
                self.canvas.create_rectangle(x, y, x + self.grid_size, y + self.grid_size, outline='blue')

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def click_grid(self, event):
        x, y = event.x - event.x % self.grid_size, event.y - event.y % self.grid_size
        draw = ImageDraw.Draw(self.image)
        draw.rectangle([x, y, x + self.grid_size, y + self.grid_size], fill='green', outline='blue')
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def run(self):
        self.root.mainloop()

# Replace 'purduemapview.png' with the path to your image file
interactive_grid = InteractiveGrid('purduemapview.png', grid_size=50)  # Adjust grid_size as needed
interactive_grid.run()
