<!-- Source: https://docs.app.barge-master.com/usage/workability_percentages.html -->

# Calculating workability percentages

After calculating a machine’s workability using the workability training, one might want to calculate a percentage. To do this, we make use of hindcasting weather data. The percentage is calculated by dividing the number of hours the machine is workable by the total number of hours in the hindcast.

For hindcast data, the most basic form is to use the DNV C205 recommended practices. This standard describes a method to calculate ‘scatter diagrams’ (hindcast data) using empirical model.

**(Commercial) Note: Calculating workability percentages using the DNV C205 recommended practice, produces highly conservative results. If this result is to be used in client communication, it may only be used in combination with a comparison to a base case. Such that you compare workability of motion compensation against non-motion compensation.**

A region of the world can be selected, using Appendix B of the DNV C205 RP. Appendix B of DNV C205 is shown in the following figure

\[image: dnv_c205_appB — not available, stored as Git LFS pointer on the server\]

Using Appendix C of DNV C205 RP, the parameters for the empirical model can be selected according to the region selected in Appendix B. Appendix C is shown in the following figure

\[image: dnv_c205_appC — not available, stored as Git LFS pointer on the server\]

The 5 parameters, alpha_s, beta_s, a1, a2, b1, b2, are used as input in the functions of the PyBM hindcasting module. It is recommended to use the following function: [`PyBM.marine.weather_hindcast.ScatterDiagram.percentage_from_workability_weibull()`](../autoapi/PyBM/marine/weather_hindcast/ScatterDiagram/index.md#PyBM.marine.weather_hindcast.ScatterDiagram.percentage_from_workability_weibull "PyBM.marine.weather_hindcast.ScatterDiagram.percentage_from_workability_weibull")

It must be considered that the workability result must be calculated with enough wave periods to cover at least 99% of the sea state occurrence in an area. The function [`percentage_from_workability_weibull`](../autoapi/PyBM/marine/weather_hindcast/ScatterDiagram/index.md#PyBM.marine.weather_hindcast.ScatterDiagram.percentage_from_workability_weibull "PyBM.marine.weather_hindcast.ScatterDiagram.percentage_from_workability_weibull") will give an error whenever not enough wave periods are used.

See the following example to calculate a workability percentage using a workability result, using the [`percentage_from_workability_weibull`](../autoapi/PyBM/marine/weather_hindcast/ScatterDiagram/index.md#PyBM.marine.weather_hindcast.ScatterDiagram.percentage_from_workability_weibull "PyBM.marine.weather_hindcast.ScatterDiagram.percentage_from_workability_weibull") function:

    from PyBM.marine.weather_hindcast.ScatterDiagram import percentage_from_workability_weibull

    # Sea state parameters
    Tp = np.arange(2, 16, 1)

    wave = Jonswap(1, Tp, main_direction=some_wavedir)
    result = directional_workability(some_rao, wave, some_machine)
    result = result.min(["lim_type", "WaveDirection"])

    # Area 11 (southern north sea)
    args = dict(zip(["alpha_s", "beta_s", "a1", "a2", "b1", "b2"], [2.19, 1.26, 0.935, 0.222, 0.1386, -0.0208]))
    workability_percentage = percentage_from_workability_weibull(result, **args)
