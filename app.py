import streamlit as st
import pandas as pd
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

model          = joblib.load('f1_model.pkl')
le_driver      = joblib.load('le_driver.pkl')
le_constructor = joblib.load('le_constructor.pkl')
le_circuit     = joblib.load('le_circuit.pkl')

st.set_page_config(page_title="F1 Race Predictor", layout="wide", page_icon="🏎️")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #080810 0%, #0c0c1a 100%); }
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.02) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] label {
    color: #555 !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #cc0000, #ff2222) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 800 !important;
    font-size: 13px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 14px !important;
    width: 100% !important;
    box-shadow: 0 0 30px rgba(200,0,0,0.4) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    color: #444 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    background: transparent !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    color: #e10600 !important;
    border-bottom: 2px solid #e10600 !important;
    background: transparent !important;
}
hr { border-color: rgba(255,255,255,0.05) !important; }
.block-container { padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:24px;">
  <div style="font-size:32px; font-weight:900; letter-spacing:-1px; margin-bottom:4px;">
    <span style="color:white;">F1 RACE </span><span style="color:#e10600;">PREDICTOR</span>
  </div>
  <div style="font-size:11px; color:#333; letter-spacing:2px; text-transform:uppercase;">
    XGBoost &nbsp;·&nbsp; Ergast Dataset 2010-2023 &nbsp;·&nbsp; MAE 2.87 positions
  </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["PREDICT", "INSIGHTS"])

with tab1:
    with st.sidebar:
        st.markdown("""
        <div style="padding:8px 0 20px;">
          <div style="font-size:10px; color:#333; letter-spacing:2px; text-transform:uppercase;">Session</div>
          <div style="font-size:20px; font-weight:700; color:white;">Race Setup</div>
        </div>
        """, unsafe_allow_html=True)
        driver        = st.selectbox("Driver",          sorted(le_driver.classes_))
        constructor   = st.selectbox("Constructor",     sorted(le_constructor.classes_))
        circuit       = st.selectbox("Circuit",         sorted(le_circuit.classes_))
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        grid          = st.slider("Grid position", 1, 20, 5)
        points_last_3 = st.slider("Avg points last 3 races", 0.0, 26.0, 5.0, step=0.5)
        weather       = st.selectbox("Conditions", ["Dry", "Wet", "Mixed"])
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        predict_btn   = st.button("PREDICT FINISH", use_container_width=True)

    if weather == "Wet":
        st.warning("🌧️  Wet race — historically 40% more position changes. Higher unpredictability expected.")
    elif weather == "Mixed":
        st.info("⛅  Mixed conditions — tyre strategy plays a bigger role than usual.")

    if not predict_btn:
        st.markdown("""
        <div style="margin-top:80px; text-align:center;">
          <div style="font-size:56px; opacity:0.08;">🏎️</div>
          <div style="color:#222; font-size:11px; letter-spacing:3px; text-transform:uppercase; margin-top:12px;">
            Configure race settings and hit predict
          </div>
        </div>
        """, unsafe_allow_html=True)

    if predict_btn:
        d_enc  = le_driver.transform([driver])[0]
        c_enc  = le_constructor.transform([constructor])[0]
        ci_enc = le_circuit.transform([circuit])[0]

        inp = pd.DataFrame(
            [[grid, points_last_3, d_enc, c_enc, ci_enc]],
            columns=['grid','points_last_3','driver_encoded',
                     'constructor_encoded','circuit_encoded'])

        pred  = model.predict(inp)[0]
        pos   = int(round(pred))
        ppct  = max(0, min(100, int((1 - (pos-1)/19)*100)))

        if pos == 1:
            col   = "#00e676"
            glow  = "rgba(0,230,118,0.25)"
            label = "RACE WINNER"
            icon  = "🏆"
        elif pos <= 3:
            col   = "#00e676"
            glow  = "rgba(0,230,118,0.15)"
            label = "PODIUM FINISH"
            icon  = "🥂"
        elif pos <= 10:
            col   = "#4da6ff"
            glow  = "rgba(77,166,255,0.15)"
            label = "POINTS FINISH"
            icon  = "✅"
        else:
            col   = "#ff6b35"
            glow  = "rgba(255,107,53,0.15)"
            label = "OUTSIDE POINTS"
            icon  = "—"

        card = (
            "<div style='"
            "background:rgba(255,255,255,0.025);"
            "border:1px solid rgba(255,255,255,0.07);"
            "border-radius:20px;"
            "padding:48px 32px;"
            "margin:16px 0;"
            "text-align:center;"
            "'>"
            "<div style='font-size:40px;margin-bottom:12px;'>" + icon + "</div>"
            "<div style='"
            "font-size:96px;"
            "font-weight:900;"
            "color:" + col + ";"
            "line-height:1;"
            "letter-spacing:-3px;"
            "text-shadow:0 0 60px " + glow + ";"
            "margin-bottom:8px;"
            "'>P" + str(pos) + "</div>"
            "<div style='"
            "font-size:12px;"
            "font-weight:700;"
            "color:" + col + ";"
            "letter-spacing:5px;"
            "text-transform:uppercase;"
            "opacity:0.75;"
            "margin-bottom:36px;"
            "'>" + label + "</div>"
            "<div style='"
            "display:flex;"
            "justify-content:center;"
            "gap:40px;"
            "padding-top:24px;"
            "border-top:1px solid rgba(255,255,255,0.05);"
            "'>"
            "<div>"
            "<div style='font-size:10px;color:#333;letter-spacing:2px;text-transform:uppercase;margin-bottom:5px;'>Driver</div>"
            "<div style='font-size:14px;font-weight:600;color:white;'>" + driver.upper() + "</div>"
            "</div>"
            "<div>"
            "<div style='font-size:10px;color:#333;letter-spacing:2px;text-transform:uppercase;margin-bottom:5px;'>Constructor</div>"
            "<div style='font-size:14px;font-weight:600;color:white;'>" + constructor.upper() + "</div>"
            "</div>"
            "<div>"
            "<div style='font-size:10px;color:#333;letter-spacing:2px;text-transform:uppercase;margin-bottom:5px;'>Circuit</div>"
            "<div style='font-size:14px;font-weight:600;color:white;'>" + circuit.upper() + "</div>"
            "</div>"
            "<div>"
            "<div style='font-size:10px;color:#333;letter-spacing:2px;text-transform:uppercase;margin-bottom:5px;'>Grid</div>"
            "<div style='font-size:14px;font-weight:600;color:white;'>P" + str(grid) + "</div>"
            "</div>"
            "</div>"
            "</div>"
        )
        st.markdown(card, unsafe_allow_html=True)

        bar_w = str(ppct) + "%"
        bottom = (
            "<div style='display:flex;gap:12px;margin-top:12px;'>"
            "<div style='"
            "flex:1;"
            "background:rgba(255,255,255,0.025);"
            "border:1px solid rgba(255,255,255,0.06);"
            "border-radius:14px;"
            "padding:20px 24px;"
            "'>"
            "<div style='font-size:10px;color:#333;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;'>Podium probability</div>"
            "<div style='background:rgba(255,255,255,0.05);border-radius:99px;height:5px;margin-bottom:10px;'>"
            "<div style='background:" + col + ";width:" + bar_w + ";height:5px;border-radius:99px;box-shadow:0 0 12px " + glow + ";'></div>"
            "</div>"
            "<div style='font-size:28px;font-weight:800;color:" + col + ";'>" + str(ppct) + "%</div>"
            "</div>"
            "<div style='"
            "flex:1;"
            "background:rgba(255,255,255,0.025);"
            "border:1px solid rgba(255,255,255,0.06);"
            "border-radius:14px;"
            "padding:20px 24px;"
            "'>"
            "<div style='font-size:10px;color:#333;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;'>Conditions</div>"
            "<div style='font-size:28px;font-weight:800;color:white;'>" + weather + "</div>"
            "<div style='font-size:11px;color:#333;margin-top:5px;'>"
            + ("Standard prediction" if weather == "Dry" else "Higher variance expected")
            + "</div>"
            "</div>"
            "</div>"
        )
        st.markdown(bottom, unsafe_allow_html=True)

with tab2:
    df_raw = pd.read_csv('results.csv')
    df_raw['grid']           = pd.to_numeric(df_raw['grid'],           errors='coerce')
    df_raw['position_order'] = pd.to_numeric(df_raw['position_order'], errors='coerce')
    df_raw = df_raw.dropna(subset=['grid','position_order'])
    df_raw = df_raw[df_raw['grid'] > 0]

    pw    = df_raw[(df_raw['grid']==1) & (df_raw['position_order']==1)]
    tp    = len(df_raw[df_raw['grid']==1])
    ppct2 = round((len(pw)/tp)*100,1)
    tr    = df_raw['race_id'].nunique()
    td    = df_raw['driver_id'].nunique()

    stats = (
        "<div style='display:flex;gap:12px;margin-bottom:28px;'>"
        "<div style='flex:1;background:rgba(225,6,0,0.07);border:1px solid rgba(225,6,0,0.18);border-radius:14px;padding:20px 24px;'>"
        "<div style='font-size:10px;color:#555;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;'>Pole to win rate</div>"
        "<div style='font-size:36px;font-weight:900;color:#e10600;'>" + str(ppct2) + "%</div>"
        "<div style='font-size:11px;color:#333;margin-top:4px;'>of pole sitters win the race</div>"
        "</div>"
        "<div style='flex:1;background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:20px 24px;'>"
        "<div style='font-size:10px;color:#555;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;'>Total races</div>"
        "<div style='font-size:36px;font-weight:900;color:white;'>" + str(tr) + "</div>"
        "<div style='font-size:11px;color:#333;margin-top:4px;'>in the dataset</div>"
        "</div>"
        "<div style='flex:1;background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:20px 24px;'>"
        "<div style='font-size:10px;color:#555;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;'>Unique drivers</div>"
        "<div style='font-size:36px;font-weight:900;color:white;'>" + str(td) + "</div>"
        "<div style='font-size:11px;color:#333;margin-top:4px;'>in the dataset</div>"
        "</div>"
        "</div>"
    )
    st.markdown(stats, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div style='font-size:10px;color:#333;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;'>Grid vs average finish</div>", unsafe_allow_html=True)
        gf = df_raw[df_raw['grid']<=10].groupby('grid')['position_order'].mean().reset_index()
        fig1, ax1 = plt.subplots(figsize=(5,3))
        fig1.patch.set_facecolor('#0c0c1a')
        ax1.set_facecolor('#0c0c1a')
        ax1.bar(gf['grid'], gf['position_order'], color='#e10600', alpha=0.9, width=0.6)
        ax1.set_xlabel('Grid Position', color='#444', fontsize=9)
        ax1.set_ylabel('Avg Finish', color='#444', fontsize=9)
        ax1.tick_params(colors='#444', labelsize=8)
        for s in ax1.spines.values(): s.set_edgecolor('#1a1a2e')
        ax1.set_xticks(gf['grid'])
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()

    with c2:
        st.markdown("<div style='font-size:10px;color:#333;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;'>Top constructors by avg finish</div>", unsafe_allow_html=True)
        cf = df_raw.groupby('constructor_id')['position_order'].mean().sort_values().head(8).reset_index()
        colors = ['#e10600' if i==0 else '#1e1e30' for i in range(len(cf))]
        fig2, ax2 = plt.subplots(figsize=(5,3))
        fig2.patch.set_facecolor('#0c0c1a')
        ax2.set_facecolor('#0c0c1a')
        ax2.barh(cf['constructor_id'], cf['position_order'], color=colors, height=0.6)
        ax2.set_xlabel('Avg Finish (lower = better)', color='#444', fontsize=9)
        ax2.tick_params(colors='#444', labelsize=8)
        ax2.invert_yaxis()
        for s in ax2.spines.values(): s.set_edgecolor('#1a1a2e')
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

st.markdown("""
<div style="text-align:center;padding:32px 0 16px;color:#1e1e1e;font-size:10px;letter-spacing:2px;text-transform:uppercase;">
F1 Race Predictor &nbsp;·&nbsp; XGBoost &nbsp;·&nbsp; MAE 2.87 &nbsp;·&nbsp; Ergast F1 2010-2023
</div>
""", unsafe_allow_html=True)
