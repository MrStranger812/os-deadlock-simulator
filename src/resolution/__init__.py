"""
Deadlock resolution strategies.

This subpackage provides implementations of various deadlock resolution techniques,
including process termination, resource preemption, and rollback.
"""

from .resolver import DeadlockResolver

__all__ = ['DeadlockResolver']
