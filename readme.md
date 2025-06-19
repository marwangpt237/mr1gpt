[العربية](README_ar.md)

# Termux EL AI Agent

This project aims to create a powerful, intelligent, and autonomous AI assistant for Termux, capable of executing commands, thinking on its own, and interacting via various interfaces, including a Telegram bot.

## Features

-   **Modular Architecture:** Organized into core components, operational modes, and interfaces for easy maintenance and expansion.
-   **AgentLoop (Think & Act):** The AI can analyze, plan, execute commands, and review results autonomously.
-   **Red Team Mode:** A specialized mode for network and system discovery, enumeration, and exploitation, integrating with tools like Nmap, Whois, and Metasploit.
-   **Telegram Bot Integration:** Control and interact with the AI agent remotely via Telegram.
-   **Silent Mode:** Execute commands and receive responses without printing them to the console.
-   **Dynamic System Prompt:** The AI's persona and behavior can be changed dynamically based on the active mode.

## Setup and Installation

### 1. Install Termux

If you don't have Termux, install it from F-Droid or GitHub (Google Play Store version might be outdated).

### 2. Update Termux Packages

```bash
pkg update && pkg upgrade
```

### 3. Install Python and Pip

```bash
pkg install python
```

### 4. Install Python Dependencies

```bash
pip install requests python-dotenv python-telegram-bot
```

### 5. Install External Tools (for Red Team Mode)

-   **Nmap & Whois:**
    ```bash
    pkg install nmap whois
    ```
-   **Metasploit Framework (Optional & Advanced):**
    Installing Metasploit in Termux is complex and resource-intensive. Search for up-to-date guides (e.g., "install metasploit termux"). A common method involves:
    ```bash
    pkg install curl wget git
    curl -LO https://raw.githubusercontent.com/Hax4us/Metasploit_termux/master/metasploit.sh
    chmod +x metasploit.sh
    ./metasploit.sh
    ```
    **Warning:** Metasploit installation can be unstable and requires significant storage.

### 6. Clone the Project (or copy files)

If you have `git` installed:
```bash
git clone <repository_url> EL # Replace <repository_url> with the actual URL if this were a repo
cd EL
```

If you're copying the files manually, ensure all files are placed in the correct modular structure:

```
EL/
├── core/
│   ├── executor.py
│   ├── memory.py
│   ├── llm_handler.py
│   └── context.py
├── modes/
│   ├── agentloop.py
│   └── redteam.py
├── interfaces/
│   └── telegram_bot.py
├── EL.py
└── .env
```

### 7. Configure Environment Variables (`.env` file)

Navigate to the `EL/` directory and open the `.env` file. You need to provide your API keys:

```
DEEPINFRA_API_KEY=YOUR_DEEPINFRA_API_KEY_HERE
DEEPINFRA_MODEL=deepseek-ai/DeepSeek-V3-0324
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
```

-   **`DEEPINFRA_API_KEY`:** Obtain this from DeepInfra (e.g., from your account dashboard).
-   **`DEEPINFRA_MODEL`:** The default is `deepseek-ai/DeepSeek-V3-0324`. You can change it to any other model supported by DeepInfra.
-   **`TELEGRAM_BOT_TOKEN`:** Talk to `@BotFather` on Telegram to create a new bot and get its token.

## Usage

### Running the Agent

Navigate to the `EL/` directory in Termux and run:

```bash
python EL.py
```

### Interacting with the Agent

Once running, you can type your commands directly into the Termux console.

#### Modes:

-   **Normal Agent Mode (Default):** The AI acts as a general-purpose assistant.
    -   To switch to this mode: `mode normal`
-   **Red Team Mode:** The AI acts as an elite red-team agent, focusing on network and system tasks.
    -   To switch to this mode: `mode redteam`

#### Special Commands:

-   `exit`: Quits the agent.
-   `silent on`: Activates silent mode. AI responses will not be printed to the console (useful for Telegram bot interaction).
-   `silent off`: Deactivates silent mode. AI responses will be printed to the console.
-   `start_telegram_bot`: Starts the Telegram bot interface. Once started, you can interact with the AI via your Telegram bot.

#### Red Team Mode Examples:

-   `scan network` (will execute `nmap -T4 -F 192.168.1.0/24` by default)
-   `whois example.com` (will execute `whois example.com`)
-   `use msf exploit/multi/handler` (will execute `msfconsole -q -x 'use exploit/multi/handler; run'`)

### Telegram Bot Usage

1.  Ensure `TELEGRAM_BOT_TOKEN` is correctly set in your `.env` file.
2.  Run the agent: `python EL.py`
3.  In the agent's console, type `start_telegram_bot`.
4.  Go to your Telegram app, find your bot by its username, and start chatting with it. You can send commands like `/start`, `/help`, or any natural language query.

## Security Considerations (CRITICAL!)

**Giving an AI direct access to execute arbitrary shell commands is a major security risk.** This project is designed for advanced users who understand these risks.

-   **Sandbox Environment:** Always run this agent in a sandboxed environment (e.g., a dedicated Termux instance, a virtual machine, or a chroot environment) that is isolated from your main system and sensitive data.
-   **Limited Permissions:** Ensure the Termux environment and the user running the script have only the absolute minimum necessary permissions.
-   **Command Confirmation:** For any production or sensitive use, **it is highly recommended to implement a user confirmation step** before the AI executes any command, especially those that are potentially destructive (e.g., `rm`, `mv`, `dd`, `format`). The current implementation executes commands directly for demonstration purposes.
-   **Network Isolation:** When using Red Team mode or any network-scanning capabilities, ensure you are only targeting networks and systems you have explicit permission to test (e.g., your own local test network, virtual machines).
-   **LLM Hallucinations:** Large Language Models can generate incorrect or non-existent commands. Always review the AI's suggested actions.

## Future Enhancements

-   **Tool Use / Function Calling:** Implement a more robust tool-use mechanism where the LLM directly calls predefined functions (e.g., `execute_command`, `read_file`) instead of parsing `<CMD>` tags.
-   **Risk Scoring:** Implement a feature to assess the risk level of suggested commands before execution.
-   **Voice Input:** Integrate voice recognition for hands-free interaction.
-   **Agent Improv Mode:** Develop self-improvement mechanisms based on successful and failed interactions.
-   **Persistent Memory:** Save conversation history and context to a file for long-term memory.

This project is a powerful tool. Use it responsibly and ethically.


