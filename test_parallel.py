import logic
import constants as c
from ai_logic import GameAI
from concurrent.futures import ProcessPoolExecutor, as_completed


def simulate_game(game_id):
    """
    Simulates a single game instance and returns detailed results.
    """
    ai = GameAI()
    game = logic.new_game(c.GRID_LEN)
    moves = 0
    max_tile = 0

    while logic.game_state(game) == "not over":
        best_move = ai.get_best_move(game)
        if best_move:
            # Execute the move
            if best_move == 'up':
                game, done = logic.up(game)
            elif best_move == 'down':
                game, done = logic.down(game)
            elif best_move == 'left':
                game, done = logic.left(game)
            elif best_move == 'right':
                game, done = logic.right(game)
            if done:
                game = logic.add_random_tile(game)
                moves += 1  # Increment move count

        # Update max tile
        max_tile = max(max_tile, max(max(row) for row in game))

    # Collect game result
    result = {
        "game_id": game_id,
        "result": logic.game_state(game),  # "win" or "lose"
        "moves": moves,
        "max_tile": max_tile
    }
    return result


def run_simulations_concurrently(num_games, num_workers=4):
    """
    Runs multiple game simulations concurrently and provides a summary of results.
    """
    results = []
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Submit all tasks
        future_to_game = {
            executor.submit(simulate_game, game_id): game_id
            for game_id in range(1, num_games + 1)
        }

        # Collect results as they complete
        for future in as_completed(future_to_game):
            game_id = future_to_game[future]
            try:
                result = future.result()
                results.append(result)
                print(f"Game {game_id} completed: Result: {result['result']}, "
                      f"Moves: {result['moves']}, Max Tile: {result['max_tile']}")
            except Exception as e:
                print(f"Game {game_id} generated an exception: {e}")

    # Calculate summary statistics
    wins = sum(1 for r in results if r["result"] == "win")
    losses = len(results) - wins
    average_moves = sum(r["moves"] for r in results) / len(results)
    average_max_tile = sum(r["max_tile"] for r in results) / len(results)

    # Display results
    print("\n--- Simulation Results ---")
    print(f"Total games: {num_games}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Average moves per game: {average_moves:.2f}")
    print(f"Average highest tile: {average_max_tile:.2f}")


if __name__ == "__main__":
    num_games = 10  # Number of simulations to run
    num_workers = 8  # Number of parallel workers
    run_simulations_concurrently(num_games, num_workers)
