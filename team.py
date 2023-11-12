from graphs import *


class Team:
	def __init__(self, team_info):
		super().__init__()

		self.team_info = team_info

		# changeable data
		self.attack = None
		self.serve = None
		self.defense = None
		self.reception = None
		self.setting = None

		self.points = None

	def update_data(self, attack_data, defense_data, setting_data, points_per_set):
		self.attack = attack_data[0]
		self.serve = attack_data[1]
		self.defense = defense_data[0]
		self.reception = defense_data[1]
		self.setting = setting_data

		self.points = points_per_set

	def get_wins(self):
		return f'Pobede:  {self.team_info[0]}'

	def get_losses(self):
		return f'Porazi:  {self.team_info[1]}'

	def get_played_games(self):
		return f'Odigrane utakmice: {self.team_info[0] + self.team_info[1]}'

	# points
	def get_points_in_every_set(self):
		return {i + 1: set_distribution[0] for i, set_distribution in enumerate(self.points)}

	def get_points(self):
		all_blocks = sum(self.defense['solo_blocks_per_set']) \
					+ sum(self.defense['double_blocks_per_set']) \
					+ sum(self.defense['triple_blocks_per_set'])
		errors = sum(self.get_errors_per_set())

		return [self.attack['attack'][0], self.serve['serve'][0], all_blocks, errors]

	def get_points_per_set(self):
		all_blocks_per_set = list(map(
			lambda x, y, z: x + y + z,
			self.defense['solo_blocks_per_set'],
			self.defense['double_blocks_per_set'],
			self.defense['triple_blocks_per_set']))

		all_points_per_set = list(map(
			lambda a, b, c: a + b + c,
			self.attack['successful_attacks_per_set'],
			self.serve['as_serve_per_set'],
			all_blocks_per_set))

		return [
			all_points_per_set,
			self.attack['successful_attacks_per_set'],
			self.serve['as_serve_per_set'],
			all_blocks_per_set,
			self.get_errors_per_set()]

	def get_errors_per_set(self):
		return list(map(lambda a, b, c, d, e: a + b + c + d + e,
						self.attack['stopped_attacks_per_set'],
						self.serve['bad_serve_per_set'],
						self.defense['block_errors_per_set'],
						self.setting['setting_errors_per_set'],
						self.reception['error_per_set']))

	# attack
	def get_overall_efficiency(self):
		return self.attack['attack']

	def get_sets_efficiency(self):
		successful = self.attack['successful_attacks_per_set']
		caught = self.attack['caught_attacks_per_set']
		stopped = self.attack['stopped_attacks_per_set']
		return list(
			map(lambda x, y, z: round((x - z) / (x + y + z), 3) if x and y and z != 0 else 0, successful, caught, stopped))

	def get_attack_per_set(self):
		return [
			self.attack['successful_attacks_per_set'],
			self.attack['caught_attacks_per_set'],
			self.attack['stopped_attacks_per_set']
		]

	def get_all_attacks_zones(self):
		return self.attack['all_attack_zones']

	def get_successful_attacks_zones(self):
		return self.attack['successful_attack_zones']

	def get_successful_attack_types(self):
		return self.attack['successful_attack_types']

	# serve
	def get_serve_per_set_table(self):
		return [
			self.serve['good_serve_per_set'],
			self.serve['neutral_serve_per_set'],
			self.serve['bad_serve_per_set']]

	def get_serve_doughnut_data(self):
		return [sum(self.serve['spike_serve']), sum(self.serve['float_serve']), sum(self.serve['ground_serve'])]

	def get_serve_doughnut_subdata(self):
		serve_subdata = []
		for serve in ['spike_serve', 'float_serve', 'ground_serve']:
			serve_subdata += [
				self.serve[serve][0] + self.serve[serve][1],
				self.serve[serve][2] + self.serve[serve][3],
				self.serve[serve][4]]

		return serve_subdata

	def get_serve_outcome(self):
		serve = self.serve['serve'].copy()
		serve.reverse()
		return serve

	def get_serve_type_outcome(self):
		spike = self.serve['spike_serve'].copy()
		spike.reverse()
		flot = self.serve['float_serve'].copy()
		flot.reverse()
		return [spike, flot]

	# defense
	def get_blocks_per_set_chart(self):
		return [
			self.defense['solo_blocks_per_set'],
			self.defense['double_blocks_per_set'],
			self.defense['triple_blocks_per_set'],
			self.defense['block_errors_per_set']
		]

	def get_all_blocks_zone(self):
		return list(map(
			lambda x, y, z: x + y + z,
			self.defense['solo_blocks_per_zone'],
			self.defense['double_blocks_per_zone'],
			self.defense['triple_blocks_per_zone']))

	def get_solo_blocks_zone(self):
		return self.defense['solo_blocks_per_zone']

	def get_double_blocks_zone(self):
		return self.defense['double_blocks_per_zone']

	def get_triple_blocks_zone(self):
		return self.defense['triple_blocks_per_zone']

	def get_digs(self):
		return self.defense['digs']

	def get_digs_per_set(self):
		return self.defense['digs_per_set']

	# setting
	def get_setting_positions_overall(self):
		return [
			sum(self.setting['opposite_hitter_per_set']),
			sum(self.setting['outside_hitter_per_set']),
			sum(self.setting['middle_hitter_per_set'])]

	def get_setting_positions_per_set(self):
		return [
			self.setting['opposite_hitter_per_set'],
			self.setting['outside_hitter_per_set'],
			self.setting['middle_hitter_per_set']]

	def get_all_zones_setting(self):
		return self.setting['all_zones']

	def get_successful_zones_setting(self):
		return self.setting['successful_zones']

	def get_easy_setting_outcome_overall(self):
		return [
			sum(self.setting['successful_easy_setting']),
			sum(self.setting['caught_easy_setting']),
			sum(self.setting['stopped_easy_setting'])]

	def get_easy_setting_outcome_per_set(self):
		return [
			self.setting['successful_easy_setting'],
			self.setting['caught_easy_setting'],
			self.setting['stopped_easy_setting']]

	def get_easy_setting_position_overall(self):
		return [
			sum(self.setting['opposite_easy_setting']),
			sum(self.setting['outside_easy_setting']),
			sum(self.setting['middle_easy_setting'])]

	def get_easy_setting_position_per_set(self):
		return [
			self.setting['opposite_easy_setting'],
			self.setting['outside_easy_setting'],
			self.setting['middle_easy_setting']]

	def get_setting_progress(self):
		return self.setting['setting']

	def get_setting_court(self):
		return self.setting['zones']

	def get_outcome_setting(self):
		return [
			self.setting['successful_setting_per_set'],
			self.setting['caught_setting_per_set'],
			self.setting['unsuccessful_setting_per_set']]

	def get_positions_setting(self):
		return [
			self.setting['opposite_hitter_per_set'],
			self.setting['outside_hitter_per_set'],
			self.setting['middle_hitter_per_set']
		]

	# reception
	def get_reception_outcome(self):
		return self.reception['reception']

	def get_reception_type(self):
		return [self.reception['upper_reception'], self.reception['lower_reception']]

	def get_reception_doughnut_data(self):
		return [sum(self.reception['upper_reception']), sum(self.reception['lower_reception'])]

	def get_reception_doughnut_subdata(self):
		upper = [
			self.reception['upper_reception'][2] + self.reception['upper_reception'][3],
			self.reception['upper_reception'][1],
			self.reception['upper_reception'][0]]

		lower = [
			self.reception['lower_reception'][2] + self.reception['lower_reception'][3],
			self.reception['lower_reception'][1],
			self.reception['lower_reception'][0]]
		return upper + lower

	def get_reception_per_set(self):
		return [self.reception['good_per_set'], self.reception['neutral_per_set'], self.reception['error_per_set']]


class Points(ctk.CTkFrame):
	def __init__(self, parent, team):
		super().__init__(master=parent, fg_color=section_color)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)

		self.team = team

		points_img = Image.open('button_img/points.png')
		points = ctk.CTkImage(dark_image=points_img, size=(30, 30))

		self.points = Section(self, 'Poeni', points)
		self.points.grid(column=0, row=0)

		self.points_distribution_header = Header(self, 'Podela poena')
		self.points_distribution_header.grid(column=0, row=1, sticky='we')

	# points per set graph
		set_distribution = ctk.CTkFrame(self, fg_color=title_color)
		set_distribution.grid(column=0, row=2, sticky='we')

		set_distribution.columnconfigure(0, weight=1)
		set_distribution.columnconfigure(1, weight=10)
		set_distribution.rowconfigure(0, weight=1)
		set_distribution.rowconfigure(1, weight=1)
		set_distribution.rowconfigure(2, weight=1)

		ctk.CTkLabel(
			set_distribution, text='Po setovima', fg_color=title_color, height=title_height, anchor='w', font=title_font,
			padx=20, width=700).grid(column=0, row=0, sticky='we', columnspan=2)

		point_sequence = ctk.CTkFrame(set_distribution, fg_color=title_color)
		point_sequence.grid(column=1, row=0, rowspan=2, sticky='e', padx=20)

		ctk.CTkLabel(
			point_sequence, text='Najduža serija poena:', fg_color=title_color, height=30, anchor='w', font=show_font,
			padx=20).grid(column=0, row=0, columnspan=2)

		plus_img = Image.open('button_img/plus.png')
		plus = ctk.CTkImage(dark_image=plus_img, size=(20, 20))
		ctk.CTkLabel(
			point_sequence, text='7', fg_color=title_color, height=30, anchor='w',
			font=show_font, padx=5, image=plus, compound='left').grid(column=0, row=1)

		minus_img = Image.open('button_img/minus.png')
		minus = ctk.CTkImage(dark_image=minus_img, size=(20, 20))
		ctk.CTkLabel(
			point_sequence, text='5', fg_color=title_color, height=30, anchor='w',
			font=show_font, padx=5, image=minus, compound='left').grid(column=1, row=1)

		self.show = ctk.CTkLabel(
			set_distribution, text='Prikaži:', fg_color=title_color, height=title_height, anchor='w', font=show_font,
			padx=20)
		self.show.grid(column=0, row=1, sticky='w')

		self.points_in_all_sets = self.team.get_points_in_every_set()

		self.set_charts = []
		self.set_sections_charts = []
		for i in range(len(self.points_in_all_sets), 0, -1):
			point_distribution_chart = PointsDistribution(
				set_distribution, self.points_in_all_sets[i], (8, 2))
			point_distribution_chart.grid(column=0, row=2, columnspan=2, pady=30, padx=80)

			self.set_charts.append(point_distribution_chart)

			set_section_points = SetSectionPoints(
				set_distribution, self.points_in_all_sets[i], (8, 3))
			set_section_points.grid(column=0, row=3, columnspan=2, pady=30, padx=80)
			self.set_sections_charts.append(set_section_points)

		self.selected_set = ctk.StringVar(value='1. Set')
		self.set_button = ctk.CTkSegmentedButton(
			set_distribution, values=[f'{set_number}. Set' for set_number in range(1, len(self.points_in_all_sets) + 1)],
			font=show_font, fg_color=title_color, variable=self.selected_set, command=self.toggle,
			selected_color='#51504c', unselected_color=title_color, selected_hover_color='#51504c',
			unselected_hover_color='#51504c')
		self.set_button.grid(column=1, row=1, sticky='w')

	# different point types
		point_types = FinishedGraph(self, 'Po tipu')
		point_types.grid(column=0, row=3, sticky='we', pady=2)
		self.doughnut_points = PieChart2(
			point_types,
			(8, 4),
			self.team.get_points(),
			['Napad', "Servis", "Blok", "Greške"],
			["#3c7a9f", "#49bdb8", "#f4bc4e", "#f08173"])
		self.doughnut_points.grid(column=0, row=1, pady=30, padx=80)

	# set and type distribution
		type_and_set = FinishedGraph(self, 'Po tipu i setu')
		type_and_set.grid(column=0, row=4, sticky='we')
		self.type_and_set_chart = GeneralSetChart(
			type_and_set,
			self.team.get_points_per_set(),
			(8, 4),
			['Svi poeni', 'Iz napada', 'As poeni', 'Blokovi', 'Greške'],
			['#81b64c', '#3c7a9f', '#49bdb8', '#f4bc4e', '#f08173'])
		self.type_and_set_chart.grid(column=0, row=1, pady=30, padx=80)

	def toggle(self, _):
		sets = self.set_charts.copy()
		set_section = self.set_sections_charts.copy()

		sets.reverse()
		set_section.reverse()

		selection = int(self.selected_set.get()[0]) - 1

		selected = sets.pop(selection)
		selected_set_section = set_section.pop(selection)

		selected.grid(column=0, row=2, columnspan=2, pady=30, padx=80)
		selected_set_section.grid(column=0, row=3, columnspan=2, pady=30, padx=80)

		for unselected in sets:
			unselected.grid_forget()

		for unselected in set_section:
			unselected.grid_forget()

	def longest_point_streak(self):
		for set_points in self.points_in_all_sets.items():
			for point in set_points:
				pass

	def get_headers(self):
		return self.points_distribution_header

	def update_chart_content(self):
		pass


class Attack(ctk.CTkFrame):
	def __init__(self, parent, team):
		super().__init__(master=parent, fg_color=section_color)

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

		self.team = team

		attack_img = Image.open('button_img/attacks.png')
		attack = ctk.CTkImage(dark_image=attack_img, size=(30, 30))

		Section(self, 'Napad', attack).grid(column=0, row=0)

		self.efficiency_header = Header(self, 'Efikasnost napada')
		self.efficiency_header.grid(column=0, row=1, sticky='we')

		self.attack_progress = ProgressPercentage(self, 'napada', self.team.get_overall_efficiency())
		self.attack_progress.grid(column=0, row=1, sticky='e', padx=30)

	# efficiency
		efficiency = FinishedGraph(self, 'Po setovima', True)
		efficiency.grid(column=0, row=2, sticky='we')
		self.efficiency_per_set = EfficiencyGraph(
			efficiency,
			self.team.get_sets_efficiency(),
			'#3c7a9f',
			(8, 4))
		self.efficiency_per_set.grid(column=0, row=1, pady=30)

		successful = ctk.CTkFrame(self, fg_color=title_color)
		successful.grid(column=0, row=3, sticky='we', pady=2)

		successful.columnconfigure(0, weight=1)
		successful.columnconfigure(1, weight=10)
		successful.rowconfigure(0, weight=1)
		successful.rowconfigure(1, weight=1)
		successful.rowconfigure(2, weight=1)

		ctk.CTkLabel(
			successful, text='Po uspešnosti', fg_color=title_color, height=title_height, anchor='w', font=title_font,
			padx=20, width=800).grid(column=0, row=0, sticky='w', columnspan=2, pady=4)

		self.show = ctk.CTkLabel(
			successful, text='Prikaži:', fg_color=title_color, height=title_height, anchor='w', font=show_font,
			padx=20)
		self.show.grid(column=0, row=1, sticky='w')

		self.selected_graph = ctk.StringVar(value='Ukupno')
		self.selection_button = ctk.CTkSegmentedButton(
			successful, values=['Ukupno', 'Po setovima'], font=show_font, fg_color=title_color,
			selected_color='#51504c', unselected_color=title_color, selected_hover_color='#51504c',
			unselected_hover_color='#51504c', variable=self.selected_graph, command=self.toggle
		)
		self.selection_button.grid(column=1, row=1, sticky='w')

	# set and successfulness distribution
		self.successful_and_set_chart = AttackChart2(
			successful,
			self.team.get_attack_per_set(),
			["#3c7a9f", "#A7C7E7", "#f08173"],
			['Uspešni napadi', "Uhvaćeni napadi", "Greške iz napada"],
			(8, 4))
		self.successful_and_set_chart.grid(column=0, row=2, pady=30, columnspan=2, padx=80)

	# successfulness of attack
		self.doughnut_successfulness = PieChart2(
			successful,
			(8, 4),
			self.team.get_overall_efficiency(),
			['Uspešni napadi', "Uhvaćeni napadi", "Greške iz napada"],
			["#3c7a9f", "#A7C7E7", "#f08173"])
		self.doughnut_successfulness.grid(column=0, row=2, pady=30, columnspan=2, padx=80)

		Separator(self).grid(column=0, row=4, sticky='w')

	# distribution
		self.attack_header = Header(self, 'Podela uspešnih napada')
		self.attack_header.grid(column=0, row=5, sticky='we')

		zone_distribution = FinishedGraph(self, 'Po zonama', True)
		zone_distribution.grid(column=0, row=6, sticky='we')
		self.zone_successful_attacks = CourtGraph(
			zone_distribution,
			'app_images/court_blue.png',
			'#008FD5',
			self.team.get_successful_attacks_zones(),
			'Uspešni napadi',
			(300, 280),
			title_font,
			title_font)
		self.zone_successful_attacks.grid(column=0, row=1, pady=30, sticky='w', padx=80)

		self.zone_all_attacks = CourtGraph(
			zone_distribution,
			'app_images/court_blue.png',
			'#008FD5',
			self.team.get_all_attacks_zones(),
			'Svi napadi',
			(300, 280),
			title_font,
			title_font)
		self.zone_all_attacks.grid(column=0, row=1, pady=30, sticky='e', padx=80)

		type_distribution = FinishedGraph(self, 'Po tipu napada')
		type_distribution.grid(column=0, row=7, sticky='we', pady=2)
		self.doughnut_type = PieChart2(
			type_distribution,
			(8, 4),
			self.team.get_successful_attack_types(),
			['Dijagonala', "Paralela", "Kuvanje", "Blok-aut"],
			['#3c3484', '#4A0CCB', '#008FD5', '#A7C7E7'])
		self.doughnut_type.grid(column=0, row=1, pady=30, padx=80)

		# attacker_position_distribution = FinishedGraph(self, 'Po pozicijama')
		# attacker_position_distribution.grid(column=0, row=8, sticky='we')
		# self.doughnut_position = PieChart2(
		# 	attacker_position_distribution,
		# 	(8, 4),
		# 	[6, 5, 3, 1, 0],
		# 	['Primači', 'Korekcija', 'Srednjaci', 'Dizači', 'Libero'],
		# 	['#EC7063', '#3c7a9f', '#f4bc4e', 'yellow', 'purple'])
		# self.doughnut_position.grid(column=0, row=1, pady=30, padx=80)

	def toggle(self, _):
		graphs = [self.doughnut_successfulness, self.successful_and_set_chart]
		blocks_dict = {'Ukupno': 0, 'Po setovima': 1}
		selection = blocks_dict[self.selected_graph.get()]

		selected = graphs.pop(selection)
		selected.grid(column=0, row=2, pady=30, columnspan=2, padx=80)
		graphs[0].grid_forget()

	def get_headers(self):
		return [self.efficiency_header, self.attack_header]

	def update_chart_content(self):
		self.efficiency_per_set.update_chart_content(self.team.get_sets_efficiency())
		self.successful_and_set_chart.update_chart_content(self.team.get_attack_per_set())
		self.doughnut_successfulness.update_chart_content(self.team.get_overall_efficiency())
		self.zone_successful_attacks.update_chart_content(self.team.get_successful_attacks_zones())
		self.zone_all_attacks.update_chart_content(self.team.get_all_attacks_zones())
		self.doughnut_type.update_chart_content(self.team.get_successful_attack_types())
		# self.doughnut_position.update_chart_content()


class Serve(ctk.CTkFrame):
	def __init__(self, parent, team):
		super().__init__(master=parent, fg_color=section_color)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)

		self.team = team

		serve_img = Image.open('button_img/serve.png')
		serve = ctk.CTkImage(dark_image=serve_img, size=(30, 30))

		Section(self, 'Servis', serve).grid(column=0, row=0)

		self.serve_distribution_header = Header(self, 'Podela servisa')
		self.serve_distribution_header.grid(column=0, row=1, sticky='we')

		serve_per_set = FinishedGraph(self, 'Po setovima i uspešnosti', True)
		serve_per_set.grid(column=0, row=2, sticky='we')
		self.serve_per_set_chart = AttackChart2(
			serve_per_set,
			self.team.get_serve_per_set_table(),
			['#81b64c', '#AEB4AE', '#f08173'],
			['As servis i pomeren prijem', "Idealan i prijem u 3m", "Greške iz servisa"],
			(8, 4))
		self.serve_per_set_chart.grid(column=0, row=1, pady=30, padx=80)

		serve_per_type = FinishedGraph(self, 'Po vrsti i uspešnosti')
		serve_per_type.grid(column=0, row=3, sticky='we', pady=2)
		self.serve_doughnut = NestedDoughnut(
			serve_per_type,
			['Smeč servis', 'Flot servis', 'Sa zemlje'],
			self.team.get_serve_doughnut_data(),
			['#467847', '#6D904F', '#9abd8f'],
			self.team.get_serve_doughnut_subdata(),
			['As + Pomeren', 'U 3m + Idealan', 'Greška'],
			(8, 4),
			True)
		self.serve_doughnut.grid(column=0, row=1, pady=30, padx=80)

		Separator(self).grid(column=0, row=4, sticky='w')

		self.serve_outcome_header = Header(self, 'Ishod servisa')
		self.serve_outcome_header.grid(column=0, row=5, sticky='we')

		overall = FinishedGraph(self, 'Ukupno', True)
		overall.grid(column=0, row=6, sticky='we')
		self.horizontal_serve_chart = HBarChart(
			overall,
			['Servis\ngreške', 'Idealan\nprijem', 'Prijem\nu 3 m', 'Pomeren\nprijem', 'As servis'],
			self.team.get_serve_outcome(),
			['#f08173', '#AEB4AE', '#AEB4AE', '#81b64c', '#81b64c'],
			(8, 4))
		self.horizontal_serve_chart.grid(column=0, row=1, pady=30, padx=80)

		serve_type = FinishedGraph(self, 'Po vrsti servisa')
		serve_type.grid(column=0, row=7, sticky='we', pady=2)
		self.double_horizontal_serve_chart = HBarChart2(
			serve_type,
			['Servis\ngreške', 'Idealan\nprijem', 'Prijem\nu 3 m', 'Pomeren\nprijem', 'As servis'],
			self.team.get_serve_type_outcome(),
			['#467847', '#6D904F'],
			(8, 4),
			['Smeč servis', 'Flot servis'])
		self.double_horizontal_serve_chart.grid(column=0, row=1, pady=30, padx=80)

	def get_headers(self):
		return [self.serve_distribution_header, self.serve_outcome_header]

	def update_chart_content(self):
		self.serve_per_set_chart.update_chart_content(self.team.get_serve_per_set_table())
		self.serve_doughnut.update_chart_content(self.team.get_serve_doughnut_data(), self.team.get_serve_doughnut_subdata())
		self.horizontal_serve_chart.update_chart_content(self.team.get_serve_outcome())
		self.double_horizontal_serve_chart.update_chart_content(self.team.get_serve_type_outcome())


class Defense(ctk.CTkFrame):
	def __init__(self, parent, team):
		super().__init__(master=parent, fg_color=section_color)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)

		self.team = team

		defense_img = Image.open('button_img/defense.png')
		defense = ctk.CTkImage(dark_image=defense_img, size=(30, 30))

		Section(self, 'Odbrana', defense).grid(column=0, row=0)

		self.blocks_header = Header(self, 'Podela blokova')
		self.blocks_header.grid(column=0, row=1, sticky='we')

		blocks_zone = ctk.CTkFrame(self, fg_color=title_color)
		blocks_zone.grid(column=0, row=2, sticky='we')

		blocks_zone.columnconfigure(0, weight=1)
		blocks_zone.columnconfigure(1, weight=10)
		blocks_zone.rowconfigure(0, weight=1)
		blocks_zone.rowconfigure(1, weight=1)
		blocks_zone.rowconfigure(2, weight=1)

		ctk.CTkLabel(
			blocks_zone, text='Po zonama', fg_color=title_color, height=title_height, anchor='w', font=title_font,
			padx=20, width=800).grid(column=0, row=0, sticky='w', columnspan=2)

		ctk.CTkLabel(
			blocks_zone, text='Prikaži:', fg_color=title_color, height=title_height, anchor='w', font=show_font,
			padx=20).grid(column=0, row=1, sticky='w')

		self.selected_graph = ctk.StringVar(value='Dvojni blokovi')
		self.selection_button = ctk.CTkSegmentedButton(
			blocks_zone, values=['Solo blokovi', 'Dvojni blokovi', 'Trojni blokovi'], font=show_font, fg_color=title_color,
			selected_color='#51504c', unselected_color=title_color, selected_hover_color='#51504c',
			unselected_hover_color='#51504c', variable=self.selected_graph, command=lambda event: self.toggle(event, 1)
		)
		self.selection_button.grid(column=1, row=1, sticky='w')

		self.zone_blocks = CourtGraph(
			blocks_zone,
			'app_images/court_red_purple.png',
			'#8a5277',
			self.team.get_all_blocks_zone(),
			'Svi blokovi',
			(300, 280),
			title_font,
			title_font)
		self.zone_blocks.grid(column=0, row=2, pady=30, sticky='w', padx=80, columnspan=2)

		self.solo_blocks = CourtGraph(
			blocks_zone,
			'app_images/court_purple.png',
			'#9A1FBF',
			self.team.get_solo_blocks_zone(),
			'Solo blokovi',
			(300, 280),
			title_font,
			title_font)
		self.solo_blocks.grid(column=0, row=2, pady=30, sticky='e', padx=80, columnspan=2)

		self.triple_blocks = CourtGraph(
			blocks_zone,
			'app_images/court_red_purple.png',
			"#895376",
			self.team.get_triple_blocks_zone(),
			'Trojni blokovi',
			(300, 280),
			title_font,
			title_font)
		self.triple_blocks.grid(column=0, row=2, pady=30, sticky='e', padx=80, columnspan=2)

		self.double_blocks = CourtGraph(
			blocks_zone,
			'app_images/court_light_purple.png',
			'#C387D5',
			self.team.get_double_blocks_zone(),
			'Dvojni blokovi',
			(300, 280),
			title_font,
			title_font)
		self.double_blocks.grid(column=0, row=2, pady=30, sticky='e', padx=80, columnspan=2)

		blocks_and_set = FinishedGraph(self, 'Po setovima')
		blocks_and_set.grid(column=0, row=3, sticky='we', pady=2)
		self.block_and_set_chart = AttackChart2(
			blocks_and_set,
			self.team.get_blocks_per_set_chart(),
			['#9A1FBF', '#C387D5', "#895376", '#f08173'],
			['Solo blokovi', "Dvojni blokovi", "Trojni blokovi", "Greške"],
			(8, 4))
		self.block_and_set_chart.grid(column=0, row=1, pady=30, padx=80)

		Separator(self).grid(column=0, row=4, sticky='w')

		self.field_header = Header(self, 'Podela polja')
		self.field_header.grid(column=0, row=5, sticky='we')

		# field = FinishedGraph(self, 'Po tipu odbrane', True)
		# field.grid(column=0, row=6, sticky='we')

		field = ctk.CTkFrame(self, fg_color=title_color)
		field.grid(column=0, row=6, sticky='we')

		field.columnconfigure(0, weight=1)
		field.columnconfigure(1, weight=10)
		field.rowconfigure(0, weight=1)
		field.rowconfigure(1, weight=1)
		field.rowconfigure(2, weight=1)

		ctk.CTkLabel(
			field, text='Po tipu odbrane', fg_color=title_color, height=title_height, anchor='w', font=title_font,
			padx=20, width=800).grid(column=0, row=0, sticky='w', columnspan=2)

		ctk.CTkLabel(
			field, text='Prikaži:', fg_color=title_color, height=title_height, anchor='w', font=show_font,
			padx=20).grid(column=0, row=1, sticky='w')

		self.selected_field = ctk.StringVar(value='Ukupno')
		self.selection_field_button = ctk.CTkSegmentedButton(
			field, values=['Ukupno', 'Po setovima'], font=show_font, fg_color=title_color,
			selected_color='#51504c', unselected_color=title_color, selected_hover_color='#51504c',
			unselected_hover_color='#51504c', variable=self.selected_field, command=lambda event: self.toggle(event, 2)
		)
		self.selection_field_button.grid(column=1, row=1, sticky='w')

		self.field_per_set = AttackChart2(
			field,
			self.team.get_digs_per_set(),
			['#EC7063', '#3c7a9f', '#f4bc4e', 'purple'],
			['Od smeča', 'Od kuvanja', 'Od bloka', 'Kontre'],
			(8, 4))
		self.field_per_set.grid(column=0, row=2, pady=30, columnspan=2, padx=80)

		self.doughnut_field = PieChart2(
			field,
			(8, 4),
			self.team.get_digs(),
			['Od smeča', 'Od kuvanja', 'Od bloka', 'Kontre'],
			['#EC7063', '#3c7a9f', '#f4bc4e', 'purple'])
		self.doughnut_field.grid(column=0, row=2, columnspan=2, pady=30, padx=80)

	def toggle(self, _, x):
		key = None
		graphs = None
		tabs_dict = None

		if x == 1:
			graphs = [self.solo_blocks, self.double_blocks, self.triple_blocks]
			key = self.selected_graph.get()
			tabs_dict = {'Solo blokovi': 0, 'Dvojni blokovi': 1, 'Trojni blokovi': 2}

		elif x == 2:
			graphs = [self.doughnut_field, self.field_per_set]
			key = self.selected_field.get()
			tabs_dict = {'Ukupno': 0, 'Po setovima': 1}

		selection = tabs_dict[key]

		selected = graphs.pop(selection)
		selected.grid(column=0, row=2, pady=30, columnspan=2, padx=80, sticky='e' if x == 1 else None)

		for unselected in graphs:
			unselected.grid_forget()

	def get_headers(self):
		return [self.blocks_header, self.field_header]

	def update_chart_content(self):
		self.zone_blocks.update_chart_content(self.team.get_all_blocks_zone())
		self.solo_blocks.update_chart_content(self.team.get_solo_blocks_zone())
		self.triple_blocks.update_chart_content(self.team.get_triple_blocks_zone())
		self.double_blocks.update_chart_content(self.team.get_double_blocks_zone())
		self.block_and_set_chart.update_chart_content(self.team.get_blocks_per_set_chart())
		self.field_per_set.update_chart_content(self.team.get_digs_per_set())
		self.doughnut_field.update_chart_content(self.team.get_digs())


class Setting(ctk.CTkFrame):
	def __init__(self, parent, team):
		super().__init__(master=parent, fg_color=section_color)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)

		self.team = team

		setting_img = Image.open('button_img/lifting.png').crop((100, 100, 400, 400))
		setting = ctk.CTkImage(dark_image=setting_img, size=(30, 30))

		Section(self, 'Dizanje', setting).grid(column=0, row=0)

		self.setting_distribution_header = Header(self, 'Podela dizanja')
		self.setting_distribution_header.grid(column=0, row=1, sticky='we')

		setting_positions = ctk.CTkFrame(self, fg_color=title_color)
		setting_positions.grid(column=0, row=2, sticky='we')

		setting_positions.columnconfigure(0, weight=1)
		setting_positions.columnconfigure(1, weight=10)
		setting_positions.rowconfigure(0, weight=1)
		setting_positions.rowconfigure(1, weight=1)
		setting_positions.rowconfigure(2, weight=1)

		ctk.CTkLabel(
			setting_positions, text='Po pozicijama', fg_color=title_color, height=title_height, anchor='w', font=title_font,
			padx=20, width=800).grid(column=0, row=0, sticky='w', columnspan=2)

		self.show = ctk.CTkLabel(
			setting_positions, text='Prikaži:', fg_color=title_color, height=title_height, anchor='w', font=show_font,
			padx=20)
		self.show.grid(column=0, row=1, sticky='w')

		self.selected_graph = ctk.StringVar(value='Ukupno')
		self.selection_button = ctk.CTkSegmentedButton(
			setting_positions, values=['Ukupno', 'Po setovima'], font=show_font, fg_color=title_color,
			selected_color='#51504c', unselected_color=title_color, selected_hover_color='#51504c',
			unselected_hover_color='#51504c', variable=self.selected_graph, command=lambda event: self.toggle(event, 1)
		)
		self.selection_button.grid(column=1, row=1, sticky='w')

		self.set_setting = AttackChart2(
			setting_positions,
			self.team.get_setting_positions_per_set(),
			["#F4D03F", "#C6AE16", "#75660C"],
			['Korekcija', 'Primači', 'Srednjaci'],
			(8, 4))
		self.set_setting.grid(column=0, row=2, pady=30, columnspan=2, padx=80)

		self.doughnut_setting = PieChart2(
			setting_positions,
			(8, 4),
			self.team.get_setting_positions_overall(),
			['Korekcija', 'Primači', 'Srednjaci'],
			["#F4D03F", "#C6AE16", "#75660C"])
		self.doughnut_setting.grid(column=0, row=2, pady=30, columnspan=2, padx=80)

		zone_setting = FinishedGraph(self, 'Po zonama')
		zone_setting.grid(column=0, row=3, sticky='we', pady=2)
		self.all_setting_zone = CourtGraph(
			zone_setting,
			'app_images/court_yellow.png',
			'#F4D03F',
			self.team.get_all_zones_setting(),
			'Sva dizanja',
			(300, 280),
			title_font,
			title_font)
		self.all_setting_zone.grid(column=0, row=2, pady=30, sticky='e', padx=80)

		self.successful_setting_zone = CourtGraph(
			zone_setting,
			'app_images/court_yellow.png',
			'#F4D03F',
			self.team.get_successful_zones_setting(),
			'Uspešna dizanja',
			(300, 280),
			title_font,
			title_font)
		self.successful_setting_zone.grid(column=0, row=2, pady=30, sticky='w', padx=80)

		Separator(self).grid(column=0, row=4, sticky='w')

		self.setting_usability_header = Header(self, 'Iskoristljivost dizanja kod dobrog prijema i kontri')
		self.setting_usability_header.grid(column=0, row=5, sticky='we')

		setting_outcome = ctk.CTkFrame(self, fg_color=title_color)
		setting_outcome.grid(column=0, row=6, sticky='we')

		setting_outcome.columnconfigure(0, weight=1)
		setting_outcome.columnconfigure(1, weight=10)
		setting_outcome.rowconfigure(0, weight=1)
		setting_outcome.rowconfigure(1, weight=1)
		setting_outcome.rowconfigure(2, weight=1)

		ctk.CTkLabel(
			setting_outcome, text='Po ishodu', fg_color=title_color, height=title_height, anchor='w', font=title_font,
			padx=20, width=800).grid(column=0, row=0, sticky='w', columnspan=2)

		ctk.CTkLabel(
			setting_outcome, text='Prikaži:', fg_color=title_color, height=title_height, anchor='w', font=show_font,
			padx=20).grid(column=0, row=1, sticky='w')

		self.selected_outcome_graph = ctk.StringVar(value='Ukupno')
		self.selection_button = ctk.CTkSegmentedButton(
			setting_outcome, values=['Ukupno', 'Po setovima'], font=show_font, fg_color=title_color,
			selected_color='#51504c', unselected_color=title_color, selected_hover_color='#51504c',
			unselected_hover_color='#51504c', variable=self.selected_outcome_graph, command=lambda event: self.toggle(event, 2)
		)
		self.selection_button.grid(column=1, row=1, sticky='w')

		self.set_setting_outcome = AttackChart2(
			setting_outcome,
			self.team.get_easy_setting_outcome_per_set(),
			["#3c7a9f", "#A7C7E7", "#f08173"],
			['Uspešni napadi', "Uhvaćeni napadi", "Greške iz napada"],
			(8, 4))
		self.set_setting_outcome.grid(column=0, row=2, pady=30, columnspan=2, padx=80)

		self.doughnut_setting_outcome = PieChart2(
			setting_outcome,
			(8, 4),
			self.team.get_easy_setting_outcome_overall(),
			['Uspešni napadi', "Uhvaćeni napadi", "Greške iz napada"],
			["#3c7a9f", "#A7C7E7", "#f08173"])
		self.doughnut_setting_outcome.grid(column=0, row=2, pady=30, columnspan=2, padx=80)

		position_outcome = ctk.CTkFrame(self, fg_color=title_color)
		position_outcome.grid(column=0, row=7, sticky='we', pady=2)

		position_outcome.columnconfigure(0, weight=1)
		position_outcome.columnconfigure(1, weight=10)
		position_outcome.rowconfigure(0, weight=1)
		position_outcome.rowconfigure(1, weight=1)
		position_outcome.rowconfigure(2, weight=1)

		ctk.CTkLabel(
			position_outcome, text='Po pozicijama', fg_color=title_color, height=title_height, anchor='w', font=title_font,
			padx=20, width=800).grid(column=0, row=0, sticky='w', columnspan=2, pady=4)

		ctk.CTkLabel(
			position_outcome, text='Prikaži:', fg_color=title_color, height=title_height, anchor='w', font=show_font,
			padx=20).grid(column=0, row=1, sticky='w')

		self.selected_position_outcome_graph = ctk.StringVar(value='Ukupno')
		self.selection_button = ctk.CTkSegmentedButton(
			position_outcome, values=['Ukupno', 'Po setovima'], font=show_font, fg_color=title_color,
			selected_color='#51504c', unselected_color=title_color, selected_hover_color='#51504c',
			unselected_hover_color='#51504c', variable=self.selected_position_outcome_graph,
			command=lambda event: self.toggle(event, 3)
		)
		self.selection_button.grid(column=1, row=1, sticky='w')

		self.set_position_outcome = AttackChart2(
			position_outcome,
			self.team.get_easy_setting_position_per_set(),
			["#F4D03F", "#C6AE16", "#75660C"],
			['Korekcija', 'Primači', 'Srednjaci'],
			(8, 4))
		self.set_position_outcome.grid(column=0, row=2, pady=30, columnspan=2, padx=80)

		self.doughnut_position_outcome = PieChart2(
			position_outcome,
			(8, 4),
			self.team.get_easy_setting_position_overall(),
			['Korekcija', 'Primači', 'Srednjaci'],
			["#F4D03F", "#C6AE16", "#75660C"])
		self.doughnut_position_outcome.grid(column=0, row=2, pady=30, columnspan=2, padx=80)

	def toggle(self, _, x):
		key = None
		graphs = None

		if x == 1:
			graphs = [self.doughnut_setting, self.set_setting]
			key = self.selected_graph.get()
		elif x == 2:
			graphs = [self.doughnut_setting_outcome, self.set_setting_outcome]
			key = self.selected_outcome_graph.get()
		elif x == 3:
			graphs = [self.doughnut_position_outcome, self.set_position_outcome]
			key = self.selected_position_outcome_graph.get()

		tabs_dict = {'Ukupno': 0, 'Po setovima': 1}
		selection = tabs_dict[key]

		selected = graphs.pop(selection)
		selected.grid(column=0, row=2, pady=30, columnspan=2, padx=80)
		graphs[0].grid_forget()

	def get_headers(self):
		return [self.setting_distribution_header, self.setting_usability_header]

	def update_chart_content(self):
		self.set_setting.update_chart_content(self.team.get_setting_positions_per_set())
		self.doughnut_setting.update_chart_content(self.team.get_setting_positions_overall())
		self.all_setting_zone.update_chart_content(self.team.get_all_zones_setting())
		self.successful_setting_zone.update_chart_content(self.team.get_successful_zones_setting())
		self.set_setting_outcome.update_chart_content(self.team.get_easy_setting_outcome_per_set())
		self.doughnut_setting_outcome.update_chart_content(self.team.get_easy_setting_outcome_overall())
		self.set_position_outcome.update_chart_content(self.team.get_easy_setting_position_per_set())
		self.doughnut_position_outcome.update_chart_content(self.team.get_easy_setting_position_overall())


class Reception(ctk.CTkFrame):
	def __init__(self, parent, team):
		super().__init__(master=parent, fg_color=section_color)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)

		self.team = team

		setting_img = Image.open('button_img/hammer.png')
		setting = ctk.CTkImage(dark_image=setting_img, size=(30, 30))

		Section(self, 'Prijem', setting).grid(column=0, row=0)

		self.reception_outcome_header = Header(self, 'Ishod prijema')
		self.reception_outcome_header.grid(column=0, row=1, sticky='we')

		overall = FinishedGraph(self, 'Ukupno', True)
		overall.grid(column=0, row=2, sticky='we')
		self.horizontal_reception_chart = HBarChart(
			overall,
			['Greške u\nprijemu', 'Pomeren\nprijem', 'Prijem u\n3 m', 'Idealan\nprijem'],
			self.team.get_reception_outcome(),
			['#f08173', '#AEB4AE', '#900C3F', '#900C3F'],
			(8, 4))
		self.horizontal_reception_chart.grid(column=0, row=1, pady=30, padx=80)

		reception_type = FinishedGraph(self, 'Po vrsti prijema')
		reception_type.grid(column=0, row=3, sticky='we', pady=2)
		self.horizontal_reception = HBarChart2(
			reception_type,
			['Greške u\nprijemu', 'Pomeren\nprijem', 'Prijem u\n3 m', 'Idealan\nprijem'],
			self.team.get_reception_type(),
			['#900C3F', '#EC7063'],
			(8, 4),
			['Prijem prstima', 'Prijem čekićem'])
		self.horizontal_reception.grid(column=0, row=1, pady=30, padx=80)

		Separator(self).grid(column=0, row=4, sticky='w')

		self.reception_distribution_header = Header(self, 'Podela prijema')
		self.reception_distribution_header.grid(column=0, row=5, sticky='we')

		nested_reception = FinishedGraph(self, 'Po vrsti', True)
		nested_reception.grid(column=0, row=6, sticky='we')
		self.nested_doughnut_reception = NestedDoughnut(
			nested_reception,
			['Prijem prstima', 'Prijem čekićem'],
			self.team.get_reception_doughnut_data(),
			['#900C3F', '#EC7063'],
			self.team.get_reception_doughnut_subdata(),
			['Idealan + u 3m', 'Pomeren', 'Greška'],
			(8, 4),
			True)
		self.nested_doughnut_reception.grid(column=0, row=1, pady=30, padx=80)

		set_reception = FinishedGraph(self, 'Po setovima')
		set_reception.grid(column=0, row=7, sticky='we', pady=2)
		self.reception_per_set_chart = AttackChart2(
			set_reception,
			self.team.get_reception_per_set(),
			['#81b64c', '#AEB4AE', '#f08173'],
			["Idealan i prijem u 3m", 'Pomeren prijem', "Greške iz prijema"],
			(8, 4))
		self.reception_per_set_chart.grid(column=0, row=1, pady=30, padx=80)

	def get_headers(self):
		return [self.reception_outcome_header, self.reception_distribution_header]

	def update_chart_content(self):
		self.horizontal_reception_chart.update_chart_content(self.team.get_reception_outcome())
		self.horizontal_reception.update_chart_content(self.team.get_reception_type())
		self.nested_doughnut_reception.update_chart_content(
			self.team.get_reception_doughnut_data(), self.team.get_reception_doughnut_subdata())
		self.reception_per_set_chart.update_chart_content(self.team.get_reception_per_set())
