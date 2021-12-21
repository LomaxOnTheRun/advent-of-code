import aocd, typing as t

data = """Player 1 starting position: 4
Player 2 starting position: 8"""

data = aocd.get_data(year=2021, day=21)

Game = t.Dict[t.Tuple[int, int, int, int], int]

# Outcome of 3 dice rolls, and number of ways of getting that value
THREE_ROLES = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


def update_game(game: Game, player_id: int) -> Game:
    """Keep track of all game states and num occurences"""
    updated_game = {}
    for (p1_pos, p1_score, p2_pos, p2_score), old_state_num in game.items():
        pos = [p1_pos, p2_pos][player_id]
        score = [p1_score, p2_score][player_id]

        for roll, roll_num in THREE_ROLES.items():
            new_pos = ((pos + roll - 1) % 10) + 1
            new_score = score + new_pos

            if player_id == 0:
                new_state = (new_pos, new_score, p2_pos, p2_score)
            else:
                new_state = (p1_pos, p1_score, new_pos, new_score)

            if new_state not in updated_game:
                new_num = old_state_num * roll_num
            else:
                new_num = updated_game[new_state] + (old_state_num * roll_num)
            updated_game[new_state] = new_num

    return updated_game


def update_wins(game: Game, wins: t.Tuple[int, int]):
    """Tally and delete any finished games"""
    finished = []
    for state in game:
        # Player 1 wins
        if state[1] >= 21:
            wins[0] += game[state]
            finished.append(state)

        # Player 2 wins
        if state[3] >= 21:
            wins[1] += game[state]
            finished.append(state)

    return {state: num for state, num in game.items() if state not in finished}, wins


# {(p1_pos, p1_score, p2_pos, p2_score): num_universes}
game = {(int(data[28]), 0, int(data[-1]), 0): 1}
player_id = 0

wins = [0, 0]  # [P1, P2]
while game:
    # Update game
    game = update_game(game, player_id)

    # Tally and delete any finished games
    game, wins = update_wins(game, wins)

    # Switch player
    player_id = 1 - player_id

print(max(wins))
