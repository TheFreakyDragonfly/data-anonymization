import ollama
import re
from ExtensionHelper import ext_print

threshold_yes = 0.2


class LLMInteractor:
    """
    Class that contains interactions with LLMs.
    """

    def __init__(self):
        self.llm = 'llama3'

    def set_llm(self, llm_name):
        self.llm = llm_name

    def ask_about_column_name(self, column_name):
        yes_count = 0
        no_count = 0

        yes_pattern = re.compile(r'\byes\b', re.IGNORECASE)
        no_pattern = re.compile(r'\bno\b', re.IGNORECASE)

        message_content = f'You are tasked with deciding whether a given piece of information can strongly help ' \
                          f'uniquely identifying an individual. If it contributes to ' \
                          f'identification it should be anonymised. Keep your answers to "yes" ' \
                          f'or "no". The piece of information is: "{column_name}"'

        yes_tendency = 0.0
        for n in range(5):
            messages = [{'role': 'user', 'content': message_content}]

            stream = ollama.chat(
                model=self.llm,
                messages=messages,
                stream=True,
            )

            for chunk in stream:
                response = chunk['message']['content']

                yes_matches = yes_pattern.findall(response)
                no_matches = no_pattern.findall(response)

                yes_count += len(yes_matches)
                no_count += len(no_matches)

                yes_tendency = yes_count / (yes_count + no_count)
                ext_print('[tendency] ' + column_name + ';' + str(yes_tendency))

        return yes_tendency >= threshold_yes
