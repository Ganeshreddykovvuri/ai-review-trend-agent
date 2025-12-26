import json
from agents.openrouter_client import client


class TopicCanonicalizationAgent:
    def __init__(self, memory_path):
        self.memory_path = memory_path
        self._load_memory()

    def _load_memory(self):
        try:
            with open(self.memory_path, "r") as f:
                self.topic_store = json.load(f)
        except:
            self.topic_store = {}
            with open(self.memory_path, "w") as f:
                json.dump({}, f)

    def _save_memory(self):
        with open(self.memory_path, "w") as f:
            json.dump(self.topic_store, f, indent=2)

    def canonicalize(self, new_topic):
        new_topic = new_topic.strip()

        if not self.topic_store:
            self.topic_store[new_topic] = {"aliases": [new_topic]}
            self._save_memory()
            return new_topic

        existing_topics = list(self.topic_store.keys())

        prompt = f"""
Decide if the NEW topic represents the SAME user issue
as one of the EXISTING topics.

NEW topic:
"{new_topic}"

EXISTING topics:
{existing_topics}

Rules:
- Return ONLY the best matching EXISTING topic
- If none match, return the NEW topic exactly
- Do NOT explain your answer
- Do NOT return sentences

Return ONE topic string only.
"""

        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            candidate = response.choices[0].message.content.strip()

            # 🔒 HARD VALIDATION (critical fix)
            invalid_phrases = [
                "none of the existing",
                "no existing",
                "do not represent",
                "same user issue",
                "cannot be mapped"
            ]

            if (
                len(candidate) > 80
                or any(p in candidate.lower() for p in invalid_phrases)
                or candidate not in existing_topics
            ):
                canonical = new_topic
            else:
                canonical = candidate

        except Exception:
            canonical = new_topic

        if canonical in self.topic_store:
            self.topic_store[canonical]["aliases"].append(new_topic)
        else:
            self.topic_store[canonical] = {"aliases": [new_topic]}

        self._save_memory()
        return canonical
