"""
Type definitions of the configuration file
"""

from dataclasses import dataclass


@dataclass
class General:
    max_workers: int
    script_name: str
    default_args: dict
    path: dict


@dataclass
class Paths:
    paths: dict


@dataclass
class Rules:
    rules: dict


@dataclass
class ParametricSimulatorConfig:
    general: General
    paths: Paths
    rules: Rules
