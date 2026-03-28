extends Node2D

const ALPHABET := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
const FALL_SPEED := 80.0
const LETTER_SIZE := 40.0

var velocity: Vector2 = Vector2.ZERO
var letter: String = ""
var font: Font
var font_size: int = 40

func _ready() -> void:
	font = preload("res://assets/fonts/DM_Sans/DMSans-Regular.ttf")
	if letter == "":
		letter = ALPHABET[randi() % ALPHABET.length()]

func setup(p_letter: String, p_position: Vector2, p_font_size: int = 40) -> void:
	letter = p_letter
	position = p_position
	font_size = p_font_size
	velocity = Vector2(0, FALL_SPEED)

func _process(delta: float) -> void:
	position += velocity * delta

func _draw() -> void:
	var text_size := font.get_string_size(letter, HORIZONTAL_ALIGNMENT_CENTER, -1, font_size)
	var offset := -text_size / 2.0
	draw_string(font, Vector2(offset.x, -offset.y), letter, HORIZONTAL_ALIGNMENT_CENTER, -1, font_size, Color("#1A1A1A"))

func get_rect() -> Rect2:
	return Rect2(position - Vector2(LETTER_SIZE / 2, LETTER_SIZE / 2), Vector2(LETTER_SIZE, LETTER_SIZE))
