"""Impermanent loss for constant-product and concentrated liquidity positions."""
import argparse
import math


def il_v2(ratio: float) -> float:
    if ratio <= 0:
        raise ValueError("price ratio must be positive")
    return 2 * math.sqrt(ratio) / (1 + ratio) - 1


def _amounts(price: float, lower: float, upper: float) -> tuple[float, float]:
    """Token amounts (x = base, y = quote) for liquidity 1 at a given price."""
    p = min(max(price, lower), upper)
    sp, sa, sb = math.sqrt(p), math.sqrt(lower), math.sqrt(upper)
    return 1 / sp - 1 / sb, sp - sa


def il_v3(p0: float, p1: float, lower: float, upper: float) -> float:
    if not 0 < lower < upper:
        raise ValueError("need 0 < lower < upper")
    x0, y0 = _amounts(p0, lower, upper)
    x1, y1 = _amounts(p1, lower, upper)
    hold = x0 * p1 + y0
    lp = x1 * p1 + y1
    return lp / hold - 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ratio", type=float, help="new price / entry price")
    ap.add_argument("--from", dest="p0", type=float)
    ap.add_argument("--to", dest="p1", type=float)
    ap.add_argument("--range", nargs=2, type=float, metavar=("LOWER", "UPPER"))
    ap.add_argument("--table", action="store_true", help="print IL for common price moves")
    a = ap.parse_args()

    if a.table:
        print(f"{'price move':>11}  {'IL':>8}")
        for r in (0.25, 0.5, 0.75, 0.9, 1.1, 1.25, 1.5, 2, 3, 5, 10):
            print(f"{(r - 1):>+10.0%}  {il_v2(r):>8.2%}")
        return

    if a.range:
        if a.p0 is None or a.p1 is None:
            ap.error("--range needs --from and --to")
        print(f"v3 IL in [{a.range[0]}, {a.range[1]}]: {il_v3(a.p0, a.p1, *a.range):.2%}")
        return

    ratio = a.ratio if a.ratio else (a.p1 / a.p0 if a.p0 and a.p1 else None)
    if ratio is None:
        ap.error("give --ratio, or --from and --to")
    print(f"price ratio {ratio:.4f} -> IL {il_v2(ratio):.2%}")


if __name__ == "__main__":
    main()
