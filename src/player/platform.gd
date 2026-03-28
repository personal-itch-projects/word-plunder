extends Node2D

const MOVE_SPEED := 400.0
const PLATFORM_WIDTH := 100.0
const PLATFORM_HEIGHT := 16.0
const CANNON_WIDTH := 8.0
const CANNON_HEIGHT := 30.0
const ALPHABET := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

var screen_width: float
var next_letter: String = ""
var font: Font

@onready var flock_manager: Node2D = get_parent().get_node("FlockManager")

func _ready() -> void:
	screen_width = get_viewport().get_visible_rect().size.x
	font = preload("res://assets/fonts/DM_Sans/DMSans-Regular.ttf")
	var screen_height: float = get_viewport().get_visible_rect().size.y
	position = Vector2(screen_width / 2.0, screen_height - 50)
	_pick_next_letter()

func reset() -> void:
	position.x = screen_width / 2.0
	_pick_next_letter()
	# Remove any existing projectiles
	for child in get_children():
		child.queue_free()

func _process(delta: float) -> void:
	if GameManager.current_state != GameState.State.PLAYING:
		return

	# Movement
	var direction := 0.0
	if Input.is_action_pressed("ui_left"):
		direction = -1.0
	if Input.is_action_pressed("ui_right"):
		direction = 1.0
	position.x += direction * MOVE_SPEED * delta
	position.x = clampf(position.x, PLATFORM_WIDTH / 2.0, screen_width - PLATFORM_WIDTH / 2.0)

	queue_redraw()

func _unhandled_input(event: InputEvent) -> void:
	if GameManager.current_state != GameState.State.PLAYING:
		return
	if event.is_action_pressed("ui_accept"):
		_shoot()

func _shoot() -> void:
	var ProjectileScript := preload("res://src/player/projectile.gd")
	var proj := Node2D.new()
	proj.set_script(ProjectileScript)
	proj.setup(next_letter, Vector2(position.x, position.y - PLATFORM_HEIGHT - CANNON_HEIGHT), flock_manager)
	get_parent().add_child(proj)
	_pick_next_letter()

func _pick_next_letter() -> void:
	next_letter = ALPHABET[randi() % ALPHABET.length()]
	queue_redraw()

func _draw() -> void:
	# Platform
	var platform_rect := Rect2(-PLATFORM_WIDTH / 2.0, -PLATFORM_HEIGHT / 2.0, PLATFORM_WIDTH, PLATFORM_HEIGHT)
	draw_rect(platform_rect, Color("#1A1A1A"))

	# Cannon
	var cannon_rect := Rect2(-CANNON_WIDTH / 2.0, -PLATFORM_HEIGHT / 2.0 - CANNON_HEIGHT, CANNON_WIDTH, CANNON_HEIGHT)
	draw_rect(cannon_rect, Color("#1A1A1A"))

	# Next letter preview on cannon
	if next_letter != "":
		var text_size := font.get_string_size(next_letter, HORIZONTAL_ALIGNMENT_CENTER, -1, 18)
		draw_string(font, Vector2(-text_size.x / 2.0, -PLATFORM_HEIGHT / 2.0 - CANNON_HEIGHT - 8), next_letter, HORIZONTAL_ALIGNMENT_CENTER, -1, 18, Color("#1A1A1A"))
