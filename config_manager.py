import yaml
from evaluators.evaluation_types import EvaluationType
from typing import Dict, Any, List


class ConfigManager:
    def __init__(self, config_path: str = 'config.yml'):
        self.config_path = config_path
        self._config = None

    def load_config(self) -> Dict[str, Any]:
        if self._config is None:
            with open(self.config_path, 'r') as file:
                self._config = yaml.safe_load(file)
            self._config['evaluation_type'] = EvaluationType[self._config['evaluation_type']]
        return self._config

    @property
    def subject_models(self) -> List[Dict[str, str]]:
        return self.load_config()['subject_models']

    @property
    def evaluator(self) -> str:
        return self.load_config()['evaluator']

    @property
    def evaluator_model(self) -> str:
        return self.load_config()['evaluator_model']

    @property
    def number_of_tests(self) -> int:
        return self.load_config()['number_of_tests']

    @property
    def dataset(self) -> str:
        return self.load_config()['dataset']

    @property
    def evaluation_type(self) -> EvaluationType:
        return self.load_config()['evaluation_type']

    @property
    def powermetrics(self) -> bool:
        return self.load_config()['powermetrics']