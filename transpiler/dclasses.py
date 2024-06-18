from dataclasses import dataclass
import ast


@dataclass
class ConvertedDict:
    dict: ast.Dict
    name: ast.Name