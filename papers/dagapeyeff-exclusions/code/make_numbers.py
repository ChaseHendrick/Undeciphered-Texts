"""Write every number and table the manuscript prints from the frozen search results.

    python3 papers/dagapeyeff-exclusions/code/make_numbers.py          # rewrite paper/numbers.tex and tab_*.tex
    python3 papers/dagapeyeff-exclusions/code/make_numbers.py --check  # fail if they are stale

The inputs are the JSON files in engine/data/swarm_cache, each the frozen output of one probe in engine/.
Nothing here searches; it only reads and formats. No letter string from any search is read or written.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CACHE = ROOT / "engine" / "data" / "swarm_cache"
DATA = ROOT / "engine" / "data"
PAPER = Path(__file__).resolve().parents[1] / "paper"

INPUTS = (
    "corpus", "columnar", "columnar14c", "exhaustive", "exhaustive10", "double", "keywords",
    "foursquare", "pairmap", "grillec", "quick", "homophone", "additive", "direction",
)


def load(name: str) -> dict:
    data = json.loads((CACHE / f"dagapeyeff-{name}.json").read_text(encoding="utf-8"))
    if data.get("solved") is not False or data.get("claimed_plaintext") is not None:
        raise SystemExit(f"{name}: a frozen result claims a reading; refusing to print it")
    return data


def n(value: int) -> str:
    """An integer with thin thousands separators."""
    text = f"{value:,}"
    return text.replace(",", "{,}")


def d(value: float, places: int = 4) -> str:
    """A signed decimal in math mode."""
    return f"\\ensuremath{{{value:.{places}f}}}"


def p(value: float, places: int = 2) -> str:
    return f"\\ensuremath{{{value:.{places}f}}}"


def macros() -> dict[str, str]:
    out: dict[str, str] = {}
    corpus = load("corpus")
    out["corpusLetters"] = n(corpus["corpus_letters"])
    out["corpusWindows"] = n(corpus["windows"])
    out["corpusAllThree"] = n(corpus["windows_all_three"])
    out["cellsDistinct"] = str(corpus["cell_distinct"])
    out["cellsLargest"] = str(corpus["cell_largest"])
    out["cellsChi"] = p(corpus["cell_chi_square"])

    held = {name: len("".join(ch for ch in (DATA / f"{name}.txt").read_text(encoding="utf-8").upper() if "A" <= ch <= "Z"))
            for name in ("neural_train_austen", "neural_heldout_doyle", "neural_audit_wells")}
    out["heldAusten"] = n(held["neural_train_austen"])
    out["heldDoyle"] = n(held["neural_heldout_doyle"])
    out["heldWells"] = n(held["neural_audit_wells"])

    columnar = load("columnar")
    small = [row for row in columnar["rows"] if row["width"] in (1, 2, 4, 7)]
    out["subCellsLow"] = d(min(row["cells_per_letter"] for row in small))
    out["subCellsHigh"] = d(max(row["cells_per_letter"] for row in small))
    out["subPlantedLow"] = d(min(pl["true_per_letter"] for row in small for pl in row["planted"]))
    out["subRecovered"] = str(sum(row["planted_recovered"] for row in small))
    out["subPlanted"] = str(sum(len(row["planted"]) for row in small))

    c14 = load("columnar14c")
    out["widthFourteenRecovered"] = str(sum(v[0] for v in c14["planted_recovered"].values()))
    out["widthFourteenPlanted"] = str(sum(v[1] for v in c14["planted_recovered"].values()))
    out["widthFourteenWithErrors"] = str(sum(1 for pl in c14["planted"] if pl["errors"] > 0))
    out["widthFourteenErrors"] = str(max(pl["errors"] for pl in c14["planted"]))
    out["widthFourteenSteps"] = n(c14["search"]["steps"])
    out["widthFourteenRestarts"] = str(c14["search"]["restarts"])
    scores = [row["per_letter"] for row in c14["searched"].values()]
    out["widthFourteenCellsLow"] = d(min(scores))
    out["widthFourteenCellsHigh"] = d(max(scores))
    out["widthFourteenPlantedLow"] = d(c14["planted_lowest_true"])
    highs = [row["shuffles_as_high"] for row in c14["searched"].values()]
    out["widthFourteenShufflesLow"] = str(min(highs))
    out["widthFourteenShufflesHigh"] = str(max(highs))
    out["widthFourteenShuffles"] = str(len(next(iter(c14["searched"].values()))["shuffles"]))

    ex = load("exhaustive")
    out["exhaustiveCases"] = str(len(ex["rows"]))
    out["exhaustivePlantedSmallest"] = p(ex["planted_smallest_excess"], 4)
    out["exhaustiveCellsLargest"] = p(ex["cells_largest_excess"], 4)
    out["exhaustiveRegroupedLargest"] = p(ex["regrouped_largest_excess"], 4)
    ex10 = {row["family"]: row for row in load("exhaustive10")["rows"]}
    done = ex10["columnar-done"]
    out["tenDonePlantedLow"] = p(min(pl["excess"] for pl in done["planted"]), 4)
    out["tenDoneCells"] = p(done["cells"]["excess"], 4)
    out["tenDoneRegrouped"] = p(done["regrouped"]["excess"], 4)

    double = load("double")
    out["doubleCases"] = str(double["cases"])
    out["doubleBelow"] = str(double["cases_cells_below_planted"])

    kw = load("keywords")
    out["keywordCount"] = n(kw["keywords"])
    out["keywordOrders"] = n(kw["orders_scored"])
    out["keywordCells"] = p(kw["cells_best_mi"], 4)
    out["keywordNullHigh"] = p(max(kw["null_best_mi"]), 4)
    out["keywordPlants"] = str(len(kw["plants"]))
    out["keywordPlantsFirst"] = str(kw["plants_ranked_first"])
    out["keywordPlantsLow"] = p(min(pl["top_mi"] for pl in kw["plants"]), 4)

    fs = load("foursquare")
    counts = fs["counts"]
    low, high = sorted(counts["texts"]["cells"]["pairs-from-first"])
    out["fsCellsLow"] = str(low)
    out["fsCellsHigh"] = str(high)
    out["fsRegroupedA"], out["fsRegroupedB"] = (str(x) for x in counts["texts"]["regrouped"]["pairs-from-first"])
    out["fsStandardWindows"] = n(counts["standard_windows"])
    out["fsStandardFewest"] = str(counts["standard_fewest_larger_side"])
    out["fsKeyedDraws"] = n(counts["keyed_draws"])
    out["fsKeyedFewest"] = str(counts["keyed_fewest_larger_side"])
    out["fsKeyedReaching"] = str(counts["keyed_reaching_cells"])
    out["fsRecovered"] = str(fs["planted_recovered"])
    out["fsPlanted"] = str(len(fs["planted"]))
    out["fsPlantedLow"] = d(fs["planted_lowest_true"])
    out["fsSteps"] = n(fs["search"]["steps"])
    out["fsRestarts"] = str(fs["search"]["restarts"])
    rows = fs["searched"]
    out["fsCellsBest"] = d(max(r["per_letter"] for k, r in rows.items() if k.startswith("cells")))
    out["fsRegroupedBest"] = d(max(r["per_letter"] for k, r in rows.items() if k.startswith("regrouped")))
    out["fsShufflesMin"] = str(min(r["shuffles_as_high"] for r in rows.values()))
    out["fsShuffles"] = str(len(next(iter(rows.values()))["shuffles"]))

    pm = load("pairmap")
    t = pm["texts"]
    out["pairCellsA"] = str(t["cells"]["phase 0"]["different_pairs"])
    out["pairCellsB"] = str(t["cells"]["phase 1"]["different_pairs"])
    out["pairCellsAMany"] = n(t["cells"]["phase 0"]["windows_as_many"])
    out["pairCellsBMany"] = n(t["cells"]["phase 1"]["windows_as_many"])
    out["pairRegrouped"] = str(t["regrouped"]["phase 0"]["different_pairs"])
    out["pairRegroupedAMany"] = n(t["regrouped"]["phase 0"]["windows_as_many"])
    out["pairRegroupedBMany"] = n(t["regrouped"]["phase 1"]["windows_as_many"])

    gr = load("grillec")
    for case in ("known", "joint", "seeded"):
        found, total = gr["recovered"][case]
        out[f"grille{case.capitalize()}"] = f"{found} of {total}"
    out["grilleJointSteps"] = n(gr["search"]["joint"]["steps"])
    joint = [pl for pl in gr["planted"] if pl["case"] == "joint"]
    out["grilleJointHolesHigh"] = str(max(pl["holes_right"] for pl in joint))

    q = load("quick")
    out["quickRecovered"] = str(q["planted_recovered"])
    out["quickPlanted"] = str(len(q["planted"]))
    out["quickPlantedLow"] = d(q["planted_lowest_true"])
    out["quickVariants"] = str(q["search"]["variants"])
    out["quickShuffles"] = str(q["search"]["shuffles"])
    out["quickBest"] = d(q["searched_best"]["per_letter"])
    out["quickShuffleBestHigh"] = d(max(q["shuffle_bests"]))
    out["quickShuffleBestLow"] = d(min(q["shuffle_bests"]))
    out["quickShuffleBestAsHigh"] = str(q["shuffle_bests_as_high"])
    sp = q["spaces"]
    out["spacesSeparators"] = str(sp["separators"])
    out["spacesLetters"] = str(sp["letters"])
    out["spacesMean"] = p(sp["mean_word_length"])
    out["spacesEnglishMax"] = p(sp["english_longest_mean_word"], 1)
    out["spacesRuns"] = n(sp["english_runs"])
    out["spacesDistinct"] = str(sp["distinct_letters"])
    out["spacesEnglishFewest"] = str(sp["english_fewest_distinct"])
    cd = q["column_digits"]
    out["coincidenceA"] = p(cd["phase 0"]["coincidence"], 4)
    out["coincidenceB"] = p(cd["phase 1"]["coincidence"], 4)
    out["coincidenceEnglishLow"] = p(min(r["english_lowest"] for r in cd.values()), 4)
    out["coincidenceWindows"] = n(cd["phase 0"]["english_windows"])
    out["coincidenceShufflesA"] = n(cd["phase 0"]["shuffles_at_or_above"])
    out["coincidenceShufflesB"] = n(cd["phase 1"]["shuffles_at_or_above"])
    out["coincidenceShuffles"] = n(cd["phase 0"]["shuffles"])

    h = load("homophone")
    out["homCap"] = str(h["search"]["letter_cap"])
    out["homRecovered"] = str(h["planted_recovered"])
    out["homPlanted"] = str(len(h["planted"]))
    out["homPlantedLow"] = d(h["planted_lowest_true"])
    out["homCells"] = d(h["searched"]["cells"]["per_letter"])
    out["homCellsAsHigh"] = str(h["searched"]["cells"]["shuffles_as_high"])
    out["homRegrouped"] = d(h["searched"]["regrouped"]["per_letter"])
    out["homRegroupedAsHigh"] = str(h["searched"]["regrouped"]["shuffles_as_high"])
    out["homShuffles"] = str(len(h["searched"]["cells"]["shuffles"]))

    a = load("additive")
    rows = a["counts"]["rows"]
    out["addDraws"] = n(sum(r["draws"] for r in rows))
    out["addFewest"] = str(min(r["fewest_distinct"] for r in rows))
    out["addReaching"] = str(sum(r["reaching_cells"] for r in rows))
    out["addTopRows"] = str(a["counts"]["cells"]["top_three_rows"])
    out["addTopRowsEnglish"] = str(max(r["most_in_top_three_rows"] for r in rows))
    out["addRecovered"] = str(a["planted_recovered"])
    out["addPlanted"] = str(len(a["planted"]))
    out["addPlantedLow"] = d(a["planted_lowest_true"])
    out["addBest"] = d(a["searched_best"])
    out["addSteps"] = n(a["search"]["steps"])
    out["addRestarts"] = str(a["search"]["restarts"])
    out["addCases"] = str(len(a["searched"]))
    out["addAsHighMin"] = str(min(r["shuffles_as_high"] for r in a["searched"].values()))
    out["addShuffles"] = str(len(next(iter(a["searched"].values()))["shuffles"]))

    dr = load("direction")
    out["dirTransforms"] = n(dr["search"]["transforms"])
    out["dirShuffles"] = str(dr["search"]["shuffles"])
    out["dirRecovered"] = str(dr["planted_recovered"])
    out["dirPlanted"] = str(len(dr["planted"]))
    out["dirPlantedLow"] = d(dr["planted_lowest_true"])
    fam = dr["families"]
    out["dirBest"] = d(fam["all"]["cells_best"])
    out["dirShuffleBestHigh"] = d(max(fam["all"]["shuffle_bests"]))
    out["dirShuffleBestLow"] = d(min(fam["all"]["shuffle_bests"]))
    out["dirAsHigh"] = str(fam["all"]["shuffle_bests_as_high"])
    top = dr["top"][0]
    out["dirTopTransform"] = top["transform"].replace(":", "{:}")
    out["dirTopZ"] = p(top["z"])
    out["dirTopScore"] = d(top["per_letter"])
    return out


def power_table() -> str:
    """One row per searched family: planted recovered, weakest planted text, the cells' best, shuffles as high."""
    rows = []

    def row(family: str, recovered: str, planted: str, cells: str, shuffles: str) -> None:
        rows.append(f"{family} & {recovered} & {planted} & {cells} & {shuffles} \\\\")

    columnar = load("columnar")
    small = [r for r in columnar["rows"] if r["width"] in (1, 2, 4, 7)]
    row("Keyed square; columnar widths 1, 2, 4, 7",
        f"{sum(r['planted_recovered'] for r in small)}/{sum(len(r['planted']) for r in small)}",
        d(min(pl["true_per_letter"] for r in small for pl in r["planted"]), 2),
        d(max(r["cells_per_letter"] for r in small), 2),
        f"{min(r['shuffles_as_high'] for r in small)}--{max(r['shuffles_as_high'] for r in small)}/4")
    c14 = load("columnar14c")
    rec = c14["planted_recovered"]
    best = max(c14["searched"].values(), key=lambda r: r["per_letter"])
    row("Columnar width 14, both directions",
        f"{sum(v[0] for v in rec.values())}/{sum(v[1] for v in rec.values())}",
        d(c14["planted_lowest_true"], 2), d(best["per_letter"], 2),
        f"{best['shuffles_as_high']}/{len(best['shuffles'])}")
    fs = load("foursquare")
    best = max(fs["searched"].values(), key=lambda r: r["per_letter"])
    row("Four-square", f"{fs['planted_recovered']}/{len(fs['planted'])}", d(fs["planted_lowest_true"], 2),
        d(best["per_letter"], 2), f"{best['shuffles_as_high']}/{len(best['shuffles'])}")
    a = load("additive")
    best = max(a["searched"].values(), key=lambda r: r["per_letter"])
    row("Repeating shift, periods 2--14", f"{a['planted_recovered']}/{len(a['planted'])}",
        d(a["planted_lowest_true"], 2), d(best["per_letter"], 2),
        f"{best['shuffles_as_high']}/{len(best['shuffles'])}")
    q = load("quick")
    row("Nulls by place; reversed; column digits", f"{q['planted_recovered']}/{len(q['planted'])}",
        d(q["planted_lowest_true"], 2), d(q["searched_best"]["per_letter"], 2),
        f"{q['shuffle_bests_as_high']}/{len(q['shuffle_bests'])}\\textsuperscript{{a}}")
    h = load("homophone")
    best = max(h["searched"].values(), key=lambda r: r["per_letter"])
    row("Homophonic key, capped", f"{h['planted_recovered']}/{len(h['planted'])}", d(h["planted_lowest_true"], 2),
        d(best["per_letter"], 2), f"{best['shuffles_as_high']}/{len(best['shuffles'])}")
    dr = load("direction")
    fam = dr["families"]["all"]
    row("Delays, nulls 2--14, rails, columns 10--28", f"{dr['planted_recovered']}/{len(dr['planted'])}",
        d(dr["planted_lowest_true"], 2), d(fam["cells_best"], 2),
        f"{fam['shuffle_bests_as_high']}/{len(fam['shuffle_bests'])}\\textsuperscript{{a}}")
    head = ("\\begin{tabular}{@{}p{0.38\\linewidth}cccc@{}}\n\\toprule\n"
            "Family searched & Planted found & Weakest planted & Cells' best & Shuffles as high \\\\\n\\midrule")
    return head + "\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n"


def render() -> dict[str, str]:
    values = macros()
    lines = ["% Written by ../code/make_numbers.py from engine/data/swarm_cache. Do not edit by hand."]
    for name in INPUTS:
        digest = hashlib.sha256((CACHE / f"dagapeyeff-{name}.json").read_bytes()).hexdigest()
        lines.append(f"% dagapeyeff-{name}.json sha256 {digest}")
    for key in sorted(values):
        lines.append(f"\\newcommand{{\\{key}}}{{{values[key]}}}")
    return {
        "numbers.tex": "\n".join(lines) + "\n",
        "tab_power.tex": "% Written by ../code/make_numbers.py. Do not edit by hand.\n" + power_table(),
    }


def main() -> int:
    stale = []
    for name, text in render().items():
        path = PAPER / name
        if path.exists() and path.read_text(encoding="utf-8") == text:
            continue
        if "--check" in sys.argv:
            stale.append(name)
        else:
            path.write_text(text, encoding="utf-8")
            print(f"wrote {name}")
    if stale:
        print("stale: " + ", ".join(stale))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
