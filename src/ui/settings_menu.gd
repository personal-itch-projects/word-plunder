extends Control

var font: Font
var screen_size: Vector2
var waiting_for_key: String = ""

var move_left_bubble: BubbleButton
var move_right_bubble: BubbleButton
var music_vol_bubble: BubbleButton
var sfx_vol_bubble: BubbleButton
var language_bubble: BubbleButton
var back_bubble: BubbleButton

func _ready() -> void:
	font = preload("res://assets/fonts/Nunito/Nunito-Regular.ttf")
	screen_size = get_viewport().get_visible_rect().size
	var center_x: float = screen_size.x / 2.0
	var center_y: float = screen_size.y / 2.0

	move_left_bubble = BubbleButton.create(self, Vector2(center_x, center_y - 125), _get_move_left_text(), _on_move_left_clicked, false)
	move_right_bubble = BubbleButton.create(self, Vector2(center_x, center_y - 55), _get_move_right_text(), _on_move_right_clicked, false)
	music_vol_bubble = BubbleButton.create(self, Vector2(center_x, center_y + 15), _get_music_vol_text(), _on_music_vol_clicked, false)
	sfx_vol_bubble = BubbleButton.create(self, Vector2(center_x, center_y + 85), _get_sfx_vol_text(), _on_sfx_vol_clicked, false)
	language_bubble = BubbleButton.create(self, Vector2(center_x, center_y + 155), _get_language_text(), _on_language_clicked, false)
	back_bubble = BubbleButton.create(self, Vector2(center_x, center_y + 225), GameManager.tr_text("BACK"), _on_back_clicked)

	visibility_changed.connect(_on_visibility_changed)

func _on_visibility_changed() -> void:
	if visible:
		waiting_for_key = ""
		var from_game := GameManager.previous_state == GameState.State.PAUSED
		language_bubble.set_visible(not from_game)
		_rebuild_all()
		for bubble in [move_left_bubble, move_right_bubble, music_vol_bubble, sfx_vol_bubble, language_bubble, back_bubble]:
			if bubble:
				bubble.reset_state()

func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if waiting_for_key != "" and event is InputEventKey and event.pressed:
		GameManager.bindings[waiting_for_key] = event.physical_keycode
		waiting_for_key = ""
		_rebuild_all()
		get_viewport().set_input_as_handled()

func _on_move_left_clicked() -> void:
	waiting_for_key = "move_left"
	move_left_bubble.rebuild(_get_move_left_text())

func _on_move_right_clicked() -> void:
	waiting_for_key = "move_right"
	move_right_bubble.rebuild(_get_move_right_text())

func _on_language_clicked() -> void:
	waiting_for_key = ""
	if GameManager.language == "en":
		GameManager.language = "ru"
	else:
		GameManager.language = "en"
	WordDictionary.load_dictionary(GameManager.language)
	_rebuild_all()

func _on_music_vol_clicked() -> void:
	GameManager.cycle_music_volume()
	music_vol_bubble.rebuild(_get_music_vol_text())

func _on_sfx_vol_clicked() -> void:
	GameManager.cycle_sfx_volume()
	sfx_vol_bubble.rebuild(_get_sfx_vol_text())

func _on_back_clicked() -> void:
	waiting_for_key = ""
	if GameManager.previous_state == GameState.State.PAUSED:
		GameManager.pause_game()
	else:
		GameManager.go_to_menu()

func _rebuild_all() -> void:
	move_left_bubble.rebuild(_get_move_left_text())
	move_right_bubble.rebuild(_get_move_right_text())
	music_vol_bubble.rebuild(_get_music_vol_text())
	sfx_vol_bubble.rebuild(_get_sfx_vol_text())
	language_bubble.rebuild(_get_language_text())
	back_bubble.rebuild(GameManager.tr_text("BACK"))

func _get_move_left_text() -> String:
	if waiting_for_key == "move_left":
		return GameManager.tr_text("Press key...")
	return GameManager.tr_text("Move Left:") + " " + OS.get_keycode_string(GameManager.bindings["move_left"])

func _get_move_right_text() -> String:
	if waiting_for_key == "move_right":
		return GameManager.tr_text("Press key...")
	return GameManager.tr_text("Move Right:") + " " + OS.get_keycode_string(GameManager.bindings["move_right"])

func _get_language_text() -> String:
	var lang_key := "Language: Russian" if GameManager.language == "ru" else "Language: English"
	return GameManager.tr_text(lang_key)

func _get_volume_percent(volume: float) -> String:
	return str(int(volume * 100)) + "%"

func _get_music_vol_text() -> String:
	return GameManager.tr_text("Music:") + " " + _get_volume_percent(GameManager.music_volume)

func _get_sfx_vol_text() -> String:
	return GameManager.tr_text("SFX:") + " " + _get_volume_percent(GameManager.sfx_volume)

func _draw() -> void:
	# Title
	var title := GameManager.tr_text("SETTINGS")
	var title_size := font.get_string_size(title, HORIZONTAL_ALIGNMENT_CENTER, -1, 42)
	draw_string(font, Vector2(screen_size.x / 2.0 - title_size.x / 2.0, screen_size.y / 2.0 - 180), title, HORIZONTAL_ALIGNMENT_CENTER, -1, 42, Color("#1A1A1A"))
