import streamlit as st

st.set_page_config(page_title="Evaluación de Inversión - Modelo M/M/1", layout="wide")

st.title("Evaluación de Inversión: Comparación de Configuraciones M/M/1")
st.markdown("### Clínica privada - Ventanilla única de atención")

st.markdown("---")

# =========================
# FUNCIONES DEL MODELO
# =========================

def modelo_mm1(lam, mu):
    if lam >= mu:
        return None
    
    rho = lam / mu
    Lq = (lam**2) / (mu * (mu - lam))
    L = lam / (mu - lam)
    Wq = Lq / lam
    W = 1 / (mu - lam)
    
    return rho, Lq, L, Wq, W


# =========================
# ENTRADA DE DATOS
# =========================

st.sidebar.header("Parámetros del Sistema")

lambda_value = st.sidebar.number_input("Tasa de llegada λ (pacientes/hora)", value=20.0, min_value=0.1)

mu_A = st.sidebar.number_input("Tasa de servicio μ - Alternativa A", value=26.0, min_value=0.1)
mu_B = st.sidebar.number_input("Tasa de servicio μ - Alternativa B", value=32.0, min_value=0.1)

st.markdown("---")

# =========================
# CÁLCULO DE ALTERNATIVAS
# =========================

resultado_A = modelo_mm1(lambda_value, mu_A)
resultado_B = modelo_mm1(lambda_value, mu_B)

col1, col2 = st.columns(2)

# =========================
# ALTERNATIVA A
# =========================

with col1:
    st.subheader("Alternativa A")
    
    if resultado_A:
        rho_A, Lq_A, L_A, Wq_A, W_A = resultado_A
        
        st.write(f"Utilización (ρ): {rho_A:.4f}")
        st.write(f"Número promedio en cola (Lq): {Lq_A:.4f}")
        st.write(f"Número promedio en sistema (L): {L_A:.4f}")
        st.write(f"Tiempo promedio en cola (Wq): {Wq_A*60:.2f} minutos")
        st.write(f"Tiempo promedio en sistema (W): {W_A*60:.2f} minutos")
    else:
        st.error("Sistema inestable (λ ≥ μ)")

# =========================
# ALTERNATIVA B
# =========================

with col2:
    st.subheader("Alternativa B")
    
    if resultado_B:
        rho_B, Lq_B, L_B, Wq_B, W_B = resultado_B
        
        st.write(f"Utilización (ρ): {rho_B:.4f}")
        st.write(f"Número promedio en cola (Lq): {Lq_B:.4f}")
        st.write(f"Número promedio en sistema (L): {L_B:.4f}")
        st.write(f"Tiempo promedio en cola (Wq): {Wq_B*60:.2f} minutos")
        st.write(f"Tiempo promedio en sistema (W): {W_B*60:.2f} minutos")
    else:
        st.error("Sistema inestable (λ ≥ μ)")

# =========================
# MEJORA PORCENTUAL
# =========================

st.markdown("---")
st.subheader("Comparación Técnica")

if resultado_A and resultado_B:
    mejora = ((Wq_A - Wq_B) / Wq_A) * 100
    
    st.write(f"Mejora porcentual en tiempo de espera en cola: {mejora:.2f}%")
    
    if mejora > 0:
        st.success("La Alternativa B reduce significativamente el tiempo de espera.")
    else:
        st.warning("No existe mejora en la Alternativa B.")

# =========================
# INTERPRETACIÓN GERENCIAL
# =========================

st.markdown("---")
st.subheader("Interpretación Gerencial")

if resultado_A and resultado_B:
    if rho_A > 0.75:
        st.write("La Alternativa A opera con una utilización alta, lo que genera presión operativa.")
    
    if rho_B < rho_A:
        st.write("La Alternativa B reduce la utilización del sistema, generando mayor estabilidad.")
    
    st.write("Desde el punto de vista técnico, una mayor tasa de servicio reduce no linealmente los tiempos de espera.")
    
    st.write("Conclusión: Si el costo de digitalización es razonable, la Alternativa B es superior en términos de desempeño del sistema.")
