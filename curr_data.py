import pandas as pd

stats_data = pd.read_excel('412data.xlsx', sheet_name='Points')
salary_data = pd.read_excel('412data.xlsx', sheet_name='Salary')

class data:

    def get_points(self):
        points = stats_data['pts']
        return points

    def get_positions(self):
        positions = stats_data['Pos']
        return positions

    def get_minutes_played(self):
        minutes_played = stats_data['MP']
        return minutes_played

    def get_three_percent(self):
        three_percent = stats_data['3P%']
        return three_percent

    def get_free_throw_percent(self):
        free_throw_percent = stats_data['FT%']
        return free_throw_percent

    def get_turnovers(self):
        turnovers = stats_data['TOV']
        return turnovers

    def get_fg_percent(self):
        fg_percent = stats_data['FG%']
        return fg_percent

    def get_assists(self):
        assists = stats_data['AST']
        return assists

    def get_rebounds(self):
        rebounds = stats_data['TRB']
        return rebounds

    def get_players(self):
        players = stats_data['Player']
        return players

    def get_salaries(self):
        unordered_salaries = salary_data['salary']
        salary_players = list(salary_data['Player'])
        salaries = [0] * len(self.get_players())
        for i, player in enumerate(self.get_players()):
            index = salary_players.index(player)
            salaries[i] = unordered_salaries[index]
        return salaries

    def get_fg_attempted(self):
        fg_attempted = stats_data['FGA']
        return fg_attempted

    def get_three_attempts(self):
        threes_attempted = stats_data['3PA']
        return threes_attempted

    def get_fg_made(self):
        fg_made = stats_data['FG']
        return fg_made

    def get_threes_made(self):
        threes_made = stats_data['3P']
        return threes_made