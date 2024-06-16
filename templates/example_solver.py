import sys


class Answer:
    def __init__(self, value: int) -> None:
        self.value = value

    def calc_score(self) -> int:
        return self.value * self.value


def solve() -> int:
    """Solve the problem and return the score."""
    a, b = map(int, input().split())
    answer = Answer(a + b)
    print(answer.value)
    return answer.calc_score()


score = solve()

# Here is an example of how to pass the score to cp-heuristics-adapter.
if len(sys.argv) > 1:
    # Destination file path is passed as the first argument.
    score_file_name = sys.argv[1]
    with open(score_file_name, "w") as f:
        # Print the score in a line.
        f.write(str(score))
