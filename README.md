# Model AuM III. penzijního pilíře ČR (2026–2040)

Komplexní interaktivní aktuárský a makroekonomický model objemu spravovaných prostředků (**AuM – Assets under Management**) ve III. pilíři českého penzijního systému (Transformované fondy PP & Účastnické fondy DPS) na horizontu **2026–2040**.

## Výchozí auditovaná data (APS ČR & MF ČR)
Model je ukotven na oficiálních statistikách **Asociace penzijních společností ČR (APS ČR)** a **Ministerstva financí ČR** za uzavřené roky 2024 a 2025:
- **Konec roku 2024:** Celkové AuM **605,01 mld. Kč** (Transformované fondy: 376,46 mld. Kč, Účastnické fondy DPS: 228,54 mld. Kč), 3,982 mil. účastníků.
- **Konec roku 2025:** Celkové AuM **659,85 mld. Kč** (Transformované fondy: 348,70 mld. Kč, Účastnické fondy DPS: 311,15 mld. Kč), 3,894 mil. účastníků (z toho 1,723 mil. s příspěvkem zaměstnavatele).

## Klíčové funkce modelu
- **Makroekonomický a tržní modul:** Inflace (CPI), nominální a reálný růst mezd, výnos 10Y CZK státních dluhopisů, hrubé výnosy akciových (dynamických), vyvážených a transformovaných fondů, volitelné cyklické tržní korekce a pásmo nejistoty **P10–P90**.
- **Dynamika příspěvků (Inflows):** Růst průměrné měsíční úložky střadatele v DPS i TF dle mzdové elasticity, růst příspěvku zaměstnavatele a penetrace zaměstnaneckých benefitů, dopad **zákona č. 324/2025 Sb.** (povinný příspěvek 4 % ze mzdy pro náročné profese 3. kategorie od r. 2026) a státní příspěvky.
- **Kmen účastníků a migrace TF → DPS:** Postupné dobíhání uzavřených Transformovaných fondů, výplaty dávek a odbytného a vnitřní migrace účastníků i majetku do DPS.
- **Alokace a poplatková reforma:** Posun alokace DPS směrem k dynamickým a alternativním fondům a modelování dopadu reformy poplatků („Lepší penzijko“) či automatického vstupu (**Auto-enrollment**).
- **Nominální vs. Reálné zobrazení & Export:** Okamžité přepínání mezi nominálními cenami a reálnými cenami roku 2026, dekompozice změny AuM (Waterfall) a export kompletní časové řady 2024–2040 do **CSV**.

## Spuštění

### 1. Samostatná webová aplikace (HTML/JS)
Stačí otevřít soubor `index.html` v libovolném moderním webovém prohlížeči nebo přes GitHub Pages.

### 2. Streamlit aplikace (Python / Streamlit Community Cloud)
Pro spuštění v prostředí **Streamlit**:
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Pro nasazení na **Streamlit Community Cloud** (share.streamlit.io) stačí propojit tento GitHub repozitář (`stevens7910/pension-system-aum-model`), zvolit větev `main` a jako hlavní soubor zadat `streamlit_app.py`.
