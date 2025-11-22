import numpy as np
import pandas as pd
from scipy.stats import rayleigh
from sklearn.linear_model import LinearRegression
import streamlit as st


def preparar_features_target(df: pd.DataFrame):
    features = df[
        [
            "Presupuesto",
            "NumTrabajadores",
            "RetrasoInicioDias",
            "RetrasoFinalDias",
            "ProductividadPromedio",
        ]
    ]
    target = df["TotalErrores"]
    return features, target


@st.cache_data(show_spinner=False)
def entrenar_modelo(df_proyectos: pd.DataFrame) -> LinearRegression:
    features, target = preparar_features_target(df_proyectos)
    modelo = LinearRegression()
    modelo.fit(features, target)
    return modelo


def rayleigh_curve(total_defectos: float, duracion: int, sigma: float) -> pd.DataFrame:
    tiempo = np.linspace(0, duracion, num=duracion + 1)
    cdf = rayleigh.cdf(tiempo, scale=sigma)
    defectos_acumulados = total_defectos * cdf
    return pd.DataFrame({"Tiempo": tiempo, "DefectosAcumulados": defectos_acumulados})


def calcular_sigma(duracion: int, complejidad: str) -> float:
    base = max(duracion / 4, 1)
    factor = {"baja": 0.8, "media": 1.0, "alta": 1.3}.get(complejidad, 1.0)
    return base * factor
