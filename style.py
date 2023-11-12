import customtkinter as ctk


section_font = ('Montserrat', 26, 'bold')
section_height = 90
section_color = '#51504c'

header_font = ('Montserrat', 22, 'bold')
header_height = 80
header_color = '#2b2b28'

title_font = ('Montserrat', 18, 'bold')
title_height = 70
title_color = '#393835'
show_font = ('Montserrat', 14, 'bold')

graph_bg = '#2b2b28'


class Section(ctk.CTkLabel):
	def __init__(self, parent, text, image):
		super().__init__(
			master=parent, text=text, fg_color=section_color, height=header_height, anchor='w', compound='left',
			font=section_font, padx=20, image=image)


class Header(ctk.CTkLabel):
	def __init__(self, parent, text):
		super().__init__(
			master=parent, text=text, fg_color=header_color, height=header_height, anchor='w', compound='left',
			font=header_font, padx=20, width=800)


class Separator(ctk.CTkLabel):
	def __init__(self, parent):
		super().__init__(
			master=parent, text='', fg_color=section_color, height=30, anchor='w', compound='left',
			font=header_font, padx=20, width=800)


class FinishedGraph(ctk.CTkFrame):
	def __init__(self, parent, title, under_header=False):
		super().__init__(master=parent, fg_color=title_color)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		ctk.CTkLabel(
			self, text=title, fg_color=title_color, height=title_height, anchor='w',
			font=title_font, padx=20, width=800).grid(column=0, row=0, sticky='we', pady=4 if under_header is False else 0)


class FinishedGraph2(ctk.CTkFrame):
	def __init__(self, parent, title, under_header=False):
		super().__init__(master=parent, fg_color=title_color)

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)

		ctk.CTkLabel(
			self, text=title, fg_color=title_color, height=title_height, anchor='w',
			font=title_font, padx=20, width=800).grid(columnspan=2, column=0, row=0, sticky='we', pady=4 if under_header is False else 0)
