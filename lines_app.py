from __future__ import annotations
from dataclasses import dataclass

EPS = 1e-8

MIN_VAL = -149
MAX_VAL = 149


class InputError(ValueError):
    pass


def is_zero(z: float, eps: float = EPS) -> bool:
    return abs(z) <= eps


def require_int_in_range(name: str, value: int) -> int:
    if not isinstance(value, int):
        raise InputError(
            f"{name}: expected an integer, got {type(value).__name__}.; "
            f"Fix: enter an integer in range [{MIN_VAL}; {MAX_VAL}]."
        )
    if value < MIN_VAL or value > MAX_VAL:
        raise InputError(
            f"{name}: value {value} is out of range [{MIN_VAL}; {MAX_VAL}].; "
            f"Fix: enter a value inside the range."
        )
    return value


@dataclass(frozen=True)
class Line:
    A: float
    B: float
    C: float

    def det2(self, other: "Line") -> float:
        return self.A * other.B - other.A * self.B

    def is_parallel(self, other: "Line") -> bool:
        return is_zero(self.det2(other))

    def intersection(self, other: "Line") -> tuple[float, float] | None:
        det = self.det2(other)
        if is_zero(det):
            return None

        x = (self.B * other.C - other.B * self.C) / det
        y = (other.A * self.C - self.A * other.C) / det
        return (x, y)

    def normalized(self) -> "Line":
        norm = (self.A * self.A + self.B * self.B) ** 0.5
        if is_zero(norm):
            raise ValueError("Invalid line: A and B are both zero.")

        a = self.A / norm
        b = self.B / norm
        c = self.C / norm

        if (not is_zero(a) and a < 0) or (is_zero(a) and b < 0):
            a, b, c = -a, -b, -c

        return Line(round(a, 12), round(b, 12), round(c, 12))

    def is_same_as(self, other: "Line") -> bool:
        return self.normalized() == other.normalized()


def line_from_slope(k: int, b: int) -> Line:
    require_int_in_range("k", k)
    require_int_in_range("b", b)

    if b == 0:
        raise InputError(
            "b cannot be 0 for y = kx + b.; "
            "Fix: enter b != 0 (e.g., 1 or -1)."
        )

    return Line(float(k), -1.0, float(b))


def line_from_point_normal(x0: int, y0: int, a: int, b: int, idx: int) -> Line:
    require_int_in_range(f"x0{idx}", x0)
    require_int_in_range(f"y0{idx}", y0)
    require_int_in_range(f"a{idx}", a)
    require_int_in_range(f"b{idx}", b)

    if a == 0 and b == 0:
        raise InputError(
            f"(a{idx}, b{idx}) cannot be (0,0).; "
            f"Fix: make a{idx} and/or b{idx} non-zero."
        )

    c = -(a * x0 + b * y0)
    return Line(float(a), float(b), float(c))


def unique_points(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    result: list[tuple[float, float]] = []

    for x, y in points:
        exists = False
        for ux, uy in result:
            if abs(x - ux) <= EPS and abs(y - uy) <= EPS:
                exists = True
                break
        if not exists:
            result.append((x, y))

    return result


def analyze_three_lines(
    l1: Line, l2: Line, l3: Line
) -> tuple[str, list[tuple[float, float]]]:
    lines = [l1, l2, l3]

    unique_lines: list[Line] = []
    for line in lines:
        if not any(line.is_same_as(existing) for existing in unique_lines):
            unique_lines.append(line)

    if len(unique_lines) == 1:
        return ("COINCIDE", [])

    points: list[tuple[float, float]] = []
    n = len(unique_lines)

    for i in range(n):
        for j in range(i + 1, n):
            p = unique_lines[i].intersection(unique_lines[j])
            if p is not None:
                points.append(p)

    points = unique_points(points)

    if len(points) == 0:
        return ("NONE", [])
    if len(points) == 1:
        return ("ONE", points)
    if len(points) == 2:
        return ("TWO", points)
    return ("THREE", points)


def format_result(status: str, points: list[tuple[float, float]]) -> str:
    if status == "COINCIDE":
        return "Lines coincide"
    if status == "NONE":
        return "Lines do not intersect"
    if status == "ONE":
        x0, y0 = points[0]
        return f"Single intersection point (x0, y0): x0= {x0:.6f}, y0= {y0:.6f}"
    if status == "TWO":
        (x1, y1), (x2, y2) = points
        return (
            f"Two intersection points: "
            f"(x1, y1)=({x1:.6f}, {y1:.6f}), "
            f"(x2, y2)=({x2:.6f}, {y2:.6f})"
        )
    if status == "THREE":
        (x1, y1), (x2, y2), (x3, y3) = points
        return (
            f"Three intersection points: "
            f"(x1, y1)=({x1:.6f}, {y1:.6f}), "
            f"(x2, y2)=({x2:.6f}, {y2:.6f}), "
            f"(x3, y3)=({x3:.6f}, {y3:.6f})"
        )
    return "Unknown result"


def main() -> None:
    try:
        print("Line 1: y = kx + b (b != 0)")
        k = int(input("k = "))
        b = int(input("b = "))

        print("\nLine 2: a1(x-x01) + b1(y-y01) = 0")
        x01 = int(input("x01 = "))
        y01 = int(input("y01 = "))
        a1 = int(input("a1 = "))
        b1 = int(input("b1 = "))

        print("\nLine 3: a2(x-x02) + b2(y-y02) = 0")
        x02 = int(input("x02 = "))
        y02 = int(input("y02 = "))
        a2 = int(input("a2 = "))
        b2 = int(input("b2 = "))

        l1 = line_from_slope(k, b)
        l2 = line_from_point_normal(x01, y01, a1, b1, idx=1)
        l3 = line_from_point_normal(x02, y02, a2, b2, idx=2)

        status, points = analyze_three_lines(l1, l2, l3)
        print("\n" + format_result(status, points))

    except InputError as e:
        print(f"Input error: {e}")
    except ValueError:
        print("Input error: expected an integer.; Fix: enter only integer numbers.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()