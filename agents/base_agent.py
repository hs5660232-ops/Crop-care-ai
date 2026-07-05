import os

class OfflineAgent:
    """
    Base agent class for our offline farming assistant.
    Simulates a Google ADK agent by loading a local SKILL.md file for instruction guidance
    and executing logic in a structured manner.
    """
    def __init__(self, name: str, skill_folder: str = None, data_dir: str = "data"):
        self.name = name
        self.data_dir = data_dir
        self.skill_content = ""
        self.skill_metadata = {}
        
        if skill_folder:
            self.load_skill(skill_folder)

    def load_skill(self, skill_folder: str):
        """
        Loads the instructions and metadata from a local SKILL.md file.
        """
        skill_path = os.path.join("skills", skill_folder, "SKILL.md")
        if os.path.exists(skill_path):
            try:
                with open(skill_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Simple YAML front-matter parser
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        yaml_part = parts[1]
                        self.skill_content = parts[2].strip()
                        
                        # Parse lines
                        for line in yaml_part.strip().split("\n"):
                            if ":" in line:
                                key, val = line.split(":", 1)
                                self.skill_metadata[key.strip()] = val.strip().strip('"').strip("'")
                    else:
                        self.skill_content = content
                else:
                    self.skill_content = content
            except Exception as e:
                print(f"Error loading skill for agent {self.name}: {e}")
                self.skill_content = f"Error reading skill instructions: {e}"
        else:
            self.skill_content = "Default instruction: Act as a specialist agent in agricultural operations."

    def run(self, context: dict) -> dict:
        """
        To be implemented by specialist agents.
        Accepts a context dictionary and returns a result dictionary.
        """
        raise NotImplementedError("Specialist agents must override the run method.")
