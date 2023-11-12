import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
from tktooltip import ToolTip
import numpy as np
from tkinter import ttk
from style import *
from PIL import Image


class Width(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent)

		self.f = Figure(figsize=(8, 0.01), dpi=100)
		self.f.patch.set_facecolor(title_color)
		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')


class SetSectionPoints(ctk.CTkFrame):
	def __init__(self, parent, data, size):
		super().__init__(parent)

		plt.style.use('seaborn-dark')
		self.f = Figure(figsize=size, dpi=100)
		self.ax = self.f.add_subplot(111)
		self.f.subplots_adjust(left=0, right=1)
		self.f.patch.set_facecolor(graph_bg)
		self.ax.set_facecolor(graph_bg)

		self.update_chart_content(data)

	def update_chart_content(self, new_data):
		bar_dimensions = self.score_difference(new_data)

		data = bar_dimensions[0]
		bar_width = bar_dimensions[1]

		self.ax.clear()

		set_section = ('Početak seta', 'Sredina seta', 'Kraj seta')
		x_pos = [bar_width[0] / 2, bar_width[0] + bar_width[1] / 2, bar_width[0] + bar_width[1] + bar_width[2] / 2]

		self.ax.bar(
			x_pos,
			data,
			align='center',
			alpha=1,
			width=bar_width,
			color=['#81b64c' if y > 0 else '#b23330' for y in data],
			edgecolor=graph_bg)

		self.ax.bar_label(self.ax.containers[0], color='white', label_type='center', fontsize=20)

		self.ax.set_xticks(x_pos, set_section, size=15)
		self.ax.set_ylabel('Razlika u poenima')

		self.ax.yaxis.label.set_color('white')
		self.ax.xaxis.label.set_color('white')

		self.ax.tick_params(axis='both', colors='white')

		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')

	def score_difference(self, set_result):
		team_score = 0
		team_section_score = 0

		rival_team_score = 0
		rival_team_section_score = 0

		start_score = 0
		middle_score = 0

		start_width = 0
		middle_width = 0
		for point in set_result:
			if point == '1':
				team_score += 1
				team_section_score += 1
			else:
				rival_team_score += 1
				rival_team_section_score += 1

			if (team_score == 10 or rival_team_score == 10) and start_score == 0:
				start_score = team_section_score - rival_team_section_score
				start_width = (team_score + rival_team_score) / len(set_result)
				team_section_score = 0
				rival_team_section_score = 0
			if (team_score == 20 or rival_team_score == 20) and middle_score == 0:
				middle_score = team_section_score - rival_team_section_score
				middle_width = (team_score + rival_team_score) / len(set_result) - start_width
				team_section_score = 0
				rival_team_section_score = 0

		finish_score = team_section_score - rival_team_section_score
		finish_width = 1.0 - middle_width - start_width

		return [[start_score, middle_score, finish_score], [start_width, middle_width, finish_width]]


class PointsDistribution(ctk.CTkFrame):
	def __init__(self, parent, data, size):
		super().__init__(parent)

		plt.style.use('seaborn-dark')
		self.f = Figure(figsize=size, dpi=100)
		self.ax = self.f.add_subplot(111)
		self.f.subplots_adjust(left=0, right=1)
		self.f.patch.set_facecolor(graph_bg)
		self.ax.set_facecolor(graph_bg)

		self.update_chart_content(data)

	def update_chart_content(self, new_data):
		data = [1 if y == '1' else -1 for y in new_data]

		self.ax.clear()

		facecolors = ['#81b64c' if y > 0 else '#b23330' for y in data]
		x_values = [n for n in range(1, len(data) + 1)]

		self.ax.bar(x_values, data, color=facecolors, alpha=1, edgecolor=graph_bg, width=1)

		transpose_data = [
			new_data[:index+1].count('0') if x == '0' else new_data[:index+1].count('1') for index, x in enumerate(new_data)]

		self.get_result_label(new_data, data, transpose_data)

		self.ax.tick_params(axis='x', colors=header_color, labelcolor=header_color)
		self.ax.tick_params(axis='y', colors='#282828', labelcolor='#282828')

		# self.ax.yaxis.set_major_locator(NullLocator())
		y_ticks = range(-2, 4)
		self.ax.set_yticks(y_ticks)
		self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))

		patch1 = mpatches.Patch(color='#81b64c', label="MOK Kikinda")
		patch2 = mpatches.Patch(color='#b23330', label='OK Kulpin')

		self.ax.legend(handles=[patch1, patch2], prop={"size": 9}, loc="upper left", labelcolor='white', ncol=2)

		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')

	def get_result_label(self, x, y, data):
		for i in range(len(x)):
			self.ax.text(i + 1, y[i] + 0.1 if y[i] > 0 else y[i] - 0.45, data[i], ha='center', color='white')


class PieChart2(ctk.CTkFrame):
	def __init__(self, parent, figsize, slices, labels, colors):
		super().__init__(parent)

		self.original_colors = colors
		self.original_labels = labels
		self.original_slices = slices

		plt.style.use("seaborn-dark")

		self.f = Figure(figsize=figsize, dpi=100)
		self.ax = self.f.add_subplot(111)
		self.ax.set_facecolor(graph_bg)
		self.f.patch.set_facecolor(graph_bg)

		self.update_chart_content(slices)

	def remove_zero_slices(self, data):
		zero_indices = [i for i, size in enumerate(data) if size == 0]

		self.labels = [label for i, label in enumerate(self.original_labels) if i not in zero_indices]
		self.slices = [pie_slice for i, pie_slice in enumerate(data) if i not in zero_indices]
		self.colors = [color for i, color in enumerate(self.original_colors) if i not in zero_indices]

	def update_chart_content(self, new_data):
		self.slices = new_data

		self.remove_zero_slices(self.slices)
		self.textprops = {'color': 'white', 'fontweight': 'bold', 'fontsize': 'large'}

		self.ax.clear()

		total = sum(self.slices)
		percentages = [(size / total) * 100 for size in self.slices]

		self.labels_to_slices = {}
		for index, label in enumerate(self.labels):
			self.labels_to_slices[label] = self.slices[index]

		if len(self.slices) == 0:
			self.slices = [1]
			self.ax.text(0, 0, "Nema\npodataka", ha='center', va='center', fontsize=14, color='white')

			self.ax.pie(self.slices, labels=None, colors=['gray'], wedgeprops={'edgecolor': 'black', 'width': 0.6},
						textprops={'color': 'grey'}, radius=1)
		else:
			self.wedges, _, _ = self.ax.pie(
				self.slices,
				labels=[f'{label} ({percentage:.1f}%)' for label, percentage in zip(self.labels, percentages)],
				autopct='',
				colors=self.colors,
				wedgeprops={'width': 0.6},
				textprops=self.textprops,
				shadow=True,
				labeldistance=1.3
				)

			self.wedge_size_mapping = {wedge: size for wedge, size in zip(self.wedges, self.slices)}

			self.selected_wedge = None
			self.annotation = self.ax.annotate(
				"", xy=(0, 0), xytext=(10, 0), textcoords="offset points", color='white',
				bbox=dict(boxstyle="round", fc="#282828", ec="black", lw=1))
			self.annotation.set_visible(False)
			self.f.canvas.mpl_connect("motion_notify_event", self.hover)

		for widget in self.winfo_children():
			widget.destroy()

		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')

	def update_transparency(self, amount):
		for wedge in self.wedges:
			wedge.set_alpha(amount)

	def hover(self, event):
		if self.selected_wedge is not None:
			self.selected_wedge.set_center((0, 0))
			self.selected_wedge = None
		if event.inaxes == self.ax:
			for i, w in enumerate(self.wedges):
				if w.contains_point([event.x, event.y]):
					self.annotation.set_text(self.wedge_size_mapping[w])
					# self.annotation.set_text(
					# 	f'{self.labels_to_slices[w.get_label()] if len(self.slices) > 1 else self.slices[0]}')
					self.annotation.xy = (event.xdata, event.ydata)
					self.annotation.set_visible(True)

					self.selected_wedge = w
					self.f.canvas.draw_idle()
					self.update_transparency(0.2)
					w.set_alpha(1)
		if self.selected_wedge is None and self.annotation.get_visible():
			self.annotation.set_visible(False)
			self.update_transparency(1)
			self.f.canvas.draw_idle()


class GeneralSetChart(ctk.CTkFrame):
	def __init__(self, parent, data, size, labels, colors):
		super().__init__(parent, fg_color='#282828')

		self.data = data
		self.labels = labels
		self.colors = colors
		self.size = size

		plt.style.use('seaborn-dark')
		self.f = Figure(figsize=size, dpi=100)
		self.ax = self.f.add_subplot(111)
		sets_x = [1, 2, 3, 4, 5]
		self.f.patch.set_facecolor(graph_bg)
		self.ax.set_facecolor(graph_bg)
		self.x_indexes = np.arange(1, len(sets_x) + 1)
		self.width = 0.15 if len(data) == 5 else 0.1

		self.update_chart_content(self.data)

	def update_annot(self, bar, event):
		y = bar.get_y()+bar.get_height()
		self.annot.xy = (event.xdata, event.ydata)
		text = f"{bar.get_label()}: {int(y) if y.is_integer() else y}"
		self.annot.set_text(text)
		self.annot.get_bbox_patch().set_alpha(1)

	def update_transparency(self, amount):
		for x in self.bars:
			for y in x:
				y.set_alpha(amount)

	def hover(self, event):
		vis = self.annot.get_visible()
		if event.inaxes == self.ax:
			for bar in self.bars:
				for single_bar in bar:
					cont, ind = single_bar.contains(event)
					if cont:
						self.update_annot(single_bar, event)
						self.annot.set_visible(True)
						self.f.canvas.draw_idle()

						self.update_transparency(0.5)
						single_bar.set_alpha(1)
						return
		if vis:
			self.annot.set_visible(False)
			self.update_transparency(1)
			self.f.canvas.draw_idle()

	def update_chart_content(self, new_data):
		self.data = new_data
		self.ax.clear()

		bar_cord = {
			0: self.x_indexes - 2 * self.width,
			1: self.x_indexes - self.width,
			2: self.x_indexes,
			3: self.x_indexes + self.width,
			4: self.x_indexes + 2 * self.width,
			5: self.x_indexes + 3 * self.width}

		no_info_data = {
			0: [4, 3, 4, 3, 1],
			1: [2, 2, 2, 1, 0],
			2: [1, 1, 1, 0, 0],
			3: [0, 0, 1, 1, 1],
			4: [1, 0, 0, 1, 0],
			5: [1, 2, 2, 1, 1]}

		valid_data = sum(self.data[0]) + sum(self.data[-1])

		if valid_data == 0:
			self.ax.text(
				0.5, 0.5, "Nema\npodataka", ha='center', va='center', fontsize=18, color='white',
				transform=self.ax.transAxes, bbox=dict(fc="#323232", lw=4, ec='#323232'))
			for index, _ in enumerate(self.labels):
				self.ax.bar(bar_cord[index], no_info_data[index], width=self.width, color="grey", edgecolor='black')

		else:
			self.bars = []
			for index, label in enumerate(self.labels):
				bar = self.ax.bar(
					bar_cord[index], self.data[index], width=self.width, color=self.colors[index],
					label=[label for x in range(0, 5)],
					edgecolor=graph_bg)
				self.bars.append(bar)

			self.annot = self.ax.annotate(
				"", xy=(0, 0), xytext=(15, -3), textcoords="offset points", color='white',
				bbox=dict(fc="#282828", ec="black", lw=0.5))
			self.annot.set_visible(False)
			self.f.canvas.mpl_connect("motion_notify_event", self.hover)

		# legend
		patches = []
		for index, label in enumerate(self.labels):
			patch = mpatches.Patch(color=self.colors[index] if valid_data > 0 else 'grey', label=label)
			patches.append(patch)

		self.f.legend(handles=patches, prop={"size": 9 if self.size[0] == 8 else 7}, loc="upper right", labelcolor='white')

		self.ax.set_xlabel("Setovi")
		self.ax.set_ylabel("Poeni")
		self.ax.yaxis.label.set_color('white')
		self.ax.xaxis.label.set_color('white')

		self.ax.tick_params(axis='both', colors='white')

		if max(self.data[0]) <= 4:
			y_ticks = range(0, 5)
			self.ax.set_yticks(y_ticks)
			self.ax.set_yticklabels(y_ticks, color='white')
		else:
			self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))

		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')


class AttackChart2(ctk.CTkFrame):
	def __init__(self, parent, data, color, labels, size):
		super().__init__(parent)

		self.color = color
		self.labels = labels

		self.sets = ['1', '2', '3', '4', '5']

		plt.style.use('seaborn-dark')
		self.f = Figure(figsize=size, dpi=100)
		self.ax = self.f.add_subplot(111)

		self.f.patch.set_facecolor(graph_bg)
		self.ax.set_facecolor(graph_bg)

		self.update_chart_content(data)

	def update_annot(self, bar, event):
		self.annot.xy = (event.xdata, event.ydata)
		self.annot.set_text(bar.get_height())
		self.annot.get_bbox_patch().set_alpha(1)

	def update_transparency(self, amount):
		for x in self.bars:
			for y in x:
				y.set_alpha(amount)

	def hover(self, event):
		vis = self.annot.get_visible()
		if event.inaxes == self.ax:
			for j, bar in enumerate(self.bars):
				for i, single_bar in enumerate(bar):
					cont, ind = single_bar.contains(event)
					if cont:
						self.update_annot(single_bar, event)
						self.update_transparency(0.5)
						single_bar.set_alpha(1)
						self.annot.set_visible(True)
						self.f.canvas.draw_idle()
						return

		if vis:
			self.update_transparency(1)
			self.annot.set_visible(False)
			self.f.canvas.draw_idle()

	def update_chart_content(self, new_data):
		data = new_data

		self.ax.clear()

		data = np.array(data)
		self.bars = []
		for index, one_bar in enumerate(data):
			bar = self.ax.bar(
				self.sets,
				data[index],
				label=[self.labels[index], self.labels[index], self.labels[index], self.labels[index], self.labels[index]],
				bottom=np.sum(data[:index], axis=0),
				color=self.color[index],
				width=0.5)
			self.bars.append(bar)

		# annotation
		self.annot = self.ax.annotate(
			"", xy=(0, 0), xytext=(15, -3), textcoords="offset points", color='white',
			bbox=dict(fc="#282828", ec="black", lw=0.5))
		self.annot.set_visible(False)
		self.f.canvas.mpl_connect("motion_notify_event", self.hover)

		self.ax.bar_label(self.ax.containers[len(data) - 1], color='white')

		patches = []
		for index, patch in enumerate(self.color):
			patch = mpatches.Patch(color=self.color[index], label=self.labels[index])
			patches.append(patch)

		patches.reverse()

		# legend
		self.f.legend(handles=patches, prop={"size": 8}, loc='upper right', labelcolor='white')

		self.ax.set_ylabel("Količina")
		self.ax.set_xlabel("Setovi")
		self.ax.title.set_color('white')
		self.ax.yaxis.label.set_color('white')
		self.ax.xaxis.label.set_color('white')

		self.ax.tick_params(axis='x', colors='white')
		self.ax.tick_params(axis='y', colors='white')

		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')


class ProgressPercentage(ctk.CTkFrame):
	def __init__(self, parent, element, data):
		super().__init__(parent, fg_color=header_color, bg_color=header_color)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.element = element

		self.progressbar = ctk.CTkProgressBar(self, orientation='horizontal', width=150)
		self.progressbar.grid(column=1, row=0)

		self.element_percentage = None
		self.display_label = ctk.CTkLabel(self, font=show_font)
		self.display_label.grid(column=0, row=0, padx=20)

		self.update_data(data)

	def update_data(self, data):
		all_attempts = sum(data)
		successful_attempts = data[0]
		stopped_attempts = data[2]

		if all_attempts == 0:
			element_percentage = 0
			color = 'grey'
		else:
			element_percentage = (successful_attempts - stopped_attempts) / all_attempts
			if element_percentage <= 0.1:
				color = 'red'
			elif 0.1 < element_percentage <= 0.2:
				color = 'orange'
			elif 0.2 < element_percentage <= 0.3:
				color = 'green'
			else:
				if self.element == 'napada':
					color = '#008FD5'
				else:
					color = 'yellow'

		self.progressbar.configure(progress_color=color)
		self.progressbar.set(element_percentage / 0.4)
		self.display_label.configure(text=f'{element_percentage:.3f}')


class EfficiencyGraph(ctk.CTkFrame):
	def __init__(self, parent, data, color, size):
		super().__init__(parent)

		self.maxcolor = color

		self.sets = ['1', '2', '3', '4', '5']

		plt.style.use('seaborn-dark')
		self.f = Figure(figsize=size, dpi=100)
		self.ax = self.f.add_subplot(111)

		self.f.patch.set_facecolor(graph_bg)
		self.ax.set_facecolor(graph_bg)

		self.update_chart_content(data)

	def update_annot(self, bar, event):
		self.annot.xy = (event.xdata, event.ydata)
		self.annot.set_text(bar.get_height())
		self.annot.get_bbox_patch().set_alpha(1)

	def update_transparency(self, amount):
		for x in self.bar:
			x.set_alpha(amount)

	def hover(self, event):
		vis = self.annot.get_visible()
		if event.inaxes == self.ax:
				for i, single_bar in enumerate(self.bar):
					cont, ind = single_bar.contains(event)
					if cont:
						self.update_annot(single_bar, event)
						self.update_transparency(0.2)
						single_bar.set_alpha(1)
						self.annot.set_visible(True)
						self.f.canvas.draw_idle()
						return

		if vis:
			self.update_transparency(1)
			self.annot.set_visible(False)
			self.f.canvas.draw_idle()

	def update_chart_content(self, new_data):
		data = new_data

		self.ax.clear()
		colors = []
		for set_efficiency in data:
			if set_efficiency <= 0.1:
				color = '#f08173'
			elif 0.1 < set_efficiency <= 0.2:
				color = '#f4bc4e'
			elif 0.2 < set_efficiency <= 0.3:
				color = '#81b64c'
			else:
				color = self.maxcolor
			colors.append(color)

		self.bar = self.ax.bar(
				self.sets,
				data,
				edgecolor=graph_bg,
				color=colors,
				width=1)
		# annotation
		self.annot = self.ax.annotate(
			"", xy=(0, 0), xytext=(15, -3), textcoords="offset points", color='white',
			bbox=dict(fc="#282828", ec="black", lw=0.5))
		self.annot.set_visible(False)
		self.f.canvas.mpl_connect("motion_notify_event", self.hover)

		self.ax.bar_label(self.ax.containers[0], color='white')

		patch1 = mpatches.Patch(color=self.maxcolor, label='Odlicno')
		patch2 = mpatches.Patch(color='#81b64c', label='Dobro')
		patch3 = mpatches.Patch(color='#f4bc4e', label='Slabo')
		patch4 = mpatches.Patch(color='#f08173', label='Loše')

		# legend
		self.f.legend(handles=[patch1, patch2, patch3, patch4], prop={"size": 8}, loc='upper right', labelcolor='white')

		self.ax.set_ylabel("Efikasnost")
		self.ax.set_xlabel("Setovi")
		self.ax.title.set_color('white')
		self.ax.yaxis.label.set_color('white')
		self.ax.xaxis.label.set_color('white')

		self.ax.tick_params(axis='x', colors='white')
		self.ax.tick_params(axis='y', colors='white')

		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')


class CourtGraph(ctk.CTkFrame):
	def __init__(self, parent, court_image, color, data, title, size, font, zone_font):
		super().__init__(parent, fg_color=graph_bg)

		self.color = color
		self.court_image = court_image
		self.size = size
		self.font = font
		self.title = title

		# title
		self.title_label = ctk.CTkLabel(
			self, text=f'{title} ({sum(data)})', bg_color=graph_bg, text_color='white', font=self.font, height=60,
			fg_color=graph_bg)
		self.title_label.pack(fill='x')

		# court image
		self.image_label = ctk.CTkLabel(self, fg_color=graph_bg, corner_radius=1, text='')
		self.image_label.pack(fill='both', expand=True)

		self.no_info1 = ctk.CTkLabel(
			self.image_label, text='Nema', bg_color='grey', text_color='white', height=3, font=zone_font)
		self.no_info2 = ctk.CTkLabel(
			self.image_label, text='podataka', bg_color='grey', text_color='white', height=3, font=zone_font)

		# zones
		self.zone1 = ctk.CTkLabel(self.image_label, bg_color=self.color, text_color='white', font=zone_font)
		self.zone2 = ctk.CTkLabel(self.image_label, bg_color=self.color, text_color='white', font=zone_font)
		self.zone3 = ctk.CTkLabel(self.image_label, bg_color=self.color, text_color='white', font=zone_font)
		self.zone4 = ctk.CTkLabel(self.image_label, bg_color=self.color, text_color='white', font=zone_font)
		self.zone6 = ctk.CTkLabel(self.image_label, bg_color=self.color, text_color='white', font=zone_font)

		self.zones = [self.zone1, self.zone2, self.zone3, self.zone4, self.zone6]

		self.zone1.place(relx=0.625, rely=0.32)
		self.zone2.place(relx=0.625, rely=0.07)
		self.zone3.place(relx=0.435, rely=0.07)
		self.zone4.place(relx=0.23, rely=0.07)
		self.zone6.place(relx=0.435, rely=0.32)

		self.update_chart_content(data)

	def update_chart_content(self, data):
		self.cumulative_data = sum(data)

		if self.cumulative_data == 0:
			self.no_info1.place(relx=0.41, rely=0.17)
			self.no_info2.place(relx=0.36, rely=0.30)

			for zone in self.zones:
				zone.configure(text='', bg_color='grey')

			image = Image.open('app_images/court_grey.png').crop((0, 12, 240, 190))
			grey_court = ctk.CTkImage(dark_image=image, size=self.size)

			self.image_label.configure(image=grey_court)

		else:
			self.no_info1.place_forget()
			self.no_info2.place_forget()

			s = ttk.Style(self)
			s.configure("ToolTip", font=self.font)

			for index, zone in enumerate(self.zones):
				zone.configure(
					text=f'{data[index] / self.cumulative_data * 100:.0f}%' if data[index] != 0 else '', bg_color=self.color)

				ToolTip(
					zone, msg=f'{data[index]}', delay=0.0, follow=True,
					parent_kwargs={"bg": "black", "padx": 1, "pady": 1}, fg="white", bg="#282828", padx=7, pady=7)

			image = Image.open(self.court_image).crop((0, 12, 240, 190))
			coloured_court = ctk.CTkImage(dark_image=image, size=self.size)
			self.image_label.configure(image=coloured_court)
			self.title_label.configure(text=f'{self.title} ({sum(data)})')


class NestedDoughnut(ctk.CTkFrame):
	def __init__(self, parent, labels, data, colors, sub_data, legend, size, team=False):
		super().__init__(parent)

		self.data = data
		self.original_labels = labels
		self.original_colors = colors
		self.legend = legend
		self.team = team

		self.original_sub_colors = ['orange', '#F8C666', 'grey', 'orange', '#F8C666', 'grey', 'orange', '#F8C666', 'grey']
		# self.original_sub_colors = [
		# 	'#81b64c', '#AEB4AE', '#b23330', '#81b64c', '#AEB4AE', '#b23330', '#81b64c', '#AEB4AE', '#b23330']

		plt.style.use("seaborn-dark")
		self.f = Figure(figsize=size, dpi=100)
		self.ax1 = self.f.add_subplot(111)
		self.ax2 = self.f.add_subplot(111)
		self.ax1.set_facecolor(graph_bg)
		self.ax2.set_facecolor(graph_bg)
		self.f.patch.set_facecolor(graph_bg)

		self.ax1.yaxis.label.set_color(graph_bg)
		self.ax1.xaxis.label.set_color(graph_bg)

		self.ax1.tick_params(axis='x', colors=graph_bg)
		self.ax1.tick_params(axis='y', colors=graph_bg)

		self.ax2.yaxis.label.set_color(graph_bg)
		self.ax2.xaxis.label.set_color(graph_bg)

		self.ax2.tick_params(axis='x', colors=graph_bg)
		self.ax2.tick_params(axis='y', colors=graph_bg)

		self.update_chart_content(data, sub_data)

	def remove_zero_slices(self):
		zero_indices = [i for i, size in enumerate(self.data) if size == 0]

		self.labels = [label for i, label in enumerate(self.original_labels) if i not in zero_indices]
		self.data = [pie_slice for i, pie_slice in enumerate(self.data) if i not in zero_indices]
		self.colors = [color for i, color in enumerate(self.original_colors) if i not in zero_indices]

		self.sub_colors = self.original_sub_colors[:3 * len(self.data)]

	def update_chart_content(self, new_data, new_sub_data):
		self.data = new_data
		sub_data = new_sub_data

		self.sum_sub_data = sum(sub_data)

		self.remove_zero_slices()

		self.textprops = {
			'color': 'white',
			'fontweight': 'bold' if self.team is True else None,
			'fontsize': 'large' if self.team is True else None}

		self.ax1.clear()
		self.ax2.clear()

		total = sum(self.data)
		percentages = [(size / total) * 100 for size in self.data]

		if len(self.data) == 0:
			self.data = [1]
			self.ax2.text(0, 0, "Nema\npodataka", ha='center', va='center', fontsize=11, color='white')

			self.ax2.pie(
				self.data,
				labels=None,
				colors=['gray'],
				wedgeprops={'edgecolor': 'black', 'width': 0.5},
				textprops={'color': 'grey'},
				radius=1)

			patch_colors = ['grey', 'grey', 'grey']

		else:
			self.wedges1, _ = self.ax1.pie(
				self.data,
				labels=[f'{label} ({percentage:.1f}%)' for label, percentage in zip(self.labels, percentages)],
				colors=self.colors,
				startangle=90,
				radius=1,
				textprops=self.textprops,
				wedgeprops={'width': 0.5},
				shadow=True,
				labeldistance=1.3)

			self.wedges2, _ = self.ax2.pie(
				sub_data,
				labels=sub_data,
				colors=self.sub_colors,
				startangle=90,
				radius=0.5,
				textprops={'visible': False},
				wedgeprops={'width': 0.2})

			self.wedges = self.wedges1 + self.wedges2
			self.slices = self.data + sub_data
			self.wedge_size_mapping = {wedge: size for wedge, size in zip(self.wedges, self.slices)}
			self.selected_wedge = None
			self.annotation = self.ax2.annotate(
				"", xy=(0, 0), xytext=(10, 0), textcoords="offset points", color='white',
				bbox=dict(boxstyle="round", fc="#282828", ec="black", lw=1))
			self.annotation.set_visible(False)
			self.f.canvas.mpl_connect("motion_notify_event", self.hover)
			patch_colors = ['orange', '#F8C666', 'grey']

		# legend
		patch1 = mpatches.Patch(color=patch_colors[0], label=self.legend[0])
		patch2 = mpatches.Patch(color=patch_colors[1], label=self.legend[1])
		patch3 = mpatches.Patch(color=patch_colors[2], label=self.legend[2])

		self.f.legend(
			handles=[patch1, patch2, patch3], prop={"size": 8}, labelcolor='white', loc='upper right')

		for widget in self.winfo_children():
			widget.destroy()

		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')

	def update_transparency(self, amount):
		for wedge in self.wedges:
			wedge.set_alpha(amount)

	def hover(self, event):
		if self.selected_wedge is not None:
			self.selected_wedge.set_center((0, 0))
			self.selected_wedge = None
		if event.inaxes == self.ax2:
			for w in self.wedges:
				if w.contains_point([event.x, event.y]):
					# amount = w.get_label()
					# percentage = (int(w.get_label()) / self.sum_sub_data * 100) if self.sum_sub_data > 0 else 0
					# self.annotation.set_text(
					# 	f'{amount} ({percentage:.0f}%)')
					self.annotation.set_text(self.wedge_size_mapping[w])
					self.annotation.xy = (event.xdata, event.ydata)
					self.annotation.set_visible(True)
					self.update_transparency(0.2)
					w.set_alpha(1)
					self.selected_wedge = w
					self.f.canvas.draw_idle()

		if self.selected_wedge is None and self.annotation.get_visible():
			self.update_transparency(1)
			self.annotation.set_visible(False)
			self.f.canvas.draw_idle()


class HBarChart2(ttk.Frame):
	def __init__(self, parent, labels, data, color, size, legend_labels):
		super().__init__(parent, style="Dark.TFrame")

		self.labels = labels
		self.color = color
		self.legend_labels = legend_labels

		plt.style.use('seaborn-dark')
		self.f = plt.Figure(figsize=size, dpi=100)
		self.ax = self.f.add_subplot(111)

		self.f.patch.set_facecolor(graph_bg)
		self.ax.set_facecolor(graph_bg)

		self.ax.xaxis.label.set_color(graph_bg)

		self.ax.tick_params(axis='x', colors=graph_bg)

		self.update_chart_content(data)

	def update_chart_content(self, new_data):
		data = new_data

		self.ax.clear()

		y = np.arange(len(self.labels))
		width = 0.3

		hbar1 = self.ax.barh(y - 0.15, data[0], height=width, label=self.legend_labels[0], color=self.color[0])
		self.ax.bar_label(hbar1, padding=3, color='white')

		hbar2 = self.ax.barh(y + 0.15, data[1], height=width, label=self.legend_labels[1], color=self.color[1])
		self.ax.bar_label(hbar2, padding=3, color='white')

		self.ax.set_yticks(y, self.labels)
		self.f.legend(prop={"size": 10}, loc="upper right", labelcolor='white')

		x_ticks = range(0, max(data[0]) if max(data[0]) > max(data[1]) else max(data[1]) + 1)
		self.ax.set_xticks(x_ticks)
		self.ax.set_xticklabels(x_ticks, color=graph_bg)

		self.ax.set_xlabel("Količina")
		self.ax.xaxis.label.set_color('white')

		self.ax.tick_params(axis='y', colors='white')

		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')


class HBarChart(ctk.CTkFrame):
	def __init__(self, parent, labels, data, color, size):
		super().__init__(parent, fg_color='#282828')

		self.labels = labels
		self.color = color

		plt.style.use('seaborn-dark')
		self.f = Figure(figsize=size, dpi=100)
		self.ax = self.f.add_subplot(111)

		self.f.patch.set_facecolor(graph_bg)
		self.ax.set_facecolor(graph_bg)

		self.ax.xaxis.label.set_color(graph_bg)

		self.ax.tick_params(axis='x', colors=graph_bg)

		self.update_chart_content(data)

	def update_chart_content(self, new_data):
		data = new_data

		self.ax.clear()

		if sum(data) == 0:
			self.ax.text(
				0.5, 0.5, "Nema\npodataka", ha='center', va='center', fontsize=18, color='white',
				transform=self.ax.transAxes, bbox=dict(fc="#323232", lw=12 if len(data) == 5 else 6, ec='#323232'))
			self.ax.barh(
				self.labels, [30, 70, 100, 80, 40] if len(data) == 5 else [65, 100, 80, 40],
				color=['grey'], height=0.4)

		else:
			hbar = self.ax.barh(self.labels, data, color=self.color, height=0.4)
			self.ax.bar_label(hbar, padding=3, color='white')
			self.ax.tick_params(axis='x', colors='white')

			x_ticks = range(0, 5) if max(data) < 4 else range(0, max(data) + 1)
			self.ax.set_xticks(x_ticks)
			self.ax.set_xticklabels(x_ticks, color=graph_bg)

			self.ax.set_xlabel("Količina")
			self.ax.xaxis.label.set_color('white')

		self.ax.tick_params(axis='y', colors='white')

		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')


class Table(ttk.Treeview):
	def __init__(self, parent, columns, column_text, column_width, rows):
		super().__init__(parent, columns=columns, show='headings', height=len(rows))

		self.bind('<Motion>', 'break')
		self.rows = rows

		for index, column in enumerate(columns):
			self.heading(column, text=column_text[index])
			self.column(column, width=column_width[index], anchor='center')

		# style
		self.style = ttk.Style(self)
		self.style.theme_use("default")
		self.style.configure(
			"Treeview", background=graph_bg, rowheight=30,  font=show_font,
			fieldbackground="#282828", foreground="white", borderwidth=0)
		self.style.configure('Treeview.Heading', background=graph_bg, foreground="white", font=('Montserrat', 17))
		self.style.map('Treeview', background=[('selected', graph_bg)], foreground=[('selected', 'white')])
		self.style.map('Treeview.Heading', background=[('selected', '#262626')])

		self.update_table(rows)

	def update_table(self, new_rows):
		for item in self.get_children():
			self.delete(item)

		for index, row in enumerate(new_rows):
			self.insert(parent='', index=index, values=row)


class PieChart(ctk.CTkFrame):
	def __init__(self, parent, figsize, slices, labels, colors, title, point_chart=False):
		super().__init__(parent, fg_color=graph_bg)

		self.original_colors = colors
		self.original_labels = labels
		self.original_slices = slices
		self.title = title
		self.points_chart = point_chart

		plt.style.use("seaborn-dark")

		self.f = Figure(figsize=figsize, dpi=100)
		self.ax = self.f.add_subplot(111)
		self.ax.set_facecolor(graph_bg)
		self.f.patch.set_facecolor(graph_bg)

		self.update_chart_content(slices)

	def remove_zero_slices(self, data):
		zero_indices = [i for i, size in enumerate(data) if size == 0]

		self.labels = [label for i, label in enumerate(self.original_labels) if i not in zero_indices]
		self.slices = [pie_slice for i, pie_slice in enumerate(data) if i not in zero_indices]
		self.colors = [color for i, color in enumerate(self.original_colors) if i not in zero_indices]

	def update_chart_content(self, new_data):
		self.slices = new_data

		errors = self.slices[-1] if self.points_chart is True else 0

		self.remove_zero_slices(self.slices)
		self.textprops = {'color': 'white'}

		self.ax.clear()

		self.labels_to_slices = {}
		for index, label in enumerate(self.labels):
			self.labels_to_slices[label] = self.slices[index]

		if len(self.slices) == 0:
			self.slices = [1]
			self.ax.text(0, 0, "Nema\npodataka", ha='center', va='center', fontsize=11, color='white')

			self.ax.pie(self.slices, labels=None, colors=['gray'], wedgeprops={'edgecolor': 'black'},
						textprops={'color': 'grey'}, radius=1)
			self.ax.set_title(f'{self.title} (0)')
		else:
			if len(self.slices) == 1:
				self.textprops = {'color': f'{self.colors[0]}'}
				middle_label = f'{self.labels[0]}\n100%'
				self.labels = None
				self.ax.text(0, 0, middle_label, ha='center', va='center', fontsize=11, color='white')

			self.wedges, _, _ = self.ax.pie(
				self.slices,
				labels=self.labels,
				autopct='%1.0f%%',
				colors=self.colors,
				textprops=self.textprops,
				shadow=True)

			self.selected_wedge = None
			self.annotation = self.ax.annotate(
				"", xy=(0, 0), xytext=(10, 0), textcoords="offset points", color='white',
				bbox=dict(boxstyle="round", fc="#282828", ec="black", lw=1))
			self.annotation.set_visible(False)
			self.f.canvas.mpl_connect("motion_notify_event", self.hover)

			self.ax.set_title(f'{self.title} ({sum(self.slices) - errors})')

		self.ax.title.set_color('white')

		for widget in self.winfo_children():
			widget.destroy()

		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')

	def update_transparency(self, amount):
		for wedge in self.wedges:
			wedge.set_alpha(amount)

	def hover(self, event):
		if self.selected_wedge is not None:
			self.selected_wedge.set_center((0, 0))
			self.selected_wedge = None
		if event.inaxes == self.ax:
			for i, w in enumerate(self.wedges):
				if w.contains_point([event.x, event.y]):
					self.annotation.set_text(
						f'{self.labels_to_slices[w.get_label()] if len(self.slices) > 1 else self.slices[0]}')
					self.annotation.xy = (event.xdata, event.ydata)
					self.annotation.set_visible(True)
					self.update_transparency(0.2)
					w.set_alpha(1)
					self.selected_wedge = w
					self.f.canvas.draw_idle()

		if self.selected_wedge is None and self.annotation.get_visible():
			self.update_transparency(1)
			self.annotation.set_visible(False)
			self.f.canvas.draw_idle()


class BarChart2(ctk.CTkFrame):
	def __init__(self, parent, players, data, color, labels, title, size):
		super().__init__(parent)

		self.color = color
		self.labels = labels
		self.players = players

		plt.style.use('seaborn-dark')
		self.f = Figure(figsize=size, dpi=100)
		self.ax = self.f.add_subplot(111)

		self.f.patch.set_facecolor(graph_bg)
		self.ax.set_facecolor(graph_bg)

		self.ax.set_title(title)
		self.ax.set_ylabel("Ishod")
		self.ax.title.set_color('white')
		self.ax.yaxis.label.set_color('white')

		self.ax.tick_params(axis='x', colors='white')
		self.ax.tick_params(axis='y', colors='white')

		self.update_chart_content(data)

	def update_annot(self, bar, event):
		self.annot.xy = (event.xdata, event.ydata)
		self.annot.set_text(bar.get_height())
		self.annot.get_bbox_patch().set_alpha(1)

	def hover(self, event):
		vis = self.annot.get_visible()
		if event.inaxes == self.ax:
			for bar in self.bars:
				for single_bar in bar:
					cont, ind = single_bar.contains(event)
					if cont:
						self.update_annot(single_bar, event)
						self.annot.set_visible(True)
						self.f.canvas.draw_idle()
						return
		if vis:
			self.annot.set_visible(False)
			self.f.canvas.draw_idle()

	def update_chart_content(self, new_data):
		data = new_data

		self.ax.clear()

		if sum(data[0]) + sum(data[1]) + sum(data[2]) == 0:
			self.ax.text(
				0.5, 0.5, "Nema\npodataka", ha='center', va='center', fontsize=16, color='white',
				transform=self.ax.transAxes, bbox=dict(fc="#353535", lw=4, ec='#353535'))
			self.ax.bar(self.players, [3, 4, 2], color=['grey'], edgecolor='black', width=0.5)

			patch_colors = ['grey', 'grey', 'grey']

		else:
			data = np.array(data)
			self.bars = []
			for index, subdata in enumerate(data):
				bar = self.ax.bar(
					self.players, subdata, bottom=np.sum(data[:index], axis=0), color=self.color[index], width=0.5)
				self.bars.append(bar)

			# bar1 = self.ax.bar(
			# 	self.players, data[0], bottom=np.sum(data[:0], axis=0), color=self.color[0], width=0.5)
			# bar2 = self.ax.bar(
			# 	self.players, data[1], bottom=np.sum(data[:1], axis=0), color=self.color[1], width=0.5)
			# bar3 = self.ax.bar(
			# 	self.players, data[2], bottom=np.sum(data[:2], axis=0), color=self.color[2], width=0.5)
			# self.bars = [bar1, bar2, bar3]

			# annotation
			self.annot = self.ax.annotate("", xy=(0, 0), xytext=(15, -3), textcoords="offset points", color='white',
										  bbox=dict(fc="#282828", ec="black", lw=0.5))
			self.annot.set_visible(False)
			self.f.canvas.mpl_connect("motion_notify_event", self.hover)

			self.ax.bar_label(self.ax.containers[2], color='white')

			column_sums = np.sum(data, axis=0)
			if max(column_sums) < 4:
				y_ticks = range(0, 4)
				self.ax.set_yticks(y_ticks)
				self.ax.set_yticklabels(y_ticks, color='white')

			patch_colors = ['orange', '#F8C666', 'grey']

		patch1 = mpatches.Patch(color=patch_colors[0], label=self.labels[0])
		patch2 = mpatches.Patch(color=patch_colors[1], label=self.labels[1])
		patch3 = mpatches.Patch(color=patch_colors[2], label=self.labels[2])

		# legend
		self.f.legend(handles=[patch1, patch2, patch3], prop={"size": 8}, loc='upper right', labelcolor='white')

		canvas = FigureCanvasTkAgg(self.f, self)
		canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')
