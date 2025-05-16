"""
Deadlock detection algorithms.

This subpackage provides implementations of various deadlock detection algorithms,
including resource allocation graph analysis and the banker's algorithm.
"""

from .detector import DeadlockDetector

__all__ = ['DeadlockDetector']
