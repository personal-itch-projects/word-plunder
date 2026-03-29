shader_type canvas_item;

// Small bubble shader for projectile shells.
// Draws a soft circle with edge glow, stretched by velocity.

uniform vec4 bubble_color : source_color = vec4(0.7, 0.85, 1.0, 0.3);
uniform vec4 edge_color : source_color = vec4(0.85, 0.95, 1.0, 0.6);
uniform float radius : hint_range(0.0, 1.0) = 0.45;
uniform float edge_width : hint_range(0.0, 0.2) = 0.06;
uniform float stretch : hint_range(1.0, 2.0) = 1.0;
uniform float stretch_angle : hint_range(-3.14159, 3.14159) = 0.0;

void fragment() {
	vec2 centered = UV - vec2(0.5);

	// Rotate to velocity-aligned space, then un-stretch
	float ca = cos(-stretch_angle);
	float sa = sin(-stretch_angle);
	vec2 rotated = vec2(centered.x * ca - centered.y * sa, centered.x * sa + centered.y * ca);
	rotated.x /= stretch;

	float dist = length(rotated);

	// Soft circle with edge
	float inner = radius - edge_width;
	float alpha_fill = 1.0 - smoothstep(inner, radius, dist);
	float alpha_edge = smoothstep(inner - edge_width * 0.5, inner, dist) * (1.0 - smoothstep(radius - edge_width * 0.3, radius, dist));

	vec4 fill = bubble_color * alpha_fill;
	vec4 edge = edge_color * alpha_edge;

	COLOR = fill + edge * (1.0 - fill.a);
	COLOR.a = max(fill.a, edge.a);

	if (COLOR.a < 0.01) {
		discard;
	}
}
