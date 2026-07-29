set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]

REPO := justfile_directory()

# List available recipes
default:
    @just --list

# ── Quality ───────────────────────────────────────────────────────────────────

# Ruff lint Python source
lint:
    cd '{{justfile_directory()}}'
    uv run ruff check src/

# Ruff auto-fix Python source
fix:
    cd '{{justfile_directory()}}'
    uv run ruff check --fix src/
    uv run ruff format src/

# ── Testing ───────────────────────────────────────────────────────────────────

# Run Python tests
test:
    cd '{{justfile_directory()}}'
    uv run pytest

# Run tests verbosely
test-v:
    cd '{{justfile_directory()}}'
    uv run pytest -v

# ── Serving ───────────────────────────────────────────────────────────────────

# Start backend only (HTTP mode on port 11122)
serve:
    cd '{{justfile_directory()}}'
    uv run python -m vfx_mcp --serve

# Start backend only (stdio mode)
stdio:
    cd '{{justfile_directory()}}'
    uv run python -m vfx_mcp --stdio

# ── Python ────────────────────────────────────────────────────────────────────

# Install all deps (Python). Run after git clone.
install sync="--extra dev":
    cd '{{justfile_directory()}}'
    uv sync {{sync}}
    Write-Host "Install complete." -ForegroundColor Green

# Sync Python deps with dev extras
sync:
    cd '{{justfile_directory()}}'
    uv sync --extra dev

# Bootstrap: install dev deps + pre-commit hook
bootstrap:
    uv sync --group dev
    uv run pre-commit install
    Write-Host "Pre-commit hooks installed." -ForegroundColor Green

# ── Packaging ────────────────────────────────────────────────────────────────

# Pack MCPB bundle
mcpb-pack:
    cd '{{justfile_directory()}}'
    mcpb pack . dist/vfx-mcp-v$(uv run python -c "import vfx_mcp; print(vfx_mcp.__version__)").mcpb

# ── Gates ────────────────────────────────────────────────────────────────────

# Run all gates
gates-green: fix test
    Write-Host "All gates passed." -ForegroundColor Green