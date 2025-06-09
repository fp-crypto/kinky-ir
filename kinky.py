import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


app._unparsable_cell(
    r"""
     base_borrow = 0
    slope_1 = 0.055
    slope_2 = 0.35
    optimal_util = 0.92


    def ir_1(util):
        return ((slope_1 * util) / optimal_util) + base_borrow


    def ir_2(util):
        return (slope_2 * (util - optimal_util) / (1 - optimal_util)) + ir_1(util)


    def ir(util):
        if util < 0 or util > 1:
            return NaN
        if util <= optimal_util:
            return ir_1(util)
        else:
            return ir_2(util)
    """,
    name="_"
)


@app.cell
def _(ir):
    import altair as alt
    import pandas as pd
    import numpy as np

    xs = np.linspace(0, 1, 100)
    source = pd.DataFrame({"x": xs, "f(x)": (ir(x) for x in xs)})
    alt.Chart(source).mark_line().encode(x="x", y="f(x)")
    return


@app.cell
def _():
    import marimo as mo

    start = 0
    stop = 1_000_000
    step = 10_000

    pool_1_total_assets = mo.ui.slider(
        start=start,
        stop=stop,
        step=step,
        value=500_000,
        label="Pool 1 Total Assets",
    )
    pool_2_total_assets = mo.ui.slider(
        start=start,
        stop=stop,
        step=step,
        value=200_000,
        label="Pool 2 Total Assets",
    )
    return mo, pool_1_total_assets, pool_2_total_assets, start, step


@app.cell
def _(mo, pool_1_total_assets, pool_2_total_assets):
    mo.vstack(
        [
            mo.hstack(
                [
                    pool_1_total_assets,
                    mo.md(f"Has value: {pool_1_total_assets.value}"),
                ]
            ),
            mo.hstack(
                [
                    pool_2_total_assets,
                    mo.md(f"Has value: {pool_2_total_assets.value}"),
                ]
            ),
        ]
    )
    return


@app.cell
def _(mo, pool_1_total_assets, pool_2_total_assets, start, step):
    pool_1_total_borrow = mo.ui.slider(
        start=start,
        stop=pool_1_total_assets.value,
        step=step,
        value=int(pool_1_total_assets.value / 2),
        label="Pool 1 Total Borrow",
    )
    pool_2_total_borrow = mo.ui.slider(
        start=start,
        stop=pool_2_total_assets.value,
        step=step,
        value=int(pool_2_total_assets.value * 0.9),
        label="Pool 2 Total Borrow",
    )
    return pool_1_total_borrow, pool_2_total_borrow


@app.cell
def _(mo, pool_1_total_borrow, pool_2_total_borrow):
    mo.vstack(
        [
            mo.hstack(
                [
                    pool_1_total_borrow,
                    mo.md(f"Has value: {pool_1_total_borrow.value}"),
                ]
            ),
            mo.hstack(
                [
                    pool_2_total_borrow,
                    mo.md(f"Has value: {pool_2_total_borrow.value}"),
                ]
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
