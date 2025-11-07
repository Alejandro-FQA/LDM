import numpy as np

# -----------------------------
# Semi-empirical LDM function
# -----------------------------
def ldm_model(element, params, A):
    """Semi-empirical liquid-drop model binding energy (MeV)."""
    # Get parameters
    Z = element.Z
    a_v = params["a_v"]
    a_s = params["a_s"]
    a_c = params["a_c"]
    a_a = params["a_a"]
    a_p = params["a_p"]

    # Volumne, Surface, Coulomb, Asymmetry terms
    V = a_v * A
    S = a_s * A ** (2 / 3)
    C = a_c * Z * (Z - 1) / A ** (1 / 3)
    Y = a_a * (A - 2 * Z) ** 2 / A

    # Pairing term: sign depends on even/odd nuclei
    # np.where(condition, value_if_true, value_if_false)
    sign = np.where(A % 2 == 0, 1 - 2 * (Z % 2), 0)
    P = a_p / np.sqrt(A) * sign   
    
    # Binding Energy
    BE = V - S - C - Y + P 

    # Binding energy per nucleon
    return BE / A 