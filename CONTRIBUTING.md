# Contributing to DQMJ1 Ultimate Decompilation

Thank you for your interest in contributing to this project. We aim to document, reverse engineer, and decompile 100% of the game logic and binary structures of *Dragon Quest Monsters: Joker* (Nintendo DS).

## Ground Rules

1. Zero guesswork: Any assertion regarding game mechanics, formulas, or memory offsets must reference verified assembly addresses (ARM9, overlays, or ARM7) or extraction proofs.
2. Commit message format: Follow standard conventional commits:
   - `feat:` for new extraction tools, algorithms, or decompilation modules.
   - `fix:` for fixing incorrect mappings, struct alignments, or logic.
   - `docs:` for documentation updates.
   - `refactor:` for code cleanups without functional change.
3. No emojis in commits, code comments, or documentation files.
4. Professional tone: Write clear, concise, and technically rigorous explanations.

## Workflow

1. Fork the repository and create your feature branch: `git checkout -b feat/my-feature`.
2. Ensure your scripts are reproducible: running the script should cleanly generate the targeted outputs without manual intervention.
3. Open a Pull Request with a detailed description of the changes and assembly evidence.
