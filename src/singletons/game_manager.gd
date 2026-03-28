extends Node

signal state_changed(new_state: GameState.State)
signal score_changed(new_score: int)
signal lives_changed(new_lives: int)

var current_state: GameState.State = GameState.State.MAIN_MENU
var score: int = 0
var lives: int = 3

const MAX_LIVES := 3

func change_state(new_state: GameState.State) -> void:
	current_state = new_state
	state_changed.emit(new_state)

func add_score(amount: int) -> void:
	score += amount
	score_changed.emit(score)

func lose_life() -> void:
	lives -= 1
	lives_changed.emit(lives)
	if lives <= 0:
		change_state(GameState.State.DEFEAT)

func reset_game() -> void:
	score = 0
	lives = MAX_LIVES
	score_changed.emit(score)
	lives_changed.emit(lives)

func start_game() -> void:
	reset_game()
	change_state(GameState.State.PLAYING)

func restart_game() -> void:
	start_game()

func go_to_menu() -> void:
	change_state(GameState.State.MAIN_MENU)

func open_settings() -> void:
	change_state(GameState.State.SETTINGS)
