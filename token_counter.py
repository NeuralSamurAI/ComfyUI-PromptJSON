from transformers import T5Tokenizer, CLIPTokenizer

class TokenCounter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "model": ("MODEL",),
            },
            "optional": {
                "use_clip": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("t5_token_count", "clip_token_count")
    FUNCTION = "count_tokens"

    CATEGORY = "utils"

    def count_tokens(self, text, model, use_clip=False):
        if not isinstance(text, str):
            raise ValueError("Input text must be a string")

        t5_tokenizer = self.get_t5_tokenizer(model)
        t5_tokens = t5_tokenizer.encode(text)
        t5_count = len(t5_tokens)

        if use_clip:
            clip_tokenizer = self.get_clip_tokenizer(model)
            clip_tokens = clip_tokenizer.encode(text)
            clip_count = len(clip_tokens)
        else:
            clip_count = None

        return t5_count, clip_count

    def get_t5_tokenizer(self, model):
        try:
            return model.model.t5_tokenizer
        except AttributeError:
            return T5Tokenizer.from_pretrained("t5-xxl", local_files_only=True)

    def get_clip_tokenizer(self, model):
        try:
            return model.model.clip_tokenizer
        except AttributeError:
            return CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14", local_files_only=True)
