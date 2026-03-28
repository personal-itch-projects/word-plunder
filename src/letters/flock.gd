extends Node2D

const GREEN_TINT := Color(0.2, 0.8, 0.3, 0.3)
const FLOAT_RADIUS := 30.0
const FLOAT_SPEED_MIN := 0.3
const FLOAT_SPEED_MAX := 0.8
const PUSH_DRAG := 2.5

var letters: Array[Node2D] = []
var velocity: Vector2 = Vector2.ZERO
var scorable: bool = false
var possible_words: Array = []
var push_velocity: Vector2 = Vector2.ZERO
var _letter_float_data: Array = []

var font: Font

func _ready() -> void:
	velocity = Vector2(0, GameManager.get_level_config()["fall_speed"])
	font = preload("res://assets/fonts/DM_Sans/DMSans-Regular.ttf")

func add_letter(letter_node: Node2D) -> void:
	letters.append(letter_node)
	add_child(letter_node)
	letter_node.set_process(false)
	_init_letter_float(letter_node)
	_update_possible_words()

func _init_letter_float(letter_node: Node2D) -> void:
	var data := {
		"angle": randf() * TAU,
		"speed": randf_range(FLOAT_SPEED_MIN, FLOAT_SPEED_MAX),
		"phase": randf() * TAU,
		"radius": randf_range(FLOAT_RADIUS * 0.5, FLOAT_RADIUS),
	}
	_letter_float_data.append(data)

func _update_possible_words() -> void:
	var letter_chars: Array[String] = []
	for l in letters:
		letter_chars.append(l.letter)
	if letters.size() < WordDictionary.MIN_WORD_LENGTH:
		possible_words = []
		scorable = false
		queue_redraw()
		return
	if possible_words.is_empty():
		possible_words = WordDictionary.find_possible_words(letter_chars)
	else:
		possible_words = WordDictionary.filter_possible_words(possible_words, letter_chars)
	scorable = not possible_words.is_empty()
	queue_redraw()

func apply_push(proj_velocity: Vector2) -> void:
	push_velocity += proj_velocity * 0.15

func _get_best_word() -> Dictionary:
	if possible_words.is_empty():
		return {}
	var best: Dictionary = possible_words[0]
	for entry in possible_words:
		if entry["word"].length() > best["word"].length():
			best = entry
		elif entry["word"].length() == best["word"].length() and entry["frequency"] < best["frequency"]:
			best = entry
	return best

func _process(delta: float) -> void:
	# Apply push with drag
	push_velocity = push_velocity.move_toward(Vector2.ZERO, PUSH_DRAG * push_velocity.length() * delta)
	position += (velocity + push_velocity) * delta

	# Update letter floating positions
	var time := Time.get_ticks_msec() / 1000.0
	for i in letters.size():
		var data: Dictionary = _letter_float_data[i]
		var angle: float = data["angle"] + time * data["speed"] + data["phase"]
		var radius: float = data["radius"]
		letters[i].position = Vector2(cos(angle), sin(angle)) * radius

func _draw() -> void:
	if scorable:
		var bubble_r := _get_bubble_radius()
		draw_rect(Rect2(-Vector2(bubble_r, bubble_r), Vector2(bubble_r, bubble_r) * 2), GREEN_TINT)
		var best := _get_best_word()
		if not best.is_empty():
			var label := "%s (%d)" % [best["word"].to_upper(), possible_words.size()]
			var text_size := font.get_string_size(label, HORIZONTAL_ALIGNMENT_CENTER, -1, 16)
			var text_x := -text_size.x / 2.0
			var text_y := -bubble_r - 6
			draw_string(font, Vector2(text_x, text_y), label, HORIZONTAL_ALIGNMENT_CENTER, -1, 16, Color(0.1, 0.6, 0.2))

func _get_bubble_radius() -> float:
	return FLOAT_RADIUS + 22.0

func get_bounding_rect() -> Rect2:
	var r := _get_bubble_radius()
	return Rect2(global_position - Vector2(r, r), Vector2(r, r) * 2)

func get_bounding_rect_local() -> Rect2:
	var r := _get_bubble_radius()
	return Rect2(-Vector2(r, r), Vector2(r, r) * 2)

func get_bottom_y() -> float:
	return global_position.y + _get_bubble_radius()

func remove_all() -> void:
	for l in letters:
		l.queue_free()
	letters.clear()
	_letter_float_data.clear()
