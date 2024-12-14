from autogen import UserProxyAgent


class CustomUserProxy(UserProxyAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="user_proxy",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False},
        )
        self.responses = []
        self.current_response_idx = 0

    def get_human_input(self, prompt: str) -> str:
        if self.current_response_idx < len(self.responses):
            response = self.responses[self.current_response_idx]
            self.current_response_idx += 1
            return input(response)
        else:
            return super().get_human_input(prompt)
