extends Node2D

const SPEED := 30.0
const SPAWN_INTERVAL := 0.3
const MIN_SIZE := 24
const MAX_SIZE := 96

var spawn_timer: float = 0.0
var letters: Array[Node2D] = []
var screen_size: Vector2
var font: Font

func _ready() -> void:
	screen_size = get_viewport().get_visible_rect().size
	font = preload("res://assets/fonts/DM_Sans/DMSans-Regular.ttf")

func _process(delta: float) -> void:
	spawn_timer += delta
	if spawn_timer >= SPAWN_INTERVAL:
		spawn_timer = 0.0
		_try_spawn()

	# Move and clean up letters
	for i in range(letters.size() - 1, -1, -1):
		var l: Node2D = letters[i]
		l.position.y += SPEED * delta
		if l.position.y > screen_size.y + 100:
			letters.remove_at(i)
			l.queue_free()

func _try_spawn() -> void:
	var rand_size := randi_range(MIN_SIZE, MAX_SIZE)
	var x_pos := randf_range(50, screen_size.x - 50)
	var y_pos := -float(rand_size) - 10.0
	var test_rect := Rect2(Vector2(x_pos - rand_size / 2.0, y_pos - rand_size / 2.0), Vector2(rand_size, rand_size))

	# Check overlap
	for l in letters:
		var lr: Rect2 = l.get_meta("rect")
		if test_rect.intersects(lr):
			return

	var letter_node := Node2D.new()
	var alphabet := WordDictionary.get_alphabet()
	var rand_letter := alphabet[randi() % alphabet.length()]
	var rand_angle := randf_range(-30, 30)
	letter_node.position = Vector2(x_pos, y_pos)
	letter_node.rotation_degrees = rand_angle
	letter_node.set_meta("letter", rand_letter)
	letter_node.set_meta("font_size", rand_size)
	letter_node.set_meta("rect", test_rect)
	letter_node.set_script(preload("res://src/letters/menu_letter_draw.gd"))
	add_child(letter_node)
	letters.append(letter_node)

func clear_letters() -> void:
	for l in letters:
		l.queue_free()
	letters.clear()
