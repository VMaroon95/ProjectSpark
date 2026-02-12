"""
Prompt Architecture Definitions
================================
Five distinct prompt strategies for evaluating LLM sensitivity
on multiple-choice benchmarks like MMLU.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class PromptArchitecture(ABC):
    """Base class for all prompt architectures."""

    name: str
    description: str
    key: str

    @abstractmethod
    def transform(self, task_prompt: str, choices: List[str], subject: Optional[str] = None) -> str:
        """Transform a raw task prompt + choices into the final prompt string."""
        ...

    def _format_choices(self, choices: List[str]) -> str:
        labels = "ABCDEFGHIJ"
        return "\n".join(f"({labels[i]}) {c}" for i, c in enumerate(choices))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"


class ZeroShot(PromptArchitecture):
    """Raw question with no examples, instructions, or scaffolding."""

    name = "Zero-Shot"
    description = "Bare question with answer choices — no examples, no instructions."
    key = "zero_shot"

    def transform(self, task_prompt: str, choices: List[str], subject: Optional[str] = None) -> str:
        return (
            f"{task_prompt}\n\n"
            f"{self._format_choices(choices)}\n\n"
            f"Answer:"
        )


class ChainOfThought(PromptArchitecture):
    """Step-by-step reasoning instruction before answering."""

    name = "Chain-of-Thought"
    description = "Prepends 'Let's think step by step' reasoning scaffold."
    key = "chain_of_thought"

    def transform(self, task_prompt: str, choices: List[str], subject: Optional[str] = None) -> str:
        return (
            f"{task_prompt}\n\n"
            f"{self._format_choices(choices)}\n\n"
            f"Let's think step by step. First, analyze what the question is asking. "
            f"Then, consider each answer choice carefully. "
            f"Finally, select the best answer based on your reasoning.\n\n"
            f"Step-by-step reasoning:\n"
        )


class PersonaBased(PromptArchitecture):
    """Wraps the prompt with a domain-expert persona."""

    name = "Persona-Based"
    description = "Assigns a domain-expert persona before posing the question."
    key = "persona_based"

    PERSONA_MAP = {
        "stem": "You are a distinguished professor of science, technology, engineering, and mathematics with 25 years of research experience and hundreds of published papers.",
        "humanities": "You are a world-renowned humanities scholar with expertise spanning philosophy, history, literature, and the arts.",
        "social_sciences": "You are a leading social scientist with deep expertise in psychology, economics, political science, and sociology.",
        "other": "You are a highly knowledgeable expert with broad interdisciplinary expertise across professional and academic domains.",
    }

    def transform(self, task_prompt: str, choices: List[str], subject: Optional[str] = None) -> str:
        persona = self.PERSONA_MAP.get(subject or "other", self.PERSONA_MAP["other"])
        return (
            f"{persona}\n\n"
            f"Given your expertise, please answer the following question:\n\n"
            f"{task_prompt}\n\n"
            f"{self._format_choices(choices)}\n\n"
            f"Based on your expert knowledge, the correct answer is:"
        )


class FewShot(PromptArchitecture):
    """Includes 3 example Q&A pairs before the actual question."""

    name = "Few-Shot"
    description = "Provides 3 solved examples before the target question."
    key = "few_shot"

    EXAMPLES = [
        {
            "question": "What is the primary function of mitochondria in eukaryotic cells?",
            "choices": ["Protein synthesis", "ATP production", "DNA replication", "Cell division"],
            "answer": "B",
            "explanation": "Mitochondria are the powerhouses of the cell, responsible for producing ATP through oxidative phosphorylation.",
        },
        {
            "question": "Which economic principle states that as the price of a good increases, the quantity demanded decreases?",
            "choices": ["Law of Supply", "Law of Demand", "Pareto Efficiency", "Comparative Advantage"],
            "answer": "B",
            "explanation": "The Law of Demand describes the inverse relationship between price and quantity demanded.",
        },
        {
            "question": "In which year did the Treaty of Westphalia establish the concept of state sovereignty?",
            "choices": ["1555", "1648", "1776", "1815"],
            "answer": "B",
            "explanation": "The Peace of Westphalia in 1648 is widely regarded as establishing the modern concept of state sovereignty.",
        },
    ]

    def transform(self, task_prompt: str, choices: List[str], subject: Optional[str] = None) -> str:
        labels = "ABCDEFGHIJ"
        example_block = ""
        for i, ex in enumerate(self.EXAMPLES, 1):
            ex_choices = "\n".join(f"({labels[j]}) {c}" for j, c in enumerate(ex["choices"]))
            example_block += (
                f"Example {i}:\n"
                f"Q: {ex['question']}\n"
                f"{ex_choices}\n"
                f"A: ({ex['answer']}) {ex['explanation']}\n\n"
            )

        return (
            f"Answer the following multiple-choice question. Here are some examples:\n\n"
            f"{example_block}"
            f"Now answer this question:\n\n"
            f"Q: {task_prompt}\n"
            f"{self._format_choices(choices)}\n\n"
            f"A:"
        )


class DelimiterHeavy(PromptArchitecture):
    """Uses explicit delimiters to clearly structure prompt sections."""

    name = "Delimiter-Heavy"
    description = "Uses ###, \"\"\", and explicit section markers for clarity."
    key = "delimiter_heavy"

    def transform(self, task_prompt: str, choices: List[str], subject: Optional[str] = None) -> str:
        return (
            f"### TASK ###\n"
            f"Answer the multiple-choice question below by selecting the correct option.\n\n"
            f"### QUESTION ###\n"
            f'"""\n'
            f"{task_prompt}\n"
            f'"""\n\n'
            f"### ANSWER CHOICES ###\n"
            f"{self._format_choices(choices)}\n\n"
            f"### INSTRUCTIONS ###\n"
            f"- Read the question carefully\n"
            f"- Evaluate each option\n"
            f"- Respond with ONLY the letter of the correct answer\n\n"
            f"### YOUR ANSWER ###\n"
        )


# Registry of all architectures
ALL_ARCHITECTURES = [
    ZeroShot(),
    ChainOfThought(),
    PersonaBased(),
    FewShot(),
    DelimiterHeavy(),
]

ARCHITECTURE_MAP = {arch.key: arch for arch in ALL_ARCHITECTURES}


def get_architecture(key: str) -> PromptArchitecture:
    """Get a prompt architecture by key."""
    if key not in ARCHITECTURE_MAP:
        raise ValueError(f"Unknown architecture: {key}. Available: {list(ARCHITECTURE_MAP.keys())}")
    return ARCHITECTURE_MAP[key]
