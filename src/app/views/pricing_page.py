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
        font-size: 1.2rem; color: #94A3B8; text-align: center; max-width: 800px; margin: 0 auto 3rem auto; line-height: 1.6;
    }

    .pricing-card {
        background: rgba(4, 22, 51, 0.7); border: 1px solid rgba(0,255,200,0.15);
        border-radius: 12px; padding: 40px 30px; text-align: center; transition: all 0.3s ease; height: 100%;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .pricing-card:hover { transform: translateY(-10px); border-color: #00ffc8; box-shadow: 0 0 20px rgba(0,255,200,0.2); }
    .pricing-card.premium { border: 2px solid #00d9ff; position: relative; overflow: hidden; }
    .pricing-card.premium::before { content: 'MOST POPULAR'; position: absolute; top: 15px; right: -35px; background: #00d9ff; color: #000814; padding: 5px 40px; transform: rotate(45deg); font-weight: bold; font-size: 0.7rem; }
    
    .p-title { font-size: 1.8rem; color: #FFFFFF; font-weight: bold; margin-bottom: 10px; }
    .p-price { font-size: 3.5rem; color: #00ffb3; font-weight: 900; margin-bottom: 5px; font-family: 'Orbitron', sans-serif; }
    .p-period { font-size: 0.9rem; color: #94A3B8; text-transform: uppercase; margin-bottom: 30px; }
    
    .p-features { text-align: left; list-style: none; padding: 0; margin-bottom: 30px; }
    .p-features li { padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05); color: #E2E8F0; font-size: 0.95rem; }
    .p-features li::before { content: '✓'; color: #00ffb3; font-weight: bold; margin-right: 10px; }

    .p-btn {
        background: transparent; border: 2px solid #00ffb3; color: #00ffb3; padding: 12px; border-radius: 8px; font-weight: bold; width: 100%; cursor: pointer; transition: 0.3s;
    }
    .p-btn:hover { background: #00ffb3; color: #000814; }
    .premium .p-btn { background: #00d9ff; border-color: #00d9ff; color: #000814; }
    .premium .p-btn:hover { background: transparent; color: #00d9ff; }

    .enterprise-footer { margin-top: 5rem; border-top: 1px solid rgba(0,255,200,0.15); padding-top: 3rem; padding-bottom: 3rem; margin-bottom: 5rem; }
    .footer-heading { color: #00d9ff; font-weight: bold; margin-bottom: 1rem; }
    .footer-link { color: #94A3B8; display: block; margin-bottom: 0.5rem; text-decoration: none; transition: color 0.3s ease; }
    .footer-link:hover { color: #00ffb3; }
</style>
""", unsafe_allow_html=True)

# ── HERO ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Transparent Pricing</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Scale your analytics infrastructure predictably. No hidden fees, no compute surprises.</div>', unsafe_allow_html=True)

# ── PRICING CARDS ───────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="pricing-card">
        <div>
            <div class="p-title">Starter</div>
            <div class="p-price">$999</div>
            <div class="p-period">per month</div>
            <ul class="p-features">
                <li>Basic Business Intelligence</li>
                <li>5 Admin Users</li>
                <li>Up to 10GB Data Storage</li>
                <li>Standard Dashboards</li>
                <li>Email Support</li>
            </ul>
        </div>
        <button class="p-btn">Start Free Trial</button>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="pricing-card premium">
        <div>
            <div class="p-title">Professional</div>
            <div class="p-price">$2,499</div>
            <div class="p-period">per month</div>
            <ul class="p-features">
                <li>Advanced Machine Learning</li>
                <li>Unlimited Viewers</li>
                <li>Up to 1TB Data Storage</li>
                <li>AI Predictive Forecasting</li>
                <li>Automated PDF Reporting</li>
                <li>Priority 24/7 Support</li>
            </ul>
        </div>
        <button class="p-btn">Upgrade to Pro</button>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="pricing-card">
        <div>
            <div class="p-title">Enterprise</div>
            <div class="p-price">Custom</div>
            <div class="p-period">contact sales</div>
            <ul class="p-features">
                <li>Dedicated Cloud Infrastructure</li>
                <li>Unlimited Everything</li>
                <li>Custom Data Connectors</li>
                <li>Row-Level Security (RLS)</li>
                <li>Advanced Governance & Audit</li>
                <li>Dedicated Account Manager</li>
            </ul>
        </div>
        <button class="p-btn">Contact Sales</button>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── FOOTER ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="enterprise-footer">
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 30px;">
        <div style="flex: 1; min-width: 250px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #00ffb3; font-family: 'Orbitron', sans-serif; margin-bottom: 1rem;">READYNEST</div>
            <p style="color: #94A3B8; font-size: 0.9rem; line-height: 1.6;">Enterprise Data Analytics Platform.<br>Transform Raw Data Into Enterprise Intelligence.</p>
        </div>
        <div style="flex: 1; min-width: 150px;">
            <div class="footer-heading">Platform</div>
            <a href="#" class="footer-link">Products</a><a href="#" class="footer-link">Services</a><a href="#" class="footer-link">Pricing</a>
        </div>
    </div>
    <div style="margin-top: 4rem; text-align: center; color: #64748B; font-size: 0.8rem; border-top: 1px solid rgba(0,255,200,0.1); padding-top: 2rem;">
        &copy; 2026 ReadyNest Enterprise Analytics. All rights reserved.
    </div>
</div>
""", unsafe_allow_html=True)
