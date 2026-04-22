"""
Prompt Renderer - Renders prompt templates with context using Jinja2.

This module is PRE-BUILT. You do not need to modify it.

Takes a prompt template (with Jinja2 variables like {{ consultant }}) and
a context dictionary, and produces the final system and user prompts
ready to send to the LLM.
"""

from jinja2 import Template


class PromptRenderer:
    """Renders Jinja2 prompt templates with provided context."""

    def render(self, template: dict, context: dict) -> tuple:
        """
        Render a prompt template with the given context.

        Args:
            template: Dict with 'system' and 'user' keys containing
                      Jinja2 template strings
            context: Dict of variables to fill into the templates

        Returns:
            Tuple of (system_prompt, user_prompt) as rendered strings
        """
        system_template = Template(template["system"])
        user_template = Template(template["user"])

        system_prompt = system_template.render(**context)
        user_prompt = user_template.render(**context)

        return system_prompt, user_prompt
