import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os


load_dotenv()


class SqlQuery:
	def __init__(self):
		super().__init__()

		self.hostname = os.getenv('HOSTNAME')
		self.database = os.getenv('DATABASE')
		self.username = os.getenv('USER')
		self.pwd = os.getenv('PASSWORD')
		self.port_id = int(os.getenv('PORT_ID'))

		self.conn = None
		self.cur = None

	def sql_data(self, query):
		try:
			self.conn = psycopg2.connect(
				host=self.hostname,
				dbname=self.database,
				user=self.username,
				password=self.pwd,
				port=self.port_id)

			self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

			self.cur.execute(query)
			data = self.cur.fetchall()

			return data

		except Exception as error:
			print(error)
		finally:
			if self.cur is not None:
				self.cur.close()
			if self.conn is not None:
				self.conn.close()

	def attack_data(self, games, player_attacks):
		try:
			self.conn = psycopg2.connect(
				host=self.hostname,
				dbname=self.database,
				user=self.username,
				password=self.pwd,
				port=self.port_id)

			self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

			attack_types = {1: 'diagonal', 2: 'parallel', 3: 'block_out', 4: 'tipping'}
			serve_outcome = {4: 'as', 5: 'depth', 6: '3m', 7: 'ideal', 8: 'error'}
			serve_type = {5: 'spike', 6: 'float', 7: 'ground'}

			# attack_counts = {
			# 	'attack': [0, 0, 0],  # successful, caught, stopped
			# 	'all_attack_per_set': [0, 0, 0, 0, 0],
			# 	'successful_attacks_per_set': [0, 0, 0, 0, 0],
			# 	'caught_attacks_per_set': [0, 0, 0, 0, 0],
			# 	'stopped_attacks_per_set': [0, 0, 0, 0, 0],
			# 	'diagonal_per_set': [0, 0, 0, 0, 0],
			# 	'parallel_per_set': [0, 0, 0, 0, 0],
			# 	'block_out_per_set': [0, 0, 0, 0, 0],
			# 	'tipping_per_set': [0, 0, 0, 0, 0],
			# 	'zones': [0, 0, 0, 0, 0],
			# 	'zone1_per_set': [0, 0, 0, 0, 0],
			# 	'zone2_per_set': [0, 0, 0, 0, 0],
			# 	'zone3_per_set': [0, 0, 0, 0, 0],
			# 	'zone6_per_set': [0, 0, 0, 0, 0],
			# 	'zone7_per_set': [0, 0, 0, 0, 0]}
			#
			# serve_counts = {
			# 	'serve': [0, 0, 0, 0, 0],  # as, depth, 3m, ideal, error
			# 	'serve_as_per_set': [0, 0, 0, 0, 0],
			# 	'serve_depth_per_set': [0, 0, 0, 0, 0],
			# 	'serve_3m_per_set': [0, 0, 0, 0, 0],
			# 	'serve_ideal_per_set': [0, 0, 0, 0, 0],
			# 	'serve_error_per_set': [0, 0, 0, 0, 0],
			# 	'spike_serve': [0, 0, 0],  # good, neutral, error
			# 	'float_serve': [0, 0, 0],  # good, neutral, error
			# 	'ground_serve': [0, 0, 0]}  # good, neutral, error

			attack_counts = {
				'attack': [0, 0, 0],  # successful, caught, stopped
				'successful_attacks_per_set': [0, 0, 0, 0, 0],
				'caught_attacks_per_set': [0, 0, 0, 0, 0],
				'stopped_attacks_per_set': [0, 0, 0, 0, 0],
				'all_attack_zones': [0, 0, 0, 0, 0],
				'successful_attack_zones': [0, 0, 0, 0, 0],
				'successful_attack_types': [0, 0, 0, 0],  # diagonal, parallel, tipping, block-out
				'attackers': [0, 0, 0, 0, 0]
			}

			serve_counts = {
				'serve': [0, 0, 0, 0, 0],  # as, depth, 3m, ideal, error
				'as_serve_per_set': [0, 0, 0, 0, 0],
				'good_serve_per_set': [0, 0, 0, 0, 0],
				'neutral_serve_per_set': [0, 0, 0, 0, 0],
				'bad_serve_per_set': [0, 0, 0, 0, 0],
				'spike_serve': [0, 0, 0, 0, 0],  # as, depth, 3m, ideal, error
				'float_serve': [0, 0, 0, 0, 0],  # as, depth, 3m, ideal, error
				'ground_serve': [0, 0, 0, 0, 0],  # as, depth, 3m, ideal, error
			}

			self.cur.execute(
				"SELECT a.attack_type_id, a.zone_id, a.grade_id, s.set_number, a.player_id "
				f"FROM attack a JOIN sets s ON a.set_id = s.set_id WHERE s.game_id IN ({games})")

			for row in self.cur.fetchall():
				attack_type = row[0]
				zone = row[1]
				grade = row[2]
				set_number = row[3]
				player_id = row[4]

				if grade < 4:
					attack_counts['all_attack_zones'][zone - 1 if zone < 4 else zone - 3] += 1
					player_attacks[player_id]['attack_outcome'][grade - 1] += 1
					if grade == 1:
						attack_counts['attack'][0] += 1
						attack_counts['successful_attacks_per_set'][set_number - 1] += 1
						attack_counts['successful_attack_zones'][zone - 1 if zone < 4 else zone - 3] += 1
						attack_counts['successful_attack_types'][attack_type - 1] += 1
						player_attacks[player_id]['attack_type'][attack_type - 1] += 1
						player_attacks[player_id]['attack_zone'][zone - 1 if zone < 4 else zone - 3] += 1
						player_attacks[player_id]['successful_attacks_per_set'][set_number - 1] += 1
					elif grade == 2:
						attack_counts['attack'][1] += 1
						attack_counts['caught_attacks_per_set'][set_number - 1] += 1
					elif grade == 3:
						attack_counts['attack'][2] += 1
						attack_counts['stopped_attacks_per_set'][set_number - 1] += 1
						player_attacks[player_id]['stopped_attacks_per_set'][set_number - 1] += 1
				else:
					serve_counts['serve'][grade - 4] += 1
					serve_counts[f'{serve_type[attack_type]}_serve'][grade - 4] += 1
					player_attacks[player_id]['serve_outcome'][grade - 4] += 1
					if grade in (4, 5):
						serve_counts['good_serve_per_set'][set_number - 1] += 1
						player_attacks[player_id][f'{serve_type[attack_type]}_serve'][0] += 1
						serve_counts['as_serve_per_set'][set_number - 1] += 1 if grade == 4 else 0
						player_attacks[player_id]['as_serve_per_set'][set_number - 1] += 1 if grade == 4 else 0
					elif grade in (6, 7):
						serve_counts['neutral_serve_per_set'][set_number - 1] += 1
						player_attacks[player_id][f'{serve_type[attack_type]}_serve'][1] += 1
					elif grade == 8:
						serve_counts['bad_serve_per_set'][set_number - 1] += 1
						player_attacks[player_id][f'{serve_type[attack_type]}_serve'][2] += 1
						player_attacks[player_id]['error_serve_per_set'][set_number - 1] += 1

				# if grade < 4:
				# 	attack_counts['all_attack_per_set'][set_number - 1] += 1
				#
				# 	if grade == 1:
				# 		attack_counts['attack'][0] += 1
				# 		attack_counts['successful_attacks_per_set'][set_number - 1] += 1
				# 		attack_counts['zones'][zone - 1 if zone < 4 else zone - 3] += 1
				# 		attack_counts[f'zone{zone}_per_set'][set_number - 1] += 1
				# 		attack_counts[f'{attack_types[attack_type]}_per_set'][set_number - 1] += 1
				#
				# 	elif grade == 2:
				# 		attack_counts['attack'][1] += 1
				# 		attack_counts['caught_attacks_per_set'][set_number - 1] += 1
				#
				# 	elif grade == 3:
				# 		attack_counts['attack'][2] += 1
				# 		attack_counts['stopped_attacks_per_set'][set_number - 1] += 1
				#
				# else:
				# 	serve_counts['serve'][grade - 4] += 1
				# 	serve_counts[f'serve_{serve_outcome[grade]}_per_set'][set_number - 1] += 1
				#
				# 	if grade in (4, 5):
				# 		serve_counts[f'{serve_type[attack_type]}_serve'][0] += 1
				# 	elif grade in (6, 7):
				# 		serve_counts[f'{serve_type[attack_type]}_serve'][1] += 1
				# 	elif grade == 8:
				# 		serve_counts[f'{serve_type[attack_type]}_serve'][2] += 1

			return [attack_counts, serve_counts, player_attacks]

		except Exception as error:
			print(error)
		finally:
			if self.cur is not None:
				self.cur.close()
			if self.conn is not None:
				self.conn.close()

	def defense_data(self, games, player_defense):
		try:
			self.conn = psycopg2.connect(
				host=self.hostname,
				dbname=self.database,
				user=self.username,
				password=self.pwd,
				port=self.port_id)

			self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

			self.player_defense = player_defense

			block = {3: 'solo', 4: 'double', 9: 'triple'}
			reception_outcome = {5: 'neutral', 6: 'good', 7: 'good', 8: 'error'}

			defense_counts = {
				'solo_blocks_per_set': [0, 0, 0, 0, 0],
				'double_blocks_per_set': [0, 0, 0, 0, 0],
				'triple_blocks_per_set': [0, 0, 0, 0, 0],
				'block_errors_per_set': [0, 0, 0, 0, 0],
				'solo_blocks_per_zone': [0, 0, 0, 0, 0],
				'double_blocks_per_zone': [0, 0, 0, 0, 0],
				'triple_blocks_per_zone': [0, 0, 0, 0, 0],
				'digs_per_set': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
				'digs': [0, 0, 0, 0]}

			reception_counts = {
				'reception': [0, 0, 0, 0],
				'good_per_set': [0, 0, 0, 0, 0],
				'neutral_per_set': [0, 0, 0, 0, 0],
				'error_per_set': [0, 0, 0, 0, 0],
				'upper_reception': [0, 0, 0, 0],  # good, neutral, error
				'lower_reception': [0, 0, 0, 0]  # good, neutral, error
			}

			self.cur.execute(
				"SELECT d.defense_type_id, d.zone_id, d.grade_id, s.set_number, d.player_id "
				f"FROM defense d JOIN sets s ON d.set_id = s.set_id WHERE s.game_id IN ({games})")

			for row in self.cur.fetchall():
				defense_type = row[0]
				zone = row[1]
				grade = row[2]
				set_number = row[3]
				player_id = row[4]

				if grade is None:
					if defense_type in (3, 4, 9):
						defense_counts[f'{block[defense_type]}_blocks_per_set'][set_number - 1] += 1
						defense_counts[f'{block[defense_type]}_blocks_per_zone'][zone - 1] += 1
						player_defense[player_id]['solo_blocks' if defense_type == 3 else 'group_blocks'][zone - 1] += 1
						player_defense[player_id]\
							['solo_blocks_per_set' if defense_type == 3 else 'group_blocks_per_set'][set_number - 1] += 1
					elif defense_type in (5, 6, 7, 8):
						defense_counts['digs'][defense_type - 5] += 1
						defense_counts['digs_per_set'][defense_type - 5][set_number - 1] += 1
						player_defense[player_id]['digs'][defense_type - 5] += 1

				elif grade in (5, 6, 7):
					reception_counts['upper_reception' if defense_type == 1 else 'lower_reception'][grade - 4] += 1
					reception_counts['reception'][grade - 4] += 1
					reception_counts[f'{reception_outcome[grade]}_per_set'][set_number - 1] += 1
					player_defense[player_id]['reception_outcome'][grade - 4] += 1
					player_defense[player_id][
						'up_reception' if defense_type == 1 else 'down_reception'][0 if grade in (6, 7) else 1] += 1

				elif grade == 8:
					if defense_type in (3, 4, 9):
						defense_counts['block_errors_per_set'][set_number - 1] += 1
						player_defense[player_id]['block_errors_per_set'][set_number - 1] += 1
					elif defense_type in (1, 2):
						reception_counts['reception'][0] += 1
						reception_counts['upper_reception' if defense_type == 1 else 'lower_reception'][0] += 1
						reception_counts[f'{reception_outcome[grade]}_per_set'][set_number - 1] += 1
						player_defense[player_id]['reception_outcome'][0] += 1
						player_defense[player_id]['up_reception' if defense_type == 1 else 'down_reception'][2] += 1
						player_defense[player_id]['reception_error_per_set'][set_number - 1] += 1

				# if grade is None:
				# 	if defense_type in (3, 4, 9):
				# 		block_counts[f'{block[defense_type]}_blocks_per_set'][set_number - 1] += 1
				# 		block_counts[f'{block[defense_type]}_blocks_per_zone'][zone - 1] += 1
				# 	elif defense_type in (5, 6, 7, 8):
				# 		block_counts['digs'][defense_type - 5] += 1
				#
				# elif grade in (5, 6, 7):
				# 	reception_counts['upper_reception' if defense_type == 1 else 'lower_reception'][0 if grade in (6, 7) else 1] += 1
				# 	reception_counts['reception'][grade - 5] += 1
				# 	reception_counts[f'{reception_outcome[grade]}_reception_per_set'][set_number - 1] += 1
				#
				# elif grade == 8:
				# 	if defense_type in (3, 4, 9):
				# 		block_counts['block_errors_per_set'][set_number - 1] += 1
				# 	elif defense_type in (1, 2):
				# 		reception_counts['reception'][3] += 1
				# 		reception_counts['upper_reception' if defense_type == 1 else 'lower_reception'][2] += 1
				# 		reception_counts[f'{reception_outcome[grade]}_reception_per_set'][set_number - 1] += 1

			defense_counts['double_blocks_per_set'] = self.reduce_blocks(defense_counts['double_blocks_per_set'], 2)
			defense_counts['double_blocks_per_zone'] = self.reduce_blocks(defense_counts['double_blocks_per_zone'], 2)
			defense_counts['triple_blocks_per_set'] = self.reduce_blocks(defense_counts['triple_blocks_per_set'], 3)
			defense_counts['triple_blocks_per_zone'] = self.reduce_blocks(defense_counts['triple_blocks_per_zone'], 3)

			return [defense_counts, reception_counts, player_defense]

		except Exception as error:
			print(error)
		finally:
			if self.cur is not None:
				self.cur.close()
			if self.conn is not None:
				self.conn.close()

	def setting_data(self, games, player_setting):
		try:
			self.conn = psycopg2.connect(
				host=self.hostname,
				dbname=self.database,
				user=self.username,
				password=self.pwd,
				port=self.port_id)

			self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

			self.player_setting = player_setting

			hitter_position = {1: 'opposite', 2: 'outside', 3: 'middle'}
			easy_setting_outcome = {1: 'successful', 2: 'caught', 3: 'stopped'}

			# setting_count = {
			# 	'setting': [0, 0, 0],  # successful, caught, unsuccessful
			# 	'all_setting_per_set': [0, 0, 0, 0, 0],
			# 	'successful_setting_per_set': [0, 0, 0, 0, 0],
			# 	'caught_setting_per_set': [0, 0, 0, 0, 0],
			# 	'unsuccessful_setting_per_set': [0, 0, 0, 0, 0],
			# 	'hitters': [0, 0, 0],  # opposite, outside, middle
			# 	'opposite_hitter_per_set': [0, 0, 0, 0, 0],
			# 	'outside_hitter_per_set': [0, 0, 0, 0, 0],
			# 	'middle_hitter_per_set': [0, 0, 0, 0, 0],
			# 	'zones': [0, 0, 0, 0, 0],
			# 	'error_setting_per_set': [0, 0, 0, 0, 0]
			# }

			setting_count = {
				'opposite_hitter_per_set': [0, 0, 0, 0, 0],
				'outside_hitter_per_set': [0, 0, 0, 0, 0],
				'middle_hitter_per_set': [0, 0, 0, 0, 0],
				'all_zones': [0, 0, 0, 0, 0],
				'successful_zones': [0, 0, 0, 0, 0],
				'successful_easy_setting': [0, 0, 0, 0, 0],
				'caught_easy_setting': [0, 0, 0, 0, 0],
				'stopped_easy_setting': [0, 0, 0, 0, 0],
				'opposite_easy_setting': [0, 0, 0, 0, 0],
				'outside_easy_setting': [0, 0, 0, 0, 0],
				'middle_easy_setting': [0, 0, 0, 0, 0],
				'setting_errors_per_set': [0, 0, 0, 0, 0]
			}

			self.cur.execute(
				"SELECT se.zone_id, se.bad_setting, se.grade_id, s.set_number, se.attacker_position, se.player_id "
				f"FROM setting se JOIN sets s ON se.set_id = s.set_id WHERE s.game_id IN ({games})")

			for row in self.cur.fetchall():
				zone = row[0]
				easy_setting = row[1]
				grade = row[2]
				set_number = row[3]
				attacker_position = row[4]
				player_id = row[5]

				if attacker_position in (1, 2, 3):
					setting_count[f'{hitter_position[attacker_position]}_hitter_per_set'][set_number - 1] += 1
					setting_count['all_zones'][zone - 1 if zone < 4 else zone - 3] += 1
					self.player_setting[player_id]['position_setting_outcome'][grade - 1][attacker_position - 1] += 1
					self.player_setting[player_id]['zone_setting'][zone - 1 if zone < 4 else zone - 3] += 1
					if easy_setting is True:
						setting_count[f'{easy_setting_outcome[grade]}_easy_setting'][set_number - 1] += 1
						setting_count[f'{hitter_position[attacker_position]}_easy_setting'][set_number - 1] += 1
						self.player_setting[player_id]['easy_setting_outcome'][grade - 1] += 1
				if grade == 1:
					setting_count['successful_zones'][zone - 1 if zone < 4 else zone - 3] += 1
				elif grade is None:
					setting_count['setting_errors_per_set'][set_number - 1] += 1
					player_setting[player_id]['setting_error_per_set'][set_number - 1] += 1

				# elif grade == 2:
				#
				# elif grade == 3:
				#
				# elif grade is None:


				# if attacker_position in (1, 2, 3):
				# 	setting_count['hitters'][attacker_position - 1] += 1
				# 	setting_count['zones'][zone - 1 if zone < 4 else zone - 3] += 1
				# 	setting_count['setting'][grade - 1] += 1
				# 	setting_count['all_setting_per_set'][set_number - 1] += 1
				# if grade == 1:
				# 	setting_count['successful_setting_per_set'][set_number - 1] += 1
				# 	setting_count[f'{hitter_position[attacker_position]}_hitter_per_set'][set_number - 1] += 1
				# elif grade == 2:
				# 	setting_count['caught_setting_per_set'][set_number - 1] += 1
				# elif grade == 3:
				# 	setting_count['unsuccessful_setting_per_set'][set_number - 1] += 1
				# elif grade is None and bad_setting is True:
				# 	setting_count['unsuccessful_setting_per_set'][set_number - 1] += 1
				# 	setting_count['error_setting_per_set'][set_number - 1] += 1
				# 	setting_count['setting'][2] += 1
				# 	setting_count['all_setting_per_set'][set_number - 1] += 1
			return [setting_count, self.player_setting]

		except Exception as error:
			print(error)
		finally:
			if self.cur is not None:
				self.cur.close()
			if self.conn is not None:
				self.conn.close()

	def reduce_blocks(self, blocks, factor):
		return list(map(lambda x: int(x / factor), blocks))
