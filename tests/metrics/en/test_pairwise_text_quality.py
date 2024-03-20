import os
from unittest.mock import Mock, patch

import pytest
from openai.types.chat import ChatCompletion

from langcheck.metrics.en.pairwise_text_quality import pairwise_comparison

################################################################################
# Tests
################################################################################


@pytest.mark.parametrize(
    'generated_outputs_a,generated_outputs_b,prompts,sources_a,sources_b,reference_outputs',  # NOQA: E501
    [("Tokyo is Japan's capital city.", "New York is Japan's capital city.",
      'What is the capital of Japan?', None, None, None),
     ("Tokyo is Japan's capital city.", "New York is Japan's capital city.",
      'What is the capital of Japan?', None, None, 'Tokyo'),
     ("Tokyo is Japan's capital city.", "New York is Japan's capital city.",
      'What is the capital of Japan?', 'Capital of Japan = Tokyo', None, None),
     ("Tokyo is Japan's capital city.", "New York is Japan's capital city.",
      'What is the capital of Japan?', 'Capital of Japan = Tokyo',
      'Capital of Japan = Tokyo', None),
     ("Tokyo is Japan's capital city.", "New York is Japan's capital city.",
      'What is the capital of Japan?', 'Capital of Japan = Tokyo',
      'Capital of Japan = Tokyo', 'Tokyo')])
def test_pairwise_comparison_openai(generated_outputs_a, generated_outputs_b,
                                    prompts, sources_a, sources_b,
                                    reference_outputs):
    '''Test the pairwise_comparison function.

    Test 1: No sources or reference outputs are provided.
    Test 2: Reference output is provided.
    Test 3: Source A is provided.
    Test 4: Both Source A and Source B are provided.
    Test 5: Source A, Source B, and the reference output are provided.
    '''
    mock_chat_completion = Mock(spec=ChatCompletion)
    mock_chat_completion.choices = [
        Mock(message=Mock(function_call=Mock(
            arguments="{\n  \"pairwise_comparison\": \"Response A\"\n}")))
    ]

    # Calling the openai.resources.chat.Completions.create method requires an
    # OpenAI API key, so we mock the return value instead
    with patch('openai.resources.chat.Completions.create',
               return_value=mock_chat_completion):
        # Set the necessary env vars for the 'openai' model type
        os.environ["OPENAI_API_KEY"] = "dummy_key"
        metric_value = pairwise_comparison(generated_outputs_a,
                                           generated_outputs_b,
                                           prompts,
                                           sources_a=sources_a,
                                           sources_b=sources_b,
                                           reference_outputs=reference_outputs,
                                           model_type='openai')
        # "Response A" gets a value of 0
        assert metric_value == 0

        # Set the necessary env vars for the 'azure_openai' model type
        os.environ["AZURE_OPENAI_KEY"] = "dummy_azure_key"
        os.environ["OPENAI_API_VERSION"] = "dummy_version"
        os.environ["AZURE_OPENAI_ENDPOINT"] = "dummy_endpoint"
        metric_value = pairwise_comparison(generated_outputs_a,
                                           generated_outputs_b,
                                           prompts,
                                           sources_a=sources_a,
                                           sources_b=sources_b,
                                           reference_outputs=reference_outputs,
                                           model_type='azure_openai',
                                           openai_args={'model': 'foo bar'})
        # "Response A" gets a value of 0
        assert metric_value == 0
