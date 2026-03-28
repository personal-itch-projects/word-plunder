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
	var FallingLetterScript := preload("res://src/letters/falling_letter.gd")
	var letter_node := Node2D.new()
	letter_node.set_script(FallingLetterScript)
	var cfg: Dictionary = GameManager.get_level_config()
	var allowed: String = cfg["allowed_letters"]
	var rand_letter := allowed[randi() % allowed.length()]
	var x_pos := randf_range(40, screen_width - 40)
	letter_node.setup(rand_letter, Vector2(x_pos, -30))
	flock_manager.create_flock_for_letter(letter_node)

func _randomize_interval() -> void:
	var cfg: Dictionary = GameManager.get_level_config()
	next_interval = randf_range(cfg["spawn_min"], cfg["spawn_max"])
