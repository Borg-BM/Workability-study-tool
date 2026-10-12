import numpy as np
from sympy import *

normal_symbols = symbols(
    "Pnitro, Fact, c_f, Fdyn, Floss, r_acc, Fmax, Fmin, Apass, P1_loss, P2_loss, P3_loss, P4_loss, Ppas_max"
)

positive_symbols = symbols("A1, A2", positive=True)

syms = {str(s): s for s in [*normal_symbols, *positive_symbols]}

# T700 parameters [1]

d_accu_T700 = 360e-3  # [m] Diameter of T700 accu [1]

V_accu_T700 = 250e-3  # [m^3] Volume of T700 accu [1]

V_nitro_T700 = 4000e-3  # [m^3] Volume of nitrogen tanks behind accu (T700) [1]

def guesser(symbols: list):
    guesses = dict(zip(symbols, [0] * len(symbols)))
    for symbol in symbols:
        symb = str(symbol)
        # guesses[symbol] = np.random.rand()
        if symb.startswith("P"):
            if symb.endswith("loss"):
                if symb == "P3_loss":
                    guesses[symbol] += -100e5
                    continue
                guesses[symbol] += 100e5
                continue
            guesses[symbol] += 200e5
            continue
        if symb.startswith("F"):
            guesses[symbol] += 1e6
            continue
        if symb.startswith("A"):
            guesses[symbol] += 0.05
            continue
        if symb.startswith("r_acc"):
            guesses[symbol] += 0.05
            continue
        if symb.startswith("stroke"):
            guesses[symbol] += 5
            continue
        if symb.startswith("c_f"):
            guesses[symbol] += 1.2
            continue
        guesses[symbol] += 0.1
    return guesses

class VariablePressureAccumulator:
    """
    All symbols:
    Pnitro - Nitrogen pressure in the accumulator at midpoint
    Fact - Max active cylinder force
    c_f - Contingency factor of required active force, meant for control delay, or pumping pressure loss/gain in the VPA. Usually 1.2
    Fdyn - Dynamic forces on cylinder, as required active force.
    Floss - Extra active force required to overcome losses in the VPA
    r_acc - Nitrogen pressure loss/gain (ratio) over full stroke of accu (+/-)
    Fmax - Maximum force of the active + passive cylinder
    Fmin - Minimum force of the active + passive cylinder
    Apass - Area of the passive cylinder/chamber
    P1_loss - Pressure loss in V1 of the VPA
    P2_loss - Pressure loss in V2 of the VPA
    P3_loss - Pressure loss in V3 of the VPA
    P4_loss - Pressure loss in V4 of the VPA
    Ppas_max - Maximum passive pressure
    A1 - Area of the tandem cylinder in V1 and V4 in the VPA
    A2 - Area of the tandem cylinder in V2 and V3 in the VPA
    """

    def __init__(
        self,
        *extra_eq1,
        Ploss_iso=2e5,
        Ploss_accu=2e5,
        Ploss_valve=3e5,
        Ploss_tank=5e5,
        Floss_ex=0,
        num_solve=False,
        guesses=False,
        **kwargs,
    ):

        self._syms = syms

        (
            Pnitro,
            Fact,
            c_f,
            Fdyn,
            Floss,
            r_acc,
            Fmax,
            Fmin,
            Apass,
            P1_loss,
            P2_loss,
            P3_loss,
            P4_loss,
            Ppas_max,
            A1,
            A2,
        ) = VariablePressureAccumulator.syms(
            "Pnitro,Fact,c_f,Fdyn,Floss,r_acc,Fmax,Fmin,Apass,P1_loss,P2_loss,P3_loss,P4_loss,Ppas_max,A1,A2"
        )
        # assuming highest losses occurs when (force, flow, stroke) = (max, out, out).
        Loss_eq = [
            Eq(P4_loss, Pnitro * r_acc + Ploss_accu),
            Eq(P3_loss, (-Ploss_tank - Ploss_valve)),  # negative means pressure gain
            Eq(P2_loss, P4_loss + Ploss_valve),
            # basic force equation
            Eq(P1_loss * A1 + P3_loss * A2, P2_loss * A2 + P4_loss * A1),
            Eq(Floss, (P1_loss + Ploss_iso) * Apass),
        ]
        VPA_equations = [
            Eq(Ppas_max, ((Fmax - Fmin) * 5 / 6 + Fmin) / Apass),
            Eq((Fmax - Fmin) / 2 + Fmin, Pnitro * Apass),
            Eq(A2 / A1, (Ppas_max) / (Pnitro) - 1),
            Eq(Fact, c_f * (1 / 6) * (Fmax - Fmin) + Fdyn + (Floss + Floss_ex)),
        ]
        # extra_eq = [Eq(symbols(k), v) for k, v in kwargs.items()]
        losses = dict(Piso=Ploss_iso, Pacc_f=Ploss_accu, Pvalve=Ploss_valve, Ptank=Ploss_tank)
        all_eqs = [*Loss_eq, *extra_eq1, *VPA_equations]
        all_eqs = [eq.subs([(self.syms(k), v) for k, v in kwargs.items()]) for eq in all_eqs]
        all_eqs = [eq.subs([(self.syms(k), v) for k, v in losses.items()]) for eq in all_eqs]
        n_eqs = len(all_eqs)
        eq_symbols = list(set.union(*[eq.atoms(Symbol) for eq in all_eqs]))
        n_symbols = len(eq_symbols)
        # if n_eqs != n_symbols:
        #     raise AttributeError(
        #         f"Warning: number of equations ({len(all_eqs)}) does not match number of symbols ({n_symbols}). The solution is under- or overdetermined."
        #     )
        solution = []
        all_eqs = [nsimplify(i, rational=1) for i in all_eqs]
        if num_solve == False:
            solution = solve(all_eqs, dict=True, domain=S.Reals)
        if len(solution) != 1:
            if num_solve == False:
                print("Multiple or no solutions found. Trying with nsolve")
            guesses = guesses or guesser(list(eq_symbols))
            try:
                solution = nsolve(
                    all_eqs,
                    list(guesses.keys()),
                    list(guesses.values()),
                    dict=True,
                    domain=S.Reals,
                    prec=15,
                    verify=False,
                )
            except (ValueError, ZeroDivisionError) as e:
                raise ValueError(f"nsolve failed: {e}. My guesses were: {guesses}")
                print(f"nsolve failed: {e}")
                print(f"My guesses were: ", *guesses.items(), sep="\n")
            if len(solution) != 1:
                raise AttributeError("Multiple or no solutions found")
        # print(f"Solution found with tolerance of at least: {np.max([((eq.lhs.subs(solution[0]) / eq.rhs.subs(solution[0]))-1) for eq in all_eqs])}")
        assert all(
            [((eq.lhs.subs(solution[0]) / eq.rhs.subs(solution[0])) - 1) < 1e-10 for eq in all_eqs]
        ), "Solution is not within 1e-10 correct."

        self.all_eqs = all_eqs

        VPA_properties = {**{str(k): float(v) for k, v in solution[0].items()}, **kwargs, **losses}

        self.properties = set.union(set(self._syms.keys()), set(VPA_properties.keys()))

        [self.__setattr__(str(prop), float(VPA_properties[prop])) for prop in self.properties]

    # @property
    # def syms(self):
    #     if k not in syms.keys():
    #         syms[k] = symbols(k)
    #     return syms[k]
    # def find_exact_solution(self, L_TDS, c_f, A_pass, P_valve, P_tank, P_acc_f, P_iso, F_dyn, F_act, n_p=3, V_nitro=V_nitro_T700):
    #     V_accu = L_TDS*A_pass*(1+3/4*F_max/(A_pass**2)*n_p)
    #     r_acc = V_accu / (2*(V_accu+V_nitro))
    #     a = (12/14*r_acc)
    #     b = 6/42*c_f+4/7*A_pass**2*r_acc+3/(2*A_pass)*(2*P_valve+P_tank+P_acc_f)
    #     c = P_iso*A_pass + A_pass*P_acc_f+F_dyn-F_act
    #     F_max = np.roots([a,b,c])
    #     return F_max

    @staticmethod

    def syms(k):
        ks = k.split(",")
        res = {}
        for k in ks:
            if k not in syms.keys():
                syms[k] = symbols(k)
            res[k] = syms[k]
        if len(ks) == 1:
            return tuple(res.values())[0]
        return tuple(res.values())

    def prop_dict(self):
        return dict(zip(self.properties, [self.__dict__[k] for k in self.properties]))

    @staticmethod

    def calc_accu_volume(A1, A2, stroke_vpa, n_pumps=3):
        # temp range is [min, max] K. or 0C to 20C
        V1 = stroke_vpa * A1
        V2 = stroke_vpa * A2
        V_accu = V1 + n_pumps / 2 * V2
        return V_accu

    @staticmethod

    def calc_nitro_loss(A1, A2, stroke_vpa, V_nitro=V_nitro_T700, n_pumps=3):
        V_accu = VariablePressureAccumulator.calc_accu_volume(A1, A2, stroke_vpa, n_pumps)
        nitro_loss = V_accu / (V_nitro + V_accu)  # [-] nitro pressure loss/gain (ratio) over full stroke of accu
        r_acc = nitro_loss / 2
        return r_acc

    @staticmethod

    def calc_accu_stroke(
        A1, A2, stroke_vpa, d_accu=d_accu_T700, n_pumps=3, temp_range=[273.15, 293.15], r_accu_fill_inaccuracy=0.04
    ):
        temp_ratio = temp_range[1] / temp_range[0]
        V_accu = (
            temp_ratio
            * (1.0 + r_accu_fill_inaccuracy)
            * VariablePressureAccumulator.calc_accu_volume(A1, A2, stroke_vpa, n_pumps)
        )
        A_accu = np.pi * (d_accu / 2) ** 2  # [m^2] Area of accu
        return V_accu / A_accu

    def get_passive_force_steps(self):
        Ftot = self.Fmax - self.Fmin
        return np.array([1 / 6, 1 / 2, 5 / 6]) * Ftot + self.Fmin
