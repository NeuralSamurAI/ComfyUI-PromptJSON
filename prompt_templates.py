import json

class PromptTemplates:
    @staticmethod
    def get_system_prompt(schema_type):
        return f"You are an AI assistant specialized in generating detailed image descriptions based on user prompts. " \
               f"Your task is to take the user's input and create a structured, detailed description that can be used for image generation. " \
               f"Use the provided {schema_type} schema to organize the information, and adjust the level of detail based on the complexity value given. " \
               f"The user will provide both a positive prompt describing what should be in the image and a negative prompt describing what should NOT be in the image. " \
               f"Ensure that your description does not include any elements mentioned in the negative prompt.  Lastly you will reply ONLY with the answer, no preamble or summary is needed."

    @staticmethod
    def get_default_schema(schema_type):
        if schema_type == "JSON":
            return {
                "title": "[Brief title for the image]",
                "subjects": [{"type": "[Subject type]", "description": "[Detailed description of the subject]"}],
                "objects": [{"type": "[Object type]", "description": "[Detailed description of the object]"}],
                "setting": {"location": "[Where the scene takes place]", "time": "[Time of day or era]"},
                "style": {"artistic_movement": "[Art style or movement]", "mood": "[Overall mood or atmosphere]"},
                "color_scheme": ["[Main colors used in the image]"]
            }
        elif schema_type == "HTML":
            return (
                "<title>[Brief title for the image]</title>\n"
                "<subject>\n"
                "  <type>[Subject type]</type>\n"
                "  <description>[Detailed description of the subject]</description>\n"
                "</subject>\n"
                "<object>\n"
                "  <type>[Object type]</type>\n"
                "  <description>[Detailed description of the object]</description>\n"
                "</object>\n"
                "<setting>\n"
                "  <location>[Where the scene takes place]</location>\n"
                "  <time>[Time of day or era]</time>\n"
                "</setting>\n"
                "<style>\n"
                "  <artistic_movement>[Art style or movement]</artistic_movement>\n"
                "  <mood>[Overall mood or atmosphere]</mood>\n"
                "</style>\n"
                "<color_scheme>\n"
                "  <color>[Main color used in the image]</color>\n"
                "</color_scheme>"
            )
        elif schema_type == "Key":
            return (
                "title: [Brief title for the image]\n"
                "subject.type: [Subject type]\n"
                "subject.description: [Detailed description of the subject]\n"
                "object.type: [Object type]\n"
                "object.description: [Detailed description of the object]\n"
                "setting.location: [Where the scene takes place]\n"
                "setting.time: [Time of day or era]\n"
                "style.artistic_movement: [Art style or movement]\n"
                "style.mood: [Overall mood or atmosphere]\n"
                "color_scheme[0]: [Main color used in the image]"
            )
        elif schema_type == "Attribute-Based":
            return [
                "[Color: description of main colors]",
                "[Lighting: description of lighting conditions]",
                "[Mood: overall atmosphere or feeling]",
                "[Composition: layout and arrangement of elements]",
                "[Style: artistic style or technique]"
            ]
        elif schema_type == "Visual Layer Breakdown":
            return {
                "background": "[Description of the furthest elements]",
                "midground": "[Description of the middle-distance elements]",
                "foreground": "[Description of the closest elements]",
                "focus": "[Main point of interest in the image]"
            }
        elif schema_type == "Compositional Grid":
            return {
                "top_left": "[Description of top-left section]",
                "top_center": "[Description of top-center section]",
                "top_right": "[Description of top-right section]",
                "middle_left": "[Description of middle-left section]",
                "middle_center": "[Description of middle-center section]",
                "middle_right": "[Description of middle-right section]",
                "bottom_left": "[Description of bottom-left section]",
                "bottom_center": "[Description of bottom-center section]",
                "bottom_right": "[Description of bottom-right section]"
            }
        elif schema_type == "Artistic Reference":
            return {
                "subject": "[Main focus or theme of the image]",
                "composition": "[Layout and arrangement of elements]",
                "color_palette": "[Main colors and their relationships]",
                "lighting": "[Type and quality of light in the scene]",
                "texture": "[Surface qualities of objects in the image]",
                "artistic_style": "[Overall artistic approach or technique]",
                "mood": "[Emotional tone or atmosphere of the image]"
            }
        else:
            raise ValueError(f"Unsupported schema type: {schema_type}")

    @staticmethod
    def get_example_prompt(schema_type, complexity):
        if complexity == "low":
            prompt = "A cat"
            negative_prompt = "dogs, human elements"
            complexity_value = 0.1
        elif complexity == "medium":
            prompt = "A bustling city street at night"
            negative_prompt = "daytime, rural elements"
            complexity_value = 0.5
        else:  # high
            prompt = "A fantastical underwater civilization with merpeople and futuristic technology"
            negative_prompt = "land animals, surface world elements"
            complexity_value = 1.0

        if schema_type == "JSON":
            return PromptTemplates._get_json_example(prompt, negative_prompt, complexity_value)
        elif schema_type == "HTML":
            return PromptTemplates._get_html_example(prompt, negative_prompt, complexity_value)
        elif schema_type == "Key":
            return PromptTemplates._get_key_example(prompt, negative_prompt, complexity_value)
        elif schema_type == "Attribute-Based":
            return PromptTemplates._get_attribute_based_example(prompt, negative_prompt, complexity_value)
        elif schema_type == "Visual Layer Breakdown":
            return PromptTemplates._get_visual_layer_breakdown_example(prompt, negative_prompt, complexity_value)
        elif schema_type == "Compositional Grid":
            return PromptTemplates._get_compositional_grid_example(prompt, negative_prompt, complexity_value)
        elif schema_type == "Artistic Reference":
            return PromptTemplates._get_artistic_reference_example(prompt, negative_prompt, complexity_value)
        else:
            raise ValueError(f"Unsupported schema type: {schema_type}")

    @staticmethod
    def _get_json_example(prompt, negative_prompt, complexity):
        if complexity == 0.1:
            output = (
                "{\n"
                '  "title": "Simple Cat Portrait",\n'
                '  "subjects": [{"type": "animal", "description": "cat: furry: domesticated: sitting"}],\n'
                '  "setting": {"location": "indoors: unspecified", "time": "unspecified"},\n'
                '  "style": {"artistic_movement": "Realism", "mood": "calm: neutral"},\n'
                '  "color_scheme": ["gray: soft", "white: clean"]\n'
                "}"
            )
        elif complexity == 0.5:
            output = (
                "{\n"
                '  "title": "Nocturnal Urban Scene",\n'
                '  "subjects": [{"type": "urban", "description": "city street: busy: crowded"}],\n'
                '  "objects": [\n'
                '    {"type": "vehicle", "description": "cars: moving: headlights on"},\n'
                '    {"type": "building", "description": "skyscrapers: tall: illuminated"}\n'
                '  ],\n'
                '  "setting": {"location": "city center: downtown", "time": "night: late"},\n'
                '  "style": {"artistic_movement": "Urban Realism", "mood": "energetic: lively"},\n'
                '  "color_scheme": ["black: deep", "yellow: bright: neon", "blue: cool: distant"]\n'
                "}"
            )
        else:
            output = (
                "{\n"
                '  "title": "Futuristic Aquatic Metropolis",\n'
                '  "subjects": [\n'
                '    {"type": "mythical", "description": "merpeople: diverse: swimming"},\n'
                '    {"type": "technology", "description": "underwater gadgets: advanced: floating"}\n'
                '  ],\n'
                '  "objects": [\n'
                '    {"type": "architecture", "description": "buildings: coral-shaped: bioluminescent"},\n'
                '    {"type": "flora", "description": "seaweed: genetically modified: glowing"},\n'
                '    {"type": "fauna", "description": "fish: robotic: schooling"}\n'
                '  ],\n'
                '  "setting": {"location": "deep ocean: underwater city", "time": "timeless: eternal"},\n'
                '  "style": {"artistic_movement": "Bio-futurism", "mood": "awe-inspiring: mysterious"},\n'
                '  "color_scheme": ["blue: bioluminescent", "green: neon", "purple: deep", "silver: metallic"]\n'
                "}"
            )
        return f"Prompt: {prompt}\nNegative prompt: {negative_prompt}\nComplexity: {complexity}\n\nOutput:\n{output}"

    @staticmethod
    def _get_html_example(prompt, negative_prompt, complexity):
        if complexity == 0.1:
            output = (
                "<title>Simple Cat Portrait</title>\n"
                "<subject>\n"
                "  <type>animal</type>\n"
                "  <description>cat: furry: domesticated: sitting</description>\n"
                "</subject>\n"
                "<setting>\n"
                "  <location>indoors: unspecified</location>\n"
                "  <time>unspecified</time>\n"
                "</setting>\n"
                "<style>\n"
                "  <artistic_movement>Realism</artistic_movement>\n"
                "  <mood>calm: neutral</mood>\n"
                "</style>\n"
                "<color_scheme>\n"
                "  <color>gray: soft</color>\n"
                "  <color>white: clean</color>\n"
                "</color_scheme>"
            )
        elif complexity == 0.5:
            output = (
                "<title>Nocturnal Urban Scene</title>\n"
                "<subject>\n"
                "  <type>urban</type>\n"
                "  <description>city street: busy: crowded</description>\n"
                "</subject>\n"
                "<object>\n"
                "  <type>vehicle</type>\n"
                "  <description>cars: moving: headlights on</description>\n"
                "</object>\n"
                "<object>\n"
                "  <type>building</type>\n"
                "  <description>skyscrapers: tall: illuminated</description>\n"
                "</object>\n"
                "<setting>\n"
                "  <location>city center: downtown</location>\n"
                "  <time>night: late</time>\n"
                "</setting>\n"
                "<style>\n"
                "  <artistic_movement>Urban Realism</artistic_movement>\n"
                "  <mood>energetic: lively</mood>\n"
                "</style>\n"
                "<color_scheme>\n"
                "  <color>black: deep</color>\n"
                "  <color>yellow: bright: neon</color>\n"
                "  <color>blue: cool: distant</color>\n"
                "</color_scheme>"
            )
        else:
            output = (
                "<title>Futuristic Aquatic Metropolis</title>\n"
                "<subject>\n"
                "  <type>mythical</type>\n"
                "  <description>merpeople: diverse: swimming</description>\n"
                "</subject>\n"
                "<subject>\n"
                "  <type>technology</type>\n"
                "  <description>underwater gadgets: advanced: floating</description>\n"
                "</subject>\n"
                "<object>\n"
                "  <type>architecture</type>\n"
                "  <description>buildings: coral-shaped: bioluminescent</description>\n"
                "</object>\n"
                "<object>\n"
                "  <type>flora</type>\n"
                "  <description>seaweed: genetically modified: glowing</description>\n"
                "</object>\n"
                "<object>\n"
                "  <type>fauna</type>\n"
                "  <description>fish: robotic: schooling</description>\n"
                "</object>\n"
                "<setting>\n"
                "  <location>deep ocean: underwater city</location>\n"
                "  <time>timeless: eternal</time>\n"
                "</setting>\n"
                "<style>\n"
                "  <artistic_movement>Bio-futurism</artistic_movement>\n"
                "  <mood>awe-inspiring: mysterious</mood>\n"
                "</style>\n"
                "<color_scheme>\n"
                "  <color>blue: bioluminescent</color>\n"
                "  <color>green: neon</color>\n"
                "  <color>purple: deep</color>\n"
                "  <color>silver: metallic</color>\n"
                "</color_scheme>"
            )
        return f"Prompt: {prompt}\nNegative prompt: {negative_prompt}\nComplexity: {complexity}\n\nOutput:\n{output}"

    @staticmethod
    def _get_key_example(prompt, negative_prompt, complexity):
        if complexity == 0.1:
            output = (
                "title: Simple Cat Portrait\n"
                "subject.type: animal\n"
                "subject.description: cat: furry: domesticated: sitting\n"
                "setting.location: indoors: unspecified\n"
                "setting.time: unspecified\n"
                "style.artistic_movement: Realism\n"
                "style.mood: calm: neutral\n"
                "color_scheme[0]: gray: soft\n"
                "color_scheme[1]: white: clean"
            )
        elif complexity == 0.5:
            output = (
                "title: Nocturnal Urban Scene\n"
                "subject.type: urban\n"
                "subject.description: city street: busy: crowded\n"
                "object[0].type: vehicle\n"
                "object[0].description: cars: moving: headlights on\n"
                "object[1].type: building\n"
                "object[1].description: skyscrapers: tall: illuminated\n"
                "setting.location: city center: downtown\n"
                "setting.time: night: late\n"
                "style.artistic_movement: Urban Realism\n"
                "style.mood: energetic: lively\n"
                "color_scheme[0]: black: deep\n"
                "color_scheme[1]: yellow: bright: neon\n"
                "color_scheme[2]: blue: cool: distant"
            )
        else:
            output = (
                "title: Futuristic Aquatic Metropolis\n"
                "subject[0].type: mythical\n"
                "subject[0].description: merpeople: diverse: swimming\n"
                "subject[1].type: technology\n"
                "subject[1].description: underwater gadgets: advanced: floating\n"
                "object[0].type: architecture\n"
                "object[0].description: buildings: coral-shaped: bioluminescent\n"
                "object[1].type: flora\n"
                "object[1].description: seaweed: genetically modified: glowing\n"
                "object[2].type: fauna\n"
                "object[2].description: fish: robotic: schooling\n"
                "setting.location: deep ocean: underwater city\n"
                "setting.time: timeless: eternal\n"
                "style.artistic_movement: Bio-futurism\n"
                "style.mood: awe-inspiring: mysterious\n"
                "color_scheme[0]: blue: bioluminescent\n"
                "color_scheme[1]: green: neon\n"
                "color_scheme[2]: purple: deep\n"
                "color_scheme[3]: silver: metallic"
            )
        return f"Prompt: {prompt}\nNegative prompt: {negative_prompt}\nComplexity: {complexity}\n\nOutput:\n{output}"

    @staticmethod
    def _get_attribute_based_example(prompt, negative_prompt, complexity):
        if complexity == 0.1:
            output = (
                "[Color: gray: soft: white: clean]\n"
                "[Lighting: neutral: even: soft]\n"
                "[Mood: calm: serene: peaceful]\n"
                "[Composition: centered: simple: portrait]\n"
                "[Style: realistic: straightforward: minimalistic]"
            )
        elif complexity == 0.5:
            output = (
                "[Color: black: deep: yellow: bright: neon: blue: cool: distant]\n"
                "[Lighting: high contrast: artificial: street lamps: neon signs: car headlights]\n"
                "[Mood: energetic: vibrant: bustling: slightly mysterious]\n"
                "[Composition: dynamic: diagonal: multiple layers: foreground to background]\n"
                "[Style: urban realism: noir-inspired: contemporary]"
            )
        else:
            output = (
                "[Color: blue: bioluminescent: green: neon: purple: deep: silver: metallic]\n"
                "[Lighting: ethereal: glowing: bioluminescent: multiple sources: complex shadows]\n"
                "[Mood: awe-inspiring: mysterious: futuristic: dreamlike]\n"
                "[Composition: multi-layered: intricate: vast scale: foreground to background depth]\n"
                "[Style: bio-futurism: surrealistic: blend of organic and technological]\n"
                "[Texture: smooth: metallic: organic: coral-like: flowing]\n"
                "[Motion: fluid: graceful: swirling currents: schools of fish]\n"
                "[Scale: monumental: sprawling: dwarfing inhabitants]"
            )
        return f"Prompt: {prompt}\nNegative prompt: {negative_prompt}\nComplexity: {complexity}\n\nOutput:\n{output}"

    @staticmethod
    def _get_visual_layer_breakdown_example(prompt, negative_prompt, complexity):
        if complexity == 0.1:
            output = (
                "background: plain: neutral tone: slightly out of focus\n"
                "midground: none specified: focus entirely on subject\n"
                "foreground: single cat: sitting: centered: detailed fur texture\n"
                "focus: cat's face: eyes: whiskers: defining features clearly visible"
            )
        elif complexity == 0.5:
            output = (
                "background: night sky: dark: few visible stars: silhouettes of distant skyscrapers\n"
                "midground: illuminated building facades: neon signs: streetlights: pools of light\n"
                "foreground: busy street: moving cars: headlights creating light streaks: pedestrians\n"
                "focus: intersection: traffic flow: interplay of light and shadow"
            )
        else:
            output = (
                "background: vast ocean depths: dark water: bioluminescent particles: starry effect\n"
                "midground: coral-shaped skyscrapers: blue-green glow: interconnected transparent tubes\n"
                "foreground: diverse merpeople: advanced gadgets: schools of robotic fish\n"
                "focus: central plaza: gathering merpeople: swirling information displays: holographic projections"
            )
        return f"Prompt: {prompt}\nNegative prompt: {negative_prompt}\nComplexity: {complexity}\n\nOutput:\n{output}"

    @staticmethod
    def _get_compositional_grid_example(prompt, negative_prompt, complexity):
        if complexity == 0.1:
            output = (
                "top_left: empty: neutral background\n"
                "top_center: cat's ears: top of head\n"
                "top_right: empty: neutral background\n"
                "middle_left: cat's body: side view\n"
                "middle_center: cat's face: main focus: detailed features\n"
                "middle_right: cat's body: opposite side view\n"
                "bottom_left: empty: neutral background\n"
                "bottom_center: cat's lower body: paws\n"
                "bottom_right: empty: neutral background"
            )
        elif complexity == 0.5:
            output = (
                "top_left: skyscraper: lit windows: partial view\n"
                "top_center: night sky: few stars: maybe moon\n"
                "top_right: another skyscraper: neon sign\n"
                "middle_left: street side: walking pedestrians\n"
                "middle_center: main intersection: traffic lights: car headlights\n"
                "middle_right: storefront: bright display windows\n"
                "bottom_left: parked car: partial view: reflective surface\n"
                "bottom_center: wet street: reflections of lights\n"
                "bottom_right: street corner: newspaper stand: fire hydrant"
            )
        else:
            output = (
                "top_left: bioluminescent coral skyscraper: reaching upwards\n"
                "top_center: school of silver robotic fish: perfect formation\n"
                "top_right: floating holographic displays: underwater charts: data\n"
                "middle_left: merpeople: operating advanced underwater vehicles\n"
                "middle_center: central plaza: giant pulsating energy core\n"
                "middle_right: seaweed farm: neon green glow: genetically modified\n"
                "bottom_left: network of transparent tubes: transportation system\n"
                "bottom_center: diverse merpeople: engaged in discussion: trade\n"
                "bottom_right: underwater laboratory: visible experiments: large windows"
            )
        return f"Prompt: {prompt}\nNegative prompt: {negative_prompt}\nComplexity: {complexity}\n\nOutput:\n{output}"

    @staticmethod
    def _get_artistic_reference_example(prompt, negative_prompt, complexity):
        if complexity == 0.1:
            output = (
                "subject: single cat: domestic: sitting pose\n"
                "composition: centered: simple portrait view: minimal background\n"
                "color_palette: grayscale: soft grays: clean whites: subtle tonal variations\n"
                "lighting: even: soft: highlights on fur: gentle shadows\n"
                "texture: soft fur: visible but not overly detailed\n"
                "artistic_style: basic realism: minimal embellishment: focus on form\n"
                "mood: calm: serene: domestic tranquility"
            )
        elif complexity == 0.5:
            output = (
                "subject: nocturnal urban street scene: busy city life\n"
                "composition: dynamic diagonal layout: streets and buildings create depth\n"
                "color_palette: rich blacks: bright yellows: cool blues: pops of neon\n"
                "lighting: high contrast: dark shadows: bright artificial lights: multiple sources\n"
                "texture: smooth reflective surfaces: cars and wet streets: rough building facades\n"
                "artistic_style: urban realism: elements of noir: capturing night city energy\n"
                "mood: energetic: slightly mysterious: sense of constant motion: urban vitality"
            )
        else:
            output = (
                "subject: futuristic underwater metropolis: merpeople civilization\n"
                "composition: multi-layered: overlapping structures: foreground to background depth\n"
                "color_palette: bioluminescent blues: neon greens: deep purples: metallic silvers\n"
                "lighting: multiple bioluminescent sources: complex interplay of shadows and glowing elements\n"
                "texture: contrasting smooth metallic surfaces: organic flowing forms: coral-like structures\n"
                "artistic_style: bio-futurism: blend of art nouveau organic forms: sci-fi technology: surrealist dreamlike quality\n"
                "mood: awe-inspiring: mysterious: sense of wonder and endless possibility\n"
                "motion: implied through swirling water currents: graceful merpeople movements: schools of robotic fish\n"
                "scale: vast and intricate: monumental structures dwarfing inhabitants: sense of grandeur and exploration"
            )
        return f"Prompt: {prompt}\nNegative prompt: {negative_prompt}\nComplexity: {complexity}\n\nOutput:\n{output}"