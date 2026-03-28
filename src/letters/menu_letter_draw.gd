extends Node2D

var font: Font

func _ready() -> void:
	font = preload("res://assets/fonts/DM_Sans/DMSans-Regular.ttf")

func _draw() -> void:
	var letter_char: String = get_meta("letter")
	var font_size: int = get_meta("font_size")
	var text_size := font.get_string_size(letter_char, HORIZONTAL_ALIGNMENT_CENTER, -1, font_size)
	var offset := -text_size / 2.0
	draw_string(font, Vector2(offset.x, -offset.y), letter_char, HORIZONTAL_ALIGNMENT_CENTER, -1, font_size, Color("#1A1A1A", 0.15))
