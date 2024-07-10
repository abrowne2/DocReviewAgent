from interpreter import interpreter
import os
import subprocess
import json

# The base model used for code analysis and generation
BASE_DEEP_SEEK_CODER_MODEL = 'ollama/wizardlm2:latest'

BASE_CONTEXT_WINDOW = 128000

# Maximum number of tokens to generate in a single response
BASE_MAX_TOKENS = 20000

# Needs ollama to run. TODO: check ollama is running
BASE_API_BASE = "http://localhost:11434/"

# The path to the Git repository to analyze
DESIRED_REPO = "/Users/adambrowne/Desktop/sequence/cloud-project-system"

class DocReviewAgent:
    def __init__(self):
        self.interpreter = interpreter
        self.interpreter.offline = True  
        self.interpreter.llm.model = BASE_DEEP_SEEK_CODER_MODEL
        self.interpreter.api_base = BASE_API_BASE
        self.interpreter.llm.context_window = BASE_CONTEXT_WINDOW
        self.interpreter.llm.max_tokens = BASE_MAX_TOKENS

    def chat(self, message):
        return self.interpreter.chat(message)

    def root_dir(self):
        return DESIRED_REPO

    def get_git_diff(self):
        try:
            diff_output = subprocess.check_output(['git', 'diff', 'main'], cwd=DESIRED_REPO).decode('utf-8')
            return diff_output
        except subprocess.CalledProcessError as e:
            print(f"Error running git diff: {e}")
            return None

    def create_diff_corpus(self):
        diff_output = self.get_git_diff()
        if diff_output is None:
            return None

        corpus = {
            "files_changed": [],
        }

        current_file = None
        for line in diff_output.split('\n'):
            if line.startswith('diff --git'):
                file_path = line.split()[-1][2:]
                print(file_path)
                if file_path not in corpus["files_changed"] and not file_path.endswith('gstreamer') and not file_path.endswith('.yaml'):
                    corpus["files_changed"].append(file_path)
                    with open(os.path.join(DESIRED_REPO, file_path), 'r') as file:
                        file_content = file.read()
                    corpus[file_path] = file_content

        if current_file:
            corpus["files_changed"].append(current_file)

        del corpus["files_changed"]
        return corpus
