extends Node2D

var spawn_timer: float = 0.0
var next_interval: float = 1.0
var spawning: bool = false
var screen_width: float

@onready var flock_manager: Node2D = get_parent().get_node("FlockManager")

func _ready() -> void:
	screen_width = get_viewport().get_visible_rect().size.x
	_randomize_interval()

func start_spawning() -> void:
	spawning = true
	spawn_timer = 0.0
	_randomize_interval()

func stop_spawning() -> void:
	spawning = false

func _process(delta: float) -> void:
	if not spawning:
		return
	spawn_timer += delta
	if spawn_timer >= next_interval:
		spawn_timer = 0.0
		_spawn_letter()
		_randomize_interval()

func _spawn_letter() -> void:
	var cfg: Dictionary = GameManager.get_level_config()
	var gaps: int = cfg.get("missing_letters", 0)
	if gaps > 0:
		_spawn_partial_word(gaps)
	else:
		_spawn_single_letter()

func _spawn_single_letter() -> void:
	var x_pos := _find_free_x_position()
	if x_pos < 0:
		return
	var FallingLetterScript := preload("res://src/letters/falling_letter.gd")
	var letter_node := Node2D.new()
	letter_node.set_script(FallingLetterScript)
	var allowed: String = GameManager.get_allowed_letters()
	var rand_letter := WordDictionary.pick_weighted_letter(allowed)
	letter_node.setup(rand_letter, Vector2(x_pos, -30))
	flock_manager.create_flock_for_letter(letter_node)

func _spawn_partial_word(gaps: int) -> void:
	var partial := WordDictionary.pick_partial_word(gaps)
	if partial.is_empty():
		_spawn_single_letter()
		return
	var kept_letters: Array = partial["letters"]
	var x_pos := _find_free_x_position_for_word(kept_letters.size())
	if x_pos < 0:
		return
	var FallingLetterScript := preload("res://src/letters/falling_letter.gd")
	var letter_nodes: Array[Node2D] = []
	for letter_char in kept_letters:
		var letter_node := Node2D.new()
		letter_node.set_script(FallingLetterScript)
		letter_node.setup(letter_char, Vector2.ZERO)
		letter_nodes.append(letter_node)
	flock_manager.create_flock_for_partial_word(letter_nodes, Vector2(x_pos, -30))

func _find_free_x_position() -> float:
	const MAX_ATTEMPTS := 10
	for _attempt in MAX_ATTEMPTS:
		var x := randf_range(40, screen_width - 40)
		if _is_x_clear(x):
			return x
	return -1.0

func _find_free_x_position_for_word(letter_count: int) -> float:
	const MAX_ATTEMPTS := 10
	const GRID_CELL := 44.0
	var word_extent := (letter_count - 1) * GRID_CELL
	var left_bound := 40.0
	var right_bound := screen_width - 40.0 - word_extent
	if right_bound < left_bound:
		return -1.0
	for _attempt in MAX_ATTEMPTS:
		var x := randf_range(left_bound, right_bound)
		if _is_x_range_clear(x, word_extent):
			return x
	return -1.0

func _is_x_clear(x: float) -> bool:
	const MIN_SPACING := 60.0
	for flock in flock_manager.flocks:
		var rect: Rect2 = flock.get_bounding_rect()
		if x > rect.position.x - MIN_SPACING and x < rect.end.x + MIN_SPACING:
			return false
	return true

func _is_x_range_clear(x: float, extent: float) -> bool:
	const MIN_SPACING := 60.0
	for flock in flock_manager.flocks:
		var rect: Rect2 = flock.get_bounding_rect()
		if x + extent > rect.position.x - MIN_SPACING and x < rect.end.x + MIN_SPACING:
			return false
	return true

func _randomize_interval() -> void:
	var cfg: Dictionary = GameManager.get_level_config()
	var min_no_overlap: float = 44.0 / cfg["fall_speed"]
	next_interval = maxf(randf_range(cfg["spawn_min"], cfg["spawn_max"]), min_no_overlap)
