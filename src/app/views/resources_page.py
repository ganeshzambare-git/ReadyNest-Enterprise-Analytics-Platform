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

    .res-card {
        background: rgba(4, 22, 51, 0.4); border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px; overflow: hidden; transition: all 0.3s ease; height: 100%;
        display: flex; flex-direction: column;
    }
    .res-card:hover { transform: translateY(-5px); border-color: #00d9ff; box-shadow: 0 10px 20px rgba(0,217,255,0.1); }
    
    .res-img { height: 180px; background: linear-gradient(135deg, rgba(0,255,179,0.2), rgba(0,217,255,0.2)); display: flex; align-items: center; justify-content: center; font-size: 4rem; }
    .res-content { padding: 25px; flex: 1; display: flex; flex-direction: column; }
    .res-tag { display: inline-block; background: rgba(0,255,179,0.1); color: #00ffb3; font-size: 0.75rem; padding: 4px 10px; border-radius: 20px; font-weight: bold; text-transform: uppercase; margin-bottom: 15px; align-self: flex-start; }
    .res-title { color: #FFFFFF; font-size: 1.2rem; margin-bottom: 10px; font-weight: 600; }
    .res-desc { color: #94A3B8; font-size: 0.9rem; line-height: 1.5; flex: 1; }
    
    .res-link { color: #00d9ff; text-decoration: none; font-weight: bold; font-size: 0.9rem; margin-top: 15px; display: inline-block; }
    .res-link:hover { text-decoration: underline; }

    .enterprise-footer { margin-top: 5rem; border-top: 1px solid rgba(0,255,200,0.15); padding-top: 3rem; padding-bottom: 3rem; margin-bottom: 5rem; }
    .footer-heading { color: #00d9ff; font-weight: bold; margin-bottom: 1rem; }
    .footer-link { color: #94A3B8; display: block; margin-bottom: 0.5rem; text-decoration: none; transition: color 0.3s ease; }
    .footer-link:hover { color: #00ffb3; }
</style>
""", unsafe_allow_html=True)

# ── HERO ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Resource Center</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Explore case studies, whitepapers, and webinars to help you master enterprise data analytics.</div>', unsafe_allow_html=True)

# ── RESOURCES GRID ──────────────────────────────────────────────────────────────
st.markdown("<h3 style='margin-bottom: 2rem;'>Latest Publications</h3>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="res-card">
        <div class="res-img">📉</div>
        <div class="res-content">
            <span class="res-tag">Case Study</span>
            <div class="res-title">How TechCorp Reduced Churn by 24% Using AI</div>
            <div class="res-desc">Discover how implementing ReadyNest's predictive ML pipelines helped identify at-risk customers 30 days before they churned.</div>
            <a href="#" class="res-link">Read Case Study →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="res-card">
        <div class="res-img">📄</div>
        <div class="res-content">
            <span class="res-tag">Whitepaper</span>
            <div class="res-title">The Future of Zero-Trust Data Governance</div>
            <div class="res-desc">A deep dive into securing enterprise data lakes with Row-Level Security, audit trails, and automated compliance tracking.</div>
            <a href="#" class="res-link">Download Whitepaper →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="res-card">
        <div class="res-img">📺</div>
        <div class="res-content">
            <span class="res-tag">Webinar</span>
            <div class="res-title">Mastering Executive Reporting</div>
            <div class="res-desc">Watch our product team demonstrate how to automate complex 60-page PDF reports across thousands of data points instantly.</div>
            <a href="#" class="res-link">Watch On-Demand →</a>
        </div>
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
            <div class="footer-heading">Resources</div>
            <a href="#" class="footer-link">Blog</a><a href="#" class="footer-link">Whitepapers</a><a href="#" class="footer-link">Webinars</a>
        </div>
    </div>
    <div style="margin-top: 4rem; text-align: center; color: #64748B; font-size: 0.8rem; border-top: 1px solid rgba(0,255,200,0.1); padding-top: 2rem;">
        &copy; 2026 ReadyNest Enterprise Analytics. All rights reserved.
    </div>
</div>
""", unsafe_allow_html=True)
