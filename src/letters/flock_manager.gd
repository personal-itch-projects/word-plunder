extends Node2D

var flocks: Array[Node2D] = []
var screen_height: float

func _ready() -> void:
	screen_height = get_viewport().get_visible_rect().size.y

func _process(_delta: float) -> void:
	_check_bottom()

func _unhandled_input(event: InputEvent) -> void:
	if GameManager.current_state != GameState.State.PLAYING:
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_try_click_flock(event.position)

func _try_click_flock(click_pos: Vector2) -> void:
	for i in range(flocks.size() - 1, -1, -1):
		var flock: Node2D = flocks[i]
		if flock.scorable and flock.get_bounding_rect().has_point(click_pos):
			GameManager.add_score(4)
			_remove_flock(i)
			return

func create_flock_for_letter(letter_node: Node2D) -> Node2D:
	var flock_scene := preload("res://src/letters/flock.gd")
	var flock := Node2D.new()
	flock.set_script(flock_scene)
	flock.position = letter_node.position
	letter_node.position = Vector2.ZERO
	letter_node.velocity = Vector2.ZERO
	flock.add_child(letter_node)
	flock.letters.append(letter_node)
	flock._update_scorable()
	add_child(flock)
	flocks.append(flock)
	return flock

func check_projectile_collision(proj_rect: Rect2, proj_letter: String) -> Node2D:
	for flock in flocks:
		if flock.get_bounding_rect().intersects(proj_rect):
			return flock
	return null

func add_letter_to_flock(flock: Node2D, letter_char: String, from_pos: Vector2) -> void:
	var FallingLetterScript := preload("res://src/letters/falling_letter.gd")
	var new_letter := Node2D.new()
	new_letter.set_script(FallingLetterScript)
	new_letter.letter = letter_char
	new_letter.velocity = Vector2.ZERO
	flock.add_letter(new_letter)

func _check_bottom() -> void:
	if GameManager.current_state != GameState.State.PLAYING:
		return
	for i in range(flocks.size() - 1, -1, -1):
		var flock: Node2D = flocks[i]
		if flock.get_bottom_y() >= screen_height:
			GameManager.lose_life()
			_remove_flock(i)

func _remove_flock(index: int) -> void:
	var flock: Node2D = flocks[index]
	flocks.remove_at(index)
	flock.remove_all()
	flock.queue_free()

func clear_all() -> void:
	for flock in flocks:
		flock.remove_all()
		flock.queue_free()
	flocks.clear()
