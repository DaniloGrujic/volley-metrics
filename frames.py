from team import *
from player import *


class Filters(ctk.CTkFrame):
	def __init__(self, parent, all_games, get_filter):
		super().__init__(master=parent, fg_color='#2c2b28', border_width=0)

		self.place(relx=0, rely=0, relwidth=0.1, relheight=1)

		self.columnconfigure(0, weight=2)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)
		self.rowconfigure(8, weight=3)
		self.rowconfigure(9, weight=1)

		self.all_games = all_games
		self.get_filter = get_filter

		self.chosen_games = []

		button_height = 50
		font = ('Montserrat', 16, 'bold')

		logo_img = Image.open('app_images/logo.png').resize((220, 200))
		logo = ctk.CTkImage(dark_image=logo_img, size=(120, 70))

		logo_label = ctk.CTkLabel(self, image=logo, text='')
		logo_label.grid(column=0, row=0, pady=15, sticky='wens')

		ball_img = Image.open('button_img/ball.png')
		ball = ctk.CTkImage(dark_image=ball_img)
		self.select_newest_game = ctk.CTkButton(
			self, text=' Poslednja', image=ball, height=button_height, font=font,
			anchor='w', fg_color='#2c2b28', hover_color='#3a3a36', command=lambda: self.button_pressed(1))
		self.select_newest_game.grid(column=0, row=1)

		multiple_balls_img = Image.open('button_img/multiple_balls.png')
		multiple_balls = ctk.CTkImage(dark_image=multiple_balls_img)
		self.select_all_games = ctk.CTkButton(
			self, text=' Sve', fg_color='#2c2b28', image=multiple_balls, hover_color='#3a3a36', height=button_height, font=font,
			anchor='w', command=lambda: self.button_pressed(2))
		self.select_all_games.grid(column=0, row=2)

		house_img = Image.open('button_img/house.png')
		house = ctk.CTkImage(dark_image=house_img)
		self.select_home_games = ctk.CTkButton(
			self, text=' Kod kuće', fg_color='#2c2b28', image=house, hover_color='#3a3a36', height=button_height, font=font,
			anchor='w', command=lambda: self.button_pressed(3))
		self.select_home_games.grid(column=0, row=3)

		car_img = Image.open('button_img/car2.png')
		car = ctk.CTkImage(dark_image=car_img)
		self.select_away_games = ctk.CTkButton(
			self, text=' Gostovanja', fg_color='#2c2b28', image=car, hover_color='#3a3a36', height=button_height, font=font,
			anchor='w', command=lambda: self.button_pressed(4))
		self.select_away_games.grid(column=0, row=4)

		roman1_img = Image.open('button_img/roman1.png').crop((20, 20, 200, 200))
		roman1 = ctk.CTkImage(dark_image=roman1_img)
		self.select_first_half = ctk.CTkButton(
			self, text=' 1. Deo', fg_color='#2c2b28', image=roman1, hover_color='#3a3a36', height=button_height, font=font,
			anchor='w', command=lambda: self.button_pressed(5))
		self.select_first_half.grid(column=0, row=5)

		roman2_img = Image.open('button_img/roman2.png').crop((50, 50, 450, 450))
		roman2 = ctk.CTkImage(dark_image=roman2_img)
		self.select_second_half = ctk.CTkButton(
			self, text=' 2. Deo', fg_color='#2c2b28', image=roman2, hover_color='#3a3a36', height=button_height, font=font,
			anchor='w', command=lambda: self.button_pressed(6))
		self.select_second_half.grid(column=0, row=6)

		advanced_img = Image.open('button_img/advanced.png').crop((50, 50, 430, 430))
		advanced = ctk.CTkImage(dark_image=advanced_img)
		self.advanced_search = ctk.CTkButton(
			self, text=' Pretraži', fg_color='#2c2b28', image=advanced, hover_color='#3a3a36', height=button_height, font=font,
			anchor='w', command=self.select_choice)
		self.advanced_search.grid(column=0, row=7)

		self.scrollable_check_box = ScrollableCheckBoxFrame(self, item_list=range(1, 10))

		self.advanced_text_box = ctk.CTkTextbox(
			self, text_color='white', state='disabled', font=('Montserrat', 12, 'bold'), width=140)
		self.advanced_text_box.grid(column=0, row=8, pady=20, sticky='nsew', padx=5)

		calculate_img = Image.open('button_img/calculate.png')
		calculate = ctk.CTkImage(dark_image=calculate_img)
		self.calculate_games = ctk.CTkButton(
			self, text=' Preračunaj', fg_color='orange', image=calculate, hover_color='#3a3a36', height=button_height,
			font=font, anchor='w',  width=130, command=self.calc_games)
		self.calculate_games.grid(column=0, row=10, padx=8, pady=60)

		self.toplevel_window = None

		self.output_Var = ctk.StringVar(value='')
		self.output_label = ctk.CTkLabel(
			self, text='', text_color='red', textvariable=self.output_Var, font=('Montserrat', 12), height=2)
		self.output_label.grid(column=0, row=9, sticky='sw', padx=8)

		self.button_pressed(1)

	def calc_games(self):
		if len(self.chosen_games) == 0:
			self.output_Var.set('*Izaberite filter')
		else:
			self.output_Var.set('')
			self.get_filter()

	def get_selected_filter(self):
		return self.chosen_games

	def button_pressed(self, button):
		buttons = {
			1: self.select_newest_game,
			2: self.select_all_games,
			3: self.select_home_games,
			4: self.select_away_games,
			5: self.select_first_half,
			6: self.select_second_half}

		buttons.pop(button).configure(fg_color='#3a3a36', hover_color='#3a3a36')
		for _, b in buttons.items():
			b.configure(fg_color='#2c2b28', hover_color='#3a3a36')

		filtered_games = {
			1: [self.all_games[-1]],
			2: self.all_games,
			3: [game for game in self.all_games if game[5] == 'D'],
			4: [game for game in self.all_games if game[5] == 'G'],
			5: [game for game in self.all_games if game[6] == 1],
			6: [game for game in self.all_games if game[6] == 2]}

		self.clear_box()
		self.chosen_games = []
		self.advanced_text_box.configure(state="normal")
		for game in filtered_games[button]:
			self.chosen_games.append(game[0])
			self.advanced_text_box.insert(ctk.END, f"{game[0]}. " + game[2] + f" - {game[7]}" + "\n")
		self.advanced_text_box.configure(state="disabled")

	def clear_box(self):
		self.chosen_games = []
		self.advanced_text_box.configure(state="normal")
		self.advanced_text_box.delete("1.00", ctk.END)
		self.advanced_text_box.configure(state="disabled")

	def add_game(self, games):
		self.clear_box()
		self.toplevel_window.destroy()
		for game in games:
			if game not in self.advanced_text_box.get("1.00", ctk.END):

				self.chosen_games.append(int(game[0]))

				self.advanced_text_box.configure(state="normal")
				self.advanced_text_box.insert(ctk.END, game + "\n")
				self.advanced_text_box.configure(state="disabled")

	def select_choice(self):
		if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
			self.toplevel_window = AdvancedSelect(self, self.add_game, self.all_games)

		else:
			self.toplevel_window.focus()


class ScrollableFrame(ctk.CTkScrollableFrame):
	def __init__(self, parent, update_fast_search, positions, team):
		super().__init__(
			master=parent, fg_color='#51504c', scrollbar_button_color='#3a3a36',
			scrollbar_button_hover_color='#3a3a36')
		self.pack(expand=True, fill='both')

		self._parent_canvas.configure(xscrollincrement=1, yscrollincrement=2)

		self.update_fast_search = update_fast_search
		self.positions = positions

		self.tabview = ctk.CTkTabview(
			master=self, segmented_button_selected_color='#555555',
			segmented_button_selected_hover_color='#555555', segmented_button_unselected_color='#282828',
			segmented_button_fg_color='#282828', segmented_button_unselected_hover_color='#666666',
			fg_color='#51504c', text_color='white', width=350, command=self.update_fast_search)
		# tabview.place(relx=0.2, y=50, relwidth=0.55, relheight=1)
		self.tabview.pack(pady=80, padx=300, side='left')

		# tab1
		self.tab_1 = self.tabview.add("Timska statistika")

		self.points = Points(self.tabview.tab("Timska statistika"), team)
		self.points.grid(column=0, row=0)

		self.attacks = Attack(self.tabview.tab("Timska statistika"), team)
		self.attacks.grid(column=0, row=1)

		self.serve = Serve(self.tabview.tab("Timska statistika"), team)
		self.serve.grid(column=0, row=2)

		self.defense = Defense(self.tabview.tab("Timska statistika"), team)
		self.defense.grid(column=0, row=3)

		self.setting = Setting(self.tabview.tab("Timska statistika"), team)
		self.setting.grid(column=0, row=4)

		self.reception = Reception(self.tabview.tab("Timska statistika"), team)
		self.reception.grid(column=0, row=5)

		# tab2
		self.tab_2 = self.tabview.add("Statistika igrača")

		setter_img = Image.open('button_img/player_setter.png')
		self.setters = PositionAndPlayers(self.tabview.tab("Statistika igrača"), "Dizači", setter_img, self.positions['Dizač'])
		self.setters.grid(column=0, row=1)

		outside_img = Image.open('button_img/player_reception.png')
		self.outsides = PositionAndPlayers(self.tabview.tab("Statistika igrača"), "Primači", outside_img, self.positions['Primač'])
		self.outsides.grid(column=0, row=2)

		opposite_img = Image.open('button_img/player_opposite.png')
		self.opposites = PositionAndPlayers(self.tabview.tab("Statistika igrača"), "Korekcija", opposite_img, self.positions['Korektor'])
		self.opposites.grid(column=0, row=3)

		middle_img = Image.open('button_img/player_blocker.png')
		self.middles = PositionAndPlayers(self.tabview.tab("Statistika igrača"), "Srednjaci", middle_img, self.positions['Srednjak'])
		self.middles.grid(column=0, row=4)

		libero_img = Image.open('button_img/player_libero.png')
		self.liberos = PositionAndPlayers(self.tabview.tab("Statistika igrača"), "Libero", libero_img, self.positions['Libero'])
		self.liberos.grid(column=0, row=5)

		self.tabview._segmented_button._buttons_dict["Timska statistika"].configure(
			font=('Montserrat', 16, 'bold'), width=200, height=40)
		self.tabview._segmented_button._buttons_dict["Statistika igrača"].configure(
			font=('Montserrat', 16, 'bold'), width=200, height=40)

	def update_chart_content(self):
		for tab in self.tabview.winfo_children():
			for widget in tab.winfo_children():
				print(widget)
				widget.update_chart_content()

	def get_current_tab(self):
		return self.tabview.get()

	def get_y_cords_team(self):
		self.tabview._tab_dict['Timska statistika'].grid(
			row=3, column=0, sticky="nsew",
			padx=self._apply_widget_scaling(max(self.tabview._corner_radius, self.tabview._border_width)),
			pady=self._apply_widget_scaling(max(self.tabview._corner_radius, self.tabview._border_width)))
		self.tabview._tab_dict['Timska statistika'].update_idletasks()

		height = self.winfo_height() + self.winfo_y()

		increment = self.points.points.winfo_height() / 2
		y_cords_section = {
			'points': (self.points.winfo_rooty() - increment) / height,
			'attacks': (self.attacks.winfo_rooty() - increment) / height,
			'serve': (self.serve.winfo_rooty() - increment) / height,
			'defense': (self.defense.winfo_rooty() - increment) / height,
			'setting': (self.setting.winfo_rooty() - increment) / height,
			'reception': (self.reception.winfo_rooty() - increment) / height}

		increment_titles = self.points.get_headers().winfo_height() / 2
		y_cords_titles = {
			'points': ((self.points.get_headers().winfo_rooty() - increment_titles) / height,),
			'attacks': [(attacks.winfo_rooty() - increment_titles) / height for attacks in self.attacks.get_headers()],
			'serve': [(serve.winfo_rooty() - increment_titles) / height for serve in self.serve.get_headers()],
			'defense': [(defense.winfo_rooty() - increment_titles) / height for defense in self.defense.get_headers()],
			'setting': [(setting.winfo_rooty() - increment_titles) / height for setting in self.setting.get_headers()],
			'reception': [(reception.winfo_rooty() - increment_titles) / height for reception in self.reception.get_headers()]
		}

		return [y_cords_section, y_cords_titles]

	def get_y_cords_players(self):
		self.tabview._tab_dict['Timska statistika'].grid_forget()
		self.tabview._tab_dict['Statistika igrača'].grid(
			row=3, column=0, sticky="nsew",
			padx=self._apply_widget_scaling(max(self.tabview._corner_radius, self.tabview._border_width)),
			pady=self._apply_widget_scaling(max(self.tabview._corner_radius, self.tabview._border_width)))
		self.tabview._tab_dict['Statistika igrača'].update_idletasks()

		height = self.winfo_height() + self.winfo_y()
		increment = self.setters.get_player_names()[0].winfo_height() / 2
		y_cords_names = {
			'setters':
				[(setter.winfo_rooty() - increment) / height for setter in self.setters.get_player_names()],
			'outsides':
				[(outside.winfo_rooty() - increment) / height for outside in self.outsides.get_player_names()],
			'opposites':
				[(opposite.winfo_rooty() - increment) / height for opposite in self.opposites.get_player_names()],
			'middles':
				[(middle.winfo_rooty() - increment) / height for middle in self.middles.get_player_names()],
			'libero':
				[(libero.winfo_rooty() - increment) / height for libero in self.liberos.get_player_names()]}

		increment_positions = self.setters.get_position().winfo_height() / 2
		y_cords_positions = {
			'setters': (self.setters.get_position().winfo_rooty() - increment_positions) / height,
			'outsides': (self.outsides.get_position().winfo_rooty() - increment_positions) / height,
			'opposites': (self.opposites.get_position().winfo_rooty() - increment_positions) / height,
			'middles': (self.middles.get_position().winfo_rooty() - increment_positions) / height,
			'libero': (self.liberos.get_position().winfo_rooty() - increment_positions) / height}

		self.tabview._tab_dict['Statistika igrača'].grid_forget()

		return [y_cords_names, y_cords_positions]


class FastSearchTeam(ctk.CTkFrame):
	def __init__(self, parent, scroll_frame):
		super().__init__(master=parent, fg_color=section_color)

		self.scroll_frame = scroll_frame

		y_cords = self.scroll_frame.get_y_cords_team()

		points_img = Image.open('button_img/points.png')
		self.points = ExpandableButton(self, points_img, "Poeni", self.update_scroll, y_cords[0]['points'], self.expand_frame)
		self.points.grid(column=0, row=0, sticky='we', pady=1)

		self.points_drop = DropDownFrame(
			self, ('Podela poena',), self.update_scroll, y_cords[1]['points'])

		attack_img = Image.open('button_img/attacks.png')
		self.attack = ExpandableButton(self, attack_img, "Napad", self.update_scroll, y_cords[0]['attacks'], self.expand_frame)
		self.attack.grid(column=0, row=2, sticky='we', pady=1)

		self.attack_drop = DropDownFrame(
			self, ('Efikasnost napada', 'Podela napada'), self.update_scroll, y_cords[1]['attacks'])

		serve_img = Image.open('button_img/serve.png')
		self.serve = ExpandableButton(self, serve_img, "Servis", self.update_scroll, y_cords[0]['serve'], self.expand_frame)
		self.serve.grid(column=0, row=4, sticky='we', pady=1)

		self.serve_drop = DropDownFrame(
			self, ('Podela servisa', 'Ishod servisa'), self.update_scroll, y_cords[1]['serve'])

		defense_img = Image.open('button_img/defense.png')
		self.defense = ExpandableButton(
			self, defense_img, "Odbrana", self.update_scroll, y_cords[0]['defense'], self.expand_frame)
		self.defense.grid(column=0, row=6, sticky='we', pady=1)

		self.defense_drop = DropDownFrame(
			self, ('Podela bloka', 'Podela polja'), self.update_scroll, y_cords[1]['defense'])

		setting_img = Image.open('button_img/lifting.png').crop((100, 100, 400, 400))
		self.setting = ExpandableButton(
			self, setting_img, "Dizanje", self.update_scroll, y_cords[0]['setting'], self.expand_frame)
		self.setting.grid(column=0, row=8, sticky='we', pady=1)

		self.setting_drop = DropDownFrame(
			self, ('Podela dizanja', 'Iskoristljivost dizanja'), self.update_scroll, y_cords[1]['setting'])

		reception_img = Image.open('button_img/hammer.png')
		self.reception = ExpandableButton(
			self, reception_img, "Prijem", self.update_scroll, y_cords[0]['reception'], self.expand_frame)
		self.reception.grid(column=0, row=10, sticky='we', pady=1)

		self.reception_drop = DropDownFrame(
			self, ('Ishod prijema', 'Podela prijema'), self.update_scroll, y_cords[1]['reception'])

		self.previous_button = None
		self.previous_frame = None
		self.place(relx=0.75, rely=0.1, relwidth=0.2)

	def update_scroll(self, y):
		self.scroll_frame._parent_canvas.yview_moveto(y)

	def expand_frame(self, expand_button):
		expandable_frames = [
			self.points_drop, self.attack_drop, self.serve_drop, self.defense_drop, self.setting_drop, self.reception_drop]
		expandable_buttons = [self.points, self.attack, self.serve, self.defense, self.setting, self.reception]

		drops = {'Poeni': (0, 1), 'Napad': (1, 3), 'Servis': (2, 5), 'Odbrana': (3, 7), 'Dizanje': (4, 9), 'Prijem': (5, 11)}
		index = drops[expand_button][0]
		row = drops[expand_button][1]

		selected_frame = expandable_frames.pop(index)
		selected_frame.grid_forget() if selected_frame.winfo_manager() else selected_frame.grid(column=0, row=row, sticky='we')

		selected_button = expandable_buttons.pop(index)
		selected_button.reverse_arrow_image()

		if self.previous_button is not None and self.previous_button != selected_button:
			self.previous_button.reverse_arrow_image()
			self.previous_frame.grid_forget()

		self.previous_frame = selected_frame if self.previous_frame != selected_frame else None
		self.previous_button = selected_button if self.previous_button != selected_button else None


class FastSearchPlayers(ctk.CTkFrame):
	def __init__(self, parent, scroll_frame, postitions):
		super().__init__(master=parent, fg_color=section_color)

		self.positions = postitions
		self.scroll_frame = scroll_frame

		y_cords = self.scroll_frame.get_y_cords_players()

		setter_img = Image.open('button_img/player_setter.png')
		self.setters = ExpandableButton(
			self, setter_img, "Dizači", self.update_scroll,  y_cords[1]['setters'], self.expand_frame)
		self.setters.grid(column=0, row=0, sticky='we', pady=1)

		self.setters_drop = DropDownFrame(
			self, [x.get_full_name() for x in self.positions['Dizač']], self.update_scroll, y_cords[0]['setters'])

		outside_img = Image.open('button_img/player_reception.png')
		self.outside_hitters = ExpandableButton(
			self, outside_img, "Primači", self.update_scroll, y_cords[1]['outsides'], self.expand_frame)
		self.outside_hitters.grid(column=0, row=2, sticky='we', pady=1)

		self.outside_hitters_drop = DropDownFrame(
			self, [x.get_full_name() for x in self.positions['Primač']], self.update_scroll, y_cords[0]['outsides'])

		opposite_img = Image.open('button_img/player_opposite.png')
		self.opposite_hitters = ExpandableButton(
			self, opposite_img, "Korekcija", self.update_scroll, y_cords[1]['opposites'], self.expand_frame)
		self.opposite_hitters.grid(column=0, row=4, sticky='we', pady=1)

		self.opposite_hitters_drop = DropDownFrame(
			self, [x.get_full_name() for x in self.positions['Korektor']], self.update_scroll, y_cords[0]['opposites'])

		middle_img = Image.open('button_img/player_blocker.png')
		self.middle_hitters = ExpandableButton(
			self, middle_img, "Srednjaci", self.update_scroll, y_cords[1]['middles'], self.expand_frame)
		self.middle_hitters.grid(column=0, row=6, sticky='we', pady=1)

		self.middle_hitters_drop = DropDownFrame(
			self, [x.get_full_name() for x in self.positions['Srednjak']], self.update_scroll, y_cords[0]['middles'])

		libero_img = Image.open('button_img/player_libero.png')
		self.libero = ExpandableButton(
			self, libero_img, "Libero", self.update_scroll, y_cords[1]['libero'], self.expand_frame)
		self.libero.grid(column=0, row=8, sticky='we', pady=1)

		self.libero_drop = DropDownFrame(
			self, [x.get_full_name() for x in self.positions['Libero']], self.update_scroll, y_cords[0]['libero'])

		self.previous_button = None
		self.previous_frame = None
		self.place(relx=0.75, rely=0.1, relwidth=0.2)

	def update_scroll(self, y):
		self.scroll_frame._parent_canvas.yview_moveto(y)

	def expand_frame(self, expand_button):
		expandable_frames = [
			self.setters_drop,
			self.outside_hitters_drop,
			self.opposite_hitters_drop,
			self.middle_hitters_drop,
			self.libero_drop]

		expandable_buttons = [self.setters, self.outside_hitters, self.opposite_hitters, self.middle_hitters, self.libero]

		drops = {'Dizači': (0, 1), 'Primači': (1, 3), 'Korekcija': (2, 5), 'Srednjaci': (3, 7), 'Libero': (4, 9)}
		index = drops[expand_button][0]
		row = drops[expand_button][1]

		selected_frame = expandable_frames.pop(index)
		selected_frame.grid_forget() if selected_frame.winfo_manager() else selected_frame.grid(column=0, row=row, sticky='we')

		selected_button = expandable_buttons.pop(index)
		selected_button.reverse_arrow_image()

		if self.previous_button is not None and self.previous_button != selected_button:
			self.previous_button.reverse_arrow_image()
			self.previous_frame.grid_forget()

		self.previous_frame = selected_frame if self.previous_frame != selected_frame else None
		self.previous_button = selected_button if self.previous_button != selected_button else None


class AdvancedSelect(ctk.CTkToplevel):
	def __init__(self, master, add_game, all_games):
		super().__init__(master, fg_color=title_color)

		self.all_games = all_games
		self.add_game = add_game

		ctk.set_appearance_mode('dark')
		x = self.winfo_screenwidth() * 0.1
		y = self.winfo_screenheight() * 0.5
		self.geometry('300x300' + '+' + str(x) + '+' + str(y))
		self.title('')
		self.resizable(False, False)
		self.bind('<Escape>', lambda event: self.quit())
		self.after(250, lambda: self.iconbitmap('app_images/icon.ico'))
		self.grab_set()

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.advanced_search_box = ScrollableCheckBoxFrame(
			self, [f"{game[0]}. " + game[2] + f" - {game[7]}" for game in self.all_games])
		self.advanced_search_box.grid(column=0, row=0, sticky='wesn')

		advanced_img = Image.open('button_img/advanced.png').crop((50, 50, 430, 430))
		advanced = ctk.CTkImage(dark_image=advanced_img)
		self.choose_button = ctk.CTkButton(
			self, text=' Izaberi', fg_color='orange', image=advanced, hover_color='#3a3a36', height=50,
			font=('Montserrat', 16, 'bold'), anchor='w',  width=130, command=self.get_checked_items)
		self.choose_button.grid(column=0, row=1)

	def get_checked_items(self):
		game_id = self.advanced_search_box.get_checked_items()
		self.add_game(game_id)


class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
	def __init__(self, master, item_list, command=None, **kwargs):
		super().__init__(master, **kwargs, fg_color=title_color)

		self.command = command
		self.checkbox_list = []
		for i, item in enumerate(item_list):
			self.add_item(item)

	def add_item(self, item):
		checkbox = ctk.CTkCheckBox(
			self, text=item, checkbox_width=20, checkbox_height=20, font=('Montserrat', 16, 'bold'), fg_color='orange',
			hover_color='orange', border_color=header_color)
		if self.command is not None:
			checkbox.configure(command=self.command)
		checkbox.grid(row=len(self.checkbox_list), column=0, sticky='w', padx=10)
		self.checkbox_list.append(checkbox)

	def remove_item(self, item):
		for checkbox in self.checkbox_list:
			if item == checkbox.cget("text"):
				checkbox.destroy()
				self.checkbox_list.remove(checkbox)
				return

	def get_checked_items(self):
		return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]


class ExpandableButton(ctk.CTkFrame):
	def __init__(self, parent, image, text, update_scroll, scroll_y, expand_frame):
		super().__init__(master=parent, fg_color='#3a3a36')

		self.update_scroll = update_scroll
		self.expand_frame = expand_frame

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)

		ctk_img = ctk.CTkImage(dark_image=image)
		main_button = ctk.CTkButton(
			self, text=f' {text}', fg_color='#3a3a36', hover_color='#3a3a36', height=60, width=250, anchor='w',
			command=lambda: self.update_scroll_position(scroll_y), font=('Montserrat', 20, 'bold'), image=ctk_img)
		main_button.grid(column=0, row=0, sticky='we')

		self.arrow_img = Image.open('button_img/down_arrow.png')
		self.arrow = ctk.CTkImage(dark_image=self.arrow_img, size=(15, 7))
		self.expendable_button = ctk.CTkButton(
			self, fg_color='#3a3a36', hover_color='#3a3a36', height=60, width=60, image=self.arrow, text='',
			command=lambda: self.expand(text))
		self.expendable_button.grid(column=1, row=0, sticky='we')

	def update_scroll_position(self, y):
		self.update_scroll(y)

	def expand(self, text):
		self.expand_frame(text)

	def reverse_arrow_image(self):
		self.arrow_img = self.arrow_img.rotate(180)
		self.arrow = ctk.CTkImage(dark_image=self.arrow_img, size=(15, 7))
		self.expendable_button.configure(image=self.arrow)


class DropDownFrame(ctk.CTkFrame):
	def __init__(self, parent, buttons_name, update_scroll, scroll_y):
		super().__init__(master=parent, fg_color='#3a3a36')

		self.update_scroll = update_scroll

		for index, button_name in enumerate(buttons_name):
			self.button = ctk.CTkButton(
				self, text=f'          {button_name}', fg_color='#3a3a36', hover_color='#3a3a36', height=60, width=310,
				anchor='w', command=lambda idx=index: self.update_scroll_position(scroll_y[idx]),
				font=('Montserrat', 18, 'bold'))
			self.button.grid(column=0, row=index, sticky='we')

	def update_scroll_position(self, y):
		self.update_scroll(y)
