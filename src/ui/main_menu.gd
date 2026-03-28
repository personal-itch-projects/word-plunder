extends Control

var font: Font
var font_bold: Font
var play_rect: Rect2
var settings_rect: Rect2
var hover_play: bool = false
var hover_settings: bool = false
var screen_size: Vector2

func _ready() -> void:
	font = preload("res://assets/fonts/DM_Sans/DMSans-Regular.ttf")
	font_bold = preload("res://assets/fonts/DM_Sans/DMSans-Regular.ttf")
	screen_size = get_viewport().get_visible_rect().size
	var center_x: float = screen_size.x / 2.0
	var center_y: float = screen_size.y / 2.0
	play_rect = Rect2(center_x - 100, center_y - 30, 200, 50)
	settings_rect = Rect2(center_x - 100, center_y + 40, 200, 50)

func _process(_delta: float) -> void:
	var mouse_pos := get_viewport().get_mouse_position()
	var was_hover_play := hover_play
	var was_hover_settings := hover_settings
	hover_play = play_rect.has_point(mouse_pos) and visible
	hover_settings = settings_rect.has_point(mouse_pos) and visible
	if hover_play != was_hover_play or hover_settings != was_hover_settings:
		queue_redraw()

func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if play_rect.has_point(event.position):
			GameManager.start_game()
			get_viewport().set_input_as_handled()
		elif settings_rect.has_point(event.position):
			GameManager.open_settings()
			get_viewport().set_input_as_handled()

func _draw() -> void:
	# Title
	var title_text := "LETTER FALL"
	var title_size := font_bold.get_string_size(title_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 52)
	draw_string(font_bold, Vector2(screen_size.x / 2.0 - title_size.x / 2.0, screen_size.y / 2.0 - 100), title_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 52, Color("#1A1A1A"))

	# Play button
	_draw_button(play_rect, "PLAY", hover_play)

	# Settings button
	_draw_button(settings_rect, "SETTINGS", hover_settings)

func _draw_button(rect: Rect2, text: String, hovered: bool) -> void:
	var bg_color := Color.WHITE
	var border_color := Color("#1A1A1A") if not hovered else Color("#CC3333")
	draw_rect(rect, bg_color)
	draw_rect(rect, border_color, false, 2.0)
	var text_size := font_bold.get_string_size(text, HORIZONTAL_ALIGNMENT_CENTER, -1, 24)
	var text_pos := Vector2(rect.position.x + rect.size.x / 2.0 - text_size.x / 2.0, rect.position.y + rect.size.y / 2.0 + text_size.y / 4.0)
	draw_string(font_bold, text_pos, text, HORIZONTAL_ALIGNMENT_CENTER, -1, 24, Color("#1A1A1A"))
