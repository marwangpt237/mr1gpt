#!/usr/bin/env python3
import os
import re
import json
import subprocess
from datetime import datetime
from pathlib import Path
import hashlib
import requests
import platform

# ======================
# CORE FUNCTIONALITY
# ======================
class TermuxAI:
    def __init__(self):
        self.memory = []
        self.config = self.load_config()
        self.setup_features()

    def load_config(self):
        default_config = {
            "api_key": os.getenv("OPENROUTER_API"),
            "features": {
                "command_suggest": {"enabled": True},
                "package_manager": {"enabled": True, "confirm_destructive": True},
                "task_scheduler": {"enabled": True, "cron_dir": str(Path.home() / ".cronjobs")},
                "self_updater": {"enabled": False, "repo_url": "https://github.com/your/repo/raw/main/"}
            }
        }
        try:
            with open("ai_config.json") as f:
                return {**default_config, **json.load(f)}
        except (FileNotFoundError, json.JSONDecodeError):
            return default_config

    def setup_features(self):
        """Initialize all integrated features"""
        # Feature 2: Command Suggestions
        if self.config['features']['command_suggest']['enabled']:
            self.add_command("suggest", self.suggest_commands)

        # Feature 3: Package Manager
        if self.config['features']['package_manager']['enabled']:
            self.add_command("pkg", self.pkg_manager)

        # Feature 10: Task Scheduler
        if self.config['features']['task_scheduler']['enabled']:
            self.add_command("schedule", self.schedule_task)
            self.add_command("cron", self.list_scheduled_tasks)

        # Feature 15: Self Updater
        if self.config['features']['self_updater']['enabled']:
            self.add_command("update", self.self_update)

    # ======================
    # FEATURE IMPLEMENTATIONS
    # ======================

    # --- Feature 2: Auto-Command Suggestion ---
    def suggest_commands(self, prompt):
        """AI-powered command suggestions"""
        llm_prompt = f"""Suggest 3 Termux commands for: '{prompt}'. 
        Format response as:
        - `command1`: explanation
        - `command2`: explanation"""
        
        response = self.ask_llm(llm_prompt)
        return self.extract_commands(response) or [("No suggestions", "Try a different query")]

    def extract_commands(self, text):
        """Extract commands from markdown-style response"""
        return re.findall(r'- `(.+?)`: (.+)', text)

    # --- Feature 3: Package Manager ---
    def pkg_manager(self, args):
        """Safe package operations"""
        actions = {
            'install': {'cmd': 'apt install -y', 'confirm': False},
            'remove': {'cmd': 'apt purge -y', 'confirm': self.config['features']['package_manager']['confirm_destructive']},
            'search': {'cmd': 'apt search', 'confirm': False},
            'update': {'cmd': 'apt update && apt upgrade -y', 'confirm': False}
        }

        try:
            action, *target = args.split()
            target = ' '.join(target)
        except ValueError:
            return "Usage: !pkg [install|remove|search|update] [target]"

        if action not in actions:
            return f"Invalid action. Choose from: {', '.join(actions.keys())}"

        if actions[action]['confirm']:
            if input(f"Confirm {action} {target}? [y/N] ").lower() != 'y':
                return "Action cancelled"

        result = subprocess.run(
            f"pkg {actions[action]['cmd']} {target}",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout or result.stderr or "Action completed"

    # --- Feature 10: Task Scheduler ---
    def schedule_task(self, schedule_cmd):
        """Create cron jobs"""
        try:
            # Parse schedule and command (supporting quoted commands)
            parts = schedule_cmd.split('"')
            if len(parts) >= 3:  # Has quotes
                schedule = parts[0].strip()
                command = parts[1]
            else:  # No quotes
                schedule, command = schedule_cmd.split(maxsplit=1)
        except (IndexError, ValueError):
            return 'Usage: !schedule "*/5 * * * *" "command"'

        cron_dir = Path(self.config['features']['task_scheduler']['cron_dir'])
        cron_dir.mkdir(exist_ok=True)

        # Fixed job counting with proper parenthesis
        job_count = len(list(cron_dir.glob('*')))
        job_file = cron_dir / f"job_{job_count + 1}.cron"
        
        job_file.write_text(f"{schedule} {command}\n")
        subprocess.run(f"crontab {cron_dir}/*", shell=True)
        return f"⏰ Scheduled: '{command}' at {schedule}"

    def list_scheduled_tasks(self, _):
        """List active cron jobs"""
        return subprocess.getoutput("crontab -l") or "No scheduled tasks"

    # --- Feature 15: Self-Updater ---
    def self_update(self, _):
        """Secure self-update mechanism"""
        if not self.config['features']['self_updater']['enabled']:
            return "Self-update disabled in config"

        repo_url = self.config['features']['self_updater']['repo_url']
        if "YOUR_OFFICIAL_REPO" in repo_url:
            return "❌ Please configure your repo URL in ai_config.json"

        # Verify current file hash
        with open(__file__, 'rb') as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()

        # Get latest hash
        try:
            new_hash = requests.get(f"{repo_url}/checksum.sha256").text.strip()
        except requests.RequestException:
            return "❌ Failed to fetch update info"

        if new_hash == current_hash:
            return "✅ Already running latest version"

        # Perform update
        try:
            response = requests.get(f"{repo_url}/ai_assistant.py")
            response.raise_for_status()
            with open(__file__, 'w') as f:
                f.write(response.text)
            return "🔄 Update complete. Please restart."
        except Exception as e:
            return f"❌ Update failed: {str(e)}"

    # --- Bonus: Context System ---
    def get_system_context(self):
        """Gather real-time system info"""
        return {
            "system": {
                "os": platform.system(),
                "termux": os.path.exists("/data/data/com.termux"),
                "storage": subprocess.getoutput("df -h /").splitlines()[1],
                "time": datetime.now().isoformat()
            },
            "environment": {
                "cwd": os.getcwd(),
                "python": platform.python_version()
            }
        }

    def enhance_prompt(self, prompt):
        """Augment user prompts with context"""
        context = self.get_system_context()
        return f"""
        [System Context]
        {json.dumps(context, indent=2)}
        
        [User Query]
        {prompt}
        """

    # ======================
    # CORE METHODS
    # ======================
    def add_command(self, prefix, handler):
        """Register new command handlers"""
        setattr(self, f"cmd_{prefix}", handler)

    def ask_llm(self, prompt):
        """LLM communication handler"""
        if not self.config['api_key']:
            return "❌ Error: No API key configured"
        
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": self.enhance_prompt(prompt)}]
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ API Error: {str(e)}"

    def process_command(self, user_input):
        """Main command processor"""
        if user_input.startswith("!"):
            for prefix in self.config['features']:
                if user_input.startswith(f"!{prefix}"):
                    handler = getattr(self, f"cmd_{prefix}", None)
                    if handler:
                        return handler(user_input[len(prefix)+2:].strip())
        
        return self.run_shell(user_input)

    def run_shell(self, command):
        """Safe shell execution"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                executable='/data/data/com.termux/files/usr/bin/bash',
                capture_output=True,
                text=True
            )
            output = (result.stdout or result.stderr or "Command executed").strip()
            self.memory.append({"command": command, "output": output, "time": datetime.now().isoformat()})
            return output
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ======================
# MAIN EXECUTION
# ======================
if __name__ == "__main__":
    ai = TermuxAI()
    print("🤖 Termux AI Assistant - All-in-One Edition")
    print("Type '!help' for available commands")

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                break

            if user_input == "!help":
                print("""
                🆘 Available Commands:
                !suggest [query] - Get command suggestions
                !pkg [action] [target] - Package management
                !schedule \"time\" \"cmd\" - Schedule tasks
                !cron - List scheduled jobs
                !update - Update the assistant
                """)
                continue

            print(ai.process_command(user_input))

        except KeyboardInterrupt:
            print("\nUse 'exit' or 'quit' to exit")
        except Exception as e:
            print(f"💥 Critical error: {str(e)}")