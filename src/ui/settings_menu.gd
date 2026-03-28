extends Control

var font: Font
var back_rect: Rect2
var hover_back: bool = false
var screen_size: Vector2

func _ready() -> void:
	font = preload("res://assets/fonts/DM_Sans/DMSans-Regular.ttf")
	screen_size = get_viewport().get_visible_rect().size
	var center_x: float = screen_size.x / 2.0
	var center_y: float = screen_size.y / 2.0
	back_rect = Rect2(center_x - 100, center_y + 60, 200, 50)

func _process(_delta: float) -> void:
	var mouse_pos := get_viewport().get_mouse_position()
	var was := hover_back
	hover_back = back_rect.has_point(mouse_pos) and visible
	if hover_back != was:
		queue_redraw()

func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if back_rect.has_point(event.position):
			GameManager.go_to_menu()
			get_viewport().set_input_as_handled()

func _draw() -> void:
	# Title
	var title := "SETTINGS"
	var title_size := font.get_string_size(title, HORIZONTAL_ALIGNMENT_CENTER, -1, 42)
	draw_string(font, Vector2(screen_size.x / 2.0 - title_size.x / 2.0, screen_size.y / 2.0 - 40), title, HORIZONTAL_ALIGNMENT_CENTER, -1, 42, Color("#1A1A1A"))

	# Placeholder text
	var placeholder := "Coming soon..."
	var ph_size := font.get_string_size(placeholder, HORIZONTAL_ALIGNMENT_CENTER, -1, 22)
	draw_string(font, Vector2(screen_size.x / 2.0 - ph_size.x / 2.0, screen_size.y / 2.0 + 20), placeholder, HORIZONTAL_ALIGNMENT_CENTER, -1, 22, Color("#1A1A1A", 0.5))

	# Back button
	var bg_color := Color.WHITE
	var border_color := Color("#1A1A1A") if not hover_back else Color("#CC3333")
	draw_rect(back_rect, bg_color)
	draw_rect(back_rect, border_color, false, 2.0)
	var text_size := font.get_string_size("BACK", HORIZONTAL_ALIGNMENT_CENTER, -1, 24)
	var text_pos := Vector2(back_rect.position.x + back_rect.size.x / 2.0 - text_size.x / 2.0, back_rect.position.y + back_rect.size.y / 2.0 + text_size.y / 4.0)
	draw_string(font, text_pos, "BACK", HORIZONTAL_ALIGNMENT_CENTER, -1, 24, Color("#1A1A1A"))
