#!/usr/bin/env python3

class Players:
    def __init__(self):
        self.playerList = []

class Game:
    def __init__(self):
        self.players = Players()
        self.places_in_game = [0] * 6
        self.purses = [0] * 6
        self.in_penalty_box = [0] * 6

        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []

        self.current_player = 0
        self.out_of_penalty_box = False

        for i in range(50):
            self.pop_questions.append(self.create_question("Pop", i))
            self.science_questions.append(self.create_question("Science", i))
            self.sports_questions.append(self.create_question("Sports", i))
            self.rock_questions.append(self.create_question("Rock", i))

    def create_question(self, category, index):
        return "%s Question %s" % (category, index)

    def is_playable(self):
        lowest_number_of_players = 2
        return self.how_many_players >= lowest_number_of_players

    def addPlayer(self, player_name):
        self.players.playerList.append(player_name)
        self.places_in_game[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self.in_penalty_box[self.how_many_players] = False

        print(player_name + " was added")
        print("They are player number %s" % len(self.players.playerList))

        return True

    @property
    def how_many_players(self):
        return len(self.players.playerList)

    def is_roll_odd(self, roll):
        return roll % 2 != 0

    def roll(self, roll_of_die):
        print("%s is the current player" % self.players.playerList[self.current_player])
        print("They have rolled a %s" % roll_of_die)

        last_place_on_board = 11
        if self.is_in_penalty_box(self.current_player):
            self.try_to_get_out_of_penalty_box(last_place_on_board, roll_of_die, self.current_player)
        else:
            self.move_on_board(self.current_player, roll_of_die)
            self.loop_around_board(last_place_on_board, self.current_player)

            print(self.players.playerList[self.current_player] + \
                        '\'s new location is ' + \
                  str(self.places_in_game[self.current_player]))
            print("The category is %s" % self._current_game_category)
            self._ask_question()

    def try_to_get_out_of_penalty_box(self, last_place_on_board, roll_of_die, current_player):
        if self.is_roll_odd(roll_of_die):
            self.out_of_penalty_box = True

            print("%s is getting out of the penalty box" % self.players.playerList[current_player])
            self.move_on_board(current_player, roll_of_die)
            self.loop_around_board(last_place_on_board, self.current_player)

            print(self.players.playerList[current_player] + \
                  '\'s new location is ' + \
                  str(self.places_in_game[current_player]))
            print("The category is %s" % self._current_game_category)
            self._ask_question()
        else:
            print("%s is not getting out of the penalty box" % self.players.playerList[current_player])
            self.out_of_penalty_box = False

    def move_on_board(self, player, roll_of_die):
        self.places_in_game[player] = self.places_in_game[player] + roll_of_die

    def loop_around_board(self, last_place_on_board, current_player):
        if self.places_in_game[current_player] > last_place_on_board:
            self.places_in_game[current_player] = self.places_in_game[current_player] - 12

    def _ask_question(self):
        if self._current_game_category == 'Pop': print(self.pop_questions.pop(0))
        if self._current_game_category == 'Science': print(self.science_questions.pop(0))
        if self._current_game_category == 'Sports': print(self.sports_questions.pop(0))
        if self._current_game_category == 'Rock': print(self.rock_questions.pop(0))

    @property
    def _current_game_category(self):

        categories = ['Pop', 'Science', 'Sports', 'Rock']
        index = self.places_in_game[self.current_player]
        while index > 3:
            index = index - 4

        return categories[index]

    def was_correctly_answered(self):
        if self.is_in_penalty_box(self.current_player):
            if self.out_of_penalty_box:
                print('Answer was correct!!!!')
                self.purses[self.current_player] += 1
                print(self.players.playerList[self.current_player] + \
                    ' now has ' + \
                    str(self.purses[self.current_player]) + \
                    ' Gold Coins.')

                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players.playerList): self.current_player = 0

                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players.playerList): self.current_player = 0
                return True



        else:

            print("Answer was corrent!!!!")
            self.purses[self.current_player] += 1
            print(self.players.playerList[self.current_player] + \
                ' now has ' + \
                str(self.purses[self.current_player]) + \
                ' Gold Coins.')

            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players.playerList): self.current_player = 0

            return winner

    def wrong_answer(self):
        print('Question was incorrectly answered')
        print(self.players.playerList[self.current_player] + " was sent to the penalty box")
        self.put_player_in_penalty_box(self.current_player)

        self.current_player += 1
        if self.current_player == len(self.players.playerList): self.current_player = 0
        return True

    def put_player_in_penalty_box(self, player):
        self.in_penalty_box[player] = True

    def _did_player_win(self):
        return not (self.purses[self.current_player] == 6)

    def is_in_penalty_box(self, player):
        return self.in_penalty_box[player]


def run(number):
    not_a_winner = False

    game = Game()

    game.addPlayer('Chet')
    game.addPlayer('Pat')
    game.addPlayer('Sue')

    seed(number)

    while True:
        game.roll(randrange(5) + 1)

        if randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break


from random import randrange, seed, randint

if __name__ == '__main__':
    random_number = randint(1, 10000)
    run(random_number)