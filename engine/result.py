"""Common result object returned by every registered solver."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SolveResult:
    method: str
    plaintext: str
    key: str
    score: float
    details: dict = field(default_factory=dict)

    def summary(self) -> str:
        lines = [
            f"method: {self.method}",
            f"key: {self.key}",
            f"score: {self.score:.4f}",
        ]
        for name, value in self.details.items():
            lines.append(f"{name}: {value}")
        lines.append("plaintext:")
        lines.append(self.plaintext)
        return "\n".join(lines)
