extends Control

const CELL_SIZE := 30.0
const CELL_GAP := 4.0
const ARSENAL_FONT_SIZE := 18

var font: Font
var font_bold: Font
var screen_size: Vector2

@onready var platform: Node2D = get_node("/root/Main/GameLayer/Platform")

func _ready() -> void:
	font = preload("res://assets/fonts/Nunito/Nunito-Regular.ttf")
	font_bold = preload("res://assets/fonts/Nunito/Nunito-Bold.ttf")
	screen_size = get_viewport().get_visible_rect().size
	GameManager.score_changed.connect(_on_score_changed)
	GameManager.lives_changed.connect(_on_lives_changed)
	GameManager.level_changed.connect(_on_level_changed)
	GameManager.goal_progress_changed.connect(_on_goal_progress_changed)
	# Initial update
	_on_score_changed(GameManager.score)
	_on_lives_changed(GameManager.lives)

func _process(_delta: float) -> void:
	if visible:
		queue_redraw()

func _on_score_changed(_score: int) -> void:
	queue_redraw()

func _on_lives_changed(_lives: int) -> void:
	queue_redraw()

func _on_level_changed(_level: int) -> void:
	queue_redraw()

func _on_goal_progress_changed() -> void:
	queue_redraw()

func _draw() -> void:
	# Score
	draw_string(font_bold, Vector2(20, 40), GameManager.tr_text("SCORE") + ": " + str(GameManager.score), HORIZONTAL_ALIGNMENT_LEFT, -1, 28, Color("#1A1A1A"))

	# Level
	draw_string(font_bold, Vector2(20, 70), GameManager.tr_text("LEVEL") + ": " + str(GameManager.current_level + 1), HORIZONTAL_ALIGNMENT_LEFT, -1, 22, Color("#1A1A1A"))

	# Goal progress (center)
	var goal_text := _get_goal_text()
	var goal_size := font_bold.get_string_size(goal_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 28)
	draw_string(font_bold, Vector2(screen_size.x / 2.0 - goal_size.x / 2.0, 40), goal_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 28, Color("#1A1A1A"))

	# Elapsed time (small, below goal)
	var elapsed: int = int(GameManager.level_timer)
	var minutes: int = elapsed / 60
	var seconds: int = elapsed % 60
	var timer_text := "%d:%02d" % [minutes, seconds]
	var timer_size := font.get_string_size(timer_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 18)
	draw_string(font, Vector2(screen_size.x / 2.0 - timer_size.x / 2.0, 62), timer_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 18, Color("#666666"))

	# Lives (heart bubbles)
	var heart_size := 14.0
	var heart_gap := 6.0
	var hearts_total_w := GameManager.MAX_LIVES * (heart_size * 2.0) + (GameManager.MAX_LIVES - 1) * heart_gap
	var heart_start_x := screen_size.x - hearts_total_w - 20.0
	var heart_y := 30.0
	for i in GameManager.MAX_LIVES:
		var cx := heart_start_x + i * (heart_size * 2.0 + heart_gap) + heart_size
		if i < GameManager.lives:
			_draw_heart(Vector2(cx, heart_y), heart_size, Color("#E63946"), Color("#FF6B7A"))
		else:
			_draw_heart(Vector2(cx, heart_y), heart_size, Color("#CCCCCC"), Color("#DDDDDD"))

	# Arsenal
	if platform and not platform.arsenal.is_empty():
		_draw_arsenal()

func _get_goal_text() -> String:
	var cfg: Dictionary = GameManager.get_level_config()
	match cfg["goal_type"]:
		"words":
			return GameManager.tr_text("Words:") + " " + str(GameManager.level_words) + "/" + str(cfg["goal_target"])
		"score":
			return GameManager.tr_text("Score:") + " " + str(GameManager.level_score) + "/" + str(cfg["goal_target"])
		"words_of_length":
			return str(cfg["goal_word_length"]) + GameManager.tr_text("-letter words:") + " " + str(GameManager.level_words_of_length) + "/" + str(cfg["goal_target"])
	return ""

func _draw_arsenal() -> void:
	var count: int = platform.arsenal.size()
	var total_w: float = count * CELL_SIZE + (count - 1) * CELL_GAP
	var start_x: float = screen_size.x / 2.0 - total_w / 2.0
	var y: float = screen_size.y - CELL_SIZE - 8.0

	for i in count:
		var x: float = start_x + i * (CELL_SIZE + CELL_GAP)
		var rect := Rect2(x, y, CELL_SIZE, CELL_SIZE)
		var bg := Color.WHITE if i > 0 else Color("#FFF3CC")
		var border := Color("#CC3333") if i == 0 else Color("#1A1A1A")
		draw_rect(rect, bg)
		draw_rect(rect, border, false, 2.0)
		var letter: String = platform.arsenal[i]
		var text_size := font.get_string_size(letter, HORIZONTAL_ALIGNMENT_CENTER, -1, ARSENAL_FONT_SIZE)
		var tx: float = x + CELL_SIZE / 2.0 - text_size.x / 2.0
		var ty: float = y + CELL_SIZE / 2.0 + text_size.y / 4.0
		draw_string(font, Vector2(tx, ty), letter, HORIZONTAL_ALIGNMENT_CENTER, -1, ARSENAL_FONT_SIZE, Color("#1A1A1A"))

func _draw_heart(center: Vector2, size: float, fill_color: Color, highlight_color: Color) -> void:
	var cx := center.x
	var cy := center.y
	var r := size * 0.45
	# Two filled circles for the lobes
	draw_circle(Vector2(cx - r, cy), r, fill_color)
	draw_circle(Vector2(cx + r, cy), r, fill_color)
	# Triangle to fill the bottom and gap between lobes
	var tri := PackedVector2Array([
		Vector2(cx - r * 2.0, cy),
		Vector2(cx + r * 2.0, cy),
		Vector2(cx, cy + r * 2.4),
	])
	draw_colored_polygon(tri, fill_color)
	# Highlight for bubble shine
	draw_circle(Vector2(cx - r * 0.6, cy - r * 0.4), r * 0.3, highlight_color)
