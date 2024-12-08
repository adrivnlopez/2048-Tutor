import concurrent.futures
import random
import logic
import constants as c
from ai_logic import GameAI

def simulate_game(instance_id):
    """
    Simulates a single game instance and returns the result.
    """
    print(f"Starting simulation {instance_id}")  # Log the start of the simulation
    ai = GameAI()
    game = logic.new_game(c.GRID_LEN)

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

    game_state = logic.game_state(game)
    print(f"Simulation {instance_id} finished with result: {game_state}")  # Log the result
    return f"Instance {instance_id}: {game_state}"

def main():
    num_simulations = 10  # Number of simulations to run in parallel

    # Use ProcessPoolExecutor for running the simulations concurrently
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(simulate_game, i): i for i in range(num_simulations)}

        # Collect and print results as they complete
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(result)

    # Summary of results
    wins = sum(1 for result in results if "win" in result)
    losses = sum(1 for result in results if "lose" in result)
    print(f"\nSummary: {wins} wins, {losses} losses out of {num_simulations} simulations.")

if __name__ == "__main__":
    main()
