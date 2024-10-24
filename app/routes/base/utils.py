class UserMetrics:
    def __init__(
        self,
        courses_count: int = 0,
        completed_courses_count: int = 0,
        assessments_count: int = 0,
        learning_hours: float = 0.0,
        longest_strike: float = 0.0,
    ):
        self.courses_count = courses_count
        self.completed_courses_count = completed_courses_count
        self.assessments_count = assessments_count
        self.learning_hours = learning_hours
        self.longest_strike = longest_strike

    @staticmethod
    def calculate_duration(duration: float):
        _days, _remaining_hours = 0, 0

        if duration > 24:
            _days = int(duration // 24)
            _remaining_hours = round(duration % 24, 1)
        else:
            _remaining_hours = round(duration, 1)

        return _days, _remaining_hours

    @property
    def learning_hours_fmt(self) -> str:
        _days, _remaining_hours = self.calculate_duration(self.learning_hours)
        if _days != 0:
            return f"{_days} Days {_remaining_hours} Hours"

        return f"{_remaining_hours} Hours"

    @property
    def longest_strike_fmt(self) -> str:
        _days, _remaining_hours = self.calculate_duration(self.longest_strike)
        if _days != 0:
            return f"{_days} Days {_remaining_hours} Hours"

        return f"{_remaining_hours} Hours"
