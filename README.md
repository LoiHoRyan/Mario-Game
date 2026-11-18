# Mosslight: The Lost Garden

A small, asset-free Python/Pygame platform game. Restore three overgrown groves by reaching each banner, collecting luminous seeds, and outsmarting the garden creatures.

## Run

```bash
python -m pip install pygame
python main.py
```

## Controls

| Key | Action |
| --- | --- |
| A/D or ←/→ | Move |
| Space, W, or ↑ | Jump (short jump buffering and coyote time make controls forgiving) |
| Shift | Short dash; recharges automatically |
| R | Restart the current level; on game over/victory, start a new run |

## Play features

- Three hand-built stages with distinct routes, optional rewards, safer lower paths, and increasing enemy variety.
- Walker and hopping creatures patrol platform-sized boundaries; a stomp from above defeats them.
- Seeds award score; every tenth seed grants a life. Hearts restore a life (up to five), and stars grant temporary invulnerability.
- A small dash helps cross gaps; it recharges automatically. Enemy contact and falling cost a life and briefly protect the player after respawn.
- Handmade character, enemy, collectible, flag, and layered background graphics require no external assets.

## Project files

`main.py` starts the game; `game.py` owns the loop and progression; `player.py`, `enemy.py`, `collectible.py`, and `game_platform.py` contain gameplay actors; `level.py` defines stages; `ui.py` draws the HUD and end screens.
