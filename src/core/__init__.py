"""
Core components for the deadlock simulator.

This subpackage contains the fundamental classes and functions for simulating
processes, resources, and system interactions.
"""

from .process import Process
from .resource import Resource
from .system import System

__all__ = ['Process', 'Resource', 'System']
