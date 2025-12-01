import random
from typing import Optional
from morse_dict import MORSE_DICT


class QuizManager:
    def __init__(self):
        self.current_letter: Optional[str] = None
        self.score = 0
        self.total_questions = 0

    def new_question(self) -> str:
        self.current_letter = random.choice(list(MORSE_DICT.keys()))
        return MORSE_DICT[self.current_letter]

    def get_options(self) -> list:
        """Gera alternativas para o modo fácil."""
        options = [self.current_letter]
        letters = list(MORSE_DICT.keys())

        while len(options) < 4:
            choice = random.choice(letters)
            if choice not in options:
                options.append(choice)

        random.shuffle(options)
        return options

    def check_answer(self, answer: str) -> bool:
        """Valida resposta (modo fácil ou difícil)."""
        self.total_questions += 1

        if not self.current_letter:
            return False

        if answer.strip().upper() == self.current_letter:
            self.score += 1
            return True

        return False
