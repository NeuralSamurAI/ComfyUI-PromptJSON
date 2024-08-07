# PromptJSON Node for ComfyUI

## Description
PromptJSON is a custom node for ComfyUI that structures natural language prompts and generates prompts for external LLM nodes in image generation workflows. It aids in creating consistent, schema-based image descriptions.

## Features
- Structures natural language prompts according to a custom schema
- Generates prompts for external LLM nodes with multiple strategies
- Supports negative prompts
- Adjustable complexity for output detail
- Custom color scheme input
- Custom schema support for fine-tuning prompt structure
- Multiple prompt generation strategies
- Token counting for T5 and CLIP models
- Batch processing support
- Debug mode for detailed information
- Error handling for robust operation

## Installation
1. Navigate to your ComfyUI custom nodes directory.
2. Clone this repository or copy the `prompt_json.py`, `token_counter.py`, and `__init__.py` files into a new directory named `PromptJSON`.
3. Install required dependencies:
   ```
   pip install nltk
   ```
4. Restart ComfyUI or refresh your workflow.

## Usage
1. Find the "Prompt JSON" node in the "prompt_converters" category in ComfyUI.
2. Connect the following inputs:
   - `prompt`: Your main prompt text
   - `negative_prompt`: Elements to avoid in the image
   - `complexity`: A float value between 0.1 and 1.0 to adjust output detail
   - `max_tokens`: Maximum number of tokens for the output JSON
   - `model`: The model to use for tokenization
   - `llm_prompt_type`: Choose between "One Shot Learning", "System Prompt", or "Combined"
   - `color_scheme` (optional): Comma-separated list of colors
   - `seed` (optional): Seed for random number generation (-1 for random seed)
   - `custom_schema` (optional): JSON string for custom schema
   - `debug_mode` (optional): Boolean to enable debug information in output
   - `batch_size` (optional): Number of outputs to generate in a batch

3. Use the outputs:
   - `llm_prompt`: The prompt to be sent to the external LLM node
   - `structured_prompt`: A JSON representation of the input prompt, structured according to the schema
   - `custom_schema`: The schema used to structure the prompt and guide the LLM

## LLM Prompt Types
- **One Shot Learning**: Provides an example of a structured response based on the input prompt.
- **System Prompt**: Gives instructions to the LLM on how to generate structured descriptions.
- **Combined**: Merges the System Prompt and One Shot Learning example for potentially increased accuracy.

## Workflow
1. The PromptJSON node takes the user's input and structures it according to the custom schema.
2. It generates an LLM prompt based on the chosen prompt type, incorporating the structured prompt and schema.
3. The `llm_prompt` output is sent to an external LLM node.
4. The external LLM node generates the final, detailed JSON description based on this prompt.

## Custom Schema
The custom schema feature allows you to define the structure of the output JSON and influence the generated LLM prompt.

### Example: Custom Schema for Image Generation
```
{
  "scene": {
    "time_of_day": "string",
    "weather": "string",
    "location": "string"
  },
  "subjects": [
    {
      "type": "string",
      "description": "string",
      "position": "string"
    }
  ],
  "style": {
    "artistic_movement": "string",
    "color_palette": ["string"],
    "mood": "string"
  },
  "camera": {
    "angle": "string",
    "shot_type": "string"
  }
}
```

This schema will guide the structuring of the input prompt and the generation of the LLM prompt.

## Example Output
Input:
- prompt: "A serene lake at sunset with a lone fisherman in a small boat"
- negative_prompt: "urban, city, crowds"
- complexity: 0.7
- max_tokens: 2048
- color_scheme: "orange, purple, blue"
- custom_schema: (The schema shown above)
- llm_prompt_type: "Combined"

Output:
1. LLM Prompt:
```
You are an AI assistant specialized in generating detailed image descriptions based on the following schema: 
{
  "scene": {
    "time_of_day": "string",
    "weather": "string",
    "location": "string"
  },
  "subjects": [
    {
      "type": "string",
      "description": "string",
      "position": "string"
    }
  ],
  "style": {
    "artistic_movement": "string",
    "color_palette": ["string"],
    "mood": "string"
  },
  "camera": {
    "angle": "string",
    "shot_type": "string"
  }
}

Here's an example of how to structure your response:

{
  "scene": {
    "time_of_day": "sunset",
    "weather": "clear",
    "location": "serene lake"
  },
  "subjects": [
    {
      "type": "character",
      "description": "lone fisherman",
      "position": "in a small boat"
    },
    {
      "type": "object",
      "description": "small boat",
      "position": "on the lake"
    }
  ],
  "style": {
    "artistic_movement": "Impressionism",
    "color_palette": ["orange", "purple", "blue"],
    "mood": "tranquil"
  },
  "camera": {
    "angle": "wide shot",
    "shot_type": "landscape"
  }
}

Please generate a similar structured description for the given prompt, but with more detail and creativity.

Generate a detailed image description based on the following prompt, adhering to the provided schema: 
{
  "scene": {
    "time_of_day": "sunset",
    "weather": "clear",
    "location": "serene lake"
  },
  "subjects": [
    {
      "type": "character",
      "description": "lone fisherman",
      "position": "in a small boat"
    },
    {
      "type": "object",
      "description": "small boat",
      "position": "on the lake"
    }
  ],
  "style": {
    "artistic_movement": "Impressionism",
    "color_palette": ["orange", "purple", "blue"],
    "mood": "tranquil"
  },
  "camera": {
    "angle": "wide shot",
    "shot_type": "landscape"
  }
}
```

2. Structured Prompt: (The JSON representation of the input prompt, as shown in the LLM Prompt)

3. Custom Schema: (The schema used, as shown at the beginning of the LLM Prompt)

## Notes
- The `structured_prompt` output is an intermediate representation, not the final detailed JSON.
- The `llm_prompt` is designed to guide an external LLM in generating the final, detailed structured image description.
- Experiment with different LLM prompt types to find the most effective one for your specific LLM and use case.
- The custom schema defines the structure for both the intermediate prompt and the final LLM output.
- Adjust the complexity parameter to control the level of detail in the generated prompts.

## Token Counter Usage
The Token Counter node is available in the "utils" category:

1. Connect the following inputs:
   - `text`: The text to count tokens for
   - `model`: The model to use for tokenization
   - `use_clip` (optional): Boolean to enable CLIP token counting

2. Use the outputs:
   - `t5_token_count`: Number of tokens using T5 tokenizer
   - `clip_token_count`: Number of tokens using CLIP tokenizer (if enabled)

## Support
For issues, feature requests, or contributions, please open an issue or pull request in the GitHub repository.