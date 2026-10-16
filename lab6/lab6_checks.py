"""
Answer checks for ENGR 10200 Lab 6.

In the notebook, run   check("q1_1")   after answering a question,
or   check_all()   at the end to see every question at once.
"""
import numpy as np
import pandas as pd


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
class _NotAnswered(Exception):
    pass


def _namespace():
    """The notebook's variables (works in Jupyter, Colab, and plain Python)."""
    try:
        return get_ipython().user_ns  # noqa: F821 (defined inside IPython)
    except NameError:
        import __main__
        return vars(__main__)


def _get(name):
    ns = _namespace()
    if name not in ns or ns[name] is Ellipsis:
        raise _NotAnswered(name)
    return ns[name]


def _close(a, b, tol):
    return abs(float(a) - float(b)) <= tol


# Each question is a list of (hint shown on failure, function returning True/False).
# Functions receive `g`, which looks up a variable from the notebook by name.
CHECKS = {}


def _q(name, *cases):
    CHECKS[name] = list(cases)


# ----------------------------------------------------------------------------
# Part 1: resistor quality control
# ----------------------------------------------------------------------------
_q("q1_1",
   ("`resistors` should be an array of 10,000 values",
    lambda g: len(g("resistors")) == 10000),
   ("Call np.random.seed(2026) right before np.random.normal(100, 2, 10000)",
    lambda g: np.allclose(g("resistors"), np.random.RandomState(2026).normal(100, 2, 10000))),
   ("`mean_R` should be the mean of `resistors`",
    lambda g: _close(g("mean_R"), np.mean(g("resistors")), 1e-9)),
   ("`median_R` should be the median of `resistors`",
    lambda g: _close(g("median_R"), np.median(g("resistors")), 1e-9)),
   ("`sd_R` should be the standard deviation of `resistors` (use np.std)",
    lambda g: _close(g("sd_R"), np.std(g("resistors")), 1e-9)),
   )

_q("q1_2",
   ("in_spec(np.array([95, 96, 100, 104, 105])) should give [False, True, True, True, False]. "
    "Are your limits inclusive (>= and <=)?",
    lambda g: list(g("in_spec")(np.array([95, 96, 100, 104, 105]))) == [False, True, True, True, False]),
   ("in_spec should use the `low` and `high` arguments, not fixed numbers",
    lambda g: list(g("in_spec")(np.array([1, 2, 3, 4, 5]), 2, 4)) == [False, True, True, True, False]),
   ("`frac_in_spec` should be the fraction (0 to 1) of `resistors` that are in spec",
    lambda g: _close(g("frac_in_spec"), np.mean((g("resistors") >= 96) & (g("resistors") <= 104)), 1e-9)),
   ("96 and 104 are each 2 standard deviations from the mean. What fraction does the rule predict?",
    lambda g: _close(g("rule_estimate"), 0.95, 0.006)),
   )

_q("q1_3",
   ("`R_bins` should start at 90",
    lambda g: _close(g("R_bins")[0], 90, 1e-9)),
   ("`R_bins` should end at 110. np.arange does not include its stop value.",
    lambda g: _close(g("R_bins")[-1], 110, 1e-9)),
   ("`R_bins` should step by 0.5",
    lambda g: np.allclose(np.diff(g("R_bins")), 0.5)),
   )

_q("q1_4",
   ("r1, r2, and r3 should each have 5000 values",
    lambda g: len(g("r1")) == len(g("r2")) == len(g("r3")) == 5000),
   ("r1, r2, and r3 should be drawn from `resistors` with np.random.choice",
    lambda g: all(np.isin(g(r), g("resistors")).all() for r in ["r1", "r2", "r3"])),
   ("`total` should be r1 + r2 + r3",
    lambda g: np.allclose(g("total"), g("r1") + g("r2") + g("r3"))),
   ("`all_in` should be True only where r1, r2, AND r3 are all in spec (combine in_spec results with &)",
    lambda g: np.array_equal(g("all_in"), g("in_spec")(g("r1")) & g("in_spec")(g("r2")) & g("in_spec")(g("r3")))),
   ("`p_all_in_sim` should be the fraction of circuits where `all_in` is True",
    lambda g: _close(g("p_all_in_sim"), np.mean(g("all_in")), 1e-9)),
   ("`p_all_in_rule` should use the multiplication rule with frac_in_spec",
    lambda g: _close(g("p_all_in_rule"), g("frac_in_spec") ** 3, 1e-9)),
   ("Your simulation and the multiplication rule should agree closely",
    lambda g: _close(g("p_all_in_sim"), g("p_all_in_rule"), 0.02)),
   )

_q("q1_5",
   ("`circuit_ok` should be in_spec(total, 297, 303)",
    lambda g: np.array_equal(g("circuit_ok"), (g("total") >= 297) & (g("total") <= 303))),
   ("`p_circuit_ok` should be the fraction of circuits that are OK",
    lambda g: _close(g("p_circuit_ok"), np.mean(g("circuit_ok")), 1e-9)),
   ("`p_ok_given_all_in` should be P(circuit OK and all in spec) / P(all in spec)",
    lambda g: _close(g("p_ok_given_all_in"),
                     np.mean(g("circuit_ok") & g("all_in")) / np.mean(g("all_in")), 1e-9)),
   ("Are there circuits where every resistor passed but the circuit still failed?",
    lambda g: g("qc_guarantees_circuit") is False),
   )

# ----------------------------------------------------------------------------
# Part 2: flight delays
# ----------------------------------------------------------------------------
_q("q2_1",
   ("`united` should have 13825 rows and 4 columns",
    lambda g: g("united").shape == (13825, 4)),
   ("`pop_mean` should be the mean of the Delay column",
    lambda g: _close(g("pop_mean"), 16.658155515370705, 1e-6)),
   ("`pop_median` should be the median of the Delay column",
    lambda g: _close(g("pop_median"), 2.0, 1e-9)),
   ("`pop_sd` should use np.std on the Delay column (pandas .std() divides by N-1, not N)",
    lambda g: _close(g("pop_sd"), 39.480199851609314, 1e-6)),
   ("`pct_late_60` should be a PERCENT of flights delayed more than 60 minutes",
    lambda g: _close(g("pct_late_60"), 8.889692585895117, 1e-6)),
   )

_q("q2_2",
   ("`deterministic` should take every 100th row starting at row 0",
    lambda g: list(g("deterministic").index) == list(range(0, 13825, 100))),
   ("`systematic` should start at a random row from 0 to 99 and take every 100th row",
    lambda g: 0 <= g("systematic").index[0] <= 99
    and np.all(np.diff(g("systematic").index) == 100)
    and g("systematic").index[-1] + 100 >= 13825),
   ("`srs` should be a random sample of 139 different flights (no replacement)",
    lambda g: len(g("srs")) == 139 and g("srs").index.is_unique),
   ("`comparison` should have 4 rows and the columns 'method' and 'mean_delay'",
    lambda g: g("comparison").shape == (4, 2) and list(g("comparison").columns) == ["method", "mean_delay"]),
   ("The mean_delay values should be, in order: deterministic, systematic, srs, population",
    lambda g: np.allclose(g("comparison")["mean_delay"],
                          [g("deterministic")["Delay"].mean(), g("systematic")["Delay"].mean(),
                           g("srs")["Delay"].mean(), g("pop_mean")])),
   ("Which method picks exactly the same rows every time you run the cell?",
    lambda g: g("never_changes") == "deterministic"),
   )

_q("q2_3",
   ("sample_mean_delay(n) should return a single number",
    lambda g: isinstance(g("sample_mean_delay")(50), (int, float, np.number))),
   ("Sampling ALL 13825 flights without replacement should give exactly pop_mean",
    lambda g: _close(g("sample_mean_delay")(13825), g("pop_mean"), 1e-9)),
   ("`lln_means` should have one sample mean for each size in `sizes`",
    lambda g: len(g("lln_means")) == len(g("sizes")) == 300),
   ("The biggest samples should have means close to pop_mean",
    lambda g: np.all(np.abs(np.asarray(g("lln_means"))[-20:] - g("pop_mean")) < 3)),
   )

_q("q2_4",
   ("`means_100` should hold 1000 sample means, each from a sample of 100 flights",
    lambda g: len(g("means_100")) == 1000 and np.std(g("means_100")) < 8),
   ("`mean_of_means` should be the mean of means_100. It should be close to pop_mean.",
    lambda g: _close(g("mean_of_means"), np.mean(g("means_100")), 1e-9) and _close(g("mean_of_means"), g("pop_mean"), 1)),
   ("`sd_of_means` should be the standard deviation of means_100 (use np.std)",
    lambda g: _close(g("sd_of_means"), np.std(g("means_100")), 1e-9)),
   ("`frac_within_2sd` should use in_spec with limits mean_of_means ± 2*sd_of_means",
    lambda g: _close(g("frac_within_2sd"),
                     np.mean(g("in_spec")(g("means_100"), g("mean_of_means") - 2 * g("sd_of_means"),
                                          g("mean_of_means") + 2 * g("sd_of_means"))), 1e-9)),
   ("About 95% of the sample means should be within 2 SD, as the 68-95-99.7 rule predicts",
    lambda g: 0.92 <= g("frac_within_2sd") <= 0.985),
   )

# ----------------------------------------------------------------------------
# Part 3: Monty Hall with more doors
# ----------------------------------------------------------------------------
def _rate(g, n, switch, trials=3000):
    f = g("monty_hall_n")
    return np.mean([bool(f(n, switch)) for _ in range(trials)])


_q("q3_1",
   ("monty_hall_n should return True or False",
    lambda g: isinstance(g("monty_hall_n")(3, True), (bool, np.bool_))),
   ("With 3 doors, staying should win about 1/3 of the time",
    lambda g: _close(_rate(g, 3, False), 1 / 3, 0.04)),
   ("With 3 doors, switching should win about 2/3 of the time",
    lambda g: _close(_rate(g, 3, True), 2 / 3, 0.04)),
   ("With 4 doors, staying should win about 1/4 of the time",
    lambda g: _close(_rate(g, 4, False), 1 / 4, 0.04)),
   ("With 4 doors, switching should win about 3/8. Monty opens ONE goat door, and you switch "
    "to a random door that is neither your pick nor the opened one.",
    lambda g: _close(_rate(g, 4, True), 3 / 8, 0.04)),
   )

_q("q3_2",
   ("`monty_table` should have columns 'doors', 'stay', 'switch' and one row per door count",
    lambda g: list(g("monty_table").columns) == ["doors", "stay", "switch"] and list(g("monty_table")["doors"]) == [3, 4, 5, 10]),
   ("The 'stay' column should be close to 1/doors",
    lambda g: np.allclose(g("monty_table")["stay"], 1 / np.array([3, 4, 5, 10]), atol=0.03)),
   ("The 'switch' column should be close to (n-1) / (n(n-2))",
    lambda g: np.allclose(g("monty_table")["switch"],
                          [(n - 1) / (n * (n - 2)) for n in [3, 4, 5, 10]], atol=0.03)),
   ("Compare the columns. Is switching better for every number of doors?",
    lambda g: g("always_switch") is True),
   )


# ----------------------------------------------------------------------------
# public functions
# ----------------------------------------------------------------------------
def _run(name):
    passed, messages = 0, []
    for hint, fn in CHECKS[name]:
        try:
            ok = bool(fn(_get))
        except _NotAnswered as e:
            messages.append(f"`{e}` isn't defined yet (or is still ...). Run your answer cell first.")
            break
        except Exception as e:
            ok = False
            hint = f"{hint}   [{type(e).__name__}: {e}]"
            if "NoneType" in str(e):
                hint += "  (Did your function forget to `return` its answer?)"
        if ok:
            passed += 1
        else:
            messages.append(hint)
    return passed, messages


def check(name):
    """Check one question, e.g. check("q1_1")."""
    if name not in CHECKS:
        print(f"There is no question called {name!r}.")
        return
    passed, messages = _run(name)
    total = len(CHECKS[name])
    if not messages:
        print(f"✅ {name}: all {total} checks passed!")
    else:
        print(f"❌ {name}: {passed} of {total} checks passed. Hint:")
        print("   -", messages[0])


def check_all():
    """Check every question in the lab."""
    done = 0
    for name in CHECKS:
        passed, messages = _run(name)
        mark = "✅" if not messages else "❌"
        done += not messages
        print(f"{mark} {name}  ({passed}/{len(CHECKS[name])})")
    print(f"\n{done} of {len(CHECKS)} questions fully passing.")
