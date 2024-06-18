import ollama


class LLMInteractor:
    """
    Class that contains interactions with LLMs.
    """

    def __init__(self):
        self.llm = 'llama3'

    def set_llm(self, llm_name):
        self.llm = llm_name

    def ask_about_column_name(self, column_name):
        response = ollama.chat(model=self.llm, messages=[
            {
                'role': 'user',
                'content': 'Do you think that  '
                           + column_name + ' is personal data?'
                           + ' Answer with as few words as possible!',
            },
        ])
        print(response['message']['content'])
        return "Yes" == response['message']['content'][1:4]
