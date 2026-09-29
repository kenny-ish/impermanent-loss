# impermanent-loss

Impermanent loss calculator for Uniswap-style pools. It compares an LP position with holding the
two tokens.

## v2 (full range)

```bash
python il.py --ratio 2          # price doubled
python il.py --from 2400 --to 3600
python il.py --table
```

For v2 this is the closed form `IL = 2*sqrt(r)/(1+r) - 1`, where `r` is the price ratio.

## v3 (concentrated liquidity)

```bash
python il.py --from 2400 --to 3000 --range 2000 3200
```

A v3 range has no closed form, so the script computes the token amounts of a position with
liquidity 1 at the entry price, values them at the exit price (clamped to the range) and compares
that with holding the entry amounts. Narrow ranges make the loss larger, and once the price leaves
the range the position is entirely one token.

Trading fees are not included.

## Tests

```bash
python -m unittest -v
```
