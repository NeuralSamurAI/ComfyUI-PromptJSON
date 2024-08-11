# PromptJSON Node for ComfyUI
![PromptJSON](https://github.com/NeuralSamurAI/ComfyUI-PromptJSON/blob/master/image.jpg?raw=true)
## Description
PromptJSON is a custom node for ComfyUI that structures natural language prompts and generates prompts for external LLM nodes in image generation workflows. It aids in creating consistent, schema-based image descriptions with support for various schema types.

## Features
- Structures natural language prompts according to multiple schema types
- Generates prompts for external LLM nodes with multiple strategies
- Supports negative prompts
- Adjustable complexity for output detail
- Custom schema support for fine-tuning prompt structure
- Multiple prompt generation strategies (One Shot and Few Shot)
- Support for various schema types: JSON, HTML, Key-Value, Attribute-Based, Visual Layer Breakdown, Compositional Grid, and Artistic Reference
- Error handling for robust operation

## Installation
1. Navigate to your ComfyUI custom nodes directory.
2. Clone this repository or copy the `PromptJSON.py`, `prompt_templates.py`, and `__init__.py` files into a new directory named `ComfyUI-PromptJSON`.
3. Restart ComfyUI or refresh your workflow.

## Usage
1. Find the "Prompt JSON" node in the "prompt_converters" category in ComfyUI.
2. Connect the following inputs:
   - `prompt`: Your main prompt text
   - `negative_prompt`: Elements to avoid in the image
   - `complexity`: A float value between 0.1 and 1.0 to adjust output detail
   - `llm_prompt_type`: Choose between "One Shot" or "Few Shot"
   - `schema_type`: Select from JSON, HTML, Key, Attribute-Based, Visual Layer Breakdown, Compositional Grid, or Artistic Reference
   - `custom_schema` (optional): Custom schema string (format depends on chosen schema type)

3. Use the outputs:
   - `system_prompt`: The system instructions for the LLM
   - `user_prompt`: The main prompt for the LLM, including the structured input
   - `negative_passthru`: The negative prompt passed through unchanged
   - `schema`: The formatted schema used for structuring the prompt

## LLM Prompt Types
- **One Shot**: Provides a single example of a structured response based on the input prompt.
- **Few Shot**: Provides multiple examples of structured responses at different complexity levels.

## Schema Types
1. **JSON**: Traditional JSON structure for detailed image descriptions.
2. **HTML**: HTML-like tag structure for organizing image elements.
3. **Key**: Key-value pair structure for straightforward descriptions.
4. **Attribute-Based**: List of attributes focusing on specific aspects of the image.
5. **Visual Layer Breakdown**: Structured description of background, midground, foreground, and focus elements.
6. **Compositional Grid**: 3x3 grid-based description of image elements.
7. **Artistic Reference**: Detailed breakdown of artistic elements like subject, composition, color palette, etc.

## Workflow
1. The PromptJSON node takes the user's input and structures it according to the chosen schema type.
2. It generates a system prompt and user prompt based on the chosen LLM prompt type and schema.
3. The outputs can be sent to an external LLM node for further processing.
4. The external LLM node generates the final, detailed image description based on these prompts.

## Custom Schema
The custom schema feature allows you to define the structure of the output. The format depends on the chosen schema type. For example, for JSON:

```json
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

## Example Output
Input:
- prompt: "A serene lake at sunset with a lone fisherman in a small boat"
- negative_prompt: "urban, city, crowds"
- complexity: 0.7
- llm_prompt_type: "Few Shot"
- schema_type: "JSON"
- custom_schema: (The JSON schema shown above)

Output:
1. System Prompt: (Contains instructions and examples for the LLM)
2. User Prompt: (Contains the structured input prompt and schema)
3. Negative Passthru: "urban, city, crowds"
4. Schema: (The formatted JSON schema)

## Notes
- The system prompt and user prompt are designed to guide an external LLM in generating a detailed, structured image description.
- Experiment with different LLM prompt types and schema types to find the most effective combination for your specific use case.
- Adjust the complexity parameter to control the level of detail in the generated prompts.
- Custom schemas allow for fine-tuned control over the structure of the generated descriptions.

## Support
For issues, feature requests, or contributions, please open an issue or pull request in the GitHub repository.
