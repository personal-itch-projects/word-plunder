# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Word Cannon** is a Godot 4.6 word puzzle game. Players fire letters from a cannon at falling bubble "flocks", then click flocks to form words and score points. 31 levels across 3 stages with English/Russian language support.

## Build & Run

- **Engine**: Godot 4.6 (Forward Plus renderer)
- **Run**: Open `project.godot` in Godot editor, press F5 (main scene: `src/game_scene/main.tscn`)
- **Export**: CI uses `barichello/godot-ci` container; targets are Windows (D3D12), Linux, Web
- **CI/CD**: `.github/workflows/upload-itch.yml` — exports and uploads to itch.io on git tags
- **Word list rebuild**: `python scripts/build_wordlist.py` — downloads frequency data and generates `assets/data/words.{en,ru}.csv`

## Architecture

### Singletons (Autoloads)
- **GameManager** (`src/singletons/game_manager.gd`) — Game state machine, level progression (31 levels / 3 stages), scoring, language switching, key bindings. Central signal hub: `state_changed`, `score_changed`, `level_changed`, `goal_progress_changed`, `stage_completed`.
- **WordDictionary** (`src/singletons/word_dictionary.gd`) — Trie-based word lookup, frequency-weighted letter sampling, word finding algorithms (`find_exact_word`, `find_longest_word`, `can_form_word_with_additions`). Loads CSV word lists at runtime.

### Core Gameplay (`src/`)
- **`letters/flock.gd`** — Bubble containing letters with boid physics (separation/cohesion/boundary). Tracks best formable word. Click to pop and score. Uses metaball shader for rendering.
- **`letters/flock_manager.gd`** — Creates/removes flocks, handles click-to-pop, projectile-flock collision via metaball field overlap, scoring formula: `word_length * (2 + 3 * log10(MAX_FREQ/frequency))`.
- **`letters/letter_spawner.gd`** — Spawns flocks at random positions with configurable intervals and letter counts per level.
- **`player/platform.gd`** — Cannon with 10-letter arsenal queue, A/D movement, mouse aim (±60°), shoot on click. Arsenal uses slot-aware letter selection to complement existing flocks.
- **`player/projectile.gd`** — Fired letter with trail particles, metaball collision detection, border bouncing.

### UI (`src/ui/`)
- **`bubble_button.gd`** — Reusable animated button: multi-word text, letter spring physics, hover tint spread, pop-on-click. Used across all menus.
- **`hud.gd`** — Score, level, goal progress, timer, arsenal preview (5 bubble slots).
- **`main_menu.gd`**, **`pause_menu.gd`**, **`defeat_screen.gd`**, **`stage_complete_screen.gd`**, **`settings_menu.gd`** — Screen states driven by `GameManager.state_changed` signal.

### Shaders (`src/shaders/`)
- **`metaball_bubble.gdshader`** — Analytical per-pixel metaball field with gradient lookup, two-layer Voronoi caustics, dent effect on impact, hover tint. Supports up to 32 balls.
- **`border_line.gdshader`** — Thin white core + blue glow for play area edges.

### Game State Flow
`MAIN_MENU → PLAYING → PAUSED/SETTINGS → DEFEAT/STAGE_COMPLETE`
Defined in `src/enums/game_state.gd`. All UI screens react to `GameManager.state_changed`.

## Key Patterns

- **Signal-driven UI**: All UI listens to GameManager signals rather than polling
- **Trie data structure**: WordDictionary builds a trie from CSV for fast prefix/exact word search
- **Boid physics**: Flock letters use separation + cohesion + boundary + drift forces with 3-pass hard collision
- **Metaball rendering**: GPU shader evaluates field function per-pixel; same shader used for flocks, projectiles, and UI buttons
- **Slot-aware sampling**: `pick_slot_aware_letter()` scores candidate letters by marginal value to existing flocks

## Server Directory

`server/` contains a Node.js MCP server (FastMCP) for Claude editor integration. It is a development tool only, not part of the game.

## Data Files

- `assets/data/words.en.csv` / `words.ru.csv` — Word frequency lists (format: `word,frequency`)
- `assets/data/themes.en.json` / `themes.ru.json` — Theme word lists for themed flock spawning. **Tightly coupled to word datasets**: when `words.*.csv` files are changed, removed, or replaced, theme files must be regenerated via `python scripts/generate_themes.py` to ensure all theme words exist in the dictionary.
- `assets/theme/default_theme.tres` — Global UI theme
- `assets/fonts/Nunito/` — Game fonts

## Play Area

800px wide, centered in viewport (1152x648). Border lines at edges. Flocks fall from top; cannon at bottom.
