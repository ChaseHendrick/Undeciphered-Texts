# SPDX-License-Identifier: MIT-0
"""Offline bounded ARC program synthesis inside the existing engine."""
from .solver import POLICIES, solve_task

__all__ = ['POLICIES', 'solve_task']
