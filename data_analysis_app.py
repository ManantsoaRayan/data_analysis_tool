import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
import warnings
warnings.filterwarnings('ignore')

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataLens · Analytics Studio",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme state ───────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

is_dark = st.session_state.dark_mode

# ── Theme tokens ──────────────────────────────────────────────────────────────
if is_dark:
    T = dict(
        bg="#0d0f14", surface="#161a24", border="#252b3b",
        accent="#00e5ff", accent2="#7b5ea7", text="#e2e8f0",
        muted="#64748b", success="#22d3a5", warn="#f59e0b",
        plot_bg="rgba(22,26,36,0.6)", plot_font="#e2e8f0",
        grid="#252b3b", badge_num_bg="rgba(0,229,255,.15)",
        badge_cat_bg="rgba(123,94,167,.25)", badge_cat_fg="#c4b5fd",
        insight_bg="linear-gradient(135deg,rgba(0,229,255,.06),rgba(123,94,167,.06))",
        tab_active_bg="#0d0f14",
    )
else:
    T = dict(
        bg="#f0f4f8", surface="#ffffff", border="#dde3ec",
        accent="#0077cc", accent2="#6d3eb5", text="#1a202c",
        muted="#64748b", success="#0f9c74", warn="#b45309",
        plot_bg="rgba(255,255,255,0.85)", plot_font="#1a202c",
        grid="#dde3ec", badge_num_bg="rgba(0,119,204,.12)",
        badge_cat_bg="rgba(109,62,181,.12)", badge_cat_fg="#6d3eb5",
        insight_bg="linear-gradient(135deg,rgba(0,119,204,.06),rgba(109,62,181,.06))",
        tab_active_bg="#f0f4f8",
    )

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="block-container"],
.main .block-container {{
    background: {T['bg']} !important;
    color: {T['text']} !important;
    font-family: 'DM Sans', sans-serif;
}}

[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {{
    background: {T['surface']} !important;
    border-right: 1px solid {T['border']};
}}

/* headings */
h1,h2,h3,h4 {{ font-family: 'Space Mono', monospace !important; color: {T['text']} !important; }}

/* native streamlit text */
p, label, .stMarkdown, .stText {{ color: {T['text']} !important; }}

/* metric card */
.metric-card {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    transition: border-color .2s, box-shadow .2s;
}}
.metric-card:hover {{ border-color: {T['accent']}; box-shadow: 0 0 12px {T['accent']}22; }}
.metric-value {{
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: {T['accent']};
    line-height: 1;
}}
.metric-label {{
    font-size: .8rem;
    color: {T['muted']};
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-top: 6px;
}}

/* section header */
.section-header {{
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    color: {T['accent']};
    border-bottom: 1px solid {T['border']};
    padding-bottom: 8px;
    margin: 24px 0 16px;
    letter-spacing: .05em;
}}

/* badges */
.badge {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .05em;
}}
.badge-num  {{ background: {T['badge_num_bg']}; color: {T['accent']}; }}
.badge-cat  {{ background: {T['badge_cat_bg']}; color: {T['badge_cat_fg']}; }}
.badge-date {{ background: rgba(34,211,165,.15); color: {T['success']}; }}

/* form controls */
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stSlider"] label {{ color: {T['muted']} !important; font-size:.82rem; }}

div[data-baseweb="select"] > div {{
    background: {T['surface']} !important;
    border-color: {T['border']} !important;
    color: {T['text']} !important;
}}

/* tabs */
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; background: transparent; }}
.stTabs [data-baseweb="tab"] {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 8px 8px 0 0;
    color: {T['muted']};
    font-family: 'Space Mono', monospace;
    font-size: .78rem;
}}
.stTabs [aria-selected="true"] {{
    background: {T['tab_active_bg']} !important;
    border-bottom-color: {T['tab_active_bg']} !important;
    color: {T['accent']} !important;
}}

/* dataframe */
.stDataFrame {{ border: 1px solid {T['border']}; border-radius: 8px; }}

/* insight box */
.insight-box {{
    background: {T['insight_bg']};
    border: 1px solid {T['border']};
    border-left: 3px solid {T['accent']};
    border-radius: 8px;
    padding: 14px 18px;
    margin: 8px 0;
    font-size: .88rem;
    color: {T['text']};
}}

/* theme toggle button */
.theme-toggle {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 20px;
    padding: 6px 14px;
    cursor: pointer;
    font-size: .82rem;
    color: {T['text']};
    font-family: 'DM Sans', sans-serif;
    transition: border-color .2s;
    margin-bottom: 8px;
}}
.theme-toggle:hover {{ border-color: {T['accent']}; }}
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ──────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=T['plot_bg'],
    font=dict(family="DM Sans", color=T['plot_font']),
    colorway=["#00e5ff","#7b5ea7","#22d3a5","#f59e0b","#f87171","#818cf8","#34d399","#fb923c"]
              if is_dark else
              ["#0077cc","#6d3eb5","#0f9c74","#b45309","#dc2626","#4f46e5","#047857","#c2410c"],
    xaxis=dict(gridcolor=T['grid'], zerolinecolor=T['grid']),
    yaxis=dict(gridcolor=T['grid'], zerolinecolor=T['grid']),
    margin=dict(l=10, r=10, t=40, b=10),
)

def styled_fig(fig, title=""):
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text=title, font=dict(size=14, family="Space Mono")))
    return fig

# ── Helpers ───────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(file) -> pd.DataFrame:
    return pd.read_csv(file, low_memory=False)

@st.cache_data(show_spinner=False)
def profile(df: pd.DataFrame):
    num_cols  = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols  = df.select_dtypes(include=["object","category","bool"]).columns.tolist()
    date_cols = df.select_dtypes(include=["datetime","datetimetz"]).columns.tolist()

    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    desc = df[num_cols].describe().T if num_cols else pd.DataFrame()
    desc["skew"]     = df[num_cols].skew().round(3) if num_cols else None
    desc["kurtosis"] = df[num_cols].kurtosis().round(3) if num_cols else None

    return num_cols, cat_cols, date_cols, missing, missing_pct, desc

def metric_card(val, label):
    return f"""<div class="metric-card">
        <div class="metric-value">{val}</div>
        <div class="metric-label">{label}</div>
    </div>"""

def insight(txt):
    st.markdown(f'<div class="insight-box">💡 {txt}</div>', unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"## 🔬 DataLens")
    st.markdown(f"<p style='color:{T['muted']};font-size:.82rem;margin-top:-8px'>Analytics Studio</p>",
                unsafe_allow_html=True)
    st.divider()

    # Theme toggle
    toggle_label = "☀️ Switch to Light" if is_dark else "🌙 Switch to Dark"
    if st.button(toggle_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.divider()
    uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
    st.markdown(f"<p style='color:{T['muted']};font-size:.78rem;text-align:center'>Drop any CSV · Instant analysis</p>",
                unsafe_allow_html=True)

# ── Landing ───────────────────────────────────────────────────────────────────
if uploaded is None:
    st.markdown(f"""
    <div style='text-align:center;padding:80px 20px'>
        <div style='font-family:Space Mono;font-size:3rem;color:{T['accent']};margin-bottom:8px'>DataLens</div>
        <div style='color:{T['muted']};font-size:1.1rem;margin-bottom:48px'>Drop your CSV in the sidebar and let the data speak</div>
        <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:700px;margin:0 auto'>
            <div class='metric-card'><div style='font-size:2rem'>📊</div><div class='metric-label'>Overview & Stats</div></div>
            <div class='metric-card'><div style='font-size:2rem'>📈</div><div class='metric-label'>Numerical Analysis</div></div>
            <div class='metric-card'><div style='font-size:2rem'>🏷️</div><div class='metric-label'>Categorical Analysis</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Load ──────────────────────────────────────────────────────────────────────
with st.spinner("Parsing data…"):
    df = load_data(uploaded)

num_cols, cat_cols, date_cols, missing, missing_pct, desc = profile(df)

# ═══════════════════════════════════════════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋  Overview", "📐  Numerical", "🏷️  Categorical", "⚠️  Data Quality", "📤  Export"])

# ══════════════════ TAB 1 · OVERVIEW ══════════════════════════════════════════
with tab1:
    st.markdown("### Dataset Overview")

    # top metrics
    cols = st.columns(5)
    cards = [
        (f"{df.shape[0]:,}", "Rows"),
        (f"{df.shape[1]:,}", "Columns"),
        (f"{len(num_cols)}", "Numerical"),
        (f"{len(cat_cols)}", "Categorical"),
        (f"{missing.sum():,}", "Missing Values"),
    ]
    for c, (v, l) in zip(cols, cards):
        c.markdown(metric_card(v, l), unsafe_allow_html=True)

    st.markdown('<div class="section-header">COLUMN SCHEMA</div>', unsafe_allow_html=True)

    schema_rows = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        nuniq = df[col].nunique()
        miss  = missing[col]
        miss_p= missing_pct[col]
        if col in num_cols:
            badge = '<span class="badge badge-num">NUM</span>'
        elif col in cat_cols:
            badge = '<span class="badge badge-cat">CAT</span>'
        elif col in date_cols:
            badge = '<span class="badge badge-date">DATE</span>'
        else:
            badge = f'<span class="badge badge-num">{dtype}</span>'
        schema_rows.append({"Column": col, "Type": badge, "Dtype": dtype, "Unique": nuniq,
                            "Missing": miss, "Missing %": f"{miss_p}%"})

    schema_df = pd.DataFrame(schema_rows)
    st.write(schema_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    st.markdown('<div class="section-header">DATA PREVIEW</div>', unsafe_allow_html=True)
    n_rows = st.slider("Rows to preview", 5, min(100, len(df)), 10)
    st.dataframe(df.head(n_rows), use_container_width=True)

    if num_cols:
        st.markdown('<div class="section-header">DESCRIPTIVE STATISTICS</div>', unsafe_allow_html=True)
        st.dataframe(desc.style.format(precision=3), use_container_width=True)

    # quick dtype chart
    dtype_counts = {"Numerical": len(num_cols), "Categorical": len(cat_cols), "Date/Time": len(date_cols)}
    dtype_counts = {k: v for k, v in dtype_counts.items() if v}
    if dtype_counts:
        fig = px.pie(names=list(dtype_counts.keys()), values=list(dtype_counts.values()),
                     hole=0.55, color_discrete_sequence=["#00e5ff","#7b5ea7","#22d3a5"])
        fig = styled_fig(fig, "Column Type Distribution")
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════ TAB 2 · NUMERICAL ═════════════════════════════════════════
with tab2:
    if not num_cols:
        st.warning("No numerical columns detected.")
    else:
        # ── Correlation heatmap ──
        st.markdown('<div class="section-header">CORRELATION HEATMAP</div>', unsafe_allow_html=True)
        corr_method = st.selectbox("Method", ["pearson","spearman","kendall"], key="corr_method")

        @st.cache_data(show_spinner=False)
        def get_corr(cols, method):
            return df[cols].corr(method=method).round(3)

        corr = get_corr(num_cols, corr_method)
        mask = np.triu(np.ones_like(corr, dtype=bool))
        corr_masked = corr.where(~mask)

        fig = go.Figure(go.Heatmap(
            z=corr_masked.values, x=corr.columns, y=corr.columns,
            colorscale=[[0,"#7b5ea7"],[0.5,"#0d0f14"],[1,"#00e5ff"]],
            zmid=0, text=corr_masked.round(2).values.astype(str),
            texttemplate="%{text}", hoverongaps=False,
            colorbar=dict(tickfont=dict(color="#e2e8f0")),
        ))
        fig = styled_fig(fig, f"{corr_method.capitalize()} Correlation Matrix")
        fig.update_layout(height=max(350, len(num_cols)*45))
        st.plotly_chart(fig, use_container_width=True)

        # strong correlations insight
        pairs = corr.abs().unstack().sort_values(ascending=False)
        pairs = pairs[pairs < 1].drop_duplicates()
        if not pairs.empty and pairs.iloc[0] >= 0.7:
            top = pairs.iloc[0]
            idx = pairs.index[0]
            insight(f"Strong correlation detected between <b>{idx[0]}</b> and <b>{idx[1]}</b> (r = {top:.2f})")

        # ── Histograms ──
        st.markdown('<div class="section-header">HISTOGRAMS</div>', unsafe_allow_html=True)
        hist_cols = st.multiselect("Select columns", num_cols, default=num_cols[:min(4,len(num_cols))], key="hist_sel")
        n_bins = st.slider("Bins", 10, 100, 30, key="hist_bins")

        if hist_cols:
            ncols_grid = min(2, len(hist_cols))
            nrows_grid = -(-len(hist_cols) // ncols_grid)
            fig = make_subplots(rows=nrows_grid, cols=ncols_grid,
                                subplot_titles=hist_cols, vertical_spacing=0.12)
            palette = ["#00e5ff","#7b5ea7","#22d3a5","#f59e0b","#f87171","#818cf8"]
            for i, col in enumerate(hist_cols):
                r, c = divmod(i, ncols_grid)
                vals = df[col].dropna()
                fig.add_trace(go.Histogram(x=vals, nbinsx=n_bins, name=col,
                                           marker_color=palette[i % len(palette)],
                                           opacity=0.85), row=r+1, col=c+1)
            fig = styled_fig(fig, "Distribution Histograms")
            fig.update_layout(showlegend=False, height=300*nrows_grid)
            fig.update_xaxes(gridcolor="#252b3b")
            fig.update_yaxes(gridcolor="#252b3b")
            st.plotly_chart(fig, use_container_width=True)

        # ── Box plots ──
        st.markdown('<div class="section-header">BOX PLOTS</div>', unsafe_allow_html=True)
        box_cols = st.multiselect("Select columns", num_cols, default=num_cols[:min(6,len(num_cols))], key="box_sel")
        color_by = st.selectbox("Color by (optional)", ["None"] + cat_cols, key="box_color")

        if box_cols:
            color_arg = None if color_by == "None" else color_by
            fig = go.Figure()
            palette = ["#00e5ff","#7b5ea7","#22d3a5","#f59e0b","#f87171","#818cf8"]
            if color_arg is None:
                for i, col in enumerate(box_cols):
                    fig.add_trace(go.Box(y=df[col].dropna(), name=col,
                                         marker_color=palette[i % len(palette)],
                                         boxmean=True, line_width=1.5))
            else:
                for i, col in enumerate(box_cols):
                    for j, grp in enumerate(df[color_arg].dropna().unique()):
                        fig.add_trace(go.Box(
                            y=df[df[color_arg]==grp][col].dropna(),
                            name=f"{col} · {grp}",
                            marker_color=palette[j % len(palette)],
                            boxmean=True, line_width=1.5,
                        ))
            fig = styled_fig(fig, "Box Plot Analysis")
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)

        # ── Scatter matrix ──
        st.markdown('<div class="section-header">SCATTER MATRIX (PAIRPLOT)</div>', unsafe_allow_html=True)
        scatter_cols = st.multiselect("Select columns (max 5)", num_cols,
                                       default=num_cols[:min(4,len(num_cols))], key="scatter_sel")
        scatter_color = st.selectbox("Color by", ["None"] + cat_cols, key="scatter_color")

        if scatter_cols and len(scatter_cols) >= 2:
            color_arg = None if scatter_color == "None" else scatter_color
            # FIXED
            _scatter_df = df[scatter_cols + ([color_arg] if color_arg else [])].dropna()
            sample = _scatter_df.sample(min(2000, len(_scatter_df)), random_state=42)
            
            fig = px.scatter_matrix(sample, dimensions=scatter_cols, color=color_arg,
                                    opacity=0.5, color_discrete_sequence=["#00e5ff","#7b5ea7","#22d3a5","#f59e0b"])
            fig = styled_fig(fig, "Scatter Matrix")
            fig.update_traces(diagonal_visible=False, marker=dict(size=3))
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        elif scatter_cols:
            st.info("Select at least 2 columns.")

        # ── Outlier scatter plots ──
        st.markdown('<div class="section-header">OUTLIER VISUALISATION</div>', unsafe_allow_html=True)
        out_method_sel = st.radio("Detection method", ["IQR", "Z-Score", "Both (union)"],
                                   horizontal=True, key="scatter_out_method")
        c1, c2 = st.columns(2)
        with c1:
            iqr_mult_sc = st.slider("IQR multiplier", 1.0, 3.0, 1.5, 0.1, key="sc_iqr_mult")
        with c2:
            z_thresh_sc = st.slider("Z-Score threshold", 2.0, 4.0, 3.0, 0.1, key="sc_z_thresh")

        out_x = st.selectbox("X axis", num_cols, key="out_x")
        out_y = st.selectbox("Y axis", num_cols, index=min(1, len(num_cols)-1), key="out_y")

        plot_df = df[[out_x, out_y]].dropna().copy()

        def is_outlier_iqr(series, mult):
            q1, q3 = series.quantile(.25), series.quantile(.75)
            iqr = q3 - q1
            return (series < q1 - mult*iqr) | (series > q3 + mult*iqr)

        def is_outlier_z(series, thresh):
            std = series.std()
            if std == 0: return pd.Series(False, index=series.index)
            return np.abs((series - series.mean()) / std) > thresh

        if out_method_sel == "IQR":
            mask = is_outlier_iqr(plot_df[out_x], iqr_mult_sc) | is_outlier_iqr(plot_df[out_y], iqr_mult_sc)
            method_label = f"IQR ×{iqr_mult_sc}"
        elif out_method_sel == "Z-Score":
            mask = is_outlier_z(plot_df[out_x], z_thresh_sc) | is_outlier_z(plot_df[out_y], z_thresh_sc)
            method_label = f"Z-Score >{z_thresh_sc}"
        else:
            mask = (is_outlier_iqr(plot_df[out_x], iqr_mult_sc) | is_outlier_iqr(plot_df[out_y], iqr_mult_sc) |
                    is_outlier_z(plot_df[out_x], z_thresh_sc)    | is_outlier_z(plot_df[out_y], z_thresh_sc))
            method_label = f"IQR ×{iqr_mult_sc} ∪ Z>{z_thresh_sc}"

        plot_df["_outlier"] = mask

        normal_pts = plot_df[~mask]
        outlier_pts = plot_df[mask]

        n_out = mask.sum()
        n_total = len(plot_df)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=normal_pts[out_x], y=normal_pts[out_y],
            mode="markers",
            name=f"Normal ({n_total - n_out:,})",
            marker=dict(color=T['accent'], size=5, opacity=0.55),
        ))
        fig.add_trace(go.Scatter(
            x=outlier_pts[out_x], y=outlier_pts[out_y],
            mode="markers",
            name=f"Outlier ({n_out:,})",
            marker=dict(color="#f87171", size=8, opacity=0.9,
                        line=dict(width=1, color="#ffffff")),
        ))
        fig = styled_fig(fig, f"Outliers: {out_x} vs {out_y}  [{method_label}]")
        fig.update_layout(height=480, xaxis_title=out_x, yaxis_title=out_y,
                          legend=dict(orientation="h", y=1.08))
        st.plotly_chart(fig, use_container_width=True)

        pct = n_out / n_total * 100
        insight(f"<b>{n_out:,}</b> outlier points ({pct:.1f}%) detected in the <b>{out_x}</b> vs <b>{out_y}</b> "
                f"scatter using <b>{method_label}</b>.")

        # Per-column outlier strip plots
        st.markdown('<div class="section-header">PER-COLUMN OUTLIER STRIP PLOTS</div>', unsafe_allow_html=True)
        strip_cols = st.multiselect("Select columns", num_cols,
                                     default=num_cols[:min(4, len(num_cols))], key="strip_cols")

        if strip_cols:
            ncols_g = min(2, len(strip_cols))
            nrows_g = -(-len(strip_cols) // ncols_g)
            fig = make_subplots(rows=nrows_g, cols=ncols_g,
                                subplot_titles=strip_cols, vertical_spacing=0.14)

            for i, col in enumerate(strip_cols):
                r, c = divmod(i, ncols_g)
                s = df[col].dropna()

                if out_method_sel == "IQR":
                    col_mask = is_outlier_iqr(s, iqr_mult_sc)
                elif out_method_sel == "Z-Score":
                    col_mask = is_outlier_z(s, z_thresh_sc)
                else:
                    col_mask = is_outlier_iqr(s, iqr_mult_sc) | is_outlier_z(s, z_thresh_sc)

                normal_v  = s[~col_mask]
                outlier_v = s[col_mask]

                fig.add_trace(go.Box(
                    y=s, name=col, boxpoints=False,
                    marker_color=T['accent'], line_width=1.5,
                    showlegend=False,
                ), row=r+1, col=c+1)

                # jittered strip for normals
                jitter_n = np.random.uniform(-0.2, 0.2, size=len(normal_v))
                fig.add_trace(go.Scatter(
                    x=jitter_n, y=normal_v.values,
                    mode="markers", name="Normal",
                    marker=dict(color=T['accent'], size=3, opacity=0.4),
                    showlegend=(i == 0),
                ), row=r+1, col=c+1)

                # outliers in red
                jitter_o = np.random.uniform(-0.2, 0.2, size=len(outlier_v))
                fig.add_trace(go.Scatter(
                    x=jitter_o, y=outlier_v.values,
                    mode="markers", name="Outlier",
                    marker=dict(color="#f87171", size=7, opacity=0.9,
                                line=dict(width=1, color="#ffffff")),
                    showlegend=(i == 0),
                ), row=r+1, col=c+1)

            fig = styled_fig(fig, f"Strip + Box  [{method_label}]")
            fig.update_layout(height=350*nrows_g, showlegend=True,
                              legend=dict(orientation="h", y=1.02))
            fig.update_xaxes(showticklabels=False)
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════ TAB 3 · CATEGORICAL ═══════════════════════════════════════
with tab3:
    if not cat_cols:
        st.warning("No categorical columns detected.")
    else:
        st.markdown('<div class="section-header">CATEGORICAL OVERVIEW</div>', unsafe_allow_html=True)

        # summary table
        rows = []
        for col in cat_cols:
            vc = df[col].value_counts()
            rows.append({
                "Column": col,
                "Unique Values": df[col].nunique(),
                "Top Value": vc.index[0] if len(vc) else "—",
                "Top Freq": int(vc.iloc[0]) if len(vc) else 0,
                "Top %": f"{vc.iloc[0]/len(df)*100:.1f}%" if len(vc) else "—",
                "Missing": int(missing[col]),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        # ── Count plots ──
        st.markdown('<div class="section-header">COUNT PLOTS</div>', unsafe_allow_html=True)
        cat_sel = st.selectbox("Select column", cat_cols, key="cat_count")
        top_n   = st.slider("Top N categories", 5, 50, 15, key="cat_topn")
        sort_by  = st.radio("Sort by", ["Frequency ↓","Frequency ↑","Alphabetical"], horizontal=True, key="cat_sort")
        color_sel = st.selectbox("Stack / group by", ["None"] + cat_cols, key="cat_color")

        vc = df[cat_sel].value_counts()
        if sort_by == "Frequency ↓":   vc = vc.head(top_n)
        elif sort_by == "Frequency ↑": vc = vc.sort_values().tail(top_n)
        else:                          vc = vc.sort_index().head(top_n)

        categories = vc.index.tolist()

        if color_sel == "None":
            fig = go.Figure(go.Bar(
                x=categories, y=vc.values,
                marker_color="#00e5ff", opacity=0.85,
                text=vc.values, textposition="outside",
            ))
        else:
            sub = df[df[cat_sel].isin(categories)]
            cross = pd.crosstab(sub[cat_sel], sub[color_sel])
            cross = cross.loc[categories]
            palette = ["#00e5ff","#7b5ea7","#22d3a5","#f59e0b","#f87171","#818cf8","#34d399","#fb923c"]
            fig = go.Figure()
            for i, grp in enumerate(cross.columns[:8]):
                fig.add_trace(go.Bar(name=str(grp), x=cross.index, y=cross[grp],
                                     marker_color=palette[i % len(palette)]))
            fig.update_layout(barmode="stack")

        fig = styled_fig(fig, f"Value Counts · {cat_sel}")
        fig.update_layout(height=420, xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

        # most common insight
        if len(vc):
            insight(f"<b>{vc.index[0]}</b> is the most frequent value in <b>{cat_sel}</b> "
                    f"({int(vc.iloc[0]):,} occurrences, {vc.iloc[0]/len(df)*100:.1f}%)")

        # ── Pie / Donut ──
        st.markdown('<div class="section-header">PIE / DONUT CHART</div>', unsafe_allow_html=True)
        pie_col = st.selectbox("Select column", cat_cols, key="pie_col")
        pie_top = st.slider("Top N", 3, 20, 8, key="pie_topn")
        pie_hole = st.slider("Hole size", 0.0, 0.8, 0.45, key="pie_hole")

        vc_pie = df[pie_col].value_counts().head(pie_top)
        other  = df[pie_col].value_counts().iloc[pie_top:].sum()
        if other > 0:
            vc_pie["Other"] = other

        fig = px.pie(names=vc_pie.index, values=vc_pie.values, hole=pie_hole,
                     color_discrete_sequence=["#00e5ff","#7b5ea7","#22d3a5","#f59e0b","#f87171","#818cf8","#34d399","#fb923c","#94a3b8"])
        fig = styled_fig(fig, f"Distribution · {pie_col}")
        fig.update_traces(textinfo="percent+label", textfont_size=11)
        st.plotly_chart(fig, use_container_width=True)

        # ── Cross-tab heatmap ──
        st.markdown('<div class="section-header">CROSS-TABULATION HEATMAP</div>', unsafe_allow_html=True)
        if len(cat_cols) >= 2:
            col_a = st.selectbox("Row column", cat_cols, key="cross_a")
            col_b = st.selectbox("Col column", [c for c in cat_cols if c != col_a], key="cross_b")
            top_a = st.slider("Top N rows", 3, 20, 8, key="cross_topn_a")
            top_b = st.slider("Top N cols", 3, 20, 8, key="cross_topn_b")

            top_a_vals = df[col_a].value_counts().head(top_a).index
            top_b_vals = df[col_b].value_counts().head(top_b).index
            cross = pd.crosstab(df[col_a], df[col_b])
            cross = cross.loc[cross.index.isin(top_a_vals), cross.columns.isin(top_b_vals)]

            fig = go.Figure(go.Heatmap(
                z=cross.values, x=cross.columns.astype(str), y=cross.index.astype(str),
                colorscale=[[0,"#0d0f14"],[0.5,"#7b5ea7"],[1,"#00e5ff"]],
                text=cross.values, texttemplate="%{text}",
                colorbar=dict(tickfont=dict(color="#e2e8f0")),
            ))
            fig = styled_fig(fig, f"Cross-Tab: {col_a} × {col_b}")
            fig.update_layout(height=max(300, len(top_a_vals)*40))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 categorical columns for cross-tab.")

        # ── Num by category box ──
        if num_cols:
            st.markdown('<div class="section-header">NUMERICAL BY CATEGORY</div>', unsafe_allow_html=True)
            num_sel2 = st.selectbox("Numerical column", num_cols, key="num_by_cat")
            cat_sel2 = st.selectbox("Group by", cat_cols, key="grp_cat")
            top_grp  = st.slider("Top N groups", 3, 20, 8, key="grp_topn")

            top_grps = df[cat_sel2].value_counts().head(top_grp).index
            sub = df[df[cat_sel2].isin(top_grps)]

            palette = ["#00e5ff","#7b5ea7","#22d3a5","#f59e0b","#f87171","#818cf8","#34d399","#fb923c"]

            def hex_to_rgba(hex_color, alpha=0.15):
                h = hex_color.lstrip("#")
                r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
                return f"rgba({r},{g},{b},{alpha})"

            fig = go.Figure()
            for i, grp in enumerate(top_grps):
                vals = sub[sub[cat_sel2] == grp][num_sel2].dropna()
                color = palette[i % len(palette)]
                fig.add_trace(go.Violin(y=vals, name=str(grp),
                                        line_color=color,
                                        fillcolor=hex_to_rgba(color),
                                        box_visible=True, meanline_visible=True))
            fig = styled_fig(fig, f"{num_sel2} by {cat_sel2}")
            fig.update_layout(height=450, showlegend=True, violingap=0.2)
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════ TAB 4 · DATA QUALITY ══════════════════════════════════════
with tab4:
    st.markdown("### Data Quality Report")

    total_cells = df.shape[0] * df.shape[1]
    total_missing = missing.sum()
    completeness = (1 - total_missing / total_cells) * 100

    cols4 = st.columns(4)
    cards4 = [
        (f"{completeness:.1f}%", "Completeness"),
        (f"{total_missing:,}", "Missing Cells"),
        (f"{df.duplicated().sum():,}", "Duplicate Rows"),
        (f"{df.shape[0]:,}", "Total Rows"),
    ]
    for c, (v, l) in zip(cols4, cards4):
        c.markdown(metric_card(v, l), unsafe_allow_html=True)

    # ── Missing values bar ──
    st.markdown('<div class="section-header">MISSING VALUES BY COLUMN</div>', unsafe_allow_html=True)
    miss_df = pd.DataFrame({"Column": missing.index, "Missing": missing.values,
                             "Pct": missing_pct.values}).query("Missing > 0").sort_values("Pct", ascending=True)

    if miss_df.empty:
        insight("🎉 No missing values found — dataset is complete!")
    else:
        fig = go.Figure(go.Bar(
            x=miss_df["Pct"], y=miss_df["Column"], orientation="h",
            text=miss_df["Pct"].apply(lambda x: f"{x:.1f}%"), textposition="outside",
            marker=dict(
                color=miss_df["Pct"],
                colorscale=[[0,"#22d3a5"],[0.5,"#f59e0b"],[1,"#f87171"]],
                showscale=True,
                colorbar=dict(title="Missing %", tickfont=dict(color="#e2e8f0")),
            ),
        ))
        fig = styled_fig(fig, "Missing Values (%)")
        fig.update_layout(height=max(300, len(miss_df)*28), xaxis_title="Missing %")
        st.plotly_chart(fig, use_container_width=True)

        worst = miss_df.iloc[-1]
        insight(f"Column <b>{worst['Column']}</b> has the highest missingness: {worst['Pct']:.1f}%")

    # ── Missing heatmap (sample) ──
    if not miss_df.empty:
        st.markdown('<div class="section-header">MISSINGNESS PATTERN (SAMPLE)</div>', unsafe_allow_html=True)
        miss_cols = miss_df["Column"].tolist()
        sample_size = min(200, len(df))
        samp = df[miss_cols].sample(sample_size, random_state=42).isnull().astype(int)

        fig = go.Figure(go.Heatmap(
            z=samp.T.values, x=list(range(sample_size)), y=miss_cols,
            colorscale=[[0,"#161a24"],[1,"#f87171"]],
            showscale=False,
        ))
        fig = styled_fig(fig, f"Missingness Pattern (sample of {sample_size} rows)")
        fig.update_layout(height=max(250, len(miss_cols)*22),
                          xaxis_title="Row index (sampled)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    # ── Outlier summary ──
    if num_cols:
        st.markdown('<div class="section-header">OUTLIER DETECTION</div>', unsafe_allow_html=True)

        out_method = st.radio("Detection method", ["IQR", "Z-Score", "Both"], horizontal=True, key="dq_out_method")
        zscore_thresh = st.slider("Z-Score threshold", 2.0, 4.0, 3.0, 0.1, key="dq_zscore_thresh") \
            if out_method in ["Z-Score", "Both"] else 3.0
        iqr_mult = st.slider("IQR multiplier", 1.0, 3.0, 1.5, 0.1, key="dq_iqr_mult") \
            if out_method in ["IQR", "Both"] else 1.5

        outlier_rows = []
        for col in num_cols:
            s = df[col].dropna()
            q1, q3 = s.quantile(.25), s.quantile(.75)
            iqr = q3 - q1
            n_iqr = int(((s < q1 - iqr_mult*iqr) | (s > q3 + iqr_mult*iqr)).sum())

            mean, std = s.mean(), s.std()
            n_z = int((np.abs((s - mean) / std) > zscore_thresh).sum()) if std > 0 else 0

            row = {"Column": col,
                   "Q1": round(q1,3), "Q3": round(q3,3), "IQR": round(iqr,3)}
            if out_method in ["IQR", "Both"]:
                row["IQR Outliers"] = n_iqr
                row["IQR %"] = f"{n_iqr/len(df)*100:.2f}%"
            if out_method in ["Z-Score", "Both"]:
                row["Mean"] = round(mean,3)
                row["Std"] = round(std,3)
                row["Z Outliers"] = n_z
                row["Z %"] = f"{n_z/len(df)*100:.2f}%"
            if out_method == "Both":
                n_either = int(((s < q1 - iqr_mult*iqr) | (s > q3 + iqr_mult*iqr) |
                                (np.abs((s - mean)/std) > zscore_thresh if std > 0 else False)).sum())
                row["Either Outliers"] = n_either
            outlier_rows.append(row)

        out_df = pd.DataFrame(outlier_rows)
        sort_col = "IQR Outliers" if "IQR Outliers" in out_df.columns else "Z Outliers"
        out_df = out_df.sort_values(sort_col, ascending=False)
        st.dataframe(out_df, use_container_width=True)

        # comparison bar chart
        if out_method == "Both" and len(num_cols) > 0:
            fig = go.Figure()
            fig.add_trace(go.Bar(name="IQR Outliers", x=out_df["Column"],
                                  y=out_df["IQR Outliers"], marker_color=T['accent'], opacity=0.85))
            fig.add_trace(go.Bar(name="Z-Score Outliers", x=out_df["Column"],
                                  y=out_df["Z Outliers"], marker_color="#f87171", opacity=0.85))
            fig = styled_fig(fig, f"IQR vs Z-Score Outlier Count (IQR×{iqr_mult}, Z>{zscore_thresh})")
            fig.update_layout(barmode="group", height=380, xaxis_tickangle=-30)
            st.plotly_chart(fig, use_container_width=True)

        worst = out_df.iloc[0]
        if out_method != "Z-Score" and worst.get("IQR Outliers", 0) > 0:
            insight(f"<b>{worst['Column']}</b> has the most IQR outliers: "
                    f"{worst['IQR Outliers']:,} rows ({worst['IQR %']})")
        if out_method != "IQR" and worst.get("Z Outliers", 0) > 0:
            insight(f"<b>{worst['Column']}</b> has the most Z-score outliers: "
                    f"{worst['Z Outliers']:,} rows ({worst['Z %']})")

    # ── Duplicate rows ──
    st.markdown('<div class="section-header">DUPLICATE ROWS</div>', unsafe_allow_html=True)
    n_dup = df.duplicated().sum()
    if n_dup == 0:
        insight("No duplicate rows found.")
    else:
        st.warning(f"⚠️ {n_dup:,} duplicate rows detected ({n_dup/len(df)*100:.2f}% of dataset)")
        if st.button("Show duplicate rows"):
            st.dataframe(df[df.duplicated(keep=False)].head(50), use_container_width=True)

# ══════════════════ TAB 5 · EXPORT ════════════════════════════════════════════
with tab5:
    st.markdown("### Export & Download")
    st.markdown("<p style='color:#64748b;font-size:.9rem'>Download your data, statistics, or a full EDA report in multiple formats.</p>", unsafe_allow_html=True)

    # ── helpers ──────────────────────────────────────────────────────────────
    def df_to_csv_bytes(dataframe):
        return dataframe.to_csv(index=False).encode("utf-8")

    def df_to_excel_bytes(sheets: dict) -> bytes:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            for sheet_name, frame in sheets.items():
                frame.to_excel(writer, sheet_name=sheet_name[:31], index=True)
        return buf.getvalue()

    def build_html_report(dataframe, num_c, cat_c, desc_df, miss, miss_pct, fname) -> str:
        import plotly.io as pio

        PALETTE = ["#00e5ff","#7b5ea7","#22d3a5","#f59e0b","#f87171","#818cf8","#34d399","#fb923c"]
        RPT_LAYOUT = dict(
            paper_bgcolor="#161a24", plot_bgcolor="#1a1f2e",
            font=dict(family="DM Sans", color="#e2e8f0", size=12),
            colorway=PALETTE,
            xaxis=dict(gridcolor="#252b3b", zerolinecolor="#252b3b"),
            yaxis=dict(gridcolor="#252b3b", zerolinecolor="#252b3b"),
            margin=dict(l=40, r=40, t=50, b=40),
        )

        def rpt_fig(fig, title="", h=420):
            fig.update_layout(**RPT_LAYOUT,
                              title=dict(text=title, font=dict(size=13, family="Space Mono, monospace")),
                              height=h)
            return fig

        def fig_html(fig):
            return pio.to_html(fig, full_html=False, include_plotlyjs=False,
                               config={"responsive": True, "displayModeBar": True})

        def hex_to_rgba(hex_color, alpha=0.18):
            h = hex_color.lstrip("#")
            r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
            return f"rgba({r},{g},{b},{alpha})"

        def tbl(frame, max_rows=50):
            return frame.head(max_rows).to_html(classes="tbl", border=0, escape=True)

        # ── Stats ──────────────────────────────────────────────────────────────
        total_cells   = dataframe.shape[0] * dataframe.shape[1]
        total_missing = miss.sum()
        completeness  = (1 - total_missing / total_cells) * 100
        n_dup         = dataframe.duplicated().sum()

        # outliers table
        outlier_rows = []
        for col in num_c:
            q1, q3 = dataframe[col].quantile(.25), dataframe[col].quantile(.75)
            iqr = q3 - q1
            n_out = ((dataframe[col] < q1-1.5*iqr) | (dataframe[col] > q3+1.5*iqr)).sum()
            outlier_rows.append({"Column": col, "Outliers": int(n_out),
                                  "Outlier %": f"{n_out/len(dataframe)*100:.2f}%",
                                  "Q1": round(q1,3), "Q3": round(q3,3), "IQR": round(iqr,3)})
        out_df = pd.DataFrame(outlier_rows)

        # cat summary table
        cat_summary_rows = []
        for col in cat_c:
            vc = dataframe[col].value_counts()
            cat_summary_rows.append({
                "Column": col, "Unique": dataframe[col].nunique(),
                "Top Value": str(vc.index[0]) if len(vc) else "—",
                "Top Freq": int(vc.iloc[0]) if len(vc) else 0,
                "Top %": f"{vc.iloc[0]/len(dataframe)*100:.1f}%" if len(vc) else "—",
                "Missing": int(miss[col]),
            })
        cat_df = pd.DataFrame(cat_summary_rows)
        miss_tbl = pd.DataFrame({"Column": miss.index, "Missing": miss.values,
                                  "Missing %": miss_pct.values}).query("Missing > 0")

        # ── PLOTS ──────────────────────────────────────────────────────────────

        # 1. Correlation heatmap
        corr_plot_html = ""
        if len(num_c) >= 2:
            corr = dataframe[num_c].corr().round(3)
            mask = np.triu(np.ones_like(corr, dtype=bool))
            corr_masked = corr.where(~mask)
            fig = go.Figure(go.Heatmap(
                z=corr_masked.values, x=corr.columns, y=corr.columns,
                colorscale=[[0,"#7b5ea7"],[0.5,"#1a1f2e"],[1,"#00e5ff"]],
                zmid=0, text=corr_masked.round(2).values.astype(str),
                texttemplate="%{text}", hoverongaps=False,
                colorbar=dict(tickfont=dict(color="#e2e8f0")),
            ))
            rpt_fig(fig, "Correlation Heatmap (Pearson)", h=max(380, len(num_c)*45))
            corr_plot_html = fig_html(fig)

        # 2. Histograms — one subplot grid
        hist_plot_html = ""
        if num_c:
            cols_to_plot = num_c[:12]
            ncols_g = min(3, len(cols_to_plot))
            nrows_g = -(-len(cols_to_plot) // ncols_g)
            fig = make_subplots(rows=nrows_g, cols=ncols_g,
                                subplot_titles=cols_to_plot, vertical_spacing=0.1)
            for i, col in enumerate(cols_to_plot):
                r, c = divmod(i, ncols_g)
                vals = dataframe[col].dropna()
                fig.add_trace(go.Histogram(x=vals, nbinsx=30, name=col,
                                           marker_color=PALETTE[i % len(PALETTE)],
                                           opacity=0.85), row=r+1, col=c+1)
            rpt_fig(fig, "Histograms — Numerical Distributions", h=300*nrows_g)
            fig.update_layout(showlegend=False)
            fig.update_xaxes(gridcolor="#252b3b"); fig.update_yaxes(gridcolor="#252b3b")
            hist_plot_html = fig_html(fig)

        # 3. Box plots — all numerical columns
        box_plot_html = ""
        if num_c:
            fig = go.Figure()
            for i, col in enumerate(num_c):
                fig.add_trace(go.Box(
                    y=dataframe[col].dropna(), name=col,
                    marker_color=PALETTE[i % len(PALETTE)],
                    boxmean=True, line_width=1.5,
                ))
            rpt_fig(fig, "Box Plots — All Numerical Columns", h=460)
            box_plot_html = fig_html(fig)

        # 4. Count plots — top categorical columns (up to 6)
        count_plots_html = ""
        for col in cat_c[:6]:
            vc = dataframe[col].value_counts().head(15)
            fig = go.Figure(go.Bar(
                x=vc.index.astype(str), y=vc.values,
                marker_color=PALETTE[cat_c.index(col) % len(PALETTE)],
                text=vc.values, textposition="outside", opacity=0.88,
            ))
            rpt_fig(fig, f"Count Plot · {col}", h=360)
            fig.update_layout(xaxis_tickangle=-30)
            count_plots_html += f"<div class='plot-wrap'>{fig_html(fig)}</div>"

        # 5. Missing values bar
        missing_plot_html = ""
        if not miss_tbl.empty:
            miss_sorted = miss_tbl.sort_values("Missing %", ascending=True)
            fig = go.Figure(go.Bar(
                x=miss_sorted["Missing %"], y=miss_sorted["Column"], orientation="h",
                text=miss_sorted["Missing %"].apply(lambda x: f"{x:.1f}%"), textposition="outside",
                marker=dict(
                    color=miss_sorted["Missing %"],
                    colorscale=[[0,"#22d3a5"],[0.5,"#f59e0b"],[1,"#f87171"]],
                    showscale=False,
                ),
            ))
            rpt_fig(fig, "Missing Values by Column (%)", h=max(300, len(miss_sorted)*28))
            missing_plot_html = fig_html(fig)

        # ── Assemble HTML ──────────────────────────────────────────────────────
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>EDA Report — {fname}</title>
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#0d0f14;color:#e2e8f0;font-family:'DM Sans',sans-serif;padding:40px 60px;}}
  h1{{font-family:'Space Mono',monospace;color:#00e5ff;font-size:2rem;margin-bottom:4px}}
  h2{{font-family:'Space Mono',monospace;color:#00e5ff;font-size:1rem;margin:40px 0 14px;
      border-bottom:1px solid #252b3b;padding-bottom:7px;letter-spacing:.06em;text-transform:uppercase}}
  .sub{{color:#64748b;font-size:.85rem;margin-bottom:32px}}
  .metrics{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:24px}}
  .metrics3{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:32px}}
  .card{{background:#161a24;border:1px solid #252b3b;border-radius:10px;padding:16px;text-align:center}}
  .card .val{{font-family:'Space Mono',monospace;font-size:1.5rem;color:#00e5ff;font-weight:700}}
  .card .lbl{{font-size:.7rem;color:#64748b;text-transform:uppercase;letter-spacing:.08em;margin-top:4px}}
  .tbl{{width:100%;border-collapse:collapse;font-size:.82rem;margin-bottom:8px}}
  .tbl th{{background:#161a24;color:#00e5ff;font-family:'Space Mono',monospace;
            font-size:.72rem;padding:8px 12px;text-align:left;border-bottom:1px solid #252b3b}}
  .tbl td{{padding:6px 12px;border-bottom:1px solid #1e2430;color:#cbd5e1}}
  .tbl tr:hover td{{background:#1a1f2e}}
  .insight{{background:linear-gradient(135deg,rgba(0,229,255,.06),rgba(123,94,167,.06));
             border:1px solid #252b3b;border-left:3px solid #00e5ff;
             border-radius:8px;padding:12px 16px;margin:10px 0;font-size:.85rem}}
  .plot-wrap{{background:#161a24;border:1px solid #252b3b;border-radius:10px;
              padding:12px;margin:12px 0;overflow:hidden}}
  .footer{{margin-top:48px;color:#64748b;font-size:.75rem;border-top:1px solid #252b3b;padding-top:14px}}
  @media print{{
    body{{background:#fff!important;color:#111!important;padding:20px 30px}}
    h1,h2{{color:#0070a0!important}}
    .card{{background:#f8fafc!important;border-color:#e2e8f0!important}}
    .card .val{{color:#0070a0!important}}
    .tbl th{{background:#f1f5f9!important;color:#0070a0!important}}
    .tbl td{{color:#334155!important}}
    .plot-wrap{{border-color:#e2e8f0!important;background:#f8fafc!important}}
  }}
</style>
</head>
<body>
<h1>📊 EDA Report</h1>
<p class="sub">File: <b>{fname}</b> &nbsp;·&nbsp; Generated by <b>DataLens Analytics Studio</b></p>

<h2>Dataset Overview</h2>
<div class="metrics">
  <div class="card"><div class="val">{dataframe.shape[0]:,}</div><div class="lbl">Rows</div></div>
  <div class="card"><div class="val">{dataframe.shape[1]:,}</div><div class="lbl">Columns</div></div>
  <div class="card"><div class="val">{len(num_c)}</div><div class="lbl">Numerical</div></div>
  <div class="card"><div class="val">{len(cat_c)}</div><div class="lbl">Categorical</div></div>
  <div class="card"><div class="val">{completeness:.1f}%</div><div class="lbl">Completeness</div></div>
</div>
<div class="metrics3">
  <div class="card"><div class="val">{total_missing:,}</div><div class="lbl">Missing Cells</div></div>
  <div class="card"><div class="val">{n_dup:,}</div><div class="lbl">Duplicate Rows</div></div>
  <div class="card"><div class="val">{dataframe.memory_usage(deep=True).sum()/1024/1024:.2f} MB</div><div class="lbl">Memory Usage</div></div>
</div>

<h2>Descriptive Statistics</h2>
{tbl(desc_df.round(4), 100) if not desc_df.empty else "<p style='color:#64748b;margin:8px 0'>No numerical columns.</p>"}

{'<h2>Correlation Heatmap</h2><div class="plot-wrap">' + corr_plot_html + '</div>' if corr_plot_html else ''}

{'<h2>Histograms — Distributions</h2><div class="plot-wrap">' + hist_plot_html + '</div>' if hist_plot_html else ''}

{'<h2>Box Plots</h2><div class="plot-wrap">' + box_plot_html + '</div>' if box_plot_html else ''}

{'<h2>Categorical Count Plots</h2>' + count_plots_html if count_plots_html else ''}

<h2>Categorical Summary</h2>
{tbl(cat_df, 100) if not cat_df.empty else "<p style='color:#64748b;margin:8px 0'>No categorical columns.</p>"}

<h2>Missing Values</h2>
{('<div class="plot-wrap">' + missing_plot_html + '</div>' + tbl(miss_tbl, 100)) if not miss_tbl.empty else "<div class='insight'>✅ No missing values — dataset is complete.</div>"}

<h2>Outlier Summary (IQR Method)</h2>
{tbl(out_df, 100) if not out_df.empty else "<p style='color:#64748b;margin:8px 0'>No numerical columns.</p>"}

<h2>Data Sample (first 20 rows)</h2>
{tbl(dataframe.head(20), 20)}

<p class="footer">Generated by DataLens Analytics Studio &nbsp;·&nbsp;
Print this page (Ctrl+P / Cmd+P) to save as PDF &nbsp;·&nbsp; All charts are interactive in browser</p>
</body></html>"""
        return html

    # ── Section: Data Exports ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">DATA EXPORTS</div>', unsafe_allow_html=True)

    fname = uploaded.name if uploaded else "dataset"

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("**📄 Raw CSV**")
        st.caption("Download the uploaded dataset as-is")
        st.download_button(
            label="⬇ Download CSV",
            data=df_to_csv_bytes(df),
            file_name=f"{fname.replace('.csv','')}_export.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col_b:
        st.markdown("**📊 Excel Workbook**")
        st.caption("Multiple sheets: data + stats + missing")
        sheets = {"Data": df.reset_index(drop=True)}
        if not desc.empty:
            sheets["Descriptive Stats"] = desc
        miss_sheet = pd.DataFrame({"Column": missing.index, "Missing": missing.values,
                                    "Missing %": missing_pct.values})
        sheets["Missing Values"] = miss_sheet.reset_index(drop=True)
        if num_cols:
            outlier_rows_exp = []
            for col in num_cols:
                q1, q3 = df[col].quantile(.25), df[col].quantile(.75)
                iqr = q3 - q1
                n_out = ((df[col] < q1-1.5*iqr) | (df[col] > q3+1.5*iqr)).sum()
                outlier_rows_exp.append({"Column": col, "Outliers": int(n_out),
                                          "Outlier %": round(n_out/len(df)*100,2)})
            sheets["Outliers"] = pd.DataFrame(outlier_rows_exp)
        excel_bytes = df_to_excel_bytes(sheets)
        st.download_button(
            label="⬇ Download Excel",
            data=excel_bytes,
            file_name=f"{fname.replace('.csv','')}_analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    with col_c:
        st.markdown("**📈 Statistics CSV**")
        st.caption("Descriptive stats table only")
        if not desc.empty:
            st.download_button(
                label="⬇ Download Stats CSV",
                data=df_to_csv_bytes(desc.reset_index()),
                file_name=f"{fname.replace('.csv','')}_stats.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.info("No numerical columns for stats export.")

    # ── Section: Report Exports ───────────────────────────────────────────────
    st.markdown('<div class="section-header">EDA REPORT</div>', unsafe_allow_html=True)

    col_d, col_e = st.columns(2)

    with col_d:
        st.markdown("**🌐 HTML Report**")
        st.caption("Full EDA report — open in browser, then print to PDF (Ctrl+P)")
        html_report = build_html_report(df, num_cols, cat_cols, desc, missing, missing_pct, fname)
        st.download_button(
            label="⬇ Download HTML Report",
            data=html_report.encode("utf-8"),
            file_name=f"{fname.replace('.csv','')}_eda_report.html",
            mime="text/html",
            use_container_width=True,
        )
        st.markdown("""<div class='insight-box'>
        💡 <b>To get a PDF:</b> Download the HTML, open it in your browser, then press
        <b>Ctrl+P</b> (or Cmd+P on Mac) → <i>Save as PDF</i>. The report includes
        print-friendly styles automatically.
        </div>""", unsafe_allow_html=True)

    with col_e:
        st.markdown("**👁 Report Preview**")
        st.caption("Preview the HTML report inline")
        if st.button("Generate Preview", use_container_width=True):
            html_report = build_html_report(df, num_cols, cat_cols, desc, missing, missing_pct, fname)
            b64 = base64.b64encode(html_report.encode()).decode()
            st.markdown(
                f'<iframe src="data:text/html;base64,{b64}" width="100%" height="700px" '
                f'style="border:1px solid #252b3b;border-radius:8px;background:#0d0f14"></iframe>',
                unsafe_allow_html=True,
            )

    # ── Section: Custom column export ─────────────────────────────────────────
    st.markdown('<div class="section-header">CUSTOM COLUMN EXPORT</div>', unsafe_allow_html=True)
    selected_cols = st.multiselect("Select columns to export", df.columns.tolist(),
                                    default=df.columns.tolist()[:min(5, len(df.columns))],
                                    key="custom_export_cols")
    row_limit = st.slider("Max rows", 100, len(df), min(10000, len(df)), step=100, key="custom_export_rows")

    if selected_cols:
        custom_df = df[selected_cols].head(row_limit)
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                label=f"⬇ Download {len(selected_cols)} cols · {row_limit:,} rows (CSV)",
                data=df_to_csv_bytes(custom_df),
                file_name=f"{fname.replace('.csv','')}_custom.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with c2:
            custom_excel = df_to_excel_bytes({"Custom Export": custom_df.reset_index(drop=True)})
            st.download_button(
                label=f"⬇ Download {len(selected_cols)} cols · {row_limit:,} rows (Excel)",
                data=custom_excel,
                file_name=f"{fname.replace('.csv','')}_custom.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        st.dataframe(custom_df.head(10), use_container_width=True)
    else:
        st.info("Select at least one column above.")
