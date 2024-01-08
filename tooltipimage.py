import time
import tkinter as tk
from typing import Any, Callable
from PIL import Image, ImageTk

# This code is based on Ioannis Nikiteas, tkinter-tooltip, licensed under an MIT License; https://github.com/gnikit/tkinter-tooltip
# The original code has been modified to add an image to the tooltip

class ToolTipImage(tk.Toplevel):
    """
    Creates a ToolTip (pop-up) widget for tkinter
    """

    def __init__(
        self,
        widget: tk.Widget,
        msg: str | list[str] | Callable[[], str | list[str]],
        image_path: str = None,  # New parameter
        image_size: tuple[int, int] = None,  # New parameter
        delay: float = 0.0,
        follow: bool = True,
        refresh: float = 1.0,
        x_offset: int = +10,
        y_offset: int = +10,
        parent_kwargs: dict[Any, Any] = {"bg": "black", "padx": 1, "pady": 1},
        **message_kwargs: Any,
    ):
        self.widget = widget
        tk.Toplevel.__init__(self, **parent_kwargs)
        self.withdraw() 
        self.overrideredirect(True)

        self.msgVar = tk.StringVar()
        self.msg = msg
        self.delay = delay
        self.follow = follow
        self.refresh = refresh
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.status = "outside"
        self.last_moved = 0

        ###! This is added - Load the image if an image path is provided
        self.image = None
        if image_path is not None:
            image = Image.open(image_path)
            if image_size is not None:
                image = image.resize(image_size)
            self.image = ImageTk.PhotoImage(image)

        ###! Label intstead of Message widget
        label = tk.Label(self, textvariable=self.msgVar, image=self.image, **message_kwargs)
        label.grid()

        # Add bindings to the widget without overriding the existing ones
        self.widget.bind("<Enter>", self.on_enter, add="+")
        self.widget.bind("<Leave>", self.on_leave, add="+")
        self.widget.bind("<Motion>", self.on_enter, add="+")
        self.widget.bind("<ButtonPress>", self.on_leave, add="+")

    def on_enter(self, event) -> None:
        self.last_moved = time.time()
        if self.status == "outside":
            self.status = "inside"
        if not self.follow:
            self.status = "inside"
            self.withdraw()
        self.geometry(f"+{event.x_root + self.x_offset}+{event.y_root + self.y_offset}")
        self.after(int(self.delay * 1000), self._show)

    def on_leave(self, event=None) -> None:
        self.status = "outside"
        self.withdraw()

    def _show(self) -> None:
        if self.status == "inside" and time.time() - self.last_moved > self.delay:
            self.status = "visible"
        if self.status == "visible":
            if callable(self.msg):
                self.msgVar.set(self.msg())
            elif isinstance(self.msg, str):
                self.msgVar.set(self.msg)
            elif isinstance(self.msg, list):
                self.msgVar.set("\n".join(self.msg))
            self.deiconify()
            self.after(int(self.refresh * 1000), self._show)
