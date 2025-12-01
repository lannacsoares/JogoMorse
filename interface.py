import tkinter as tk
from quiz_manager import QuizManager


class MorseQuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz de Código Morse")
        self.geometry("900x620")
        self.configure(bg="#1b1125")

        self.quiz = QuizManager()
        self.time_left = 10
        self.timer_id = None
        self.mode = "hard"  # default

        self._build_ui()
        self.new_round()

    # --------------------------------------------------------

    def _build_ui(self):
        title = tk.Label(
            self, text="Treinador de Código Morse",
            font=("Segoe UI", 30, "bold"),
            fg="#ff7ad9", bg="#1b1125"
        )
        title.pack(pady=20)

        # Seletor de modo
        mode_frame = tk.Frame(self, bg="#1b1125")
        mode_frame.pack(pady=10)

        tk.Label(
            mode_frame, text="Modo:",
            font=("Segoe UI", 16),
            bg="#1b1125", fg="#ffb3ec"
        ).pack(side="left", padx=5)

        tk.Button(
            mode_frame, text="Fácil (Múltipla escolha)",
            command=lambda: self.change_mode("easy"),
            font=("Segoe UI", 14), fg="white", bg="#5c3575",
            relief="flat", padx=10, pady=5
        ).pack(side="left", padx=8)

        tk.Button(
            mode_frame, text="Difícil (Digitar)",
            command=lambda: self.change_mode("hard"),
            font=("Segoe UI", 14), fg="white", bg="#5c3575",
            relief="flat", padx=10, pady=5
        ).pack(side="left", padx=8)

        tk.Button(
            mode_frame,
            text="Encerrar Jogo",
            command=self.end_game,
            font=("Segoe UI", 14),
            fg="white",
            bg="#ff4a7d",
            relief="flat",
            padx=14,
            pady=5
        ).pack(side="left", padx=8)

        # Morse display
        self.morse_label = tk.Label(
            self, text="---",
            font=("Consolas", 42, "bold"),
            fg="#ffb3ec", bg="#1b1125"
        )
        self.morse_label.pack(pady=20)

        # Timer
        self.timer_label = tk.Label(
            self, text="Tempo: 10",
            font=("Segoe UI", 20),
            fg="#e1c6ff", bg="#1b1125"
        )
        self.timer_label.pack()

        # Entrada modo difícil
        self.answer_entry = tk.Entry(
            self, font=("Segoe UI", 22),
            justify="center",
            fg="white", bg="#2b1940",
            insertbackground="white"
        )
        self.answer_entry.bind("<Return>", lambda e: self.submit())

        # Botão de resposta
        self.answer_button = tk.Button(
            self, text="Responder",
            command=self.submit,
            font=("Segoe UI", 18),
            fg="white", bg="#ff4fbf",
            activebackground="#ff77d4",
            relief="flat", padx=14, pady=8
        )

        # Botões de múltipla escolha
        self.choice_buttons = []
        for _ in range(4):
            b = tk.Button(
                self, text="A",
                font=("Segoe UI", 20),
                fg="white", bg="#5c3575",
                activebackground="#7c4b95",
                relief="flat",
                padx=20, pady=10,
                command=lambda opt="": self.submit_option(opt)
            )
            self.choice_buttons.append(b)

        # Feedback
        self.feedback_label = tk.Label(
            self, text="", font=("Segoe UI", 20),
            fg="#ffdfff", bg="#1b1125"
        )
        self.feedback_label.pack(pady=10)

        # Pontuação
        self.score_label = tk.Label(
            self, text="Pontuação: 0/0",
            font=("Segoe UI", 20),
            fg="#caa6ff", bg="#1b1125"
        )
        self.score_label.pack(pady=10)

    # --------------------------------------------------------

    def change_mode(self, mode):
        self.mode = mode
        self.new_round()

    # Timer ---------------------------------------------------

    def start_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)

        self.time_left = 10
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Tempo: {self.time_left}")

        if self.time_left <= 0:
            self.feedback_label.config(
                text=f"⏳ Tempo esgotado! Era: {self.quiz.current_letter}",
                fg="#ff6b6b"
            )
            self.after(1500, self.new_round)
            return

        self.time_left -= 1
        self.timer_id = self.after(1000, self.update_timer)

    # --------------------------------------------------------

    def submit_option(self, opt):
        self.submit(answer=opt)

    # --------------------------------------------------------

    def submit(self, answer=None):
        if answer is None:
            answer = self.answer_entry.get()
            self.answer_entry.delete(0, tk.END)

        correct = self.quiz.check_answer(answer)

        if correct:
            self.feedback_label.config(text="✔ Correto!", fg="#6bff9c")
        else:
            self.feedback_label.config(
                text=f"✘ Errado! Correto: {self.quiz.current_letter}",
                fg="#ff6b6b"
            )

        self.score_label.config(
            text=f"Pontuação: {self.quiz.score}/{self.quiz.total_questions}"
        )

        self.after(1200, self.new_round)

    # --------------------------------------------------------

    def new_round(self):
        self.feedback_label.config(text="")

        morse = self.quiz.new_question()
        self.morse_label.config(text=morse)
        self.start_timer()

        # limpa widgets
        self.answer_entry.pack_forget()
        self.answer_button.pack_forget()
        for b in self.choice_buttons:
            b.pack_forget()

        # modo difícil
        if self.mode == "hard":
            self.answer_entry.pack(pady=20)
            self.answer_button.pack()
            self.answer_entry.focus()

        # modo fácil
        else:
            for i, opt in enumerate(self.quiz.get_options()):
                b = self.choice_buttons[i]
                b.config(text=opt, command=lambda x=opt: self.submit_option(x))
                b.pack(pady=10)

    # Final ---------------------------------------------------

    def end_game(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)

        errors = self.quiz.total_questions - self.quiz.score
        accuracy = (
            (self.quiz.score / self.quiz.total_questions) * 100
            if self.quiz.total_questions else 0
        )

        result_window = tk.Toplevel(self)
        result_window.title("Resultado Final")
        result_window.geometry("500x350")
        result_window.configure(bg="#1b1125")

        tk.Label(
            result_window, text="Fim do Jogo!",
            font=("Segoe UI", 26, "bold"),
            fg="#ff7ad9", bg="#1b1125"
        ).pack(pady=20)

        tk.Label(
            result_window,
            text=f"✔ Acertos: {self.quiz.score}",
            font=("Segoe UI", 20),
            fg="#6bff9c", bg="#1b1125"
        ).pack()

        tk.Label(
            result_window,
            text=f"✘ Erros: {errors}",
            font=("Segoe UI", 20),
            fg="#ff6b6b", bg="#1b1125"
        ).pack()

        tk.Label(
            result_window,
            text=f"🎯 Precisão: {accuracy:.1f}%",
            font=("Segoe UI", 20),
            fg="#ffdfff", bg="#1b1125"
        ).pack(pady=20)

        tk.Button(
            result_window,
            text="Fechar",
            command=self.destroy,
            font=("Segoe UI", 16),
            fg="white", bg="#ff4a7d",
            relief="flat", padx=20, pady=8
        ).pack(pady=10)
