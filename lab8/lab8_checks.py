"""
Answer checks for ENGR 10200 Lab 8.

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


def _rel(a, b, frac):
    return abs(float(a) - float(b)) <= frac * abs(float(b))


CHECKS = {}


def _q(name, *cases):
    CHECKS[name] = list(cases)


# Reference values from the data files
_WAIT_MEAN, _WAIT_MEDIAN, _WAIT_SD = 70.8970588235294, 76.0, 13.569960017586371
_PRICE_MEAN, _PRICE_SD, _PRICE_MEDIAN = 3932.799721913237, 3989.4027576288736, 2401.0


# ----------------------------------------------------------------------------
# Part 1: Old Faithful, spread and Chebyshev
# ----------------------------------------------------------------------------
_q("q1_1",
   ("`geyser` should have 272 rows and 3 columns",
    lambda g: g("geyser").shape == (272, 3)),
   ("`waiting` should be the waiting column of `geyser`",
    lambda g: len(g("waiting")) == 272 and _close(np.sum(g("waiting")), 19284, 1e-6)),
   ("`mean_wait` should be the mean of `waiting`",
    lambda g: _close(g("mean_wait"), _WAIT_MEAN, 1e-6)),
   ("`median_wait` should be the median of `waiting`",
    lambda g: _close(g("median_wait"), _WAIT_MEDIAN, 1e-9)),
   ("`sd_wait` should use np.std (pandas .std() divides by N-1, not N)",
    lambda g: _close(g("sd_wait"), _WAIT_SD, 1e-6)),
   ("Which is larger for this data, the mean or the median?",
    lambda g: g("median_above_mean") is True),
   )

_q("q1_2",
   ("`z_90` should be (90 - mean_wait) / sd_wait",
    lambda g: _close(g("z_90"), (90 - _WAIT_MEAN) / _WAIT_SD, 1e-6)),
   ("`z` should be every waiting time converted to standard units",
    lambda g: np.allclose(g("z"), (np.asarray(g("waiting")) - _WAIT_MEAN) / _WAIT_SD)),
   ("`within` should hold the fraction of eruptions within 1, 2 and 3 SDs, in that order",
    lambda g: np.allclose(g("within"), [np.mean(np.abs(g("z")) < k) for k in (1, 2, 3)])),
   ("`chebyshev` should hold 1 - 1/k**2 for k = 1, 2, 3",
    lambda g: np.allclose(g("chebyshev"), [0, 0.75, 1 - 1 / 9])),
   ("`chebyshev_holds` should be True if every value in `within` is at least its Chebyshev bound",
    lambda g: g("chebyshev_holds") is True or g("chebyshev_holds") is np.True_),
   ("Compare within[0] with the 68% the normal rule predicts for 1 SD. Is it lower?",
    lambda g: g("below_normal_at_1sd") is True),
   )

# ----------------------------------------------------------------------------
# Part 2: diamond prices, sigma / sqrt(n) and sample size
# ----------------------------------------------------------------------------
_q("q2_1",
   ("`price` should hold all 53,940 diamond prices",
    lambda g: len(g("price")) == 53940),
   ("`mu` should be the mean price",
    lambda g: _close(g("mu"), _PRICE_MEAN, 1e-6)),
   ("`sigma` should be the population SD of price (np.std)",
    lambda g: _close(g("sigma"), _PRICE_SD, 1e-6)),
   ("`pop_median` should be the median price",
    lambda g: _close(g("pop_median"), _PRICE_MEDIAN, 1e-9)),
   )

_q("q2_2",
   ("`means_100` should hold 2000 sample means of 100 diamonds each",
    lambda g: len(g("means_100")) == 2000 and _rel(np.mean(g("means_100")), _PRICE_MEAN, 0.03)),
   ("`means_400` should hold 2000 sample means of 400 diamonds each",
    lambda g: len(g("means_400")) == 2000 and _rel(np.mean(g("means_400")), _PRICE_MEAN, 0.02)),
   ("`sd_means_100` and `sd_means_400` should be the SDs (np.std) of those arrays",
    lambda g: _close(g("sd_means_100"), np.std(g("means_100")), 1e-6)
    and _close(g("sd_means_400"), np.std(g("means_400")), 1e-6)),
   ("`formula_100` and `formula_400` should be sigma / sqrt(n)",
    lambda g: _close(g("formula_100"), _PRICE_SD / 10, 1e-6) and _close(g("formula_400"), _PRICE_SD / 20, 1e-6)),
   ("The simulated SDs should be close to the formula (within about 8%)",
    lambda g: _rel(g("sd_means_100"), _PRICE_SD / 10, 0.08) and _rel(g("sd_means_400"), _PRICE_SD / 20, 0.08)),
   )

_q("q2_3",
   ("`n_clt` should be (2 * sigma / half_width)**2, rounded UP with np.ceil",
    lambda g: _close(g("n_clt"), np.ceil((2 * _PRICE_SD / 100) ** 2), 1e-9)),
   ("`k` should solve 1 - 1/k**2 = 0.95",
    lambda g: _close(g("k"), np.sqrt(20), 1e-6)),
   ("`n_cheb` should be (k * sigma / half_width)**2, rounded UP with np.ceil",
    lambda g: _close(g("n_cheb"), np.ceil((np.sqrt(20) * _PRICE_SD / 100) ** 2), 1e-6)),
   )

# ----------------------------------------------------------------------------
# Part 3: bootstrap confidence intervals
# ----------------------------------------------------------------------------
def _rs(seed):
    return np.random.RandomState(seed)


_q("q3_1",
   ("`my_sample` should be 400 prices drawn with np.random.choice(price, 400, replace=False) right after np.random.seed(2026)",
    lambda g: np.array_equal(g("my_sample"), _rs(2026).choice(g("price"), 400, replace=False))),
   ("bootstrap_median(sample, reps) should return an array with `reps` medians",
    lambda g: len(g("bootstrap_median")(np.arange(10), 50)) == 50),
   ("Each bootstrap median should come from a resample of the sample, WITH replacement",
    lambda g: set(np.round(g("bootstrap_median")(np.array([1, 2, 3, 4, 5]), 300), 6)) <= {1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5}
    and np.std(g("bootstrap_median")(np.array([1, 2, 3, 4, 5]), 300)) > 0),
   ("`boot_medians` should hold 5000 bootstrap medians of `my_sample`",
    lambda g: len(g("boot_medians")) == 5000),
   ("`ci_low` and `ci_high` should be the 2.5th and 97.5th percentiles of `boot_medians`",
    lambda g: np.allclose([g("ci_low"), g("ci_high")], np.percentile(g("boot_medians"), [2.5, 97.5]))),
   ("`caught` should be True if pop_median is between ci_low and ci_high",
    lambda g: bool(g("caught")) == (g("ci_low") <= _PRICE_MEDIAN <= g("ci_high"))),
   )

_q("q3_2",
   ("`tips` should have 244 rows, and `tips['tip_pct']` should be 100 * tip / total_bill",
    lambda g: len(g("tips")) == 244 and np.allclose(g("tips")["tip_pct"], 100 * g("tips")["tip"] / g("tips")["total_bill"])),
   ("`smoker_pct` and `nonsmoker_pct` should be the tip_pct values for smoker == 'Yes' and 'No'",
    lambda g: len(g("smoker_pct")) == 93 and len(g("nonsmoker_pct")) == 151),
   ("boot_diff(g1, g2, reps) should return `reps` differences of means (g1 minus g2)",
    lambda g: len(g("boot_diff")(np.array([5.0, 5.0]), np.array([2.0, 2.0]), 20)) == 20
    and np.allclose(g("boot_diff")(np.array([5.0, 5.0]), np.array([2.0, 2.0]), 20), 3)),
   ("`tips_ci` should be the 2.5th and 97.5th percentiles of `tips_diffs`",
    lambda g: np.allclose(g("tips_ci"), np.percentile(g("tips_diffs"), [2.5, 97.5]))),
   ("`tips_diffs` should hold 10000 differences, smokers minus non-smokers",
    lambda g: len(g("tips_diffs")) == 10000 and _close(np.mean(g("tips_diffs")), 0.387, 0.3)),
   ("Does the interval include 0? Then do we reject H0?",
    lambda g: g("tips_reject") is (not (g("tips_ci")[0] <= 0 <= g("tips_ci")[1]))),
   )

_q("q3_3",
   ("`long_wait` and `short_wait` should be the waiting times after long and short eruptions",
    lambda g: len(g("long_wait")) == 172 and len(g("short_wait")) == 100),
   ("`geyser_diffs` should hold 10000 bootstrap differences, long minus short",
    lambda g: len(g("geyser_diffs")) == 10000 and _close(np.mean(g("geyser_diffs")), 26.2, 1.0)),
   ("`geyser_ci` should be the 2.5th and 97.5th percentiles of `geyser_diffs`",
    lambda g: np.allclose(g("geyser_ci"), np.percentile(g("geyser_diffs"), [2.5, 97.5]))),
   ("Does this interval include 0? Then do we reject H0?",
    lambda g: g("geyser_reject") is (not (g("geyser_ci")[0] <= 0 <= g("geyser_ci")[1]))),
   )

# ----------------------------------------------------------------------------
# Part 4: predicting the next eruption
# ----------------------------------------------------------------------------
_R = 0.9008111683218134
_SLOPE, _INTERCEPT = 10.729641395133527, 33.47439702275335

_q("q4_1",
   ("standard_units(x) should return (x - mean) / SD (np.std)",
    lambda g: np.allclose(g("standard_units")(np.array([1.0, 2.0, 3.0])), [-1.224744871, 0, 1.224744871])),
   ("`duration` should be the duration column of `geyser`",
    lambda g: len(g("duration")) == 272 and _close(np.mean(g("duration")), 3.4877830882352936, 1e-6)),
   ("`r` should be the mean of the product of duration and waiting in standard units",
    lambda g: _close(g("r"), _R, 1e-6)),
   )

_q("q4_2",
   ("`slope` should be r * SD(waiting) / SD(duration)",
    lambda g: _close(g("slope"), _SLOPE, 1e-6)),
   ("`intercept` should be mean(waiting) - slope * mean(duration)",
    lambda g: _close(g("intercept"), _INTERCEPT, 1e-6)),
   ("`fit` should be np.polyfit(duration, waiting, 1)",
    lambda g: np.allclose(g("fit"), [_SLOPE, _INTERCEPT])),
   ("`predicted_4min` should be the predicted wait after a 4-minute eruption",
    lambda g: _close(g("predicted_4min"), _INTERCEPT + 4 * _SLOPE, 1e-6)),
   )

_q("q4_3",
   ("`residuals` should be actual waiting minus predicted waiting",
    lambda g: np.allclose(g("residuals"), np.asarray(g("waiting")) - (_INTERCEPT + _SLOPE * np.asarray(g("duration"))))),
   ("`R2` should be 1 - var(residuals) / var(waiting)",
    lambda g: _close(g("R2"), _R ** 2, 1e-6)),
   ("`rmse` should be the square root of the mean of the squared residuals",
    lambda g: _close(g("rmse"), np.sqrt(np.mean(np.asarray(g("residuals")) ** 2)), 1e-6)),
   )


# ----------------------------------------------------------------------------
# running the checks
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
