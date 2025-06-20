[العربية](README_ar.md)

[My Portfolio](https://marwangpt237.github.io/Nefy/)

# <span style="color: #00ff00;">[[ TERMUX AI ASSISTANT ]]</span>

```bash
#####################################################################
#                                                                   #
#   A.I. Powered Shell Companion for Termux - DeepInfra Edition    #
#                                                                   #
#   > Status: ONLINE                                                #
#   > Protocol: LLM_CMD_INTERCEPT                                   #
#   > Environment: TERMUX_SHELL                                     #
#                                                                   #
#####################################################################
```

This Python script transforms your Termux environment into an interactive AI-powered command-line assistant. By integrating with the DeepInfra API, it enables conversational interaction, intelligent command suggestions, and automated execution within your shell.

## <span style="color: #00ffff;">// CORE CAPABILITIES //</span>

*   **LLM Integration**: Seamlessly connects to DeepInfra's powerful Large Language Models for natural language understanding and generation.
*   **Command Interception & Execution**: Intelligently identifies shell commands within AI responses (encapsulated in `<CMD>...</CMD>` tags) and executes them directly.
*   **Contextual Awareness**: Maintains a dynamic conversation history, providing the LLM with crucial context for more accurate and relevant interactions.
*   **Output Interpretation**: Feeds command outputs (and errors) back to the LLM for real-time analysis and further actionable insights.
*   **Configurable AI Model**: Easily switch between various DeepInfra models to tailor the AI's behavior and capabilities.

## <span style="color: #00ffff;">// SYSTEM REQUIREMENTS //</span>

Before deploying the AI Assistant, ensure your Termux environment meets the following specifications:

*   **Python 3.x**: The core interpreter for the script.
*   **pip**: Python's package management system.
*   **DeepInfra API Key**: An active API key from DeepInfra is mandatory for LLM access.

## <span style="color: #00ffff;">// DEPLOYMENT PROCEDURE //</span>

Follow these steps to set up the AI Assistant in your Termux environment:

1.  **Acquire Script**: Download or clone the `ai_assistant.py` script to your desired directory within Termux.

2.  **Install Dependencies**: Execute the following command in your Termux terminal to install required Python libraries:

    ```bash
    pip install python-dotenv requests
    ```

3.  **API Key Configuration**: Create a file named `.env` in the *same directory* as `ai_assistant.py`. Populate it with your DeepInfra API key:

    ```text
    DEEPINFRA_API_KEY=YOUR_API_KEY_HERE
    ```
    **NOTE**: Replace `YOUR_API_KEY_HERE` with your actual DeepInfra API key.

## <span style="color: #00ffff;">// OPERATIONAL PARAMETERS //</span>

Customize the AI Assistant's behavior by modifying these parameters:

*   **`DEEPINFRA_API_KEY`**: (Mandatory) Loaded from `.env`. This is your authentication token for DeepInfra services.

*   **`DEEPINFRA_MODEL`**: (Optional) Located within `ai_assistant.py`. Default is `deepseek-ai/DeepSeek-V3-0324`. Explore DeepInfra's model catalog to select an alternative:

    ```python
    DEEPINFRA_MODEL = "deepseek-ai/DeepSeek-V3-0324" # <--- ADJUST AS REQUIRED
    ```

*   **`max_tokens`**: (Optional) Controls the maximum length of AI-generated responses. Adjust in the `payload` dictionary within `get_llm_response`.

*   **`temperature`**: (Optional) Influences the creativity/randomness of AI responses (0.0 for deterministic, higher for more creative). Adjust in the `payload` dictionary.

## <span style="color: #00ffff;">// INITIATING ASSISTANT //</span>

To launch the AI Assistant, navigate to the script's directory in Termux and execute:

```bash
python ai_assistant.py
```

Interact with the AI by typing your queries or commands. The assistant will process your input, provide responses, and, if applicable, execute suggested shell commands, displaying their output.

Type `exit` to terminate the assistant session.

### <span style="color: #00ffff;">// INTERACTION LOG EXAMPLE //</span>

```text
Termux AI Assistant (powered by DeepInfra). Type 'exit' to quit.

You: What is my current working directory?
AI (raw response): Your current working directory is where you are currently operating within the file system. To find out what it is, you can use the `pwd` command. <CMD>pwd</CMD>
AI: I'm about to execute: `pwd`
Command Output:
/data/data/com.termux/files/home
AI: Your current working directory is `/data/data/com.termux/files/home`.

You: List the files in this directory.
AI (raw response): To list the files in your current directory, you can use the `ls` command. <CMD>ls</CMD>
AI: I'm about to execute: `ls`
Command Output:
ai_assistant.py
.bashrc
.env
AI: The files in your current directory are `ai_assistant.py`, `.bashrc`, and `.env`.

You: exit
Goodbye!
```

## <span style="color: #ff0000;">// SECURITY ADVISORY //</span>

**CRITICAL WARNING**: The script utilizes `shell=True` within `subprocess.run`, which poses a significant security risk if arbitrary or untrusted commands are executed. While designed for a personal Termux environment, be aware that malicious commands, whether from an unconstrained LLM or a compromised source, could potentially compromise your system.

**RECOMMENDATION**: It is **STRONGLY ADVISED** to uncomment and implement the user confirmation step before any command execution. This provides a crucial layer of security:

```python
            # --- SECURITY WARNING: Consider adding a confirmation step here! ---
            # confirm = input("Execute this command? (y/n): ").lower()
            # if confirm != 'y':
            #     print("Command execution cancelled.")
            #     conversation_history.append(f"AI: Command execution cancelled.")
            #     continue
```

## <span style="color: #ffcc00;">// TROUBLESHOOTING LOG //</span>

*   **`DEEPINFRA_API_KEY not found`**: Verify the `.env` file exists in the correct directory and contains `DEEPINFRA_API_KEY=YOUR_API_KEY_HERE`.
*   **`Error communicating with DeepInfra API`**: Check your network connectivity and confirm your `DEEPINFRA_API_KEY` is valid and active.
*   **`Command not found`**: If the AI suggests an unrecognized command, you may need to install the corresponding package in Termux (e.g., `pkg install <package_name>`).

## <span style="color: #00ff00;">// LICENSE //</span>

This project is distributed under the **MIT License**.

