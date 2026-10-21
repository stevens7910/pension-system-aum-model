import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math

st.set_page_config(
    page_title="Model AuM III. penzijního pilíře ČR (2026–2040)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS pro tmavý / moderní finanční vzhled
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 0.75rem;
        padding: 1rem;
    }
    .waterfall-card {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

HISTORICAL_DATA = [
    {
        "year": 2024,
        "status": "Audit (APS ČR)",
        "tfAuM": 376.462,
        "dpsAuM": 228.543,
        "dpsConsAuM": 58.2,
        "dpsBalAuM": 64.0,
        "dpsDynAuM": 106.343,
        "totalAuM": 605.005,
        "tfParticipants": 1982.4,
        "dpsParticipants": 1999.7,
        "totalParticipants": 3982.1,
        "empParticipants": 1715.5,
        "avgClientDps": 896.0,
        "avgClientTf": 795.0,
        "avgEmpContrib": 1140.0,
        "inflowClient": 40.4,
        "inflowEmp": 23.2,
        "inflowState": 6.1,
        "totalInflow": 69.7,
        "netReturn": 24.8,
        "totalOutflow": 49.5,
        "migratedAuM": 18.2,
        "deflator2026": 1.0,
        "nominalGDP": 7650.0,
        "p10AuM": 605.005,
        "p90AuM": 605.005,
        "netDpsYieldPct": 7.4,
        "netTfYieldPct": 1.85,
    },
    {
        "year": 2025,
        "status": "Audit (APS ČR)",
        "tfAuM": 348.700,
        "dpsAuM": 311.151,
        "dpsConsAuM": 61.5,
        "dpsBalAuM": 82.0,
        "dpsDynAuM": 167.651,
        "totalAuM": 659.851,
        "tfParticipants": 1714.8,
        "dpsParticipants": 2179.2,
        "totalParticipants": 3894.0,
        "empParticipants": 1723.1,
        "avgClientDps": 915.0,
        "avgClientTf": 805.0,
        "avgEmpContrib": 1185.0,
        "inflowClient": 41.2,
        "inflowEmp": 24.5,
        "inflowState": 5.8,
        "totalInflow": 71.5,
        "netReturn": 38.4,
        "totalOutflow": 55.0,
        "migratedAuM": 23.5,
        "deflator2026": 1.0,
        "nominalGDP": 8050.0,
        "p10AuM": 659.851,
        "p90AuM": 659.851,
        "netDpsYieldPct": 9.8,
        "netTfYieldPct": 1.57,
    },
]

PRESETS = {
    "base": {
        "name": "📊 Základní scénář (Konsenzus ČNB / APS)",
        "inflation": 2.3,
        "wageGrowth": 4.8,
        "bondYield": 3.8,
        "equityReturn": 7.8,
        "balancedReturn": 5.4,
        "tfGrossReturn": 2.6,
        "marketCycles": False,
        "clientDps2026": 940,
        "clientTf2026": 810,
        "clientElasticity": 85,
        "empContrib2026": 1230,
        "empElasticity": 100,
        "empPenetration2040": 52,
        "mandatoryRiskEmp": True,
        "indexStateSupport": False,
        "tfToDpsMigration": 4.2,
        "tfOutflowRate": 6.4,
        "dpsNewAcq": 115,
        "dpsOutflowRate": 3.3,
        "autoEnrollment": False,
        "dynShare2026": 54,
        "dynShare2040": 74,
        "consShare2040": 8,
        "feeReform": False,
    },
    "bull": {
        "name": "🚀 Dynamický růst & Reforma „Lepší penzijko“",
        "inflation": 2.2,
        "wageGrowth": 5.4,
        "bondYield": 3.9,
        "equityReturn": 8.8,
        "balancedReturn": 6.0,
        "tfGrossReturn": 2.8,
        "marketCycles": False,
        "clientDps2026": 980,
        "clientTf2026": 820,
        "clientElasticity": 100,
        "empContrib2026": 1280,
        "empElasticity": 110,
        "empPenetration2040": 60,
        "mandatoryRiskEmp": True,
        "indexStateSupport": True,
        "tfToDpsMigration": 5.8,
        "tfOutflowRate": 6.2,
        "dpsNewAcq": 135,
        "dpsOutflowRate": 3.0,
        "autoEnrollment": False,
        "dynShare2026": 56,
        "dynShare2040": 82,
        "consShare2040": 6,
        "feeReform": True,
    },
    "autoenroll": {
        "name": "🏛️ Automatický vstup (Auto-enrollment 2028)",
        "inflation": 2.3,
        "wageGrowth": 4.9,
        "bondYield": 3.8,
        "equityReturn": 7.8,
        "balancedReturn": 5.4,
        "tfGrossReturn": 2.6,
        "marketCycles": False,
        "clientDps2026": 950,
        "clientTf2026": 810,
        "clientElasticity": 90,
        "empContrib2026": 1250,
        "empElasticity": 105,
        "empPenetration2040": 66,
        "mandatoryRiskEmp": True,
        "indexStateSupport": True,
        "tfToDpsMigration": 5.0,
        "tfOutflowRate": 6.4,
        "dpsNewAcq": 130,
        "dpsOutflowRate": 3.1,
        "autoEnrollment": True,
        "dynShare2026": 55,
        "dynShare2040": 78,
        "consShare2040": 7,
        "feeReform": True,
    },
    "stagflation": {
        "name": "⚠️ Stagflace & Konkurence DIP",
        "inflation": 4.1,
        "wageGrowth": 4.2,
        "bondYield": 4.8,
        "equityReturn": 5.6,
        "balancedReturn": 4.2,
        "tfGrossReturn": 2.4,
        "marketCycles": True,
        "clientDps2026": 910,
        "clientTf2026": 790,
        "clientElasticity": 65,
        "empContrib2026": 1190,
        "empElasticity": 80,
        "empPenetration2040": 44,
        "mandatoryRiskEmp": True,
        "indexStateSupport": False,
        "tfToDpsMigration": 3.2,
        "tfOutflowRate": 7.8,
        "dpsNewAcq": 75,
        "dpsOutflowRate": 4.4,
        "autoEnrollment": False,
        "dynShare2026": 52,
        "dynShare2040": 65,
        "consShare2040": 12,
        "feeReform": False,
    },
}

# Inicializace session_state
if "initialized" not in st.session_state:
    for k, v in PRESETS["base"].items():
        if k != "name":
            st.session_state[k] = v
    st.session_state["active_preset"] = "base"
    st.session_state["initialized"] = True


def apply_preset(preset_key: str):
    for k, v in PRESETS[preset_key].items():
        if k != "name":
            st.session_state[k] = v
    st.session_state["active_preset"] = preset_key


def run_model(p: dict) -> pd.DataFrame:
    rows = [dict(h) for h in HISTORICAL_DATA]

    tfAuM = HISTORICAL_DATA[1]["tfAuM"]
    dpsAuM = HISTORICAL_DATA[1]["dpsAuM"]
    tfPart = HISTORICAL_DATA[1]["tfParticipants"]
    dpsPart = HISTORICAL_DATA[1]["dpsParticipants"]

    avgClientDps = float(p["clientDps2026"])
    avgClientTf = float(p["clientTf2026"])
    avgEmpContrib = float(p["empContrib2026"])

    dpsEmpPen = 0.413
    tfEmpPen = 0.480

    nominalGDP = 8050.0
    cumInflationFactor = 1.0

    for year in range(2026, 2041):
        t = year - 2026
        progress = t / 14.0

        if year > 2026:
            cumInflationFactor *= 1.0 + p["inflation"] / 100.0

        realGrowthGDP = max(1.0, (p["wageGrowth"] - p["inflation"]) * 0.9)
        nominalGDP *= 1.0 + (p["inflation"] + realGrowthGDP) / 100.0

        if year > 2026:
            clientDpsGrowthRate = (p["wageGrowth"] / 100.0) * (p["clientElasticity"] / 100.0)
            clientTfGrowthRate = (p["wageGrowth"] / 100.0) * max(0.25, (p["clientElasticity"] - 20.0) / 100.0)
            empGrowthRate = (p["wageGrowth"] / 100.0) * (p["empElasticity"] / 100.0)

            avgClientDps *= 1.0 + clientDpsGrowthRate
            avgClientTf *= 1.0 + clientTfGrowthRate
            avgEmpContrib *= 1.0 + empGrowthRate

        migRate = p["tfToDpsMigration"] / 100.0
        migratedParticipants = tfPart * migRate
        migratedAuM = tfAuM * migRate

        ageFactorTf = 1.0 + t * 0.018
        tfAttritionPartRate = min(0.18, (p["tfOutflowRate"] / 100.0) * 0.85 * ageFactorTf)
        tfDepartedPart = tfPart * tfAttritionPartRate

        tfPart = max(120.0, tfPart - migratedParticipants - tfDepartedPart)

        autoEnrollBoost = 0.0
        if p["autoEnrollment"] and 2028 <= year <= 2031:
            autoEnrollBoost = 160.0 if year == 2028 else (130.0 if year == 2029 else (95.0 if year == 2030 else 65.0))

        dpsAttritionPartRate = (p["dpsOutflowRate"] / 100.0) * 0.72
        dpsDepartedPart = dpsPart * dpsAttritionPartRate
        dpsPart = dpsPart + p["dpsNewAcq"] + migratedParticipants + autoEnrollBoost - dpsDepartedPart

        totalParticipants = tfPart + dpsPart

        targetDpsPen = p["empPenetration2040"] / 100.0
        dpsEmpPen = 0.413 + (targetDpsPen - 0.413) * progress
        tfEmpPen = max(0.32, 0.480 - 0.008 * t)

        dpsEmpPart = dpsPart * dpsEmpPen
        tfEmpPart = tfPart * tfEmpPen
        empParticipants = dpsEmpPart + tfEmpPart

        riskWorkersBonusMld = (
            (0.115 * 12.0 * (2150.0 * math.pow(1.0 + p["wageGrowth"] / 100.0, t))) / 1000.0
            if p["mandatoryRiskEmp"]
            else 0.0
        )

        inflowClientDps = (dpsPart * 12.0 * avgClientDps) / 1e6
        inflowClientTf = (tfPart * 12.0 * avgClientTf) / 1e6
        inflowClient = inflowClientDps + inflowClientTf

        inflowEmpDps = (dpsEmpPart * 12.0 * avgEmpContrib) / 1e6 + riskWorkersBonusMld * 0.88
        inflowEmpTf = (tfEmpPart * 12.0 * (avgEmpContrib * 0.88)) / 1e6 + riskWorkersBonusMld * 0.12
        inflowEmp = inflowEmpDps + inflowEmpTf

        stateSupportIndex = math.pow(1.0 + p["inflation"] / 100.0, t) if p["indexStateSupport"] else 1.0
        effStateDpsMonthly = min(340.0 * stateSupportIndex, max(115.0, avgClientDps * 0.155))
        effStateTfMonthly = min(340.0 * stateSupportIndex, max(85.0, avgClientTf * 0.122))

        inflowStateDps = (dpsPart * 0.89 * 12.0 * effStateDpsMonthly) / 1e6
        inflowStateTf = (tfPart * 0.68 * 12.0 * effStateTfMonthly) / 1e6
        inflowState = inflowStateDps + inflowStateTf

        totalInflow = inflowClient + inflowEmp + inflowState

        effTfOutflowRate = (p["tfOutflowRate"] / 100.0) * (1.0 + t * 0.012)
        outflowTf = tfAuM * effTfOutflowRate
        outflowDps = dpsAuM * (p["dpsOutflowRate"] / 100.0)
        totalOutflow = outflowTf + outflowDps

        dynShare = (p["dynShare2026"] + (p["dynShare2040"] - p["dynShare2026"]) * progress) / 100.0
        consShare2026 = 0.195
        consShare = consShare2026 + ((p["consShare2040"] / 100.0) - consShare2026) * progress
        balShare = max(0.0, 1.0 - dynShare - consShare)

        reformActive = p["feeReform"] and year >= 2027
        feeDynTER = (
            (0.0055 + max(0.0, p["equityReturn"] / 100.0) * 0.05)
            if reformActive
            else (0.010 + max(0.0, p["equityReturn"] / 100.0) * 0.15)
        )
        feeBalTER = (
            (0.0050 + max(0.0, p["balancedReturn"] / 100.0) * 0.05)
            if reformActive
            else (0.010 + max(0.0, p["balancedReturn"] / 100.0) * 0.15)
        )
        feeConsTER = 0.0035 if reformActive else (0.004 + max(0.0, (p["bondYield"] - 0.5) / 100.0) * 0.10)
        feeTfTER = 0.008 + max(0.0, p["tfGrossReturn"] / 100.0) * 0.10

        equityShock = 0.0
        balShock = 0.0
        if p["marketCycles"]:
            if year == 2029:
                equityShock, balShock = -0.145, -0.065
            elif year == 2030:
                equityShock, balShock = 0.065, 0.030
            elif year == 2035:
                equityShock, balShock = -0.125, -0.055
            elif year == 2036:
                equityShock, balShock = 0.055, 0.025

        netDynReturnRate = (p["equityReturn"] / 100.0) + equityShock - feeDynTER
        netBalReturnRate = (p["balancedReturn"] / 100.0) + balShock - feeBalTER
        netConsReturnRate = ((p["bondYield"] - 0.4) / 100.0) - feeConsTER
        netDpsReturnRate = dynShare * netDynReturnRate + balShare * netBalReturnRate + consShare * netConsReturnRate

        netTfReturnRate = max(0.0, (p["tfGrossReturn"] / 100.0) - feeTfTER)

        tfBaseForReturn = max(0.0, tfAuM - migratedAuM + 0.5 * (inflowClientTf + inflowEmpTf + inflowStateTf - outflowTf))
        dpsBaseForReturn = max(0.0, dpsAuM + migratedAuM + 0.5 * (inflowClientDps + inflowEmpDps + inflowStateDps - outflowDps))

        returnTf = tfBaseForReturn * netTfReturnRate
        returnDps = dpsBaseForReturn * netDpsReturnRate
        netReturn = returnTf + returnDps

        tfAuM = max(15.0, tfAuM - migratedAuM + inflowClientTf + inflowEmpTf + inflowStateTf - outflowTf + returnTf)
        dpsAuM = max(50.0, dpsAuM + migratedAuM + inflowClientDps + inflowEmpDps + inflowStateDps - outflowDps + returnDps)
        totalAuM = tfAuM + dpsAuM

        portfolioVol = 0.015 + dynShare * 0.095 + balShare * 0.045
        cumSigma = portfolioVol * math.sqrt(t + 1) * (dpsAuM / totalAuM)
        p10AuM = totalAuM * math.exp(-1.28 * cumSigma * 0.65)
        p90AuM = totalAuM * math.exp(1.28 * cumSigma * 0.65)

        rows.append(
            {
                "year": year,
                "status": "Projekce",
                "tfAuM": tfAuM,
                "dpsAuM": dpsAuM,
                "dpsConsAuM": dpsAuM * consShare,
                "dpsBalAuM": dpsAuM * balShare,
                "dpsDynAuM": dpsAuM * dynShare,
                "totalAuM": totalAuM,
                "tfParticipants": tfPart,
                "dpsParticipants": dpsPart,
                "totalParticipants": totalParticipants,
                "empParticipants": empParticipants,
                "avgClientDps": avgClientDps,
                "avgClientTf": avgClientTf,
                "avgEmpContrib": avgEmpContrib,
                "inflowClient": inflowClient,
                "inflowEmp": inflowEmp,
                "inflowState": inflowState,
                "totalInflow": totalInflow,
                "netReturn": netReturn,
                "totalOutflow": totalOutflow,
                "migratedAuM": migratedAuM,
                "deflator2026": cumInflationFactor,
                "nominalGDP": nominalGDP,
                "p10AuM": p10AuM,
                "p90AuM": p90AuM,
                "netDpsYieldPct": netDpsReturnRate * 100.0,
                "netTfYieldPct": netTfReturnRate * 100.0,
            }
        )

    return pd.DataFrame(rows)


# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("### ⚙️ Vstupní parametry modelu")
    price_mode_label = st.radio(
        "Cenové vyjádření",
        options=["Nominální Kč", "Reálné Kč (ceny 2026)"],
        horizontal=True,
    )
    is_real = price_mode_label.startswith("Reálné")

    tab1, tab2, tab3, tab4 = st.tabs(["1. Makro", "2. Úložky", "3. Kmen", "4. Fondy"])

    with tab1:
        st.caption("Makroekonomické parametry určují růst mezd, dluhopisové výnosy TF a reálný diskont.")
        st.slider("Průměrná roční inflace CPI (% p.a.)", 1.0, 6.0, step=0.1, key="inflation")
        st.slider("Nominální růst průměrné mzdy (% p.a.)", 2.0, 8.5, step=0.1, key="wageGrowth")
        real_wage = st.session_state["wageGrowth"] - st.session_state["inflation"]
        st.caption(f"Reálný růst mezd: **{real_wage:+.1f} % p.a.**")
        st.slider("Výnos 10Y CZK státních dluhopisů (% p.a.)", 1.5, 7.0, step=0.1, key="bondYield")
        st.slider("Hrubý výnos globálních akcií – Dynamické DPS (% p.a.)", 3.0, 12.0, step=0.1, key="equityReturn")
        st.slider("Hrubý výnos Vyvážených fondů DPS (% p.a.)", 2.5, 9.0, step=0.1, key="balancedReturn")
        st.slider("Hrubý výnos Transformovaných fondů TF (% p.a.)", 1.0, 5.0, step=0.1, key="tfGrossReturn")
        st.checkbox("Simulovat cyklické tržní korekce (každých 6 let)", key="marketCycles")

    with tab2:
        st.caption("Výchozí stav APS ČR (2025): DPS ~915 Kč, TF ~805 Kč, zaměstnavatel ~1 185 Kč.")
        st.slider("Výchozí úložka střadatele v DPS 2026 (Kč/měs.)", 750, 1500, step=10, key="clientDps2026")
        st.slider("Výchozí úložka střadatele v TF 2026 (Kč/měs.)", 600, 1300, step=10, key="clientTf2026")
        st.slider("Elasticita růstu úložky střadatele vůči mzdám (%)", 30, 130, step=5, key="clientElasticity")
        st.divider()
        st.slider("Výchozí příspěvek zaměstnavatele 2026 (Kč/měs.)", 900, 2200, step=10, key="empContrib2026")
        st.slider("Elasticita příspěvku zaměstnavatele ke mzdám (%)", 50, 140, step=5, key="empElasticity")
        st.slider("Cílový podíl účastníků DPS se zaměstnavatelem 2040 (%)", 38, 75, step=1, key="empPenetration2040")
        st.checkbox("Zákon č. 324/2025 Sb. (4 % ze mzdy – rizikové profese)", key="mandatoryRiskEmp")
        st.checkbox("Pravidelná valorizace limitů státního příspěvku", key="indexStateSupport")

    with tab3:
        st.caption("Transformované fondy (1,71 mil. úč. na konci 2025) jsou uzavřené a postupně dobíhají.")
        st.slider("Roční míra přechodu (migrace) z TF do DPS (% kmene/rok)", 1.0, 10.0, step=0.2, key="tfToDpsMigration")
        st.slider("Roční výplaty dávek a odbytného z TF (% z AuM/rok)", 3.5, 12.0, step=0.2, key="tfOutflowRate")
        st.slider("Organická akvizice nových smluv DPS (tis. úč./rok)", 40, 220, step=5, key="dpsNewAcq")
        st.slider("Roční výplaty a odchody v DPS (% z AuM/rok)", 1.5, 7.5, step=0.1, key="dpsOutflowRate")
        st.checkbox("Zavedení Auto-enrollmentu (povinný vstup od 2028)", key="autoEnrollment")

    with tab4:
        st.caption("Posun alokace DPS z konzervativních do dynamických (akciových) a alternativních fondů.")
        st.slider("Podíl Dynamických + Alt. fondů v DPS 2026 (%)", 35, 70, step=1, key="dynShare2026")
        st.slider("Cílový podíl Dynamických + Alt. fondů v DPS 2040 (%)", 45, 90, step=1, key="dynShare2040")
        st.slider("Podíl Konzervativních fondů v DPS 2040 (%)", 3, 25, step=1, key="consShare2040")
        bal_2040 = max(0, 100 - st.session_state["dynShare2040"] - st.session_state["consShare2040"])
        st.caption(f"Zbytek tvoří Vyvážené fondy v r. 2040: **{bal_2040} %**")
        st.checkbox("Reforma poplatků „Lepší penzijko“ (od r. 2027)", key="feeReform")

    st.divider()
    with st.expander("📋 Auditovaná základna (APS ČR 2024–2025)", expanded=False):
        st.markdown(
            """
            | Ukazatel | 31.12.2024 | 31.12.2025 |
            |---|---|---|
            | **Celkové AuM** | 605,01 mld. | **659,85 mld.** |
            | • Transformované (TF) | 376,46 mld. | 348,70 mld. |
            | • Účastnické (DPS) | 228,54 mld. | 311,15 mld. |
            | **Počet účastníků** | 3 982 tis. | **3 894 tis.** |
            | • z toho v DPS | 2 000 tis. | 2 179 tis. |
            | • se zaměstnavatelem | 1 716 tis. | 1 723 tis. |
            | **Prům. úložka (DPS/TF)** | 896 / 795 Kč | **915 / 805 Kč** |
            """
        )

# ================= HEADER & PRESETS =================
st.markdown(
    "### 🏦 Komplexní aktuárský a makroekonomický model AuM III. penzijního pilíře ČR (2026–2040)"
)
st.caption(
    "APS ČR & MF ČR Audited Baseline (2024–2025) • Dynamická projekce Transformovaných fondů (PP) a Účastnických fondů (DPS)"
)

p_cols = st.columns(4)
for idx, (pkey, pval) in enumerate(PRESETS.items()):
    with p_cols[idx]:
        if st.button(pval["name"], use_container_width=True):
            apply_preset(pkey)
            st.rerun()

# ================= RUN MODEL =================
params = {k: st.session_state[k] for k in PRESETS["base"].keys() if k != "name"}
df = run_model(params)


def adj(df_in: pd.DataFrame, col: str) -> pd.Series:
    if not is_real:
        return df_in[col]
    return df_in[col] / df_in["deflator2026"]


def adj_val(row, col: str) -> float:
    if not is_real:
        return float(row[col])
    return float(row[col]) / float(row["deflator2026"])


r2025 = df.iloc[1]
r2026 = df.iloc[2]
r2040 = df.iloc[-1]

aum2040 = adj_val(r2040, "totalAuM")
dps2040 = adj_val(r2040, "dpsAuM")
tf2040 = adj_val(r2040, "tfAuM")

cagr = (math.pow(aum2040 / r2025["totalAuM"], 1.0 / 15.0) - 1.0) * 100.0
pct_growth = ((aum2040 / r2025["totalAuM"]) - 1.0) * 100.0
gdp_share = (r2040["totalAuM"] / r2040["nominalGDP"]) * 100.0
dps_share_2040 = (r2040["dpsAuM"] / r2040["totalAuM"]) * 100.0

crossover_rows = df[df["dpsAuM"] >= df["tfAuM"]]
crossover_year = str(int(crossover_rows.iloc[0]["year"])) if not crossover_rows.empty else "po r. 2040"

df_proj = df.iloc[2:].copy()
cum_inflows = adj(df_proj, "totalInflow").sum()
cum_client = adj(df_proj, "inflowClient").sum()
cum_emp = adj(df_proj, "inflowEmp").sum()
cum_state = adj(df_proj, "inflowState").sum()
cum_returns = adj(df_proj, "netReturn").sum()
cum_outflows = adj(df_proj, "totalOutflow").sum()

# ================= KPI SUMMARY ROW =================
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric(
        "Auditovaný základ (2025)",
        "659,9 mld. Kč",
        "TF: 348,7 | DPS: 311,2 mld.",
        delta_color="off",
    )
with k2:
    st.metric(
        f"Projekce AuM 2040 ({'Reálně' if is_real else 'Nominálně'})",
        f"{aum2040:,.1f} mld. Kč".replace(",", " ").replace(".", ","),
        f"{cagr:+.1f} % p.a. (+{pct_growth:.0f} % vs 2025) • ~{gdp_share:.1f} % HDP",
    )
with k3:
    st.metric(
        "Struktura fondů 2040",
        f"{dps_share_2040:.1f} % v DPS",
        f"DPS: {dps2040:.0f} mld. | TF: {tf2040:.0f} mld. (Obrat: {crossover_year})",
        delta_color="off",
    )
with k4:
    st.metric(
        "Kumulativní přítoky & Výnos (26–40)",
        f"+{cum_inflows:,.0f} mld. Kč".replace(",", " "),
        f"Čistý výnos: +{cum_returns:,.0f} mld. | Výplaty: −{cum_outflows:,.0f} mld.".replace(",", " "),
    )
with k5:
    c2040 = round(adj_val(r2040, "avgClientDps"))
    e2040 = round(adj_val(r2040, "avgEmpContrib"))
    st.metric(
        "Průměrná úložka DPS (2026 → 2040)",
        f"{round(r2026['avgClientDps'])} → {c2040} Kč",
        f"Zaměstnavatel: {round(r2026['avgEmpContrib'])} → {e2040} Kč/měs.",
        delta_color="off",
    )

# ================= MAIN CHART =================
st.markdown("#### Vývoj celkového objemu aktiv (AuM) 2024–2040: Transformované fondy vs. DPS")
col_chk, _ = st.columns([1, 3])
with col_chk:
    show_band = st.checkbox("Zobrazit pásmo nejistoty (P10–P90)", value=True)

fig_main = go.Figure()

years_label = [f"{y}*" if y <= 2025 else str(y) for y in df["year"]]

fig_main.add_trace(
    go.Bar(
        x=years_label,
        y=adj(df, "tfAuM"),
        name="Transformované fondy (TF)",
        marker_color="#f59e0b",
    )
)
fig_main.add_trace(
    go.Bar(
        x=years_label,
        y=adj(df, "dpsConsAuM"),
        name="DPS Konzervativní",
        marker_color="#0ea5e9",
    )
)
fig_main.add_trace(
    go.Bar(
        x=years_label,
        y=adj(df, "dpsBalAuM"),
        name="DPS Vyvážené",
        marker_color="#6366f1",
    )
)
fig_main.add_trace(
    go.Bar(
        x=years_label,
        y=adj(df, "dpsDynAuM"),
        name="DPS Dynamické & Alternativní",
        marker_color="#10b981",
    )
)

if show_band:
    fig_main.add_trace(
        go.Scatter(
            x=years_label,
            y=adj(df, "p90AuM"),
            name="P90 (Optimistické pásmo)",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig_main.add_trace(
        go.Scatter(
            x=years_label,
            y=adj(df, "p10AuM"),
            name="Pásmo nejistoty P10–P90",
            fill="tonexty",
            fillcolor="rgba(244, 63, 94, 0.16)",
            line=dict(width=0),
        )
    )

fig_main.add_trace(
    go.Scatter(
        x=years_label,
        y=adj(df, "totalAuM"),
        name="Celkové AuM (medián)",
        mode="lines+markers",
        line=dict(color="#f43f5e", width=3),
        marker=dict(size=7, color="#f43f5e"),
    )
)

fig_main.update_layout(
    barmode="stack",
    template="plotly_dark",
    height=430,
    margin=dict(l=20, r=20, t=20, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    yaxis_title="Objem aktiv AuM (mld. Kč)",
    hovermode="x unified",
)
st.plotly_chart(fig_main, use_container_width=True)

# ================= SECONDARY CHARTS =================
c_left, c_right = st.columns(2)

with c_left:
    st.markdown("#### Roční dekompozice změny AuM (Cash-Flow & Výnos, 2026–2040)")
    fig_cf = go.Figure()
    x_proj = [str(y) for y in df_proj["year"]]
    fig_cf.add_trace(
        go.Bar(
            x=x_proj,
            y=adj(df_proj, "totalInflow"),
            name="Příspěvky celkem (Klient + Zam. + Stát)",
            marker_color="#3b82f6",
        )
    )
    fig_cf.add_trace(
        go.Bar(
            x=x_proj,
            y=adj(df_proj, "netReturn"),
            name="Čistý tržní výnos (po poplatcích)",
            marker_color="#10b981",
        )
    )
    fig_cf.add_trace(
        go.Bar(
            x=x_proj,
            y=-adj(df_proj, "totalOutflow"),
            name="Výplaty dávek a odbytné",
            marker_color="#f43f5e",
        )
    )
    fig_cf.update_layout(
        barmode="relative",
        template="plotly_dark",
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        yaxis_title="mld. Kč / rok",
        hovermode="x unified",
    )
    st.plotly_chart(fig_cf, use_container_width=True)

with c_right:
    sub_mode = st.radio(
        "Zobrazení vedlejšího grafu:",
        options=["Vývoj průměrné měsíční úložky (Kč/měs.)", "Vývoj počtu účastníků (v tisících osob)"],
        horizontal=True,
    )
    fig_sec = go.Figure()
    if sub_mode.startswith("Vývoj průměrné"):
        fig_sec.add_trace(
            go.Scatter(
                x=years_label,
                y=adj(df, "avgEmpContrib"),
                name="Příspěvek zaměstnavatele (Kč)",
                mode="lines+markers",
                line=dict(color="#6366f1", width=2.5),
            )
        )
        fig_sec.add_trace(
            go.Scatter(
                x=years_label,
                y=adj(df, "avgClientDps"),
                name="Úložka účastníka DPS (Kč)",
                mode="lines+markers",
                line=dict(color="#10b981", width=2.5),
            )
        )
        fig_sec.add_trace(
            go.Scatter(
                x=years_label,
                y=adj(df, "avgClientTf"),
                name="Úložka účastníka TF (Kč)",
                mode="lines+markers",
                line=dict(color="#f59e0b", width=2.5),
            )
        )
        y_label_sec = "Kč / měsíc"
    else:
        fig_sec.add_trace(
            go.Scatter(
                x=years_label,
                y=df["dpsParticipants"],
                name="Účastníci DPS (tis.)",
                mode="lines+markers",
                line=dict(color="#10b981", width=2.5),
            )
        )
        fig_sec.add_trace(
            go.Scatter(
                x=years_label,
                y=df["empParticipants"],
                name="Se zaměstnavatelem (tis.)",
                mode="lines+markers",
                line=dict(color="#6366f1", width=2.5),
            )
        )
        fig_sec.add_trace(
            go.Scatter(
                x=years_label,
                y=df["tfParticipants"],
                name="Účastníci TF (tis.)",
                mode="lines+markers",
                line=dict(color="#f59e0b", width=2.5),
            )
        )
        y_label_sec = "Tisíce účastníků"

    fig_sec.update_layout(
        template="plotly_dark",
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        yaxis_title=y_label_sec,
        hovermode="x unified",
    )
    st.plotly_chart(fig_sec, use_container_width=True)

# ================= WATERFALL BRIDGE =================
st.markdown("#### Most (Waterfall) přírůstku AuM mezi lety 2025 a 2040")
wf_cols = st.columns(6)
wf_items = [
    ("Základ 2025 (Audit)", f"{r2025['totalAuM']:.1f} mld.", "TF + DPS výchozí stav", "#94a3b8"),
    ("+ Úložky střadatelů", f"+{cum_client:.0f} mld.", "Kumulativně 2026–2040", "#3b82f6"),
    ("+ Příspěvky zaměstn.", f"+{cum_emp:.0f} mld.", "Vč. zákona č. 324/2025 Sb.", "#6366f1"),
    ("+ Státní příspěvky", f"+{cum_state:.0f} mld.", "Státní podpora MF ČR", "#0ea5e9"),
    ("+ Čisté zhodnocení", f"+{cum_returns:.0f} mld.", "Složené úročení po popl.", "#10b981"),
    ("− Výplaty a odbytné", f"−{cum_outflows:.0f} mld.", f"Konečné AuM: {aum2040:.0f} mld.", "#f43f5e"),
]
for col, (lbl, val, sub, color) in zip(wf_cols, wf_items):
    with col:
        st.markdown(
            f"""
            <div class="waterfall-card" style="border-left: 4px solid {color};">
                <div style="font-size: 0.75rem; color: #94a3b8;">{lbl}</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin: 2px 0;">{val}</div>
                <div style="font-size: 0.72rem; color: #94a3b8;">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ================= TABLE & CSV EXPORT =================
st.markdown("#### Detailní datová matice modelu (2024–2040)")

display_df = pd.DataFrame(
    {
        "Rok": df["year"],
        "Status": df["status"],
        "Celkem AuM (mld.)": adj(df, "totalAuM").round(2),
        "TF AuM (mld.)": adj(df, "tfAuM").round(2),
        "DPS AuM (mld.)": adj(df, "dpsAuM").round(2),
        "Podíl DPS (%)": ((df["dpsAuM"] / df["totalAuM"]) * 100.0).round(1),
        "Účastníci celkem (tis.)": df["totalParticipants"].round(1),
        "Úložka DPS (Kč)": adj(df, "avgClientDps").round(0).astype(int),
        "Zaměstnavatel (Kč)": adj(df, "avgEmpContrib").round(0).astype(int),
        "Přítoky (mld.)": adj(df, "totalInflow").round(2),
        "Čistý výnos (mld.)": adj(df, "netReturn").round(2),
        "Odtoky (mld.)": adj(df, "totalOutflow").round(2),
    }
)

st.dataframe(display_df, use_container_width=True, hide_index=True)

csv_data = display_df.to_csv(index=False, sep=";").encode("utf-8-sig")
st.download_button(
    label="⬇ Stáhnout kompletní matici modelu (CSV, 2024–2040)",
    data=csv_data,
    file_name=f"model_penzijni_system_AuM_2024_2040_{'real' if is_real else 'nominal'}.csv",
    mime="text/csv",
)
