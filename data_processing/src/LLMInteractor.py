import ollama
import re
from ExtensionHelper import ext_print
import anonymizer

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
        ext_print('[LLMProgress] Asking LLM about Column "' + column_name + '"')
        yes_count = 0
        no_count = 0

        yes_pattern = re.compile(r'\byes\b', re.IGNORECASE)
        no_pattern = re.compile(r'\bno\b', re.IGNORECASE)

        message_content = f'You are tasked with deciding whether a given piece of information can strongly help ' \
                          f'uniquely identifying an individual. If it contributes to ' \
                          f'identification it should be anonymised. Keep your answers to "yes" ' \
                          f'or "no". The piece of information is: "{column_name}"'

        yes_tendency = 0.0
        range_lim = 3
        for n in range(range_lim):
            messages = [{'role': 'user', 'content': message_content}]

            stream = ollama.chat(
                model=self.llm,
                messages=messages,
                stream=True,
            )
            anonymizer.llm_calls += 1

            for chunk in stream:
                response = chunk['message']['content']

                yes_matches = yes_pattern.findall(response)
                no_matches = no_pattern.findall(response)

                yes_count += len(yes_matches)
                no_count += len(no_matches)

                yes_tendency = yes_count / (yes_count + no_count)
                ext_print(
                    '[LLMProgress] Asking LLM about Column "' + column_name + '"'
                    + ' (' + str(n+1) + ' / ' + str(range_lim) + ')'
                )

        answer = yes_tendency >= threshold_yes

        ext_print('[LLMProgress] LLM Answer: ' + str(answer))

        ext_print('[LLMProgress] ...')
        return answer

    def llm_choose_option(self, column_name, column_data, functions):
        ext_print('[LLMProgress] LLM is choosing for "' + column_name + '"')
        prompt = (
            f"You are given a column called '{column_name}' and the following data examples:\n"
            f"{', '.join(column_data[:5])}\n"
            f"Choose the most appropriate function from the following list to process this data:\n"
            f"{', '.join([func.__name__ for func in functions])}\n"
            f"Provide only the function name as the answer."
        )

        print("Prompt sent to LLM:")
        print(prompt)

        messages = [{'role': 'user', 'content': prompt}]

        stream = ollama.chat(
            model=self.llm,
            messages=messages,
            stream=True)
        anonymizer.llm_calls += 1

        chosen_function_name = ""
        for chunk in stream:
            chosen_function_name += chunk['message']['content']

        chosen_function_name = chosen_function_name.strip()
        print("LLM response (chosen function name):")
        print(chosen_function_name)
        ext_print('[LLMProgress] LLM has chosen')

        chosen_option = next((func for func in functions if func.__name__ == chosen_function_name), None)

        ext_print('[LLMProgress] ...')
        return chosen_option
