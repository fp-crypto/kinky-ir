import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
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
            return 0
        if util <= optimal_util:
            return ir_1(util)
        else:
            return ir_2(util)
    return (ir,)


@app.cell
def _(ir):
    import altair as alt
    import pandas as pd
    import numpy as np

    xs = np.linspace(0, 1, 100)
    util_data = pd.DataFrame(
        {"utilization": xs, "interest rate": (ir(x) for x in xs)}
    )
    util_chart = (
        alt.Chart(util_data)
        .mark_line(color="gray")
        .encode(
            x=alt.X("utilization", axis=alt.Axis(format="%")),
            y=alt.Y("interest rate", axis=alt.Axis(format="%")),
        )
    )
    util_chart
    return alt, np, pd, util_chart


@app.cell
def _():
    import marimo as mo

    start = 0
    stop = 1_000_000
    step = 10_000

    pool_1_total_assets_slider = mo.ui.slider(
        start=start,
        stop=stop,
        step=step,
        value=500_000,
        label="Pool 1 Total Assets",
    )
    pool_2_total_assets_slider = mo.ui.slider(
        start=start,
        stop=stop,
        step=step,
        value=200_000,
        label="Pool 2 Total Assets",
    )
    return (
        mo,
        pool_1_total_assets_slider,
        pool_2_total_assets_slider,
        start,
        step,
    )


@app.cell
def _(mo, pool_1_total_assets_slider, pool_2_total_assets_slider):
    mo.vstack(
        [
            mo.hstack(
                [
                    pool_1_total_assets_slider,
                    mo.md(f"Has value: {pool_1_total_assets_slider.value}"),
                ]
            ),
            mo.hstack(
                [
                    pool_2_total_assets_slider,
                    mo.md(f"Has value: {pool_2_total_assets_slider.value}"),
                ]
            ),
        ]
    )
    return


@app.cell
def _(mo, pool_1_total_assets_slider, pool_2_total_assets_slider, start, step):
    pool_1_total_assets = pool_1_total_assets_slider.value
    pool_2_total_assets = pool_2_total_assets_slider.value

    pool_1_total_borrow_slider = mo.ui.slider(
        start=start,
        stop=pool_1_total_assets,
        step=step,
        value=400_000,
        label="Pool 1 Total Borrow",
    )
    pool_2_total_borrow_slider = mo.ui.slider(
        start=start,
        stop=pool_2_total_assets,
        step=step,
        value=199_000,
        label="Pool 2 Total Borrow",
    )
    return (
        pool_1_total_assets,
        pool_1_total_borrow_slider,
        pool_2_total_assets,
        pool_2_total_borrow_slider,
    )


@app.cell
def _(mo, pool_1_total_borrow_slider, pool_2_total_borrow_slider):
    mo.vstack(
        [
            mo.hstack(
                [
                    pool_1_total_borrow_slider,
                    mo.md(f"Has value: {pool_1_total_borrow_slider.value}"),
                ]
            ),
            mo.hstack(
                [
                    pool_2_total_borrow_slider,
                    mo.md(f"Has value: {pool_2_total_borrow_slider.value}"),
                ]
            ),
        ]
    )
    return


@app.cell
def _(
    alt,
    ir,
    pd,
    pool_1_total_assets,
    pool_1_total_borrow_slider,
    pool_2_total_assets,
    pool_2_total_borrow_slider,
    util_chart,
):
    pool_1_total_borrow = pool_1_total_borrow_slider.value
    pool_2_total_borrow = pool_2_total_borrow_slider.value

    def utilization(total_assets: int, total_borrow: int) -> float:
        return total_borrow / float(total_assets)

    pool_1_utilization = utilization(pool_1_total_assets, pool_1_total_borrow)
    pool_2_utilization = utilization(pool_2_total_assets, pool_2_total_borrow)

    pool_1_ir = ir(pool_1_utilization)
    pool_2_ir = ir(pool_2_utilization)

    pools_ir_util = pd.DataFrame(
        {
            "utilization": [pool_1_utilization, pool_2_utilization],
            "interest rate": [pool_1_ir, pool_2_ir],
            "pool": ["Pool 1", "Pool 2"],
        }
    )

    pool_ir_points = (
        alt.Chart(pools_ir_util)
        .mark_point()
        .encode(
            x="utilization",
            y="interest rate",
            color="pool",
            tooltip=[
                "pool",
                alt.X("utilization", axis=alt.Axis(format="%")),
                alt.Y("interest rate", axis=alt.Axis(format="%")),
            ],
        )
    )

    pool_ir_points + util_chart
    return pool_1_total_borrow, pool_2_total_borrow, utilization


@app.cell
def _(mo, pool_1_total_assets, pool_2_total_assets, start, step):
    pool_1_my_assets_slider = mo.ui.slider(
        start=0,
        stop=pool_1_total_assets,
        step=step,
        value= pool_1_total_assets / 10,
        label="Pool 1 My Assets",
    )
    pool_2_my_assets_slider = mo.ui.slider(
        start=start,
        stop=pool_2_total_assets,
        step=step,
        value=pool_2_total_assets * 0.8,
        label="Pool 2 My Assets",
    )
    return pool_1_my_assets_slider, pool_2_my_assets_slider


@app.cell
def _(mo, pool_1_my_assets_slider, pool_2_my_assets_slider):
    mo.vstack(
        [
            mo.hstack(
                [
                    pool_1_my_assets_slider,
                    mo.md(f"Has value: {pool_1_my_assets_slider.value}"),
                ]
            ),
            mo.hstack(
                [
                    pool_2_my_assets_slider,
                    mo.md(f"Has value: {pool_2_my_assets_slider.value}"),
                ]
            ),
        ]
    )
    return


@app.cell
def _(pool_1_my_assets_slider, pool_2_my_assets_slider):
    pool_1_my_assets = int(pool_1_my_assets_slider.value)
    pool_2_my_assets = int(pool_2_my_assets_slider.value)
    return pool_1_my_assets, pool_2_my_assets


@app.cell
def _(
    alt,
    ir,
    np,
    pd,
    pool_1_my_assets,
    pool_1_total_assets,
    pool_1_total_borrow,
    pool_2_my_assets,
    pool_2_total_assets,
    pool_2_total_borrow,
    utilization,
):
    def apr_with_delta(delta: int) -> float:
        pool_1_utilization = utilization(
            pool_1_total_assets + delta, pool_1_total_borrow
        )
        pool_2_utilization = utilization(
            pool_2_total_assets - delta, pool_2_total_borrow
        )

        return (
            ir(pool_1_utilization) * pool_1_my_assets
            + ir(pool_2_utilization) * pool_2_my_assets
        ) / (pool_1_my_assets + pool_2_my_assets)


    deltas = np.linspace(
        max(-pool_1_my_assets, -(pool_1_total_assets - pool_1_total_borrow)),
        min(pool_2_my_assets, (pool_2_total_assets - pool_2_total_borrow)),
        10000,
    )
    deltas_df = pd.DataFrame(
        {
            "delta": deltas,
            "apr": (apr_with_delta(delta) for delta in deltas),
        }
    )

    delta_chart = (
        alt.Chart(deltas_df)
        .mark_line(color="green")
        .encode(
            x=alt.X(
                "delta",
                axis=alt.Axis(format="e", title="delta"),
                scale=alt.Scale(domain=[deltas[0], deltas[-1]]),
            ),
            y=alt.Y("apr", axis=alt.Axis(format="%")),
        )
    )
    x0_line = (
        alt.Chart(pd.DataFrame({"x": [0]}))
        .mark_rule(color="gray")
        .encode(x=alt.X("x", axis=alt.Axis(title="")))
    )

    delta_chart + x0_line
    return


if __name__ == "__main__":
    app.run()
