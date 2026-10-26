def clamp(value: int, min_: int = 1, max_: int = 10000) -> int:
	return max(min_, min(value, max_))