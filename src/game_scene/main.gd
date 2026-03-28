extends Node2D

@onready var game_layer: Node2D = $GameLayer
@onready var menu_letter_spawner: Node2D = $GameLayer/MenuLetterSpawner
@onready var letter_spawner: Node2D = $GameLayer/LetterSpawner
@onready var flock_manager: Node2D = $GameLayer/FlockManager
@onready var platform: Node2D = $GameLayer/Platform
@onready var hud: Control = $UILayer/HUD
@onready var main_menu: Control = $UILayer/MainMenu
@onready var settings_menu: Control = $UILayer/SettingsMenu
@onready var defeat_screen: Control = $UILayer/DefeatScreen

func _ready() -> void:
	GameManager.state_changed.connect(_on_state_changed)
	_on_state_changed(GameManager.current_state)

func _on_state_changed(new_state: GameState.State) -> void:
	# Hide everything first
	main_menu.visible = false
	settings_menu.visible = false
	defeat_screen.visible = false
	hud.visible = false
	platform.visible = false
	letter_spawner.set_process(false)
	menu_letter_spawner.visible = false
	menu_letter_spawner.set_process(false)

	match new_state:
		GameState.State.MAIN_MENU:
			main_menu.visible = true
			menu_letter_spawner.visible = true
			menu_letter_spawner.set_process(true)
			_clear_gameplay()
		GameState.State.PLAYING:
			hud.visible = true
			platform.visible = true
			letter_spawner.set_process(true)
			letter_spawner.start_spawning()
			menu_letter_spawner.clear_letters()
		GameState.State.SETTINGS:
			settings_menu.visible = true
		GameState.State.DEFEAT:
			defeat_screen.visible = true
			hud.visible = true

func _clear_gameplay() -> void:
	flock_manager.clear_all()
	letter_spawner.stop_spawning()
	platform.reset()
