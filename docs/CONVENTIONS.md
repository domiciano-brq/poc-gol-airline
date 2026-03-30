# Conventions

## General

- Keep solutions simple and direct — no over-engineering
- No unnecessary abstractions or advanced patterns unless they add clear value
- Pragmatic approach: when two solutions work, choose the simpler one

## Git

- Branch names follow `us-NNN` format per user story
- Never `git push` without explicit confirmation
- Never `git add -A` without reviewing staged files
- Commit messages should be semantic (feat, fix, refactor, docs, etc.)

## Agents & Tasks

- All inter-agent communication happens via files in `tasks/NNN/`
- Each user story gets its own folder: `tasks/NNN/`
- Artifact naming: `US-NNN-<description>.<ext>`
- Test files always prefixed with `US-NNN-` to avoid collisions

## Documentation

- Place docs in `docs/`
- Keep CLAUDE.md up to date with project conventions as the stack evolves