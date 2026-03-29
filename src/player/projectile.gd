extends Node2D

const SPEED := 800.0
const SIZE := 15.0

# Trail: single sprite with metaball shader, positions passed as uniforms
# Same technique as flock.gd _update_bubble_uniforms()
const TRAIL_SAMPLE_INTERVAL := 0.02
const TRAIL_BALL_RADIUS := 8.0
const TRAIL_MAX_POINTS := 16

# Bubble visual
const BUBBLE_SIZE := 24.0

var letter: String = ""
var velocity: Vector2 = Vector2(0, -SPEED)
var flock_manager: Node2D
var font: Font
var screen_width: float

var _trail_timer: float = 0.0
var _trail_positions: Array[Vector2] = []
var _trail_sprite: Sprite2D
var _trail_material: ShaderMaterial
var _bubble_sprite: Sprite2D
var _bubble_material: ShaderMaterial

func setup(p_letter: String, p_position: Vector2, p_flock_manager: Node2D, p_velocity: Vector2 = Vector2(0, -SPEED)) -> void:
	letter = p_letter
	position = p_position
	flock_manager = p_flock_manager
	velocity = p_velocity
	font = preload("res://assets/fonts/Nunito/Nunito-Regular.ttf")

func _ready() -> void:
	screen_width = get_viewport().get_visible_rect().size.x
	_setup_trail()
	_setup_bubble()

func _setup_trail() -> void:
	_trail_positions.resize(TRAIL_MAX_POINTS)
	for i in TRAIL_MAX_POINTS:
		_trail_positions[i] = Vector2(-9999.0, -9999.0)

	var img := Image.create(2, 2, false, Image.FORMAT_RGBA8)
	img.fill(Color.WHITE)
	var tex := ImageTexture.create_from_image(img)

	_trail_sprite = Sprite2D.new()
	_trail_sprite.texture = tex
	_trail_sprite.top_level = true
	_trail_sprite.visible = false

	var shader := preload("res://src/shaders/metaball_bubble.gdshader")
	_trail_material = ShaderMaterial.new()
	_trail_material.shader = shader
	_trail_material.set_shader_parameter("ball_radius", TRAIL_BALL_RADIUS)

	var gradient := Gradient.new()
	gradient.offsets = PackedFloat32Array([0.0, 0.15, 0.5, 1.0])
	gradient.colors = PackedColorArray([
		Color(0.85, 0.93, 1.0, 0.55),
		Color(0.78, 0.90, 1.0, 0.45),
		Color(0.70, 0.85, 1.0, 0.30),
		Color(0.65, 0.82, 1.0, 0.25),
	])
	var grad_tex := GradientTexture1D.new()
	grad_tex.gradient = gradient
	_trail_material.set_shader_parameter("gradient_tex", grad_tex)
	_trail_material.set_shader_parameter("caustic_strength", 0.3)
	_trail_material.set_shader_parameter("caustic_scale", 0.08)
	_trail_material.set_shader_parameter("caustic_speed", 0.5)

	_trail_sprite.material = _trail_material
	add_child(_trail_sprite)

func _setup_bubble() -> void:
	var img := Image.create(2, 2, false, Image.FORMAT_RGBA8)
	img.fill(Color.WHITE)
	var tex := ImageTexture.create_from_image(img)

	_bubble_sprite = Sprite2D.new()
	_bubble_sprite.texture = tex
	_bubble_sprite.scale = Vector2(BUBBLE_SIZE, BUBBLE_SIZE)

	var shader := preload("res://src/shaders/metaball_bubble.gdshader")
	_bubble_material = ShaderMaterial.new()
	_bubble_material.shader = shader
	_bubble_material.set_shader_parameter("ball_count", 1)
	_bubble_material.set_shader_parameter("ball_positions", [Vector2.ZERO])
	_bubble_material.set_shader_parameter("ball_radius", BUBBLE_SIZE * 0.45)
	_bubble_material.set_shader_parameter("rect_size", Vector2(BUBBLE_SIZE, BUBBLE_SIZE))

	var gradient := Gradient.new()
	gradient.offsets = PackedFloat32Array([0.0, 0.15, 0.5, 1.0])
	gradient.colors = PackedColorArray([
		Color(0.85, 0.93, 1.0, 0.55),
		Color(0.78, 0.90, 1.0, 0.45),
		Color(0.70, 0.85, 1.0, 0.30),
		Color(0.65, 0.82, 1.0, 0.25),
	])
	var grad_tex := GradientTexture1D.new()
	grad_tex.gradient = gradient
	_bubble_material.set_shader_parameter("gradient_tex", grad_tex)
	_bubble_material.set_shader_parameter("caustic_strength", 0.4)
	_bubble_material.set_shader_parameter("caustic_scale", 0.06)
	_bubble_material.set_shader_parameter("caustic_speed", 0.5)

	_bubble_sprite.material = _bubble_material
	_bubble_sprite.z_index = 1
	_bubble_sprite.z_as_relative = false
	add_child(_bubble_sprite)

func _process(delta: float) -> void:
	position += velocity * delta

	# Bounce off side borders
	if position.x < 0:
		position.x = 0
		velocity.x = -velocity.x
	elif position.x > screen_width:
		position.x = screen_width
		velocity.x = -velocity.x

	# Sample trail positions into ring buffer
	_trail_timer += delta
	if _trail_timer >= TRAIL_SAMPLE_INTERVAL:
		_trail_timer = 0.0
		for i in range(TRAIL_MAX_POINTS - 1, 0, -1):
			_trail_positions[i] = _trail_positions[i - 1]
		_trail_positions[0] = global_position
	_update_trail_uniforms()

	# Check collision with flocks (circle-based)
	var hit_flock: Node2D = flock_manager.check_projectile_collision(global_position, letter)
	if hit_flock:
		flock_manager.add_letter_to_flock(hit_flock, letter, global_position, velocity)
		queue_free()
		return

	# Remove if off screen top
	if position.y < -50:
		queue_free()

func _update_trail_uniforms() -> void:
	if not _trail_material:
		return

	# Calculate bounding box of valid trail positions
	var min_pos := Vector2(INF, INF)
	var max_pos := Vector2(-INF, -INF)
	var count := 0
	for pos in _trail_positions:
		if pos.x < -9000.0:
			continue
		min_pos = Vector2(minf(min_pos.x, pos.x), minf(min_pos.y, pos.y))
		max_pos = Vector2(maxf(max_pos.x, pos.x), maxf(max_pos.y, pos.y))
		count += 1

	if count == 0:
		_trail_sprite.visible = false
		return
	_trail_sprite.visible = true

	var padding := TRAIL_BALL_RADIUS + 10.0
	var center := (min_pos + max_pos) / 2.0
	var half_size := (max_pos - min_pos) / 2.0 + Vector2(padding, padding)
	half_size = Vector2(maxf(half_size.x, padding), maxf(half_size.y, padding))

	# Position and scale sprite to cover all trail points (2x2 texture -> scale by half_size)
	_trail_sprite.global_position = center
	_trail_sprite.scale = half_size

	var rect_size := half_size * 2.0
	_trail_material.set_shader_parameter("rect_size", rect_size)
	_trail_material.set_shader_parameter("ball_count", count)

	# Convert world positions to sprite-local coordinates
	var local_positions: Array[Vector2] = []
	for pos in _trail_positions:
		if pos.x < -9000.0:
			local_positions.append(Vector2(-9999.0, -9999.0))
		else:
			local_positions.append(pos - center)
	while local_positions.size() < 16:
		local_positions.append(Vector2(-9999.0, -9999.0))
	_trail_material.set_shader_parameter("ball_positions", local_positions)

func _draw() -> void:
	if font == null:
		return
	var text_size := font.get_string_size(letter, HORIZONTAL_ALIGNMENT_CENTER, -1, 18)
	var offset := -text_size / 2.0
	draw_string(font, Vector2(offset.x, -offset.y), letter, HORIZONTAL_ALIGNMENT_CENTER, -1, 18, Color("#1A1A1A"))
