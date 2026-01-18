#!/bin/bash
#
# run-project.sh - Execute a project's INSTRUCTIONS.md via Claude Code
#
# Usage: ./run-project.sh [options] <project-name>
#
# Options:
#   -y, --auto-confirm    Skip permission prompts for unattended execution
#   -u, --user <name>     Run as a specific user (uses sudo -u)
#   -i, --interactive     Enable multi-turn interactive mode (loop for follow-up prompts)
#   -r, --resume <run>    Resume a previous run (provide run number)
#   -l, --list            List available projects
#   -h, --help            Show this help message
#
# This script:
# 1. Reads INSTRUCTIONS.md from ./projects/<project-name>/
# 2. Executes it via Claude Code
# 3. Records results in ./projects/<project-name>/<github-username>/<run-number>/
#

set -e

# Get script directory early for list_projects
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS_DIR="${SCRIPT_DIR}/projects"

# Default options
AUTO_CONFIRM=false
RUN_AS_USER=""
RESUME_RUN=""
INTERACTIVE_MODE=false

# Show help
show_help() {
    echo "Usage: $0 [options] <project-name>"
    echo ""
    echo "Execute a project's INSTRUCTIONS.md via Claude Code"
    echo ""
    echo "Options:"
    echo "  -y, --auto-confirm    Skip permission prompts for unattended execution"
    echo "  -u, --user <name>     Run as a specific user (uses sudo -u with --dangerously-skip-permissions)"
    echo "  -i, --interactive     Enable multi-turn interactive mode (loop for follow-up prompts)"
    echo "  -r, --resume <run>    Resume a previous run (provide run number)"
    echo "  -l, --list            List available projects"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 vbm-replication"
    echo "  $0 --auto-confirm vbm-replication"
    echo "  $0 --interactive vbm-replication"
    echo "  $0 --user agent vbm-replication"
    echo "  $0 --resume 1 vbm-replication \"Continue the analysis\""
    exit 0
}

# List available projects
list_projects() {
    echo "Available projects:"
    echo ""
    if [ -d "$PROJECTS_DIR" ]; then
        for project in "$PROJECTS_DIR"/*/; do
            if [ -d "$project" ]; then
                project_name=$(basename "$project")
                if [ -f "$project/INSTRUCTIONS.md" ]; then
                    echo "  $project_name"
                else
                    echo "  $project_name (missing INSTRUCTIONS.md)"
                fi
            fi
        done
    else
        echo "  (no projects directory found)"
    fi
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -y|--auto-confirm)
            AUTO_CONFIRM=true
            shift
            ;;
        -u|--user)
            RUN_AS_USER="$2"
            shift 2
            ;;
        -i|--interactive)
            INTERACTIVE_MODE=true
            shift
            ;;
        -r|--resume)
            RESUME_RUN="$2"
            shift 2
            ;;
        -l|--list)
            list_projects
            ;;
        -h|--help)
            show_help
            ;;
        -*)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
        *)
            if [ -z "$PROJECT_NAME" ]; then
                PROJECT_NAME="$1"
            else
                # Additional argument is the follow-up prompt for resume
                FOLLOWUP_PROMPT="$1"
            fi
            shift
            ;;
    esac
done

# Check for required argument
if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: $0 [options] <project-name>"
    echo "Example: $0 vbm-replication"
    echo "Use --help for more information"
    exit 1
fi

PROJECT_DIR="${PROJECTS_DIR}/${PROJECT_NAME}"
INSTRUCTIONS_FILE="${PROJECT_DIR}/INSTRUCTIONS.md"

# Validate project exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory not found: ${PROJECT_DIR}"
    echo "Available projects:"
    ls -1 "${PROJECTS_DIR}" 2>/dev/null || echo "  (no projects found)"
    exit 1
fi

# Validate INSTRUCTIONS.md exists
if [ ! -f "$INSTRUCTIONS_FILE" ]; then
    echo "Error: INSTRUCTIONS.md not found in ${PROJECT_DIR}"
    exit 1
fi

# Get GitHub username dynamically
get_github_username() {
    # Try git config first
    local username
    username=$(git config --get user.name 2>/dev/null | tr ' ' '-' | tr '[:upper:]' '[:lower:]')

    if [ -n "$username" ]; then
        echo "$username"
        return
    fi

    # Try GitHub CLI
    username=$(gh api user --jq '.login' 2>/dev/null)

    if [ -n "$username" ]; then
        echo "$username"
        return
    fi

    # Try git remote to extract username
    username=$(git remote get-url origin 2>/dev/null | sed -n 's/.*github.com[:/]\([^/]*\)\/.*/\1/p')

    if [ -n "$username" ]; then
        echo "$username"
        return
    fi

    # Fallback to system username
    echo "${USER:-unknown}"
}

GITHUB_USERNAME=$(get_github_username)
USER_DIR="${PROJECT_DIR}/${GITHUB_USERNAME}"

# Create user directory if it doesn't exist
mkdir -p "$USER_DIR"

# Determine run number by counting existing subdirectories
get_next_run_number() {
    local count=0
    if [ -d "$USER_DIR" ]; then
        count=$(find "$USER_DIR" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    fi
    echo $((count + 1))
}

# Handle resume mode
if [ -n "$RESUME_RUN" ]; then
    # Resuming a previous run
    RESUME_DIR="${USER_DIR}/${RESUME_RUN}"

    if [ ! -d "$RESUME_DIR" ]; then
        echo "Error: Run directory not found: ${RESUME_DIR}"
        echo "Available runs for ${PROJECT_NAME}/${GITHUB_USERNAME}:"
        ls -1 "${USER_DIR}" 2>/dev/null || echo "  (no runs found)"
        exit 1
    fi

    # Check for session ID in the previous run
    SESSION_FILE="${RESUME_DIR}/session_id"
    if [ ! -f "$SESSION_FILE" ]; then
        echo "Error: No session_id file found in ${RESUME_DIR}"
        echo "This run cannot be resumed (may be from before session tracking was added)"
        exit 1
    fi

    RESUME_SESSION_ID=$(cat "$SESSION_FILE")
    if [ -z "$RESUME_SESSION_ID" ]; then
        echo "Error: session_id file is empty in ${RESUME_DIR}"
        exit 1
    fi

    # For resume, we still create a new run directory to track the continuation
    RUN_NUMBER=$(get_next_run_number)
    RUN_DIR="${USER_DIR}/${RUN_NUMBER}"
    mkdir -p "$RUN_DIR"

    # Copy session ID to new run directory
    echo "$RESUME_SESSION_ID" > "${RUN_DIR}/session_id"

    # Check if follow-up prompt was provided
    if [ -z "$FOLLOWUP_PROMPT" ]; then
        echo "Error: Resume mode requires a follow-up prompt"
        echo "Usage: $0 --resume <run-number> <project-name> \"Your follow-up prompt\""
        exit 1
    fi
else
    # New run
    RUN_NUMBER=$(get_next_run_number)
    RUN_DIR="${USER_DIR}/${RUN_NUMBER}"
    mkdir -p "$RUN_DIR"

    # Generate new session ID for this run
    SESSION_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
    echo "$SESSION_ID" > "${RUN_DIR}/session_id"
fi

echo "=========================================="
echo "Agentic Replication Runner"
echo "=========================================="
echo "Project:      ${PROJECT_NAME}"
echo "GitHub User:  ${GITHUB_USERNAME}"
echo "Run Number:   ${RUN_NUMBER}"
echo "Output Dir:   ${RUN_DIR}"
echo "Auto-Confirm: ${AUTO_CONFIRM}"
echo "Interactive:  ${INTERACTIVE_MODE}"
if [ -n "$RUN_AS_USER" ]; then
    echo "Run As User:  ${RUN_AS_USER}"
fi
if [ -n "$RESUME_RUN" ]; then
    echo "Resuming:     Run ${RESUME_RUN} (session: ${RESUME_SESSION_ID:0:8}...)"
else
    echo "Session ID:   ${SESSION_ID:0:8}..."
fi
echo "=========================================="
echo ""

# Record run metadata
if [ -n "$RESUME_RUN" ]; then
    cat > "${RUN_DIR}/metadata.json" << EOF
{
    "project": "${PROJECT_NAME}",
    "github_username": "${GITHUB_USERNAME}",
    "run_number": ${RUN_NUMBER},
    "auto_confirm": ${AUTO_CONFIRM},
    "run_as_user": "${RUN_AS_USER:-null}",
    "started_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "resumed_from_run": ${RESUME_RUN},
    "session_id": "${RESUME_SESSION_ID}",
    "followup_prompt": $(echo "$FOLLOWUP_PROMPT" | jq -Rs .),
    "hostname": "$(hostname)",
    "working_directory": "${RUN_DIR}"
}
EOF
else
    cat > "${RUN_DIR}/metadata.json" << EOF
{
    "project": "${PROJECT_NAME}",
    "github_username": "${GITHUB_USERNAME}",
    "run_number": ${RUN_NUMBER},
    "auto_confirm": ${AUTO_CONFIRM},
    "run_as_user": "${RUN_AS_USER:-null}",
    "started_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "session_id": "${SESSION_ID}",
    "instructions_file": "${INSTRUCTIONS_FILE}",
    "hostname": "$(hostname)",
    "working_directory": "${RUN_DIR}"
}
EOF
fi

# Create log file path
LOG_FILE="${RUN_DIR}/run.log"

# Build the prompt file (avoids issues with long arguments)
PROMPT_FILE="${RUN_DIR}/.prompt.txt"
if [ -n "$RESUME_RUN" ]; then
    # For resume, use the follow-up prompt directly
    echo "$FOLLOWUP_PROMPT" > "$PROMPT_FILE"
else
    # For new runs, prepend instructions context
    cat > "$PROMPT_FILE" << 'PROMPT_EOF'
Please execute the following instructions. Work in the current directory and create all outputs here.

PROMPT_EOF
    cat "$INSTRUCTIONS_FILE" >> "$PROMPT_FILE"
fi

# If running as another user, ensure they own the run directory (including prompt file)
if [ -n "$RUN_AS_USER" ]; then
    sudo chown -R "$RUN_AS_USER" "$RUN_DIR"
fi

# Record run start time for total duration calculation
RUN_START_TIME=$(date +%s)

echo "Starting Claude Code execution..."
echo "Logging to: ${LOG_FILE}"
echo ""

# Change to run directory so Claude operates there
cd "$RUN_DIR"

# Find claude binary (use full path for sudo -u compatibility)
# Prefer system-wide location over user-local for multi-user support
if [ -x "/usr/local/bin/claude" ]; then
    CLAUDE_BIN="/usr/local/bin/claude"
elif [ -n "$RUN_AS_USER" ]; then
    # When running as another user, try to find claude in their PATH
    CLAUDE_BIN=$(sudo -u "$RUN_AS_USER" bash -c 'which claude 2>/dev/null || echo ""')
    if [ -z "$CLAUDE_BIN" ]; then
        echo "Error: claude not found for user $RUN_AS_USER"
        echo "Install claude to /usr/local/bin or ensure it's in the user's PATH"
        exit 1
    fi
else
    CLAUDE_BIN=$(which claude 2>/dev/null || command -v claude 2>/dev/null)
    if [ -z "$CLAUDE_BIN" ]; then
        echo "Error: claude not found"
        exit 1
    fi
fi

# Get the effective session ID (either from resume or new)
if [ -n "$RESUME_RUN" ]; then
    EFFECTIVE_SESSION_ID="$RESUME_SESSION_ID"
else
    EFFECTIVE_SESSION_ID="$SESSION_ID"
fi

# Initialize turns.json file
TURNS_FILE="${RUN_DIR}/turns.json"
echo "[]" > "$TURNS_FILE"

# Function to record turn timing to turns.json
record_turn_timing() {
    local turn_number="$1"
    local started_at="$2"
    local completed_at="$3"
    local duration_seconds="$4"
    local exit_code="$5"
    local prompt_preview="$6"

    if command -v jq &> /dev/null; then
        local temp_file
        temp_file=$(mktemp)
        jq --arg turn "$turn_number" \
           --arg started "$started_at" \
           --arg completed "$completed_at" \
           --arg duration "$duration_seconds" \
           --arg exit "$exit_code" \
           --arg prompt "$prompt_preview" \
           '. + [{
               turn: ($turn | tonumber),
               started_at: $started,
               completed_at: $completed,
               duration_seconds: ($duration | tonumber),
               exit_code: ($exit | tonumber),
               prompt_preview: $prompt
           }]' "$TURNS_FILE" > "$temp_file" && mv "$temp_file" "$TURNS_FILE"
    fi
}

# Function to execute a single Claude turn
# Arguments: $1 = prompt content, $2 = turn number, $3 = use_resume (true/false)
run_claude_turn() {
    local prompt_content="$1"
    local turn_number="$2"
    local use_resume="$3"
    local turn_log="${RUN_DIR}/turn_${turn_number}.log"

    # Record start time
    local start_time start_timestamp
    start_time=$(date +%s)
    start_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Build Claude command for this turn
    if [ "$use_resume" = "true" ]; then
        local claude_cmd="$CLAUDE_BIN --print --dangerously-skip-permissions --resume $EFFECTIVE_SESSION_ID"
    else
        local claude_cmd="$CLAUDE_BIN --print --dangerously-skip-permissions --session-id $EFFECTIVE_SESSION_ID"
    fi

    if [ -n "$RUN_AS_USER" ]; then
        {
            echo "=== Turn $turn_number started at $(date) ==="
            echo "=== Claude binary: $CLAUDE_BIN ==="
            echo "=== Working directory: $RUN_DIR ==="
            echo ""
            sudo -u "$RUN_AS_USER" bash -c "cd '$RUN_DIR' && $claude_cmd \"\$1\"" -- "$prompt_content"
            EXIT_CODE=$?
            echo ""
            echo "=== Turn $turn_number completed at $(date) with exit code ${EXIT_CODE} ==="
        } 2>&1 | sudo -u "$RUN_AS_USER" tee -a "$LOG_FILE" | tee "$turn_log"
    else
        {
            echo "=== Turn $turn_number started at $(date) ==="
            echo ""
            $claude_cmd "$prompt_content"
            EXIT_CODE=$?
            echo ""
            echo "=== Turn $turn_number completed at $(date) with exit code ${EXIT_CODE} ==="
        } 2>&1 | tee -a "$LOG_FILE" | tee "$turn_log"
    fi

    # Record end time and calculate duration
    local end_time end_timestamp duration_seconds
    end_time=$(date +%s)
    end_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    duration_seconds=$((end_time - start_time))

    # Create a preview of the prompt (first 100 chars)
    local prompt_preview
    prompt_preview=$(echo "$prompt_content" | head -c 100 | tr '\n' ' ')
    if [ ${#prompt_content} -gt 100 ]; then
        prompt_preview="${prompt_preview}..."
    fi

    # Record timing to turns.json
    record_turn_timing "$turn_number" "$start_timestamp" "$end_timestamp" "$duration_seconds" "${EXIT_CODE:-0}" "$prompt_preview"

    # Print duration summary
    echo "Turn $turn_number duration: ${duration_seconds}s"

    return $EXIT_CODE
}

# Execute initial prompt
PROMPT_CONTENT=$(cat "$PROMPT_FILE")
TURN_NUMBER=1

# First turn: use session-id for new runs, resume for resumed runs
if [ -n "$RESUME_RUN" ]; then
    run_claude_turn "$PROMPT_CONTENT" "$TURN_NUMBER" "true"
else
    run_claude_turn "$PROMPT_CONTENT" "$TURN_NUMBER" "false"
fi

# Clean up initial prompt file
if [ -n "$RUN_AS_USER" ]; then
    sudo -u "$RUN_AS_USER" rm -f "$PROMPT_FILE"
else
    rm -f "$PROMPT_FILE"
fi

# Interactive loop for follow-up prompts
if [ "$INTERACTIVE_MODE" = "true" ]; then
    echo ""
    echo "=========================================="
    echo "Interactive Mode - Enter follow-up prompts"
    echo "Press Enter for default: \"Please proceed.\""
    echo "Type 'exit', 'quit', or Ctrl+D to end session"
    echo "=========================================="

    while true; do
        echo ""
        printf "Turn %d> " "$((TURN_NUMBER + 1))"

        # Read user input
        if ! read -r USER_PROMPT; then
            # EOF (Ctrl+D)
            echo ""
            echo "End of input, exiting interactive mode."
            break
        fi

        # Check for exit commands
        case "$USER_PROMPT" in
            exit|quit|q)
                echo "Exiting interactive mode."
                break
                ;;
            "")
                # Default continuation prompt
                USER_PROMPT="Please proceed."
                echo "(using default: $USER_PROMPT)"
                ;;
        esac

        # Increment turn and run
        TURN_NUMBER=$((TURN_NUMBER + 1))
        run_claude_turn "$USER_PROMPT" "$TURN_NUMBER" "true"
    done
fi

# Update metadata with completion info
COMPLETED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
RUN_END_TIME=$(date +%s)
TOTAL_DURATION_SECONDS=$((RUN_END_TIME - RUN_START_TIME))

if command -v jq &> /dev/null; then
    if [ -n "$RUN_AS_USER" ]; then
        sudo -u "$RUN_AS_USER" bash -c "
            jq --arg completed '$COMPLETED_AT' \
               --arg exit_code '${EXIT_CODE:-0}' \
               --arg turns '$TURN_NUMBER' \
               --arg duration '$TOTAL_DURATION_SECONDS' \
               '. + {completed_at: \$completed, exit_code: (\$exit_code | tonumber), total_turns: (\$turns | tonumber), total_duration_seconds: (\$duration | tonumber)}' \
               '${RUN_DIR}/metadata.json' > '${RUN_DIR}/metadata.json.tmp' && \
            mv '${RUN_DIR}/metadata.json.tmp' '${RUN_DIR}/metadata.json'
        "
    else
        TEMP_FILE=$(mktemp)
        jq --arg completed "$COMPLETED_AT" \
           --arg exit_code "${EXIT_CODE:-0}" \
           --arg turns "$TURN_NUMBER" \
           --arg duration "$TOTAL_DURATION_SECONDS" \
           '. + {completed_at: $completed, exit_code: ($exit_code | tonumber), total_turns: ($turns | tonumber), total_duration_seconds: ($duration | tonumber)}' \
           "${RUN_DIR}/metadata.json" > "$TEMP_FILE" && mv "$TEMP_FILE" "${RUN_DIR}/metadata.json"
    fi
else
    # Fallback without jq - append to a separate file
    if [ -n "$RUN_AS_USER" ]; then
        sudo -u "$RUN_AS_USER" bash -c "
            echo 'completed_at: $COMPLETED_AT' >> '${RUN_DIR}/completion.txt'
            echo 'exit_code: ${EXIT_CODE:-0}' >> '${RUN_DIR}/completion.txt'
            echo 'total_turns: $TURN_NUMBER' >> '${RUN_DIR}/completion.txt'
            echo 'total_duration_seconds: $TOTAL_DURATION_SECONDS' >> '${RUN_DIR}/completion.txt'
        "
    else
        echo "completed_at: $COMPLETED_AT" >> "${RUN_DIR}/completion.txt"
        echo "exit_code: ${EXIT_CODE:-0}" >> "${RUN_DIR}/completion.txt"
        echo "total_turns: $TURN_NUMBER" >> "${RUN_DIR}/completion.txt"
        echo "total_duration_seconds: $TOTAL_DURATION_SECONDS" >> "${RUN_DIR}/completion.txt"
    fi
fi

# Format duration for display
format_duration() {
    local seconds=$1
    local hours=$((seconds / 3600))
    local minutes=$(((seconds % 3600) / 60))
    local secs=$((seconds % 60))
    if [ $hours -gt 0 ]; then
        printf "%dh %dm %ds" $hours $minutes $secs
    elif [ $minutes -gt 0 ]; then
        printf "%dm %ds" $minutes $secs
    else
        printf "%ds" $secs
    fi
}

echo ""
echo "=========================================="
echo "Run Complete"
echo "=========================================="
echo "Results saved to: ${RUN_DIR}"
echo "Total turns: ${TURN_NUMBER}"
echo "Total duration: $(format_duration $TOTAL_DURATION_SECONDS)"
echo ""
