extends Node2D

const GRID_CELL := 44.0
const GREEN_TINT := Color(0.2, 0.8, 0.3, 0.3)

var letters: Array[Node2D] = []
var velocity: Vector2 = Vector2.ZERO
var scorable: bool = false
var matched_word: String = ""
var matched_frequency: int = 0

var font: Font

func _ready() -> void:
	velocity = Vector2(0, GameManager.get_level_config()["fall_speed"])
	font = preload("res://assets/fonts/DM_Sans/DMSans-Regular.ttf")

func add_letter(letter_node: Node2D) -> void:
	letters.append(letter_node)
	add_child(letter_node)
	_arrange_letters()
	_update_scorable()

func _arrange_letters() -> void:
	var cols := letters.size()
	for i in letters.size():
		var col := i % cols
		var row := i / cols
		letters[i].position = Vector2(col * GRID_CELL, row * GRID_CELL)
		letters[i].velocity = Vector2.ZERO

func _update_scorable() -> void:
	var letter_chars: Array[String] = []
	for l in letters:
		letter_chars.append(l.letter)
	var result = WordDictionary.find_word(letter_chars)
	if result != null:
		scorable = true
		matched_word = result["word"]
		matched_frequency = result["frequency"]
	else:
		scorable = false
		matched_word = ""
		matched_frequency = 0
	queue_redraw()

func _process(delta: float) -> void:
	position += velocity * delta

func _draw() -> void:
	if scorable:
		var rect := get_bounding_rect_local()
		draw_rect(rect.grow(4), GREEN_TINT)
		var word_upper := matched_word.to_upper()
		var text_size := font.get_string_size(word_upper, HORIZONTAL_ALIGNMENT_CENTER, -1, 18)
		var text_x := rect.position.x + rect.size.x / 2.0 - text_size.x / 2.0
		var text_y := rect.position.y - 8
		draw_string(font, Vector2(text_x, text_y), word_upper, HORIZONTAL_ALIGNMENT_CENTER, -1, 18, Color(0.1, 0.6, 0.2))

func get_bounding_rect() -> Rect2:
	if letters.is_empty():
		return Rect2(position, Vector2.ZERO)
	var rect := Rect2(global_position + letters[0].position - Vector2(22, 22), Vector2(44, 44))
	for i in range(1, letters.size()):
		rect = rect.merge(Rect2(global_position + letters[i].position - Vector2(22, 22), Vector2(44, 44)))
	return rect

func get_bounding_rect_local() -> Rect2:
	if letters.is_empty():
		return Rect2(Vector2.ZERO, Vector2.ZERO)
	var rect := Rect2(letters[0].position - Vector2(22, 22), Vector2(44, 44))
	for i in range(1, letters.size()):
		rect = rect.merge(Rect2(letters[i].position - Vector2(22, 22), Vector2(44, 44)))
	return rect

func get_bottom_y() -> float:
	var max_y := global_position.y
	for l in letters:
		var ly: float = global_position.y + l.position.y + 22
		if ly > max_y:
			max_y = ly
	return max_y

func remove_all() -> void:
	for l in letters:
		l.queue_free()
	letters.clear()
