from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename



class Text_redactor(Tk):
    normal_width = 800
    normal_height = 800
    x_offset = 540
    y_offset = 100
    version = "1.1"
    fonts = ["Arial", "Times", "Courier", "Helvetica"] # standart font's for unix and windows
    font_size = ['6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
                 '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
                 '41', '42', '43', '44', '45', '46']
    current_font = 0
    current_font_size = 6

    def __init__(self):
        super().__init__()
        self.settings_close_button = None
        self.frame_button = None
        self.frame_combobox = None
        self.combobox_fonts = None
        self.combobox_font_size = None

        self.settings = None
        self.settings_confirm_button = None

        self.internal_buffer = ""

        self.menu_bar = Menu(self)
        self.menu_tab_file = Menu(self.menu_bar)
        self.menu_tab_text = Menu(self.menu_bar)
        self.scroll_bar_y = Scrollbar(self)
        self.text_field = Text(self)

        self.draw_window()
        self.mainloop()

    def draw_window(self):
        self.title(f"Text Redactor v_{Text_redactor.version}")
        self.geometry(
            f"{Text_redactor.normal_width}x{Text_redactor.normal_height}+{Text_redactor.x_offset}+{Text_redactor.y_offset}")
        self.config(menu=self.menu_bar)

        self.menu_tab_file.add_command(label="Open file", underline=0, command=self.open_file)
        self.menu_tab_file.add_command(label="Save as...", underline=0, command=self.save_file_as)
        self.menu_tab_file.add_separator()
        self.menu_tab_file.add_command(label="Settings", underline=1, command=self.open_settings_window)
        self.menu_tab_file.add_separator()
        self.menu_tab_file.add_command(label="Exit", underline=1, command=self.quit_program)

        self.menu_tab_text.add_command(label="Clear all", underline=1, command=self.clear_text_field)
        self.menu_tab_text.add_separator()
        self.menu_tab_text.add_command(label="Copy to internal", command=self.copy_to_internal_buf)
        self.menu_tab_text.add_command(label="Paste from internal", command=self.paste_internal_buffer)

        self.menu_bar.add_cascade(label="File", underline=0, menu=self.menu_tab_file)
        self.menu_bar.add_cascade(label="Text", menu=self.menu_tab_text)

        self.text_field.config(wrap=WORD, yscrollcommand=self.scroll_bar_y.set, bg="grey88",
                               font=Text_redactor.fonts[Text_redactor.current_font] + " " + Text_redactor.font_size[
                                        Text_redactor.current_font_size])
        self.text_field.bind("<FocusIn>", self.change_focus)
        self.text_field.bind("<FocusOut>", self.change_focus)
        self.text_field.bind("<Control-C>", self.bind_copy_to_internal_buf)
        self.text_field.bind("<Control-V>", self.bind_paste_internal_buffer)
        self.scroll_bar_y.config(command=self.text_field.yview)

        self.scroll_bar_y.pack(side=RIGHT, fill=Y, pady=1, padx=1)
        self.text_field.pack(side=RIGHT, fill=BOTH, expand=1)

    def open_settings_window(self):
        self.settings = Toplevel()
        self.settings.title("Settings")
        self.settings.geometry("250x250")
        self.frame_combobox = Frame(self.settings, width=20)
        self.frame_button = Frame(self.settings, width=20)
        self.settings_confirm_button = Button(self.frame_button, text="Confirm", command=self.update_settings)
        self.settings_close_button = Button(self.frame_button, text="Close", command=self.close_settings)
        self.combobox_fonts = ttk.Combobox(self.frame_combobox, width=9, values=Text_redactor.fonts)
        self.combobox_font_size = ttk.Combobox(self.frame_combobox, width=5, values=Text_redactor.font_size)
        self.combobox_fonts.current(Text_redactor.current_font)
        self.combobox_font_size.current(Text_redactor.current_font_size)

        self.frame_combobox.pack(anchor="nw", padx=7, pady=7)
        self.combobox_fonts.pack(side=LEFT)
        self.combobox_font_size.pack(side=RIGHT)
        self.frame_button.pack(side=BOTTOM)
        self.settings_confirm_button.pack(side=LEFT)
        self.settings_close_button.pack(side=RIGHT)

    def update_settings(self):
        Text_redactor.current_font = self.combobox_fonts.current()
        Text_redactor.current_font_size = self.combobox_font_size.current()
        self.text_field["font"] = Text_redactor.fonts[Text_redactor.current_font] + " " + Text_redactor.font_size[
                    Text_redactor.current_font_size]

    def close_settings(self):
        self.settings.destroy()

    def change_focus(self, event):
        if event.type == "9":
            event.widget["bg"] = "white"
        if event.type == "10":
            event.widget["bg"] = "grey88"

    def bind_copy_to_internal_buf(self, event):
        try:
            self.internal_buffer = event.widget.get(SEL_FIRST, SEL_LAST)
        except Exception as ex:
            print("Can't copy this")
            print(ex)

    def bind_paste_internal_buffer(self, event):
        try:
            event.widget.insert("insert", self.internal_buffer)
        except Exception as ex:
            print("Can't paste this")
            print(ex)

    def copy_to_internal_buf(self):
        try:
            self.internal_buffer = self.text_field.get(SEL_FIRST, SEL_LAST)
        except Exception as ex:
            print("Can't copy this")
            print(ex)

    def paste_internal_buffer(self):
        try:
            self.text_field.insert("insert", self.internal_buffer)
        except Exception as ex:
            print("Can't paste this")
            print(ex)

    def open_file(self):
        filepath_open = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*")])
        if not filepath_open:
            return
        self.text_field.delete("1.0", END)
        try:
            with open(filepath_open, 'r') as file:
                text = file.read()
                self.text_field.insert(END, text)
        except Exception as ex:
            show_message_box(messagebox.showerror, "Unknown error", "Something went wrong\n:(\nSee at terminal")
            print(ex)
        self.title(f"Text Redactor v_{Text_redactor.version}|{filepath_open}")

    def save_file_as(self):
        filepath_save = asksaveasfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*")])
        if not filepath_save:
            return
        try:
            with open(filepath_save, 'w') as file:
                text = self.text_field.get("1.0", END)
                file.write(text)
        except Exception as ex:
            show_message_box(messagebox.showerror, "Unknown error", "Something went wrong\n:(\nSee at terminal")
            print(ex)
        self.title(f"Text Redactor v_{Text_redactor.version}|{filepath_save}")

    def clear_text_field(self):
        self.text_field.delete("1.0", END)
        self.title(f"Text Redactor v_{Text_redactor.version}")

    def quit_program(self):
        self.destroy()


def show_message_box(box, title="window", message="\n"):
    box(title, message)


def main():
    text_app = Text_redactor()


if __name__ == '__main__':
    main()
