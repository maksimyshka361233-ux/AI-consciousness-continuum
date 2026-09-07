class Arbiter:
    def __init__(self, hysteresis=15, critical_vh=90):
        self.hysteresis = hysteresis
        self.critical_vh = critical_vh
        self.current_winner = None

    def decide(self, contours):
        vh = next(c for c in contours if c.name == "V_h")
        # Безусловное прерывание
        if vh.current_priority >= self.critical_vh:
            self.current_winner = vh
            return vh, "БЕЗУСЛОВНОЕ ПРЕРЫВАНИЕ!"

        leader = max(contours, key=lambda c: c.current_priority)
        if self.current_winner is None:
            self.current_winner = leader
            return self.current_winner, None

        # Проверяем гистерезис
        if leader.current_priority > self.current_winner.current_priority + self.hysteresis:
            self.current_winner = leader
            return self.current_winner, None
        else:
            if leader.name == self.current_winner.name:
                # Лидер тот же, всё стабильно
                explanation = None
            else:
                explanation = f"Гистерезис: {leader.name} не может перехватить управление у {self.current_winner.name} (разница {leader.current_priority - self.current_winner.current_priority} меньше {self.hysteresis})"
            return self.current_winner, explanation
