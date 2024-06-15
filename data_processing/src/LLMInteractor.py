import llm


class LLMInteractor:
    """
    Class that contains interactions with LLMs.
    """

    def __init__(self):
        self.llm = 'mistral-7b-instruct-v0'

    def set_llm(self, llm_name):
        self.llm = llm_name

    def ask_about_column_name(self, column_name):
        print('asking ' + self.llm + ' about: ' + column_name)
        model = llm.get_model(self.llm)
        model.key = ''
        response = model.prompt(
            'Do you think that  ' + column_name
            + ' is personal data?'
            + ' Answer with as few words as possible!'
        )
        print(response.text())
        return "Yes" == response.text()[1:4]
