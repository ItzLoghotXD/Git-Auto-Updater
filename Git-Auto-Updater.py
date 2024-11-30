import os
import subprocess
import yaml
from colorama import Fore, Style
import keyboard

# Configuration File Path
CONFIG_FILE = "config.yaml"

DEFAULT_CONFIG = {
    "repo_path": "path/to/local/repo",
    "commit_message": "Auto-updated",
    "shortcut": "ctrl+shift+p",
    "contents": "."
}

class GitAutoUpdater:
    def __init__(self):
        self.config = self.load_config()
        self.repo_path = self.config["repo_path"]
        self.commit_message = self.config["commit_message"]
        self.shortcut = self.config["shortcut"]
        self.contents = self.config["contents"]

    def load_config(self):
        """Load configuration from a YAML file."""
        if not os.path.exists(CONFIG_FILE):
            print(Fore.YELLOW + "Configuration file not found. Creating default config..." + Style.RESET_ALL)
            self.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        else:
            with open(CONFIG_FILE, "r") as f:
                return yaml.safe_load(f)

    def save_config(self, config):
        """Save configuration to a YAML file."""
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(config, f, default_flow_style=False)

    def update_repo(self):
        """Update the Git repository."""
        try:
            os.chdir(self.repo_path)

            # Stage files/folders dynamically
            print(Fore.CYAN + "Staging changes..." + Style.RESET_ALL)
            subprocess.run(["git", "add"] + self.contents.split(","), check=True)
            print(Fore.GREEN + "Staged all changes!" + Style.RESET_ALL)

            # Commit with a custom or default message
            subprocess.run(["git", "commit", "-m", self.commit_message], check=True)
            print(Fore.GREEN + "Committed changes!" + Style.RESET_ALL)

            # Push changes to the remote repository
            subprocess.run(["git", "push"], check=True)
            print(Fore.GREEN + "Pushed changes to GitHub!" + Style.RESET_ALL)

        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Git command failed: {e}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)

    def listen_for_shortcut(self):
        """Listen for the user-defined shortcut."""
        print(Fore.GREEN + f"Listening for '{self.shortcut}'..." + Style.RESET_ALL)
        print(Fore.YELLOW + "Press ESC+CTRL to exit." + Style.RESET_ALL)
        keyboard.add_hotkey(self.shortcut, self.update_repo)
        keyboard.wait("esc+ctrl")
        print(Fore.YELLOW + "Exiting..." + Style.RESET_ALL)

    def ensure_git_installed(self):
        """Check if Git is installed."""
        try:
            subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL)
        except FileNotFoundError:
            print(Fore.RED + "Git is not installed on your system." + Style.RESET_ALL)
            exit(1)

def main():
    updater = GitAutoUpdater()
    updater.ensure_git_installed()

    print(Fore.GREEN + "Configuration loaded from 'config.yaml':")
    print(Fore.YELLOW + f"- Repository Path: {updater.repo_path}")
    print(f"- Commit Message: {updater.commit_message}")
    print(f"- Shortcut: {updater.shortcut}" + Style.RESET_ALL)

    print(Fore.BLUE + "\nStarting Git Auto-Updater..." + Style.RESET_ALL)
    updater.listen_for_shortcut()

if __name__ == "__main__":
    main()
