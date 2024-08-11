import json
import logging
from .prompt_templates import PromptTemplates

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class PromptJSON:
    def __init__(self):
        logging.info("Initializing PromptJSON")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "negative_prompt": ("STRING", {"multiline": True}),
                "complexity": ("FLOAT", {"default": 0.5, "min": 0.1, "max": 1.0, "step": 0.1}),
                "llm_prompt_type": (["One Shot", "Few Shot"],),
                "schema_type": (["JSON", "HTML", "Key", "Attribute-Based", "Visual Layer Breakdown", "Compositional Grid", "Artistic Reference"],),
                "enhance_prompt": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "custom_schema": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("system_prompt", "user_prompt", "negative_passthru", "schema")
    FUNCTION = "process"
    CATEGORY = "prompt_converters"

    def process(self, prompt, negative_prompt, complexity, llm_prompt_type, schema_type, enhance_prompt, custom_schema=""):
        logging.info(f"Starting process method with schema_type: {schema_type}, enhance_prompt: {enhance_prompt}")
        
        system_prompt = self.generate_system_prompt(llm_prompt_type, schema_type, enhance_prompt)
        schema = self.parse_custom_schema(custom_schema, schema_type)
        user_prompt = self.generate_user_prompt(prompt, negative_prompt, schema, complexity, schema_type, enhance_prompt)
        
        return (system_prompt, user_prompt, negative_prompt, self.format_schema_for_llm(schema, schema_type))

    def generate_system_prompt(self, llm_prompt_type, schema_type, enhance_prompt):
        base_prompt = PromptTemplates.get_system_prompt(schema_type)
        
        if enhance_prompt:
            base_prompt += "\nYou are encouraged to create additional details not explicitly mentioned in the original prompt, while maintaining consistency with the given information. Use the complexity value to determine the level of detail and elaboration in your response."
        else:
            base_prompt += "\nStrictly use only the information provided in the original prompt. Do not add any details or elements not explicitly mentioned."

        if llm_prompt_type == "One Shot":
            example = PromptTemplates.get_example_prompt(schema_type, "medium")
            return f"{base_prompt}\n\nHere's an example of how to structure your response:\n\n{example}"
        else:  # Few Shot
            examples = [
                PromptTemplates.get_example_prompt(schema_type, "low"),
                PromptTemplates.get_example_prompt(schema_type, "medium"),
                PromptTemplates.get_example_prompt(schema_type, "high")
            ]
        return f"{base_prompt}\n\nHere are a few examples of how to structure your response for different complexity levels:\n\n" + "\n\n".join(examples)

    def parse_custom_schema(self, custom_schema, schema_type):
        if not custom_schema:
            return PromptTemplates.get_default_schema(schema_type)
        try:
            if schema_type in ["JSON", "Visual Layer Breakdown", "Compositional Grid", "Artistic Reference"]:
                schema = json.loads(custom_schema)
                if not isinstance(schema, dict):
                    raise ValueError(f"Custom {schema_type} schema must be a JSON object")
            elif schema_type == "HTML":
                schema = self.parse_html_schema(custom_schema)
            elif schema_type == "Key":
                schema = self.parse_key_schema(custom_schema)
            elif schema_type == "Attribute-Based":
                schema = custom_schema.strip().split('\n')
            else:
                raise ValueError(f"Unsupported schema type: {schema_type}")
            return schema
        except Exception as e:
            logging.error(f"Invalid custom schema: {str(e)}")
            return PromptTemplates.get_default_schema(schema_type)

    def parse_html_schema(self, custom_schema):
        if isinstance(custom_schema, str):
            return custom_schema.strip()
        return PromptTemplates.get_default_schema("HTML")

    def parse_key_schema(self, custom_schema):
        if isinstance(custom_schema, str):
            return custom_schema.strip()
        return PromptTemplates.get_default_schema("Key")

    def generate_user_prompt(self, prompt, negative_prompt, schema, complexity, schema_type, enhance_prompt):
        formatted_schema = self.format_schema_for_llm(schema, schema_type)
    
        enhancement_instruction = ""
        if enhance_prompt:
            enhancement_instruction = f"""
Enhance the prompt with additional details not explicitly mentioned, while maintaining consistency with the given information. 
Use the complexity value of {complexity} to determine the level of detail and elaboration in your response. 
Higher complexity should result in more detailed and nuanced descriptions.
"""
        else:
            enhancement_instruction = "Strictly use only the information provided in the original prompt. Do not add any details or elements not explicitly mentioned."

        return f"""Generate a detailed image description based on the following prompt: "{prompt}"

Negative prompt (elements to avoid): "{negative_prompt}"

{enhancement_instruction}

Use the following {schema_type} schema to structure your response. Replace the placeholders with appropriate, detailed content:
{formatted_schema}

Ensure that your response adheres strictly to this schema, providing detailed and creative content for each field. Make sure to avoid including any elements mentioned in the negative prompt.

Your response should be a valid {schema_type} structure that follows the provided schema."""

    def format_schema_for_llm(self, schema, schema_type):
        if schema_type == "JSON":
            return json.dumps(schema, indent=2)
        elif schema_type == "HTML":
            return self.format_html_schema_for_llm(schema)
        elif schema_type == "Key":
            return self.format_key_schema_for_llm(schema)
        elif schema_type == "Attribute-Based":
            return "\n".join(schema)
        elif schema_type in ["Visual Layer Breakdown", "Compositional Grid", "Artistic Reference"]:
            return json.dumps(schema, indent=2)
        else:
            raise ValueError(f"Unsupported schema type: {schema_type}")

    def format_html_schema_for_llm(self, schema):
        if isinstance(schema, str):
            return schema
        # If it's not a string, assume it's a dictionary and format it
        return self._format_html_dict(schema)

    def _format_html_dict(self, schema, indent=""):
        result = []
        for key, value in schema.items():
            if isinstance(value, dict):
                result.append(f"{indent}<{key}>")
                result.append(self._format_html_dict(value, indent + "  "))
                result.append(f"{indent}</{key}>")
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        result.append(f"{indent}<{key}>")
                        result.append(self._format_html_dict(item, indent + "  "))
                        result.append(f"{indent}</{key}>")
                    else:
                        result.append(f"{indent}<{key}>[appropriate {key}]</{key}>")
            else:
                result.append(f"{indent}<{key}>[appropriate {key}]</{key}>")
        return "\n".join(result)

    def format_key_schema_for_llm(self, schema):
        if isinstance(schema, str):
            return schema
        # If it's not a string, assume it's a dictionary and format it
        return self._format_key_dict(schema)

    def _format_key_dict(self, schema, prefix=""):
        result = []
        for key, value in schema.items():
            if isinstance(value, dict):
                result.append(self._format_key_dict(value, f"{prefix}{key}."))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        result.append(self._format_key_dict(item, f"{prefix}{key}[{i}]."))
                    else:
                        result.append(f"{prefix}{key}[{i}]: [appropriate {key}]")
            else:
                result.append(f"{prefix}{key}: [appropriate {key}]")
        return "\n".join(result)

    def format_visual_layer_breakdown_for_llm(self, schema):
        result = []
        for layer, description in schema.items():
            result.append(f"{layer.capitalize()}:")
            result.append(f"  [Describe the {layer} elements. {description}]")
        return "\n".join(result)

    def format_compositional_grid_for_llm(self, schema):
        result = [
            "Compositional Grid:",
            "┌─────────────┬─────────────┬─────────────┐",
            "│  Top Left   │ Top Center  │  Top Right  │",
            "│ [Describe]  │ [Describe]  │ [Describe]  │",
            "├─────────────┼─────────────┼─────────────┤",
            "│ Middle Left │   Center    │ Middle Right│",
            "│ [Describe]  │ [Describe]  │ [Describe]  │",
            "├─────────────┼─────────────┼─────────────┤",
            "│ Bottom Left │Bottom Center│ Bottom Right│",
            "│ [Describe]  │ [Describe]  │ [Describe]  │",
            "└─────────────┴─────────────┴─────────────┘"
        ]
        for position, description in schema.items():
            formatted_position = position.replace('_', ' ').title()
            result.append(f"\n{formatted_position}:")
            result.append(f"  [Describe this section. {description}]")
        return "\n".join(result)

    def format_artistic_reference_for_llm(self, schema):
        result = ["Artistic Reference:"]
        for aspect, description in schema.items():
            result.append(f"\n{aspect.capitalize()}:")
            result.append(f"  [Describe the {aspect}. {description}]")
        return "\n".join(result)