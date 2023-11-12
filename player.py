from graphs import *
import base64
import io


class Player:
	def __init__(self, player_info):
		super().__init__()

		self.player_info = player_info

		# changeable data
		self.attack = None
		self.defense = None
		self.setting = None

	def update_data(self, attack_data, defense_data, setting_data):
		self.attack = attack_data
		self.defense = defense_data
		self.setting = setting_data

	def get_id(self):
		return self.player_info[0]

	def get_full_name(self):
		return f'{self.player_info[2]} {self.player_info[3]}'

	def get_birth_date(self):
		return f'Godište:  {self.player_info[6]}'

	def get_jersey_number(self):
		return f'Broj:  {self.player_info[4]}'

	def get_height(self):
		return f'Visina:  {self.player_info[5]}'

	def get_img(self):
		return self.player_info[7]

	def get_position(self):
		return self.player_info[1]

	# points
	def get_points_table(self):
		all_attacks = self.attack['attack_outcome'][0] + \
					self.attack['serve_outcome'][0] + \
					  sum(self.defense['solo_blocks']) + \
					  sum(self.defense['group_blocks']) / 2
		all_errors = self.attack['attack_outcome'][2] + \
					 self.attack['serve_outcome'][4] + \
					 sum(self.defense['block_errors_per_set']) + \
					 sum(self.setting['setting_error_per_set']) + \
					 self.defense['reception_outcome'][0]
		return [
			('Svi', all_attacks),
			('Napad', self.attack['attack_outcome'][0]),
			('Servis', self.attack['serve_outcome'][0]),
			('Solo blok', sum(self.defense['solo_blocks'])),
			('Grupni blok', sum(self.defense['group_blocks']) / 2),
			('Greške', all_errors)]

	def get_points_chart(self):
		errors = self.attack['attack_outcome'][2] + \
				 self.attack['serve_outcome'][4] + \
				 sum(self.defense['block_errors_per_set']) + \
				 sum(self.setting['setting_error_per_set']) + \
				 self.defense['reception_outcome'][0]

		return [self.attack['attack_outcome'][0],
				self.attack['serve_outcome'][0],
				sum(self.defense['solo_blocks']),
				sum(self.defense['group_blocks']) / 2,
				errors]

	def get_points_per_set(self):
		self.defense['group_blocks_per_set'] = self.reduce_blocks(self.defense['group_blocks_per_set'], 2)

		all_points_per_set = list(map(
			lambda a, b, c, d: a + b + c + d,
			self.attack['successful_attacks_per_set'],
			self.attack['as_serve_per_set'],
			self.defense['solo_blocks_per_set'],
			self.defense['group_blocks_per_set']
		))
		errors_per_set = list(map(
			lambda a, b, c, d, e: a + b + c + d + e,
			self.attack['stopped_attacks_per_set'],
			self.attack['error_serve_per_set'],
			self.defense['block_errors_per_set'],
			self.setting['setting_error_per_set'],
			self.defense['reception_error_per_set']
		))
		return [
			all_points_per_set,
			self.attack['successful_attacks_per_set'],
			self.attack['as_serve_per_set'],
			self.defense['solo_blocks_per_set'],
			self.defense['group_blocks_per_set'],
			errors_per_set]

	# attacks
	def get_attack_type(self):
		return self.attack['attack_type']

	def get_attack_outcome(self):
		return self.attack['attack_outcome']

	def get_attack_zones(self):
		return self.attack['attack_zone']

	# serve
	def get_serve_outcome(self):
		outcome = self.attack['serve_outcome'].copy()
		outcome.reverse()
		return outcome

	def get_serve_doughnut_data(self):
		return [sum(self.attack['spike_serve']), sum(self.attack['float_serve']), sum(self.attack['ground_serve'])]

	def get_serve_doughnut_subdata(self):
		return self.attack['spike_serve'] + self.attack['float_serve'] + self.attack['ground_serve']

	# defense
	def get_solo_blocks(self):
		return self.defense['solo_blocks']

	def get_group_blocks(self):
		return self.defense['group_blocks']

	def get_digs(self):
		return self.defense['digs']

	# setting
	def get_easy_setting_outcomes(self):
		return self.setting['easy_setting_outcome']

	def get_setting_positions(self):
		return self.setting['position_setting_outcome']

	def get_setting_zones(self):
		return self.setting['zone_setting']

	# reception
	def get_reception_outcome(self):
		return self.defense['reception_outcome']

	def get_reception_doughnut_data(self):
		return [sum(self.defense['up_reception']), sum(self.defense['down_reception'])]

	def get_reception_doughnut_subdata(self):
		return self.defense['up_reception'] + self.defense['down_reception']

	def reduce_blocks(self, blocks, factor):
		return list(map(lambda x: float(x / factor), blocks))


class PositionAndPlayers(ctk.CTkFrame):
	def __init__(self, parent, position, position_img, same_position_players):
		super().__init__(master=parent, fg_color=section_color)

		self.position = position

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)
		self.rowconfigure(8, weight=1)
		self.rowconfigure(9, weight=1)
		self.rowconfigure(10, weight=1)
		self.rowconfigure(11, weight=1)

		points = ctk.CTkImage(dark_image=position_img, size=(30, 30))

		self.position_label = Section(self, position, points)
		self.position_label.grid(column=0, row=0)
		# Header(self, 'dasdas').grid(column=0, row=0, sticky='we', columnspan=2)

		self.name_labels = []
		i = 0
		for index, player in enumerate(same_position_players):
			player_info_and_points_frame = ctk.CTkFrame(self, fg_color=title_color)
			player_info_and_points_frame.grid(column=0, row=1 + i)

			player_info_and_points_frame.columnconfigure(0, weight=1)
			player_info_and_points_frame.columnconfigure(1, weight=1)
			player_info_and_points_frame.rowconfigure(0, weight=1)
			player_info_and_points_frame.rowconfigure(1, weight=1)
			player_info_and_points_frame.rowconfigure(2, weight=1)

			if index > 0:
				Separator(player_info_and_points_frame).grid(column=0, row=0, sticky='we', columnspan=2)

			name = Header(player_info_and_points_frame, player.get_full_name())
			name.grid(column=0, row=1, sticky='we', columnspan=2)
			self.name_labels.append(name)

			self.points = PlayerGeneralStatistics(player_info_and_points_frame, player)
			self.points.grid(column=1, row=2, pady=15, padx=30, sticky='we')

			all_stats = ctk.CTkFrame(self, fg_color=title_color)
			all_stats.grid(column=0, row=2 + i, sticky='we', pady=2)

			all_stats.columnconfigure(0, weight=1)
			all_stats.rowconfigure(0, weight=1)
			all_stats.rowconfigure(1, weight=1)

			self.tabview = ctk.CTkTabview(
				master=all_stats, segmented_button_selected_color='#555555',
				segmented_button_selected_hover_color='#555555', segmented_button_unselected_color=title_color,
				segmented_button_fg_color=title_color, segmented_button_unselected_hover_color='#666666',
				fg_color=title_color, text_color='white', width=350)
			self.tabview.grid(column=0, row=0, sticky='wesn', pady=4, columnspan=2)

			self.tab_1 = self.tabview.add("Napad")
			self.tab_1.columnconfigure(0, weight=1)
			self.tab_1.rowconfigure(0, weight=1)

			self.tab_2 = self.tabview.add("Servis")
			self.tab_2.columnconfigure(0, weight=1)
			self.tab_2.rowconfigure(0, weight=1)

			self.tab_3 = self.tabview.add("Odbrana")
			self.tab_3.columnconfigure(0, weight=1)
			self.tab_3.rowconfigure(0, weight=1)

			self.tab_4 = self.tabview.add("Dizanje")
			self.tab_4.columnconfigure(0, weight=1)
			self.tab_4.rowconfigure(0, weight=1)

			self.tab_5 = self.tabview.add("Prijem")
			self.tab_5.columnconfigure(0, weight=1)
			self.tab_5.rowconfigure(0, weight=1)

			self.tabview._segmented_button._buttons_dict["Napad"].configure(font=show_font)
			self.tabview._segmented_button._buttons_dict["Servis"].configure(font=show_font)
			self.tabview._segmented_button._buttons_dict["Odbrana"].configure(font=show_font)
			self.tabview._segmented_button._buttons_dict["Dizanje"].configure(font=show_font)
			self.tabview._segmented_button._buttons_dict["Prijem"].configure(font=show_font)

			self.show = ctk.CTkLabel(
				all_stats, text='Prikaži:', fg_color=title_color, height=title_height, anchor='w', font=show_font,
				padx=20)
			self.show.grid(column=0, row=0, sticky='nw', pady=4)

			self.attacks = PlayerAttack(self.tab_1, player)
			self.attacks.grid(column=0, row=0, pady=30, columnspan=2, sticky='nswe', padx=30)

			self.serve = PlayerServe(self.tab_2, player)
			self.serve.grid(column=0, row=0, pady=30, columnspan=2, sticky='nswe', padx=30)

			self.defense = PlayerDefense(self.tab_3, player)
			self.defense.grid(column=0, row=0, pady=30, columnspan=2, sticky='nswe', padx=30)

			self.setting = PlayerSetting(self.tab_4, player)
			self.setting.grid(column=0, row=0, pady=30, columnspan=2, sticky='nswe', padx=30)

			self.reception = PlayerReception(self.tab_5, player)
			self.reception.grid(column=0, row=0, pady=30, columnspan=2, sticky='nswe', padx=30)

			i += 2

	def get_player_names(self):
		return self.name_labels

	def get_position(self):
		return self.position_label

	def update_chart_content(self):
		self.points.update_chart_content()
		self.attacks.update_chart_content()
		self.serve.update_chart_content()
		self.defense.update_chart_content()
		self.setting.update_chart_content()
		self.reception.update_chart_content()


class PlayerGeneralStatistics(ctk.CTkFrame):
	def __init__(self, parent, player):
		super().__init__(parent, fg_color=title_color)

		self.player = player

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)

		player_info_frame = ctk.CTkFrame(self, fg_color=title_color)
		player_info_frame.grid(column=0, row=0, sticky='nw', pady=20, padx=10, rowspan=2)

		player_info_frame.columnconfigure(0, weight=1)
		player_info_frame.rowconfigure(0, weight=1)
		player_info_frame.rowconfigure(0, weight=1)

		binary_data = base64.b64decode(player.get_img())
		player_image = Image.open(io.BytesIO(binary_data))
		img = ctk.CTkImage(dark_image=player_image, size=(150, 150))

		image_label = ctk.CTkLabel(player_info_frame, image=img, text='')
		image_label.grid(column=0, row=0, sticky='n', padx=20, pady=10)

		info_label = ctk.CTkLabel(
			player_info_frame,
			text=f'{player.get_birth_date()}\n{player.get_jersey_number()}\n{player.get_height()}',
			font=show_font)
		info_label.grid(column=0, row=1, pady=10)

		tabview = ctk.CTkTabview(
			master=self, segmented_button_selected_color='#555555',
			segmented_button_selected_hover_color='#555555', segmented_button_unselected_color=title_color,
			segmented_button_fg_color=title_color, segmented_button_unselected_hover_color='#666666',
			fg_color=title_color, text_color='white', width=350)
		tabview.grid(column=1, row=0, sticky='wesn', pady=4, rowspan=2)

		self.tab_1 = tabview.add("Ukupno")
		self.tab_2 = tabview.add("Po setovima")

		tabview._segmented_button._buttons_dict["Ukupno"].configure(font=show_font)
		tabview._segmented_button._buttons_dict["Po setovima"].configure(font=show_font)

		self.set_chart = GeneralSetChart(
			self.tab_2,
			self.player.get_points_per_set(),
			(5.6, 3.19),
			['Svi poeni', 'Iz napada', 'As poeni', 'Solo blokovi', 'Grupni blokovi', 'Greške'],
			['orange', "#3c7a9f", "#49bdb8", "#C387D5", "#8a5277", "#f08173"])
		self.set_chart.ax.xaxis.label.set_color(graph_bg)
		self.set_chart.grid(column=1, columnspan=2, row=1, sticky='we', padx=20)

		Width(self).grid(column=0, row=2, columnspan=3, pady=5, padx=50)

		# int(x) if x.is_integer() else x, for displaying block assists as ints and floats
		# all_points = self.player.get_all_points()
		# block_assists = self.player.get_block_assists() / 2

		self.all_points = ctk.CTkFrame(self.tab_1, fg_color=title_color)
		self.all_points.grid(column=1, columnspan=2, row=1, sticky='we', padx=20)

		self.points_table = Table(
			self.all_points,
			('points', 'overall'),
			['Poeni', 'Količina'],
			[130, 120],
			self.player.get_points_table())
		self.points_table.grid(column=0, row=0, sticky='wn')

		# self.radar = RadarGraph(
		# 	self.all_points,
		# 	[80, 60, 70, 90, 30, 80],
		# 	'orange',
		# 	(3, 3))
		# self.radar.grid(column=0, row=0, sticky='wn')

		self.points_pie_chart = PieChart(
			self.all_points,
			(3, 3.19),
			self.player.get_points_chart(),
			['Napad', "Servis", "Solo\nblok", "Grupni\nblok", "Greške"],
			["#3c7a9f", "#49bdb8", "#C387D5", "#8a5277", "#f08173"],
			'Podela poena',
			True)
		self.points_pie_chart.grid(column=1, row=0, sticky='w', padx=5)

	def update_chart_content(self):
		self.set_chart.update_chart_content(self.player.get_points_per_set())
		# self.points_table.update_table(self.player.get_points_table())
		self.points_pie_chart.update_chart_content(self.player.get_points_chart())


class PlayerAllStats(ctk.CTkTabview):
	def __init__(self, parent):
		super().__init__(
			parent, command=self.tab_coloring, text_color='white', border_width=1, fg_color='#282828', width=900
			,
			height=300)

		# self.grid(column=0, columnspan=2, row=3, sticky='we')
		# self.grid_propagate(False)
		#
		# height = int(self.winfo_screenheight() / 3.5)
		# self.configure(height=height)
		#
		# self.player = player

		# attack tab
		self.add("Napad")
		self.attack_tab = self.tab("Napad")
		self.attack_tab.columnconfigure(0, weight=1)
		self.attack_tab.columnconfigure(1, weight=1)
		self.attack_tab.columnconfigure(2, weight=1)
		self.attack_tab.columnconfigure(3, weight=1)

		self.attack_table = Table(
			self.attack_tab,
			('', 'amount', 'average'),
			['', 'Količina', 'Prosek'],
			[120, 90, 90],
			[
				('Poeni', 3),
				('Poeni po setu', 3),
				('Svi napadi', 3),
				('Greške', 3)],
		)
		# self.attack_table.grid(column=0, row=0, sticky='n')

		self.attack_pie_chart1 = PieChart(
			self.attack_tab,
			(3, 2),
			[3, 3, 2, 2],
			['Dijagonala', 'Paralela', 'Blok aut', 'Kuvanje'],
			["#008FD5", "#3B57B7", "#96B0C0", "#84B0CC"],
			'Osvojeni poeni')
		self.attack_pie_chart1.grid(column=1, row=0, pady=20)

		self.attack_pie_chart2 = PieChart(
			self.attack_tab,
			(3, 2),
			[3, 1, 2],
			['Prošao', 'Uhvaćen', 'Greška'],
			["orange", '#F8C666', 'grey'],
			'Ishod napada')
		self.attack_pie_chart2.grid(column=2, row=0, pady=20)

		self.attack_progress = ProgressPercentage(
			self.attack_tab,
			'napada',
			[5, 2, 3])
		# self.attack_progress.grid(column=0, row=0, sticky='s')

		self.attack_court_chart = CourtGraph(
			self.attack_tab,
			'app_images/court_blue.png',
			'#008FD5',
			[4, 4, 2, 2, 1],
			'Prolaz po zonama', (185, 160), show_font, ('Montserrat', 10, 'bold'))
		self.attack_court_chart.grid(column=3, row=0)

		# serve tab
		self.add("Servis")
		self.serve_tab = self.tab("Servis")
		self.serve_tab.columnconfigure(0, weight=1)
		self.serve_tab.columnconfigure(1, weight=2)
		self.serve_tab.columnconfigure(2, weight=1)

		# defence tab
		self.add("Odbrana")
		self.defence_tab = self.tab('Odbrana')
		self.defence_tab.columnconfigure(0, weight=1)
		self.defence_tab.columnconfigure(1, weight=1)
		self.defence_tab.columnconfigure(2, weight=1)
		self.defence_tab.columnconfigure(3, weight=1)

		# setting tab
		self.add("Dizanje")
		self.setting_tab = self.tab('Dizanje')
		self.setting_tab.columnconfigure(0, weight=1)
		self.setting_tab.columnconfigure(1, weight=1)
		self.setting_tab.columnconfigure(2, weight=1)
		self.setting_tab.columnconfigure(3, weight=1)

		# reception tab
		self.add("Prijem")
		self.reception_tab = self.tab("Prijem")
		self.reception_tab.columnconfigure(0, weight=1)
		self.reception_tab.columnconfigure(1, weight=2)
		self.reception_tab.columnconfigure(2, weight=1)

	def tab_coloring(self):
		colors = {
			"Napad": "#008FD5",
			"Servis": "#6D904F",
			"Odbrana": "#C84BED",
			"Dizanje": "#75660C",
			"Prijem": "#EC7063"}

		tab = self.get()

		self.configure(
			segmented_button_selected_color=colors[tab],
			segmented_button_selected_hover_color=colors[tab],
			border_color=colors[tab])


class PlayerAttack(ctk.CTkFrame):
	def __init__(self, parent, player):
		super().__init__(master=parent, fg_color=graph_bg, corner_radius=0)

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.player = player

		self.attack_pie_chart1 = PieChart(
			self,
			(2.8, 2),
			self.player.get_attack_type(),
			['Dijagonala', 'Paralela', 'Blok aut', 'Kuvanje'],
			["#008FD5", "#3B57B7", "#96B0C0", "#84B0CC"],
			'Osvojeni poeni')
		self.attack_pie_chart1.grid(column=0, row=0, pady=20, sticky='nsew')

		self.attack_pie_chart2 = PieChart(
			self,
			(2.8, 2),
			self.player.get_attack_outcome(),
			['Prošao', 'Uhvaćen', 'Greška'],
			["orange", '#F8C666', 'grey'],
			'Ishod napada')
		self.attack_pie_chart2.grid(column=1, row=0, pady=20, sticky='nsew')

		self.attack_progress = ProgressPercentage(
			self,
			'napada',
			self.player.get_attack_outcome())
		self.attack_progress.grid(column=0, row=1, sticky='w')

		self.attack_court_chart = CourtGraph(
			self,
			'app_images/court_blue.png',
			'#008FD5',
			self.player.get_attack_zones(),
			'Prolaz po zonama',
			(185, 160),
			('Montserrat', 13),
			('Montserrat', 11, 'bold'))
		self.attack_court_chart.grid(column=2, row=0, rowspan=2)

	def update_chart_content(self):
		self.attack_pie_chart1.update_chart_content(self.player.get_attack_type())
		self.attack_pie_chart2.update_chart_content(self.player.get_attack_outcome())
		self.attack_progress.update_data(self.player.get_attack_outcome())
		self.attack_court_chart.update_chart_content(self.player.get_attack_zones())


class PlayerServe(ctk.CTkFrame):
	def __init__(self, parent, player):
		super().__init__(master=parent, fg_color=graph_bg, corner_radius=0)

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)

		self.player = player

		self.serve_bar_chart = HBarChart(
			self,
			['Greške', 'Idealan', 'U 3 m', '  Pomeren', 'As'],
			self.player.get_serve_outcome(),
			['#f08173', '#AEB4AE', '#AEB4AE', '#81b64c', '#81b64c'],
			(4.9, 2.85))
		self.serve_bar_chart.ax.xaxis.label.set_color(graph_bg)
		self.serve_bar_chart.grid(column=0, row=0, sticky='wn', padx=5)

		self.serve_doughnut_chart = NestedDoughnut(
			self,
			['Smeč servis\n', 'Flot servis\n', 'Sa zemlje\n'],
			self.player.get_serve_doughnut_data(),
			['#467847', '#6D904F', '#9abd8f'],
			self.player.get_serve_doughnut_subdata(),
			['As + Pomeren', 'U 3m + Idealan', 'Greška'],
			(4, 2.85))
		self.serve_doughnut_chart.grid(column=1, row=0, sticky='se')

	def update_chart_content(self):
		self.serve_bar_chart.update_chart_content(self.player.get_serve_outcome())
		self.serve_doughnut_chart.update_chart_content(
			self.player.get_serve_doughnut_data(), self.player.get_serve_doughnut_subdata())


class PlayerDefense(ctk.CTkFrame):
	def __init__(self, parent, player):
		super().__init__(master=parent, fg_color=graph_bg, corner_radius=0)

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.rowconfigure(0, weight=1)

		self.player = player

		self.solo_blocks = CourtGraph(
			self,
			'app_images/court_purple.png',
			'#9A1FBF',
			self.player.get_solo_blocks(),
			'Solo blokovi',
			(185, 160),
			('Montserrat', 13),
			('Montserrat', 11, 'bold'))
		self.solo_blocks.grid(column=0, row=0, padx=13)

		self.group_blocks = CourtGraph(
			self,
			'app_images/court_light_purple.png',
			'#C387D5',
			self.player.get_group_blocks(),
			'Grupni blokovi',
			(185, 160),
			('Montserrat', 13),
			('Montserrat', 11, 'bold'))
		self.group_blocks.grid(column=1, row=0, padx=13)

		self.field_pie_chart = PieChart(
			self,
			(3.6, 2.35),
			self.player.get_digs(),
			['Od smeča', "Od kuvanja", "Od bloka", "Kontre"],
			["#84368C", "#C387D5", "#9A1FBF", "#895376"],
			"Uspešne odbrane")
		self.field_pie_chart.grid(column=2, row=0, pady=20, sticky='nsew')

	def update_chart_content(self):
		self.solo_blocks.update_chart_content(self.player.get_solo_blocks())
		self.group_blocks.update_chart_content(self.player.get_group_blocks())
		self.field_pie_chart.update_chart_content(self.player.get_digs())


class PlayerSetting(ctk.CTkFrame):
	def __init__(self, parent, player):
		super().__init__(master=parent, fg_color=graph_bg, corner_radius=0)

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)

		self.player = player

		self.setting_pie_chart = PieChart(
			self,
			(3, 2),
			self.player.get_easy_setting_outcomes(),
			['Prošao', 'Uhvaćen', 'Greška'],
			["orange", '#F8C666', 'grey'],
			'Iskoristljivost kontri')
		self.setting_pie_chart.grid(column=0, row=0, pady=20)

		self.setting_court_graph = CourtGraph(
			self,
			'app_images/court_yellow.png',
			'#F4D03F',
			self.player.get_setting_zones(),
			'Distribucija po zonama',
			(185, 160),
			('Montserrat', 13),
			('Montserrat', 11, 'bold'))
		self.setting_court_graph.grid(column=2, row=0)

		self.setting_bar_chart = BarChart2(
			self,
			['Korekcija', 'Primači', 'Srednjaci'],
			self.player.get_setting_positions(),
			["orange", '#F8C666', 'grey'],
			['Prošao', 'Uhvaćen', 'Zaustavljen'],
			'',
			(3.4, 2.85))
		self.setting_bar_chart.grid(column=1, row=0)

	def update_chart_content(self):
		self.setting_pie_chart.update_chart_content(self.player.get_easy_setting_outcomes())
		self.setting_court_graph.update_chart_content(self.player.get_setting_zones())
		self.setting_bar_chart.update_chart_content(self.player.get_setting_positions())


class PlayerReception(ctk.CTkFrame):
	def __init__(self, parent, player):
		super().__init__(master=parent, fg_color=graph_bg, corner_radius=0)

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)

		self.player = player

		self.serve_bar_chart = HBarChart(
			self,
			['Greške', 'Pomeren', 'U 3 m', 'Idealan'],
			self.player.get_reception_outcome(),
			['#f08173', '#AEB4AE', '#900C3F', '#900C3F'],
			(4.9, 2.85))
		self.serve_bar_chart.ax.xaxis.label.set_color(graph_bg)
		self.serve_bar_chart.grid(column=0, row=0, sticky='wn', padx=5)

		self.serve_doughnut_chart = NestedDoughnut(
			self,
			['Prstima\n', 'Čekićem\n'],
			self.player.get_reception_doughnut_data(),
			['#900C3F', '#EC7063'],
			self.player.get_reception_doughnut_subdata(),
			['Idealan + u 3m', 'Pomeren', 'Greška'],
			(4, 2.85))
		self.serve_doughnut_chart.grid(column=1, row=0, sticky='se')

	def update_chart_content(self):
		self.serve_bar_chart.update_chart_content(self.player.get_reception_outcome())
		self.serve_doughnut_chart.update_chart_content(
			self.player.get_reception_doughnut_data(), self.player.get_reception_doughnut_subdata())
