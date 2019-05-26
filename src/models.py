from dataclasses import dataclass, asdict


@dataclass
class Player:
    name: str
    jersey_number: int
    birth_date: str
    age: int
    birth_city: str
    birth_country: str
    nationality: str
    height: str
    weight: int
    hand: str
    team: str
    position: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        current_dict = {
            'name': d.get('fullName'),
            'jersey_number': d.get('primaryNumber'),
            'birth_date': d.get('birthDate'),
            'age': d.get('currentAge'),
            'birth_city': d.get('birth_city'),
            'birth_country': d.get('birthCountry'),
            'nationality': d.get('nationality'),
            'height': d.get('height'),
            'weight': d.get('weight'),
            'hand': d.get('shootsCatches'),
            'team': d.get('currentTeam', {}).get('name'),
            'position': d.get('primaryPosition', {}).get('abbreviation')
        }
        return cls(**current_dict)

    def __str__(self):
        return "Full Name: {}\n" \
               "Jersey number : {}\n" \
               "Birth date: {}\n" \
               "Age: {}\n" \
               "Birth country: {}\n" \
               "Birth city: {}\n" \
               "Nationality: {}\n" \
               "Height: {}\n" \
               "Weight: {} lbs\n" \
               "Hand: {}\n" \
               "Team: {}\n" \
               "Position: {}\n".format(self.name,
                                       self.jersey_number,
                                       self.birth_date,
                                       self.age,
                                       self.birth_country,
                                       self.birth_city,
                                       self.nationality,
                                       self.height,
                                       self.weight,
                                       self.hand,
                                       self.team,
                                       self.position)


@dataclass
class PlayerStats:
    points: int
    assists: int
    goals: int
    plusminus: int

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __str__(self):
        return f'Points: {self.points}\n' \
               f'Goals: {self.goals}\n' \
               f'Assists: {self.assists}\n' \
               f'PlusMinus: {self.plusminus}\n'
