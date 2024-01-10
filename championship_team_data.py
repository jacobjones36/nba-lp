import pandas as pd

champ_data = pd.read_excel('412data.xlsx', sheet_name='Champion Team Stats')

class cd:

    def get_points(self):
        points = champ_data['PTS']
        return points

    def get_turnovers(self):
        turnovers = champ_data['TOV']
        return turnovers

    def get_fg_percent(self):
        fg_percent = champ_data['FG%']
        return fg_percent

    def get_fg_attempts(self):
        fg_attempts = champ_data['FGA']
        return fg_attempts

    def get_fg_made(self):
        fg_made = champ_data['FG']
        return fg_made

    def get_rebounds(self):
        rebounds = champ_data['TRB']
        return rebounds

    def get_assists(self):
        assists = champ_data['AST']
        return assists




