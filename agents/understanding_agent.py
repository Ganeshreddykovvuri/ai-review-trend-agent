import json
from agents.openrouter_client import client


class ReviewUnderstandingAgent:
    def extract_topics(self, review_text):
        prompt = f"""
You are analyzing Google Play Store reviews for the Swiggy food delivery app.

Extract ALL issues, complaints, or feature requests.
Be very specific to Swiggy app behavior and services.

Prefer app-level or service-level issues such as:
- Delivery delay
- Delivery partner behavior
- Food quality (stale, cold, poor packaging)
- Instamart availability, night hours, slot issues
- Bolt / 10-minute delivery availability
- App crashes, slow app, login issues
- GPS, maps, address detection issues
- Payment failures, refunds, wallet issues
- Order cancellation or reassignment
- Customer support issues

Rules:
- Use concise, canonical topic names
- Avoid generic labels like "general feedback"
- Merge paraphrases into one clear issue
- Create a NEW topic only if none fit

Return STRICT JSON array only.
Example:
[
  "Delivery delay",
  "Delivery partner rude",
  "Instamart night availability",
  "Bolt delivery removed"
]

Review:
"{review_text}"
"""

        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            content = response.choices[0].message.content.strip()
            raw_topics = json.loads(content)

            return self._normalize_topics(raw_topics)

        except Exception:
            # If LLM fails, return empty list (no generic noise)
            return []

    def _normalize_topics(self, topics):
        """
        Normalize topic strings to prevent duplicates:
        - Remove quotes
        - Trim spaces
        - Standardize casing
        - Remove empty or generic topics
        """
        cleaned = []
        for t in topics:
            if not isinstance(t, str):
                continue

            t = t.strip()
            t = t.strip('"').strip("'")   # remove accidental quotes
            t = t.strip()

            if not t:
                continue

            # Standardize capitalization
            t = t.title()

            # Explicitly block generic junk
            if t.lower() in {"general feedback", "feedback", "general issue"}:
                continue

            cleaned.append(t)

        return cleaned
