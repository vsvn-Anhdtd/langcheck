from __future__ import annotations

import json
import re
from typing import Callable, Container, Iterable, List, Optional

from langcheck.eval.eval_value import EvalValue


def is_int(generated_outputs: List[str],
           domain: Iterable[int] | Container[int] | None = None,
           prompts: Optional[List[str]] = None) -> EvalValue[int]:
    '''Checks if generated outputs can be parsed as integers, optionally within
    a domain of integers like `range(1, 11)` or `{1, 3, 5}`. This metric takes
    on binary 0 or 1 values.

    Args:
        generated_outputs: A list of model generated outputs to evaluate
        domain: The optional domain of valid integers
        prompts: An optional list of prompts used to generate the outputs.
            Prompts are not evaluated and only used as metadata.

    Returns:
        An EvalValue object
    '''
    # The values are binary: 1 for success and 0 for failure
    metric_values = []
    for output in generated_outputs:
        try:
            output_int = int(output)
            if domain is None or output_int in domain:
                metric_values.append(1)
            else:
                metric_values.append(0)
        except:
            metric_values.append(0)

    return EvalValue(metric_name='is_int',
                     prompts=prompts,
                     generated_outputs=generated_outputs,
                     reference_outputs=None,
                     metric_values=metric_values,
                     language=None)


def is_float(generated_outputs: List[str],
             min: Optional[float] = None,
             max: Optional[float] = None,
             prompts: Optional[List[str]] = None) -> EvalValue[int]:
    '''Checks if generated outputs can be parsed as floating point numbers,
    optionally within a min/max range. This metric takes on binary 0 or 1
    values.

    Args:
        generated_outputs: A list of model generated outputs to evaluate
        min: The optional minimum valid float
        max: The optional maximum valid float
        prompts: An optional list of prompts used to generate the outputs.
            Prompts are not evaluated and only used as metadata.


    Returns:
        An EvalValue object
    '''
    # The values are binary: 1 for success and 0 for failure
    metric_values = []
    for output in generated_outputs:
        try:
            output_float = float(output)
            if min is None and max is None:
                metric_values.append(1)
            elif min is not None and output_float < min:
                metric_values.append(0)
            elif max is not None and output_float > max:
                metric_values.append(0)
            else:
                metric_values.append(1)
        except:
            metric_values.append(0)

    return EvalValue(metric_name='is_float',
                     prompts=prompts,
                     generated_outputs=generated_outputs,
                     reference_outputs=None,
                     metric_values=metric_values,
                     language=None)


def is_json_object(generated_outputs: List[str],
                   prompts: Optional[List[str]] = None) -> EvalValue[int]:
    '''Checks if generated outputs can be parsed as JSON objects. This metric
    takes on binary 0 or 1 values.

    Args:
        generated_outputs: A list of model generated outputs to evaluate
        prompts: An optional list of prompts used to generate the outputs.
            Prompts are not evaluated and only used as metadata.

    Returns:
        An EvalValue object
    '''
    # The values are binary: 1 for success and 0 for failure
    metric_values = []
    for output in generated_outputs:
        try:
            json_output = json.loads(output)
            if isinstance(json_output, dict):
                metric_values.append(1)
            else:
                metric_values.append(0)
        except:
            metric_values.append(0)

    return EvalValue(metric_name='is_json_object',
                     prompts=prompts,
                     generated_outputs=generated_outputs,
                     reference_outputs=None,
                     metric_values=metric_values,
                     language=None)


def is_json_array(generated_outputs: List[str],
                  prompts: Optional[List[str]] = None) -> EvalValue[int]:
    '''Checks if generated outputs can be parsed as JSON arrays. This metric
    takes on binary 0 or 1 values.

    Args:
        generated_outputs: A list of model generated outputs to evaluate
        prompts: An optional list of prompts used to generate the outputs.
            Prompts are not evaluated and only used as metadata.

    Returns:
        An EvalValue object
    '''
    # The values are binary: 1 for success and 0 for failure
    metric_values = []
    for output in generated_outputs:
        try:
            json_output = json.loads(output)
            if isinstance(json_output, list):
                metric_values.append(1)
            else:
                metric_values.append(0)
        except:
            metric_values.append(0)

    return EvalValue(metric_name='is_json_array',
                     prompts=prompts,
                     generated_outputs=generated_outputs,
                     reference_outputs=None,
                     metric_values=metric_values,
                     language=None)


def matches_regex(generated_outputs: List[str],
                  regex: str,
                  prompts: Optional[List[str]] = None) -> EvalValue[int]:
    '''Checks if generated outputs fully match a given regular expression. This
    metric takes on binary 0 or 1 values.

    Args:
        generated_outputs: A list of model generated outputs to evaluate
        regex: The regular expression to match
        prompts: An optional list of prompts used to generate the outputs.
            Prompts are not evaluated and only used as metadata.

    Returns:
        An EvalValue object
    '''
    # The values are binary: 1 for success and 0 for failure
    metric_values = []
    for output in generated_outputs:
        if re.fullmatch(regex, output) is not None:
            metric_values.append(1)
        else:
            metric_values.append(0)

    return EvalValue(metric_name='matches_regex',
                     prompts=prompts,
                     generated_outputs=generated_outputs,
                     reference_outputs=None,
                     metric_values=metric_values,
                     language=None)


def contains_regex(generated_outputs: List[str],
                   regex: str,
                   prompts: Optional[List[str]] = None) -> EvalValue[int]:
    '''Checks if generated outputs partially contain a given regular expression.
    This metric takes on binary 0 or 1 values.

    Args:
        generated_outputs: A list of model generated outputs to evaluate
        regex: The regular expression to match
        prompts: An optional list of prompts used to generate the outputs.
            Prompts are not evaluated and only used as metadata.

    Returns:
        An EvalValue object
    '''
    # The values are binary: 1 for success and 0 for failure
    metric_values = []
    for output in generated_outputs:
        if re.search(regex, output) is not None:
            metric_values.append(1)
        else:
            metric_values.append(0)

    return EvalValue(metric_name='contains_regex',
                     prompts=prompts,
                     generated_outputs=generated_outputs,
                     reference_outputs=None,
                     metric_values=metric_values,
                     language=None)


def contains_all_strings(
        generated_outputs: List[str],
        strings: List[str],
        case_sensitive: bool = False,
        prompts: Optional[List[str]] = None) -> EvalValue[int]:
    '''Checks if generated outputs contain all strings in of a given list. This
    metric takes on binary 0 or 1 values.

    Args:
        generated_outputs: A list of model generated outputs to evaluate
        strings: A list of strings to match
        case_sensitive: Whether to match case sensitively or not, default False
        prompts: An optional list of prompts used to generate the outputs.
            Prompts are not evaluated and only used as metadata.

    Returns:
        An EvalValue object
    '''
    # Convert everything to lowercase if case insensitive
    if not case_sensitive:
        _strings = [string.lower() for string in strings]
        _generated_outputs = [output.lower() for output in generated_outputs]
    else:
        _strings = strings
        _generated_outputs = generated_outputs

    # The values are binary: 1 for success and 0 for failure
    metric_values = []
    for output in _generated_outputs:
        if all(string in output for string in _strings):
            metric_values.append(1)
        else:
            metric_values.append(0)

    return EvalValue(metric_name='contains_all_strings',
                     prompts=prompts,
                     generated_outputs=generated_outputs,
                     reference_outputs=None,
                     metric_values=metric_values,
                     language=None)


def contains_any_strings(
        generated_outputs: List[str],
        strings: List[str],
        case_sensitive: bool = False,
        prompts: Optional[List[str]] = None) -> EvalValue[int]:
    '''Checks if generated outputs contain any strings in a given list. This
    metric takes on binary 0 or 1 values.

    Args:
        generated_outputs: A list of model generated outputs to evaluate
        strings: A list of strings to match
        case_sensitive: Whether to match case sensitively or not, default False
        prompts: An optional list of prompts used to generate the outputs.
            Prompts are not evaluated and only used as metadata.

    Returns:
        An EvalValue object
    '''
    # Convert everything to lowercase if case insensitive
    if not case_sensitive:
        _strings = [string.lower() for string in strings]
        _generated_outputs = [output.lower() for output in generated_outputs]
    else:
        _strings = strings
        _generated_outputs = generated_outputs

    # The values are binary: 1 for success and 0 for failure
    metric_values = []
    for output in _generated_outputs:
        if any(string in output for string in _strings):
            metric_values.append(1)
        else:
            metric_values.append(0)

    return EvalValue(metric_name='contains_any_strings',
                     prompts=prompts,
                     generated_outputs=generated_outputs,
                     reference_outputs=None,
                     metric_values=metric_values,
                     language=None)


def run_valid_fn(generated_outputs: List[str],
                 valid_fn: Callable[[str], bool],
                 prompts: Optional[List[str]] = None) -> EvalValue[int]:
    '''Checks if generated outputs are valid according to an arbitrary function.
    This metric takes on binary 0 or 1 values.

    Args:
        generated_outputs: A list of model generated outputs to evaluate
        valid_fn: A function that takes a single string and returns a boolean
            determining whether the string is valid or not. The function can
            also raise an exception on failure.
        prompts: An optional list of prompts used to generate the outputs.
            Prompts are not evaluated and only used as metadata.

    Returns:
        An EvalValue object
    '''
    # The values are binary: 1 for success and 0 for failure
    metric_values = []
    for output in generated_outputs:
        try:
            if valid_fn(output):
                metric_values.append(1)
            else:
                metric_values.append(0)
        except:
            metric_values.append(0)

    return EvalValue(metric_name='run_valid_fn',
                     prompts=prompts,
                     generated_outputs=generated_outputs,
                     reference_outputs=None,
                     metric_values=metric_values,
                     language=None)