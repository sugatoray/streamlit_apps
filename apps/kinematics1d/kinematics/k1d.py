def prepare_result(ndigits: int=2, **kwargs):
    return dict((k, round(v, ndigits)) for k, v in kwargs.items())

def eval_average_velocity(vi: float=None, vf: float=None, a: float=None, Dx: float=None, v_avg: float=None, using: str="vi,vf"):
    formula = ""
    v_avg = None
    if set(using.strip().split(",")) == {"vi", "vf"}:
        v_avg = 0.5 * (vi + vf)
        formula = r"v_{avg} &= \frac{\left( v_{i} + v_{f} \right)}{2}"
    elif set(using.strip().split(",")) == {"Dx", "t"}:
        v_avg = 2 * Dx / t
        formula = r"v_{avg} &= \frac{2 \Delta x}{t}"
    return dict(value=v_avg, formula=formula)

def eval_displacement(v_avg: float, t: float):
    Dx = v_avg * t
    formula = r"\Delta x &= v_{avg} t"
    return dict(value=Dx, formula=formula)

def eval_acceleration(vi: float, vf: float, t: float):
    a = (vf - vi) / t
    formula = r"a &= \frac{\left( v_{f} - v_{i} \right)}{t}"
    return dict(value=a, formula=formula)

def eval_initial_velocity(vi: float=None, vf: float=None, a: float=None, Dx: float=None, v_avg: float=None, using: str="v_avg,a,t"):
    formula = ""
    vf = None
    if set(using.strip().split(",")) == {"v_avg", "a", "t"}:
        vi = 0.5 * (v_avg - a * t)
        formula = r"v_{i} &= \frac{1}{2} \left( v_{avg} - a t \right)"
    elif set(using.strip().split(",")) == {"vf", "a", "t"}:
        vi = 0.5 * (v_avg - a * t)
        formula = r"v_{i} &= v_{f} - a t"
    elif set(using.strip().split(",")) == {"vi", "a", "Dx"}:
        vi = (vf**2 - 2 * a * Dx) ** 0.5
        if (a > 0 and vf < vi) or (a < 0 and vf > vi): 
            vi = -vi
        formula = r"v_{i}^{2} &= v_{f}^{2} - 2 a \Delta x"
    return dict(value=vi, formula=formula)

def eval_final_velocity(vi: float=None, vf: float=None, a: float=None, Dx: float=None, v_avg: float=None, using: str="v_avg,a,t"):
    formula = ""
    vf = None
    if set(using.strip().split(",")) == {"v_avg", "a", "t"}:
        vf = 0.5 * (v_avg + a * t)
        formula = r"v_{f} &= \frac{1}{2} \left( v_{avg} + a t \right)"
    elif set(using.strip().split(",")) == {"vi", "a", "t"}:
        vf = 0.5 * (v_avg + a * t)
        formula = r"v_{f} &= v_{i} + a t"
    elif set(using.strip().split(",")) == {"vi", "a", "Dx"}:
        vf = (vi**2 + 2 * a * Dx) ** 0.5
        if (a > 0 and vf < vi) or (a < 0 and vf > vi): 
            vf = -vf
        formula = r"v_{f}^{2} &= v_{i}^{2} + 2 a \Delta x"
    return dict(value=vf, formula=formula)

def eval_time(vi: float=None, vf: float=None, a: float=None, Dx: float=None, v_avg: float=None, using: str="vi,vf,a"):
    formula = ""
    t = None
    if set(using.strip().split(",")) == {"vi", "vf", "a"}:
        t = (vf - vi) / a
        formula = r"t &= \frac{\left( v_{f} - v_{i} \right)}{a}"
    elif set(using.strip().split(",")) == {"Dx", "v_avg"}:
        t = Dx / v_avg
        formula = r"t &= \frac{\Delta x}{v_{avg}}"
    return dict(value=t, formula=formula)

def known_vi_vf_t(vi: float, vf: float, t: float, ndigits: int=5):
    """Returns displacement (Dx), acceleration (a) and average-velocity (v_avg).
    
    Parameters:
        vi: initial velocity (units: m/s)
        vf: final veocity (units: m/s)
        t: time (units: seconds)

    Usage:

        result, steps = known_vi_vf_t(vi=205, vf=315, t=1.75)

    """
    ## Steps:
    # v_avg = 0.5 * (vi + vf)
    # Dx = v_avg * t
    # a = (vf - vi) / t
    results = dict()
    steps = []

    # v_avg = 0.5 * (vi + vf)
    results["v_avg"] = eval_average_velocity(vi=vi, vf=vf, using="vi,vf")
    v_avg = results.get("v_avg",{}).get("value")
    steps.append(results.get("v_avg",{}).get("formula"))

    # Dx = v_avg * t
    results["Dx"] = eval_displacement(v_avg=v_avg, t=t)
    Dx = results.get("Dx",{}).get("value")
    steps.append(results.get("Dx",{}).get("formula"))
    
    # a = (vf - vi) / t
    results["a"] = eval_acceleration(vi=vi, vf=vf, t=t)
    a = results.get("a",{}).get("value")
    steps.append(results.get("a",{}).get("formula"))

    result = dict(Dx=Dx, a=a, v_avg=v_avg, vi=vi, vf=vf, t=t)
    return prepare_result(ndigits=ndigits, **result), steps

def known_vi_vf_a(vi: float, vf: float, a: float, ndigits: int=5, reuse: bool=False):
    """Returns displacement (Dx), time (t) and average-velocity (v_avg).
    
    Parameters:
        vi: initial velocity (units: m/s)
        vf: final veocity (units: m/s)
        a: acceleration (units: m/s^2)

    Usage:

        result, steps = known_vi_vf_a(vi=205.0, vf=315.0, a=11.0)

    """
    results = dict()
    steps = []

    # t = (vf - vi) / a    
    results["t"] = eval_time(vi=vi, vf=vf, a=a, using="vi,vf,a")
    t = results.get("t",{}).get("value")
    steps.append(results.get("t",{}).get("formula"))

    if not reuse:
        # v_avg = 0.5 * (vi + vf)
        results["v_avg"] = eval_average_velocity(vi=vi, vf=vf, using="vi,vf")
        v_avg = results.get("v_avg",{}).get("value")
        steps.append(results.get("v_avg",{}).get("formula"))
        
        # Dx = v_avg * t
        results["Dx"] = eval_displacement(v_avg=v_avg, t=t)
        Dx = results.get("Dx",{}).get("value")
        steps.append(results.get("Dx",{}).get("formula"))

        result = dict(Dx=Dx, a=a, v_avg=v_avg, vi=vi, vf=vf, t=t)
        return prepare_result(ndigits=ndigits, **result), steps
    else:
        return known_vi_vf_t(vi=vi, vf=vf, t=t), steps

def known_vi_vf_Dx(vi: float, vf: float, Dx: float, ndigits: int=5):
    """Returns time (t), acceleration (a) and average-velocity (v_avg).
    
    Parameters:
        vi: initial velocity (units: m/s)
        vf: final veocity (units: m/s)
        Dx: displacement (units: m)

    Usage:

        result, steps = known_vi_vf_Dx(vi=205, vf=315, Dx=455)

    """
    results = dict()
    steps = []

    # v_avg = 0.5 * (vi + vf)
    results["v_avg"] = eval_average_velocity(vi=vi, vf=vf, using="vi,vf")
    v_avg = results.get("v_avg",{}).get("value")
    steps.append(results.get("v_avg",{}).get("formula"))

    # t = Dx / v_avg
    results["t"] = eval_time(Dx=Dx, v_avg=v_avg, using="Dx,v_avg")
    t = results.get("t",{}).get("value")
    steps.append(results.get("t",{}).get("formula"))

    # a = (vf - vi) / t
    results["a"] = eval_acceleration(vi=vi, vf=vf, t=t)
    a = results.get("a",{}).get("value")
    steps.append(results.get("a",{}).get("formula"))

    result = dict(Dx=Dx, a=a, v_avg=v_avg, vi=vi, vf=vf, t=t)
    return prepare_result(ndigits=ndigits, **result), steps

def known_Dx_a_t(Dx: float, a: float, t: float, ndigits: int=5):
    """Returns final-velocity (vf), initial-velocity (vi) and average-velocity (v_avg).
    
    Parameters:
        Dx: displacement (units: m)
        a: acceleration (units: m/s^2)
        t: time (units: seconds)

    Usage:

        result = known_Dx_a_t(Dx=225, a=-1.8, t=12.75)

    """
    results = dict()
    steps = []

    # v_avg = 2 * Dx / t
    results["v_avg"] = eval_average_velocity(Dx=Dx, t=t, using="Dx,t")
    v_avg = results.get("v_avg",{}).get("value")
    steps.append(results.get("v_avg",{}).get("formula"))

    # vf = 0.5 * (v_avg + a*t)
    results["vf"] = eval_final_velocity(v_avg=v_avg, a=a, t=t, using="v_avg,a,t")
    vf = results.get("vf",{}).get("value")
    steps.append(results.get("vf",{}).get("formula"))

    # vi = 0.5 * (v_avg - a*t)
    results["vi"] = eval_initial_velocity(v_avg=v_avg, a=a, t=t, using="v_avg,a,t")
    vi = results.get("vi",{}).get("value")
    steps.append(results.get("vi",{}).get("formula"))

    result = dict(Dx=Dx, a=a, v_avg=v_avg, vi=vi, vf=vf, t=t)
    return prepare_result(ndigits=ndigits, **result), steps

def known_vi_a_t(vi: float, a: float, t: float, ndigits: int=5, reuse: bool=False):
    """Returns displacement (Dx), final-velocity (vf) and average-velocity (v_avg).
    
    Parameters:
        vi: initial velocity (units: m/s)
        a: acceleration (units: m/s^2)
        t: time (units: seconds)

    Usage:

        result = known_vi_a_t(vi=205, a=1.75, t=10.0)

    """
    results = dict()
    steps = []

    # vf = vi + a * t
    results["vf"] = eval_final_velocity(vi=vi, a=a, t=t, using="vi,a,t")
    vf = results.get("vf",{}).get("value")
    steps.append(results.get("vf",{}).get("formula"))
    if not reuse:
        # v_avg = 0.5 * (vi + vf)
        results["v_avg"] = eval_average_velocity(vi=vi, vf=vf, using="vi,vf")
        v_avg = results.get("v_avg",{}).get("value")
        steps.append(results.get("v_avg",{}).get("formula"))

        # Dx = v_avg * t
        results["Dx"] = eval_displacement(v_avg=v_avg, t=t)
        Dx = results.get("Dx",{}).get("value")
        steps.append(results.get("Dx",{}).get("formula"))

        result = dict(Dx=Dx, a=a, v_avg=v_avg, vi=vi, vf=vf, t=t)
        return prepare_result(ndigits=ndigits, **result), steps
    else:
        return known_vi_vf_a(vi=vi, vf=vf, a=a, ndigits=ndigits), steps

def known_vf_a_t(vf: float, a: float, t: float, ndigits: int=5, reuse: bool=False):
    """Returns displacement (Dx), initial-velocity (vi) and average-velocity (v_avg).
    
    Parameters:
        vf: final velocity (units: m/s)
        a: acceleration (units: m/s^2)
        t: time (units: seconds)

    Usage:

        result = known_vi_a_t(vi=205, a=1.75, t=10.0)

    """
    results = dict()
    steps = []

    # vi = vf - a * t
    results["vi"] = eval_initial_velocity(vf=vf, a=a, t=t, using="vf,a,t")
    vi = results.get("vi",{}).get("value")
    steps.append(results.get("vi",{}).get("formula"))
    if not reuse:
        # v_avg = 0.5 * (vi + vf)
        results["v_avg"] = eval_average_velocity(vi=vi, vf=vf, using="vi,vf")
        v_avg = results.get("v_avg",{}).get("value")
        steps.append(results.get("v_avg",{}).get("formula"))

        # Dx = v_avg * t
        results["Dx"] = eval_displacement(v_avg=v_avg, t=t)
        Dx = results.get("Dx",{}).get("value")
        steps.append(results.get("Dx",{}).get("formula"))

        result = dict(Dx=Dx, a=a, v_avg=v_avg, vi=vi, vf=vf, t=t)
        return prepare_result(ndigits=ndigits, **result), steps
    else:
        return known_vi_vf_a(vi=vi, vf=vf, a=a, ndigits=ndigits), steps

def known_vi_a_Dx(vi: float, a: float, Dx: float, ndigits: int=5, reuse: bool=False):
    """Returns time (t), final-velocity (vf) and average-velocity (v_avg).
    
    Parameters:
        vi: initial velocity (units: m/s)
        a: acceleration (units: m/s^2)
        Dx: displacement (units: m)

    Usage:

        result = known_vi_a_Dx(vi=205.0, a=1.75, Dx=455.0)

    """
    results = dict()
    steps = []

    # vf = (vi**2 + 2 * a * Dx) ** 0.5
    # if (a > 0 and vf < vi) or (a < 0 and vf > vi): 
    #     vf = -vf
    results["vf"] = eval_final_velocity(vi=vi, a=a, Dx=Dx, using="vi,a,Dx")
    vf = results.get("vf",{}).get("value")
    steps.append(results.get("vf",{}).get("formula"))
    if not reuse:
        # v_avg = 0.5 * (vi + vf)
        results["v_avg"] = eval_average_velocity(vi=vi, vf=vf, using="vi,vf")
        v_avg = results.get("v_avg",{}).get("value")
        steps.append(results.get("v_avg",{}).get("formula"))

        # t = Dx / v_avg
        results["t"] = eval_time(Dx=Dx, v_avg=v_avg, using="Dx,v_avg")
        t = results.get("t",{}).get("value")
        steps.append(results.get("t",{}).get("formula"))

        result = dict(Dx=Dx, a=a, v_avg=v_avg, vi=vi, vf=vf, t=t)
        return prepare_result(ndigits=ndigits, **result), steps
    else:
        return known_vi_vf_Dx(vi=vi, vf=vf, Dx=Dx, ndigits=ndigits), steps

def known_vf_a_Dx(vf: float, a: float, Dx: float, ndigits: int=5, reuse: bool=False):
    """Returns time (t), initial-velocity (vi) and average-velocity (v_avg).
    
    Parameters:
        vf: final velocity (units: m/s)
        a: acceleration (units: m/s^2)
        Dx: displacement (units: m)

    Usage:

        result = known_vi_a_Dx(vf=315.0, a=1.75, Dx=455.0)

    """
    results = dict()
    steps = []

    # vi = (vf**2 - 2 * a * Dx) ** 0.5
    # if (a > 0 and vf < vi) or (a < 0 and vf > vi): 
    #     vi = -vi
    results["vi"] = eval_initial_velocity(vf=vf, a=a, Dx=Dx, using="vf,a,Dx")
    vi = results.get("vi",{}).get("value")
    steps.append(results.get("vi",{}).get("formula"))
    if not reuse:
        # v_avg = 0.5 * (vi + vf)
        results["v_avg"] = eval_average_velocity(vi=vi, vf=vf, using="vi,vf")
        v_avg = results.get("v_avg",{}).get("value")
        steps.append(results.get("v_avg",{}).get("formula"))

        # t = Dx / v_avg
        results["t"] = eval_time(Dx=Dx, v_avg=v_avg, using="Dx,v_avg")
        t = results.get("t",{}).get("value")
        steps.append(results.get("t",{}).get("formula"))

        result = dict(Dx=Dx, a=a, v_avg=v_avg, vi=vi, vf=vf, t=t)
        return prepare_result(ndigits=ndigits, **result), steps
    else:
        return known_vi_vf_Dx(vi=vi, vf=vf, Dx=Dx, ndigits=ndigits), steps

def calculate1D(vi:float=None, vf:float=None, v_avg:float=None, a:float=None, Dx:float=None, t:float=None, ndigits: bool=5):
    params = dict(Dx=Dx, a=a, v_avg=v_avg, vi=vi, vf=vf, t=t)
    params = dict((k, v) for k, v in params.items() if v is not None)
    if len(params.keys()) < 3:
        raise ValueError("At least three appropriate parameters is necessary)")
    if {'vi', 'vf', 't'} - set(params.keys()) == set():
        return known_vi_vf_t(vi=vi, vf=vf, t=t, ndigits=ndigits)
    elif {'vi', 'vf', 'a'} - set(params.keys()) == set():
        return known_vi_vf_a(vi=vi, vf=vf, a=a, ndigits=ndigits)
    elif {'vi', 'vf', 'Dx'} - set(params.keys()) == set():
        return known_vi_vf_Dx(vi=vi, vf=vf, Dx=Dx, ndigits=ndigits)
    elif {'Dx', 'a', 't'} - set(params.keys()) == set():
        return known_Dx_a_t(Dx=Dx, a=a, t=t, ndigits=ndigits)
    elif {'vi', 'a', 't'} - set(params.keys()) == set():
        return known_vi_a_t(vi=vi, a=a, t=t, ndigits=ndigits)
    elif {'vf', 'a', 't'} - set(params.keys()) == set():
        return known_vf_a_t(vf=vf, a=a, t=t, ndigits=ndigits)
    elif {'vi', 'a', 'Dx'} - set(params.keys()) == set():
        return known_vi_a_Dx(vi=vi, a=a, Dx=Dx, ndigits=ndigits)
    elif {'vf', 'a', 'Dx'} - set(params.keys()) == set():
        return known_vf_a_Dx(vf=vf, a=a, Dx=Dx, ndigits=ndigits)
    else:
        raise NotImplementedError()

from textwrap import dedent
from IPython.display import display, Markdown, Latex
from typing import Dict

def show_steps(steps, as_markdown: bool=False, as_latex: bool=False, debug: bool=False):
    # from textwrap import dedent
    # from IPython.display import display, Markdown, Latex
    s = r' \\' + '\n    '
    tex = \
    r"""
    \begin(|equation|)
    \begin(|aligned|)
        {content}
    \end(|aligned|)
    \end(|equation|)
    """
    payload = dedent(tex).format(content=s.join(steps) + r" \\").replace("(|", "{").replace("|)", "}")
    if debug:
        print(payload)
    if as_markdown:
        display(Markdown(data=payload))
    if as_latex:
        display(Latex(data=payload))
    return payload

class Kinematics1D(object):
    """Kinematics1D class to calculate `Dx`, `a`, `v_avg`, `vi`, `vf`, `t` for 1D motion.

    Usage:

        ```python
        k1 = Kinematics1D(vi=205, vf=315, t=10.0)
        result, steps = k1.solve(steps_params=dict(debug=True))
        ```
    """
    params = dict((k, None) for k in ['Dx', 'a', 'v_avg', 'vi', 'vf', 't'])
    ndigits: int = 5

    def __init__(self, vi:float=None, vf:float=None, v_avg:float=None, a:float=None, Dx:float=None, t:float=None, ndigits: bool=5):
        self.params = dict(Dx=Dx, a=a, v_avg=v_avg, vi=vi, vf=vf, t=t)
        self.ndigits = ndigits
    
    def solve(self, showsteps: bool=True, steps_params: Dict[str, bool]=None, **kwargs):
        if kwargs:
            result, steps = calculate1D(ndigits=self.ndigits, **kwargs)
            if showsteps:
                show_steps(steps, **steps_params)
            return result, steps
        else:
            result, steps = calculate1D(ndigits=self.ndigits, **self.params)
            if showsteps:
                show_steps(steps, **steps_params)
            return result, steps