from dataclasses import dataclass

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING

from parametric_simulator.conf.config import Config


@dataclass
class General:
    max_simulations: int = MISSING
    script_name: str = MISSING
    default_args: dict = MISSING
    path: dict = MISSING


cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(name="general", node=General)
