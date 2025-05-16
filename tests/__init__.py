"""
Test suite for the deadlock simulator.

This package contains test scenarios and utilities for verifying the correctness
of the deadlock simulator implementation.
"""

from .test_scenarios import (
    create_simple_deadlock,
    create_dining_philosophers,
    create_resource_allocation_scenario,
    run_test_scenario
)

__all__ = [
    'create_simple_deadlock',
    'create_dining_philosophers',
    'create_resource_allocation_scenario',
    'run_test_scenario'
]
