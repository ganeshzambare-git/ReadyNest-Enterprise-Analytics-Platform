import streamlit as st

st.markdown("""
<style>
    /* Shared CSS for Platform Pages */
    .stApp { background-color: #000814; color: #E2E8F0; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { color: #FFFFFF !important; font-family: 'Orbitron', sans-serif; }
    
    .hero-title {
        font-size: 3.5rem; font-weight: 900;
        background: linear-gradient(90deg, #00ffb3, #00d9ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-top: 2rem; margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.2rem; color: #94A3B8; text-align: center; max-width: 800px; margin: 0 auto 4rem auto; line-height: 1.6;
    }

    .value-card {
        background: rgba(4, 22, 51, 0.7); border: 1px solid rgba(0,255,200,0.15);
        border-radius: 12px; padding: 30px; text-align: center; transition: all 0.3s ease; height: 100%;
    }
    .value-card:hover { transform: translateY(-5px); border-color: #00ffc8; box-shadow: 0 0 15px rgba(0,255,200,0.3); }
    .value-icon { font-size: 3rem; margin-bottom: 15px; }
    .value-title { color: #00ffb3; font-size: 1.5rem; margin-bottom: 10px; }

    .stat-container { display: flex; justify-content: center; gap: 40px; margin: 4rem 0; flex-wrap: wrap; }
    .stat-box { text-align: center; }
    .stat-val { font-size: 3.5rem; font-weight: bold; color: #00d9ff; }
    .stat-lbl { color: #94A3B8; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; }

    .enterprise-footer { margin-top: 5rem; border-top: 1px solid rgba(0,255,200,0.15); padding-top: 3rem; padding-bottom: 3rem; margin-bottom: 5rem; }
    .footer-heading { color: #00d9ff; font-weight: bold; margin-bottom: 1rem; }
    .footer-link { color: #94A3B8; display: block; margin-bottom: 0.5rem; text-decoration: none; transition: color 0.3s ease; }
    .footer-link:hover { color: #00ffb3; }
</style>
""", unsafe_allow_html=True)

# ── HERO ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">About ReadyNest</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Building the future of enterprise data intelligence. We believe that every organization should have the power to transform raw data into actionable, predictive business strategies instantly.</div>', unsafe_allow_html=True)

# ── STATS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-container">
    <div class="stat-box"><div class="stat-val">10B+</div><div class="stat-lbl">Data Points Processed</div></div>
    <div class="stat-box"><div class="stat-val">500+</div><div class="stat-lbl">Enterprise Clients</div></div>
    <div class="stat-box"><div class="stat-val">99.99%</div><div class="stat-lbl">Uptime SLA</div></div>
    <div class="stat-box"><div class="stat-val">24/7</div><div class="stat-lbl">Global Support</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: rgba(0,255,200,0.1);'><br>", unsafe_allow_html=True)

# ── CORE VALUES ─────────────────────────────────────────────────────────────────
st.markdown("<h2 style='text-align: center; color: #00d9ff; margin-bottom: 2rem;'>Our Core Pillars</h2>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="value-card">
        <div class="value-icon">🛡️</div>
        <div class="value-title">Zero-Trust Security</div>
        <p style="color: #94A3B8; font-size: 0.9rem;">Military-grade encryption, Row-Level Security, and automated compliance auditing for your most sensitive enterprise data.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="value-card">
        <div class="value-icon">🚀</div>
        <div class="value-title">Infinite Scale</div>
        <p style="color: #94A3B8; font-size: 0.9rem;">Built on cloud-native architectures capable of handling petabytes of unstructured and structured data simultaneously.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="value-card">
        <div class="value-icon">🤖</div>
        <div class="value-title">AI-First Engine</div>
        <p style="color: #94A3B8; font-size: 0.9rem;">We don't just display data; our proprietary AI models predict trends, forecast revenue, and prescribe business strategies.</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="value-card">
        <div class="value-icon">🏛️</div>
        <div class="value-title">Data Governance</div>
        <p style="color: #94A3B8; font-size: 0.9rem;">Complete metadata tracking, data lineage, and role-based access control ensuring total organizational visibility.</p>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="enterprise-footer">
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 30px;">
        <div style="flex: 1; min-width: 250px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #00ffb3; font-family: 'Orbitron', sans-serif; margin-bottom: 1rem;">READYNEST</div>
            <p style="color: #94A3B8; font-size: 0.9rem; line-height: 1.6;">Enterprise Data Analytics Platform.<br>Transform Raw Data Into Enterprise Intelligence.</p>
        </div>
        <div style="flex: 1; min-width: 150px;">
            <div class="footer-heading">Company</div>
            <a href="#" class="footer-link">About</a><a href="#" class="footer-link">Careers</a><a href="#" class="footer-link">Contact</a>
        </div>
        <div style="flex: 1; min-width: 150px;">
            <div class="footer-heading">Capabilities</div>
            <a href="#" class="footer-link">Machine Learning</a><a href="#" class="footer-link">Security</a><a href="#" class="footer-link">Governance</a>
        </div>
        <div style="flex: 1; min-width: 150px;">
            <div class="footer-heading">Social</div>
            <a href="#" class="footer-link">LinkedIn</a><a href="#" class="footer-link">Twitter</a><a href="#" class="footer-link">GitHub</a>
        </div>
    </div>
    <div style="margin-top: 4rem; text-align: center; color: #64748B; font-size: 0.8rem; border-top: 1px solid rgba(0,255,200,0.1); padding-top: 2rem;">
        &copy; 2026 ReadyNest Enterprise Analytics. All rights reserved.
    </div>
</div>
""", unsafe_allow_html=True)
