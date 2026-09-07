class Contour:
    """Базовый класс контура. Все три контура наследуют его поведение."""
    def __init__(self, name, base_priority, max_priority):
        self.name = name
        self.base_priority = base_priority
        self.max_priority = max_priority
        self.current_priority = base_priority
        self.active_events = []  # список активных событий (кортежи: имя, приоритет)

    def add_event(self, event_name, event_priority):
        """Добавляет событие и пересчитывает приоритет."""
        self.active_events.append((event_name, event_priority))
        self._recalculate()

    def clear_events(self):
        """Убирает все события и возвращает приоритет к базовому."""
        self.active_events = []
        self.current_priority = self.base_priority

    def _recalculate(self):
        """Приоритет = максимум из базового и всех событий, но не выше max_priority."""
        if self.active_events:
            priorities = [self.base_priority] + [p for _, p in self.active_events]
            self.current_priority = min(max(priorities), self.max_priority)
        else:
            self.current_priority = self.base_priority

    def status(self):
        """Возвращает строку состояния для логов."""
        if not self.active_events:
            return f"{self.name}: приоритет {self.current_priority}, событий нет"
        events = ", ".join(f"{name}={prio}" for name, prio in self.active_events)
        return f"{self.name}: приоритет {self.current_priority}, события: {events}"
class VitalContour(Contour):
    """Витальный контур (V_h) — безопасность и выживание."""
    def __init__(self):
        super().__init__("V_h", base_priority=10, max_priority=100)

class CognitiveContour(Contour):
    """Когнитивный контур (V_e) — навигация и движение."""
    def __init__(self):
        super().__init__("V_e", base_priority=40, max_priority=80)

class SocialContour(Contour):
    """Социальный контур (V_s) — взаимодействие с людьми и машинами."""
    def __init__(self):
        super().__init__("V_s", base_priority=10, max_priority=75)
