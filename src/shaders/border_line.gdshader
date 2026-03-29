shader_type canvas_item;

void fragment() {
	float center_dist = abs(UV.x - 0.5) * 2.0;

	// White core
	float core = smoothstep(0.12, 0.0, center_dist);

	// Blue glow falloff
	float glow = smoothstep(1.0, 0.0, center_dist) * 0.3;

	vec3 col = mix(vec3(0.55, 0.75, 1.0), vec3(1.0), core);
	float alpha = max(core * 0.85, glow);

	COLOR = vec4(col, alpha);
}
