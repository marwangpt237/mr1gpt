import subprocess
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration for DeepInfra ---
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")
if not DEEPINFRA_API_KEY:
    print("Error: DEEPINFRA_API_KEY not found in .env file.")
    print("Please create a .env file in the same directory as this script with: DEEPINFRA_API_KEY=YOUR_API_KEY")
    exit(1)

# Choose your DeepInfra model. You can find available models on DeepInfra's website.
# Example: mistralai/Mistral-7B-Instruct-v0.2, meta-llama/Llama-2-7b-chat-hf
DEEPINFRA_MODEL = "deepseek-ai/DeepSeek-V3-0324" # <--- IMPORTANT: Choose your desired model

DEEPINFRA_API_URL = f"https://api.deepinfra.com/v1/openai/chat/completions"

# --- LLM Interaction Function ---
def get_llm_response(prompt_text, current_context=""):
    """Sends prompt to DeepInfra LLM and gets a response."""
    headers = {
        "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
        "Content-Type": "application/json"
    }

    # DeepInfra's OpenAI-compatible API expects messages in a specific format.
    # We'll build a system message to guide the AI and user messages for the conversation.
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant operating within a Termux shell environment. "
                "Your primary goal is to help the user by providing information, answering questions, "
                "and suggesting shell commands to accomplish tasks. "
                "When suggesting a shell command, always wrap it in `<CMD>...</CMD>` tags. "
                "If you need more information from the user or the terminal, ask for it. "
                "Be concise and directly answer questions or provide commands. "
                "If a command is executed, I will provide its output for you to interpret."
            )
        }
    ]

    # Add previous conversation context
    if current_context:
        messages.append({"role": "user", "content": f"Previous context:\n{current_context}"})

    # Add the current user's request
    messages.append({"role": "user", "content": prompt_text})

    payload = {
        "model": DEEPINFRA_MODEL,
        "messages": messages,
        "max_tokens": 500, # Adjust as needed
        "temperature": 0.7, # Adjust for creativity vs. predictability
        "stream": False
    }

    try:
        response = requests.post(DEEPINFRA_API_URL, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        response_data = response.json()

        # Extract the content from the LLM's response
        if response_data and response_data.get('choices'):
            return response_data['choices'][0]['message']['content'].strip()
        else:
            return "Error: No valid response from LLM."

    except requests.exceptions.RequestException as e:
        return f"Error communicating with DeepInfra API: {e}"
    except Exception as e:
        return f"An unexpected error occurred while processing LLM response: {e}"

# --- Command Execution Function (remains the same) ---
def execute_command(command):
    """Executes a shell command and returns its output."""
    try:
        # shell=True is convenient but can be a security risk if command is not sanitized.
        # For a personal assistant, it might be acceptable, but be aware.
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return "", f"Command failed with error: {e.stderr}"
    except FileNotFoundError:
        return "", f"Command not found: {command.split()[0]}"
    except Exception as e:
        return "", f"An unexpected error occurred: {e}"

# --- Main Loop (remains largely the same) ---
def main():
    print("Termux AI Assistant (powered by DeepInfra). Type 'exit' to quit.")
    conversation_history = [] # Stores past interactions for context

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Build context for the LLM from recent conversation history
        # We'll send the last few turns to the LLM to maintain continuity
        context_for_llm = "\n".join(conversation_history[-4:]) # Keep last 4 turns (user + AI)

        llm_response = get_llm_response(user_input, context_for_llm)
        print(f"AI (raw response): {llm_response}") # For debugging the LLM's direct output

        # Add current user input to history
        conversation_history.append(f"User: {user_input}")

        # Check if the LLM suggested a command
        if "<CMD>" in llm_response and "</CMD>" in llm_response:
            start_index = llm_response.find("<CMD>") + len("<CMD>")
            end_index = llm_response.find("</CMD>")
            command_to_execute = llm_response[start_index:end_index].strip()

            print(f"AI: I'm about to execute: `{command_to_execute}`")
            # --- SECURITY WARNING: Consider adding a confirmation step here! ---
            # confirm = input("Execute this command? (y/n): ").lower()
            # if confirm != 'y':
            #     print("Command execution cancelled.")
            #     conversation_history.append(f"AI: Command execution cancelled.")
            #     continue

            stdout, stderr = execute_command(command_to_execute)

            if stdout:
                print(f"Command Output:\n{stdout}")
                # Send output back to LLM for interpretation
                interpreted_response = get_llm_response(
                    f"The command `{command_to_execute}` produced the following output:\n{stdout}\n\nPlease summarize this output or provide further assistance based on it.",
                    context_for_llm + f"\nCommand Output: {stdout}" # Add command output to context for interpretation
                )
                print(f"AI: {interpreted_response}")
                conversation_history.append(f"AI: Executed `{command_to_execute}`. Output: {stdout}. Response: {interpreted_response}")
            if stderr:
                print(f"Command Error:\n{stderr}")
                # Send error back to LLM for interpretation
                interpreted_response = get_llm_response(
                    f"The command `{command_to_execute}` produced the following error:\n{stderr}\n\nPlease explain this error or suggest a fix.",
                    context_for_llm + f"\nCommand Error: {stderr}" # Add command error to context for interpretation
                )
                print(f"AI: {interpreted_response}")
                conversation_history.append(f"AI: Executed `{command_to_execute}`. Error: {stderr}. Response: {interpreted_response}")
        else:
            # If no command was suggested, just print the LLM's direct response
            print(f"AI: {llm_response}")
            conversation_history.append(f"AI: {llm_response}")

if __name__ == "__main__":
    main()
