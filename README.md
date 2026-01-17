# Agentic Replication

A framework for repeatedly replicating experimental findings using agentic prompts executed via Claude Code.

## Overview

This project provides infrastructure for running reproducible experiments where an AI agent follows detailed instructions to replicate research findings. Each run is recorded with full logs and outputs, enabling comparison across multiple attempts.

## Directory Structure

```
agentic-replication/
├── run-project.sh          # Main runner script
├── README.md
└── projects/
    └── <project-name>/
        ├── INSTRUCTIONS.md  # Detailed instructions for the agent
        └── <github-username>/
            └── <run-number>/
                ├── metadata.json   # Run metadata
                ├── run.log         # Full conversation log
                └── ...             # Outputs created during run
```

## Usage

### Basic Usage

```bash
./run-project.sh <project-name>
```

Example:
```bash
./run-project.sh vbm-replication
```

### Auto-Confirm Mode

For unattended runs where the agent should automatically proceed past checkpoints:

```bash
./run-project.sh --auto-confirm <project-name>
# or
./run-project.sh -y <project-name>
```

In auto-confirm mode, permission checks are bypassed (`--dangerously-skip-permissions`) allowing fully unattended execution.

### Run as Different User

For isolation, you can run the agent as a different system user:

```bash
./run-project.sh --user agent <project-name>
# or
./run-project.sh -u agent <project-name>
```

This uses `sudo -u` to run Claude as the specified user, with `--dangerously-skip-permissions` enabled. The run directory ownership is transferred to the target user before execution.

### Interactive Mode (Multi-Turn)

For multi-turn conversations within the same session, use interactive mode:

```bash
./run-project.sh --interactive <project-name>
# or
./run-project.sh -i vbm-replication
```

In interactive mode:
1. The initial INSTRUCTIONS.md is executed as Turn 1
2. You're prompted for follow-up inputs at `Turn N>`
3. Each turn resumes the same Claude session with full context
4. Type `exit`, `quit`, or Ctrl+D to end the session
5. Each turn is logged to both `run.log` (combined) and `turn_N.log` (individual)

### Resume a Previous Run

To continue a previous run in a new session:

```bash
./run-project.sh --resume <run-number> <project-name> "Your follow-up prompt"
# or
./run-project.sh -r 1 vbm-replication "Now analyze the results and create visualizations"
```

This creates a new run directory that continues the conversation from the specified run.

Each run stores a `session_id` file that enables future resumption.

### Options

| Option | Description |
|--------|-------------|
| `-y`, `--auto-confirm` | Skip all permission prompts for unattended execution |
| `-u`, `--user <name>` | Run Claude as a specific user (uses sudo, implies --dangerously-skip-permissions) |
| `-i`, `--interactive` | Enable multi-turn interactive mode within the same session |
| `-r`, `--resume <run>` | Resume a previous run with a follow-up prompt |
| `-l`, `--list` | List available projects |
| `-h`, `--help` | Show help message |

## Creating a New Project

1. Create a directory under `projects/`:
   ```bash
   mkdir -p projects/my-experiment
   ```

2. Create `INSTRUCTIONS.md` with detailed instructions for the agent:
   ```bash
   vim projects/my-experiment/INSTRUCTIONS.md
   ```

3. Run the project:
   ```bash
   ./run-project.sh my-experiment
   ```

## Run Outputs

Each run creates a numbered directory with:

- **metadata.json**: Run metadata including:
  - Project name
  - GitHub username
  - Run number
  - Session ID (for resumption)
  - Start/completion timestamps
  - Exit code and total turns
  - For resumed runs: reference to the original run and follow-up prompt

- **session_id**: UUID for the Claude session (enables resumption)

- **run.log**: Complete log of the Claude Code session (all turns combined)

- **turn_N.log**: Individual log for each turn (in interactive mode)

- **Additional outputs**: Any files created by the agent during execution

## GitHub Username Detection

The script automatically detects your GitHub username using (in order):
1. GitHub CLI (`gh api user`)
2. Git config (`git config user.name`)
3. Git remote URL parsing
4. System username fallback

## Requirements

- [Claude Code CLI](https://claude.ai/claude-code) installed and configured
- Bash shell
- Optional: `jq` for JSON manipulation
- Optional: GitHub CLI (`gh`) for username detection

## Example Project

The `vbm-replication` project demonstrates replicating and extending a political science paper on vote-by-mail effects. See `projects/vbm-replication/INSTRUCTIONS.md` for the full specification.
