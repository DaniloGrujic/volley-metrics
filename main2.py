from frames import *
from pg_connection import SqlQuery


class StatsWindow(ctk.CTk):
	def __init__(self):
		super().__init__(fg_color='#51504c')

		# layout
		ctk.set_appearance_mode('dark')

		width = self.winfo_screenwidth()
		height = self.winfo_screenheight()

		self.geometry(f"{width}x{height}-10+0")
		self.title('')
		self.resizable(True, True)
		self.iconbitmap('app_images/icon.ico')
		self.bind('<Escape>', lambda event: self.quit())
		# self.state('zoomed')

		self.withdraw()

		# SQL
		self.sql_query = SqlQuery()
		self.all_players = self.sql_query.sql_data('SELECT * FROM players ORDER BY player_id')
		self.all_games = self.sql_query.sql_data('SELECT * FROM games')

		self.team = None
		self.players = None
		self.player = None

		self.attack_player_df = {}
		self.defense_player_df = {}
		self.setting_player_df = {}

		self.filter = [self.all_games[-1][0]]
		self.filter = [1]

		self.create_player_dataframe()
		self.get_data(self.filter)
		self.create_team_and_players()

		LogWindow(self, self.create_window)

		# frames
		self.scroll = ScrollableFrame(self, self.update_fast_search_frame, self.positions, self.team)
		self.filters_frame = Filters(self, self.all_games, self.get_filter)
		self.fast_search_players = FastSearchPlayers(self, self.scroll, self.positions)
		self.fast_search_team = FastSearchTeam(self, self.scroll)

		# button
		rocket_img = Image.open('button_img/rocket.png')
		rocket = ctk.CTkImage(dark_image=rocket_img, size=(30, 30))
		self.move_up = ctk.CTkButton(
			self, text='', command=lambda: self.return_to_start(0.0), image=rocket, fg_color='#3a3a36', hover_color='orange')
		self.move_up.place(relx=0.91, relwidth=0.035, rely=0.86, relheight=0.06)

		# run
		self.mainloop()

	def create_window(self):
		self.deiconify()

	def get_filter(self):
		self.filter = self.filters_frame.get_selected_filter()
		print(self.filter)

		self.get_data(self.filter)

		self.loader = ctk.CTkFrame(self)
		self.loader.place(relx=0, rely=0, relheight=1, relwidth=1)
		self.loader.columnconfigure(0, weight=1)
		self.loader.rowconfigure(0, weight=1)

		self.loading_label = ctk.CTkLabel(self.loader, text='Učitava se...', font=section_font)
		self.loading_label.grid(column=0, row=0)
		self.update_idletasks()

		self.update_displayed_data()

	def update_displayed_data(self):
		for _, player in self.players.items():
			print(player)
			player.update_data(
				self.all_attacks[2][player.get_id()],
				self.all_defense[2][player.get_id()],
				self.all_setting[1][player.get_id()])

		self.team.update_data(self.all_attacks[0:2], self.all_defense[0:2], self.all_setting[0], self.set_distribution)

		self.scroll.update_chart_content()

		self.update()

		self.loader.place_forget()

	def return_to_start(self, y):
		self.scroll._parent_canvas.yview_moveto(y)

	def update_fast_search_frame(self):
		tab = self.scroll.get_current_tab()

		if tab == 'Statistika igrača':
			self.fast_search_team.place_forget()
			self.fast_search_players.place(relx=0.75, rely=0.1, relwidth=0.2)
		elif tab == 'Timska statistika':
			self.fast_search_team.place(relx=0.75, rely=0.1, relwidth=0.2)
			self.fast_search_players.place_forget()

	def create_team_and_players(self):
		self.team = Team([1, 1])
		self.team.update_data(self.all_attacks[0:2], self.all_defense[0:2], self.all_setting[0], self.set_distribution)

		self.positions = {
			'Dizač': [],
			'Primač': [],
			'Korektor': [],
			'Srednjak': [],
			'Libero': []}

		self.players = {}
		for index, player in enumerate(self.all_players):
			self.player = Player(player)
			self.player.update_data(
				self.all_attacks[2][self.player.get_id()],
				self.all_defense[2][self.player.get_id()],
				self.all_setting[1][self.player.get_id()])
			self.players[player[0]] = self.player
			self.positions[self.player.get_position()].append(self.player)

	def get_data(self, chosen_games):
		games = ''
		for game in chosen_games:
			games += str(game) + ', ' if len(self.filter) > 1 else str(game) + ', '
		games = games[:-2]
		last_game = games

		player_attack = self.attack_player_df.copy()
		player_defense = self.defense_player_df.copy()
		player_setting = self.setting_player_df.copy()

		self.all_attacks = self.sql_query.attack_data(games, player_attack)
		self.all_defense = self.sql_query.defense_data(games, player_defense)
		self.all_setting = self.sql_query.setting_data(games, player_setting)

		self.set_distribution = self.sql_query.sql_data(f'SELECT points FROM sets WHERE game_id IN ({last_game})')

	def create_player_dataframe(self):
		for player in self.all_players:
			self.attack_player_df[player[0]] = {
				'attack_outcome': [0, 0, 0],
				'successful_attacks_per_set': [0, 0, 0, 0, 0],
				'stopped_attacks_per_set': [0, 0, 0, 0, 0],
				'attack_type': [0, 0, 0, 0],
				'attack_zone': [0, 0, 0, 0, 0],
				'serve_outcome': [0, 0, 0, 0, 0],
				'as_serve_per_set': [0, 0, 0, 0, 0],
				'error_serve_per_set': [0, 0, 0, 0, 0],
				'spike_serve': [0, 0, 0],
				'float_serve': [0, 0, 0],
				'ground_serve': [0, 0, 0]}

			self.defense_player_df[player[0]] = {
				'solo_blocks': [0, 0, 0, 0, 0],
				'group_blocks': [0, 0, 0, 0, 0],
				'solo_blocks_per_set': [0, 0, 0, 0, 0],
				'group_blocks_per_set': [0, 0, 0, 0, 0],
				'block_errors_per_set': [0, 0, 0, 0, 0],
				'digs': [0, 0, 0, 0],
				'reception_outcome': [0, 0, 0, 0],
				'reception_error_per_set': [0, 0, 0, 0, 0],
				'up_reception': [0, 0, 0],
				'down_reception': [0, 0, 0]}

			self.setting_player_df[player[0]] = {
				'easy_setting_outcome': [0, 0, 0],
				'position_setting_outcome': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
				'zone_setting': [0, 0, 0, 0, 0],
				'setting_error_per_set': [0, 0, 0, 0, 0]}


class LogWindow(ctk.CTkToplevel):
	def __init__(self, parent, create_stats_window):
		super().__init__(master=parent)

		self.create_stats_window = create_stats_window

		# layout
		ctk.set_appearance_mode('dark')
		x = self.winfo_screenwidth() // 2
		y = int(self.winfo_screenheight() // 2.4)
		self.geometry('300x300' + '+' + str(x) + '+' + str(y))
		self.title('')
		self.resizable(False, False)
		self.bind('<Escape>', lambda event: self.quit())
		self.overrideredirect(True)

		self.rowconfigure(0, weight=2)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)

		# password entry
		self.entryStr = ctk.StringVar()
		self.entry = ctk.CTkEntry(self, placeholder_text='Lozinka', textvariable=self.entryStr, show='*')
		self.entry.grid(column=0, row=1, sticky='en')

		# login button
		key_img = Image.open('app_images/key2.png')
		key = ctk.CTkImage(dark_image=key_img)
		self.button = ctk.CTkButton(
			self, text='', fg_color='orange', image=key, hover_color='#B47A05', width=50, command=self.destroy_window)
		self.button.grid(column=1, row=1, sticky='wn')

		self.bind('<Return>', lambda event: self.destroy_window())

		# output label
		self.output_string = ctk.StringVar()
		self.output_label = ctk.CTkLabel(
			self, text='', text_color='red', font=('DejaVu Sans', 10), textvariable=self.output_string)
		self.output_label.grid(column=0, row=1, pady=15)

		# # logo
		# image = Image.open('app_images/ball.png').resize((200, 200))
		# ctk_image = ctk.CTkImage(dark_image=image, size=(170, 170))
		#
		# image_label = ctk.CTkLabel(self, image=ctk_image, text='')
		# image_label.grid(column=0, row=0, columnspan=2, sticky='nsew')

		logo_img = Image.open('app_images/logo.png').resize((220, 200))
		logo = ctk.CTkImage(dark_image=logo_img, size=(160, 90))

		logo_label = ctk.CTkLabel(self, image=logo, text='')
		logo_label.grid(column=0, row=0, pady=30, sticky='wes', columnspan=2)

	def destroy_window(self):
		password = 'd'
		user_entry = self.entryStr.get()

		if user_entry == password:
			self.create_stats_window()
			self.destroy()
		else:
			self.output_string.set('*Pogrešna lozinka')


if __name__ == "__main__":
	window = StatsWindow()
