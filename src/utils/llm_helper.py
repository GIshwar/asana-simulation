"""
LLM helper utilities for generating realistic text content
in the Asana workspace simulation.

Supports OpenAI API with safe fallbacks when unavailable.
"""

from __future__ import annotations

import os
import time
import random
from typing import List, Dict

import openai
from tqdm import tqdm  # ✅ ADDED

from utils.random_utils import random_sentence
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Read key and set config
_OPENAI_KEY = os.getenv("OPENAI_API_KEY")
LLM_ENABLED = bool(_OPENAI_KEY)
_OPENAI_INITIALIZED = False

if LLM_ENABLED:
    openai.api_key = _OPENAI_KEY
    _OPENAI_INITIALIZED = True
else:
    print("[⚠️ Warning] LLM disabled: Missing OPENAI_API_KEY in .env")


def random_sentence():
    """Fallback synthetic generator if LLM not active."""
    samples = [
        "Review pending tickets and update progress.",
        "Optimize the data pipeline for faster ETL.",
        "Schedule design review meeting with UX team.",
        "Prepare product roadmap for next sprint.",
    ]
    return random.choice(samples)


# Global toggle to disable LLM usage (e.g., CI, offline runs)
# LLM_ENABLED = True
# _OPENAI_INITIALIZED = False


def init_openai(api_key: str | None = None) -> None:
    """
    Initialize OpenAI client using provided API key or environment variable.

    Args:
        api_key: Optional OpenAI API key.
    """
    global _OPENAI_INITIALIZED

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        LLM_ENABLED = False
        return

    openai.api_key = key
    _OPENAI_INITIALIZED = True


def generate_text(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.8,
    max_tokens: int = 80,
) -> str:
    """
    Generate text using OpenAI ChatCompletion API.

    Falls back to synthetic text if API is disabled or fails.

    Args:
        prompt: Input prompt.
        model: OpenAI model name.
        temperature: Sampling temperature.
        max_tokens: Max tokens to generate.

    Returns:
        Generated text string.
    """
    if not LLM_ENABLED or not _OPENAI_INITIALIZED:
        return random_sentence()

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message["content"].strip()
    except Exception:
        return random_sentence()


def safe_generate(prompt: str, retries: int = 3, base_delay: float = 1.0) -> str:
    """
    Safely generate text with retries and exponential backoff.

    Args:
        prompt: Input prompt.
        retries: Number of retry attempts.
        base_delay: Initial backoff delay in seconds.

    Returns:
        Generated text.
    """
    for attempt in range(retries):
        try:
            return generate_text(prompt)
        except Exception:
            time.sleep(base_delay * (2**attempt))

    return random_sentence()


def load_prompts(file_path: str) -> List[str]:
    """
    Load prompt templates from a text file.

    Args:
        file_path: Path to prompt file.

    Returns:
        List of prompt strings.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def generate_from_template(template: str, variables: Dict[str, str]) -> str:
    """
    Replace placeholders in a template with actual values.

    Args:
        template: Template string with placeholders.
        variables: Mapping of placeholder -> value.

    Returns:
        Rendered string.
    """
    result = template
    for key, value in variables.items():
        result = result.replace(f"{{{key}}}", str(value))
    return result


if __name__ == "__main__":
    print("=== llm_helper demo ===")

    init_openai()

    sample_prompts = [
        "Write a task description for project 'Growth Dashboard'.",
        "Generate a short comment about fixing a production bug.",
        "Describe a marketing project focused on lead generation.",
    ]

    for p in tqdm(sample_prompts, desc="Generating LLM text"):  # ✅ UPDATED
        print("-", safe_generate(p))

    print("[✅] llm_helper demo completed successfully.")  # ✅ ADDED
