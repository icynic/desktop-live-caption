import time
import tkinter as tk
import threading


class Window:
    def __init__(self, window_size_x: int = 640, window_size_y: int = 108, transparency: float = 0.65, _reference=None):
        """
        A GUI to display text
        :param window_size_x: initial window width.
        :param window_size_y: initial window height
        :param transparency: window transparency
        :param _reference: `self` will be passed to this parameter

        Use `Window()` or `run_in_another_thread()` to initialize.
        Then call `insert_at_end()` on its instance.
        """
        self.root = tk.Tk()
        # Set window size and position
        window_position_x = (self.root.winfo_screenwidth() - window_size_x) // 2
        window_position_y = self.root.winfo_screenheight() - window_size_y - 50
        self.root.geometry(f"{window_size_x}x{window_size_y}+{window_position_x}+{window_position_y}")
        # Hide the title bar
        self.root.overrideredirect(True)
        # Make the window always on top
        self.root.attributes('-topmost', True)

        self.root.configure(bg="white", pady=1, padx=1)
        self.root.attributes("-alpha", transparency)

        # Enable dragging arcoss the entire window
        self.mouse_press_position_x = 0
        self.mouse_press_position_y = 0
        self.root.bind("<Button-1>", self.press)
        self.root.bind("<B1-Motion>", self.drag)

        # Double click to change the state
        self.root.bind("<Double-Button-1>", self.double_click)
        self.is_double_click_state = False
        self.transparency = transparency

        # Text field
        self.text_field = tk.Text(self.root, wrap=tk.WORD, padx=10, pady=10, font=("Verdana", 14), foreground="white",
                                  background="black", selectbackground="black")
        self.text_field.pack(fill=tk.BOTH, expand=True)
        self.text_field.insert(tk.END, "Ready to transcribe")

        # Enable resizing via the handle
        self.resize_handle = tk.Label(self.root, text="▼", cursor="size_ns", background="black", foreground="white")
        self.resize_handle.place(relx=1.0, rely=1.0, anchor="se")
        self.resize_handle.bind("<B1-Motion>", self.resize)
        # Disable dragging while resizing
        self.resize_handle.bind("<Button-1>", self.resize_handle_press)
        self.resize_handle.bind("<ButtonRelease-1>", self.resize_handle_release)

        # Closing buttion
        self.close_button = tk.Label(self.root, text="x", foreground="white", background="black", padx=3,
                                     font=("Comic Sans MS", 14))
        self.close_button.place(relx=1.0, rely=0.0, anchor="ne")
        self.close_button.bind("<Button-1>", self.close)

        # Pass its own reference via parameter
        if _reference:
            _reference[0] = self

        self.is_transcribing = False
        self.is_closed = False
        self.root.mainloop()

    def press(self, event: tk.Event):
        self.mouse_press_position_x = event.x
        self.mouse_press_position_y = event.y

    def drag(self, event: tk.Event):
        self.root.geometry(
            f"+{event.x_root - self.mouse_press_position_x}+{event.y_root - self.mouse_press_position_y}")

    def resize_handle_press(self, event: tk.Event):
        self.root.unbind("<B1-Motion>")

    def resize_handle_release(self, event: tk.Event):
        if not self.is_double_click_state:
            self.root.bind("<B1-Motion>", self.drag)

    def resize(self, event: tk.Event):
        new_size_x = self.root.winfo_width() + event.x - self.mouse_press_position_x
        new_size_y = self.root.winfo_height() + event.y - self.mouse_press_position_y
        # Prevent negative size
        if new_size_x > 0 and new_size_y > 0:
            self.root.geometry(f"{new_size_x}x{new_size_y}")

    def close(self, event: tk.Event):
        self.is_closed = True
        self.root.destroy()

    def double_click(self, event: tk.Event):
        # Enter double click state
        if not self.is_double_click_state:
            # Zero transparency
            self.root.attributes("-alpha", 1)
            # Diable dragging
            self.root.unbind("<B1-Motion>")
            # Change state
            self.is_double_click_state = not self.is_double_click_state
            # Cancel text selection
            self.text_field.tag_remove(tk.SEL, "1.0", "end")
            # Display text selection
            self.text_field.config(selectbackground="blue")

        else:  # Quit double click state
            self.root.attributes("-alpha", self.transparency)
            self.root.bind("<B1-Motion>", self.drag)
            self.is_double_click_state = not self.is_double_click_state
            self.text_field.config(selectbackground="black")

    def insert_at_end(self, text: str):
        if not self.is_transcribing:
            self.text_field.delete("1.0", tk.END)
            self.is_transcribing = True
        if text:
            self.text_field.insert(tk.END, text)
            self.text_field.see(tk.END)


def run_in_another_thread() -> Window:
    # A hack to get the Window object which lives in a seperate thread
    reference = [None]
    threading.Thread(target=Window, kwargs={"_reference": reference}).start()
    # Wait for the Window object's initialization
    while not reference[0]:
        time.sleep(0.1)
    return reference[0]


if __name__ == '__main__':
    window = Window()
    # window = run_in_another_thread()
