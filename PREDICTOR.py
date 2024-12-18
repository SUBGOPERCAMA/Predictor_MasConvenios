import streamlit as st
import joblib
import pandas as pd

# Agregar el logo en la parte superior derecha
logo_url = "https://invadelab.cl/wp-content/uploads/2019/06/logo-ucchristus.png"

# HTML personalizado para el logo
st.markdown(
    f"""
    <style>
    .reportview-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .logo-container {{
        display: flex;
        justify-content: flex-end;
        width: 100%;
    }}
    .logo-container img {{
        width: 300px;
    }}
    </style>
    <div class="logo-container">
        <img src="{logo_url}" alt="logo">
    </div>
    """,
    unsafe_allow_html=True
)

# Cargar los modelos y transformaciones guardadas
rf_gain_model = joblib.load("optimized_rf_gain.pkl")
rf_stay_model = joblib.load("optimized_rf_stay.pkl")
label_encoder_diagnosis = joblib.load("label_encoder_diagnosis.pkl")
label_encoder_service = joblib.load("label_encoder_service.pkl")
label_encoder_convenio = joblib.load("label_encoder_convenio.pkl")
scaler = joblib.load("scaler.pkl")

# Lista de servicios de ingreso
services = [
    "NEONATOLOGIA",
    "MATERNIDAD",
    "INTERMEDIO NEUROLOGICO",
    "PLURIPENSIONADO 4º",
    "INTERMEDIO PEDIATRICO",
    "UCI PEDIATRICA",
    "PEDIATRIA",
    "INTENSIVO QX",
    "UNIDAD CORONARIA",
    "SERVICIO CIRUGIA",
    "6º RECUPERACION",
    "INTENSIVO MEDICO",
]

# Lista de diagnósticos completos
diagnoses = [
    "111202 - PH OPERACIONES DEL TRACTO URINARIO SUPERIOR W/CC",
"114123 - MH INFECCIONES DE RIÑÓN Y TRACTO URINARIO W/MCC",
"131303 - PH HISTERECTOMIA VAGINAL Y OTROS PROCEDIMIENTOS POR VIA VAGINAL W/MCC",
"146102 - PH CESÁREA W/CC",
"146103 - PH CESÁREA W/MCC",
"146122 - PH PARTO VAGINAL CON PROCED., EXCEPTO ESTERILIZACIÓN Y/O DILATACIÓN Y LEGRADO W/CC",
"146123 - PH PARTO VAGINAL CON PROCED., EXCEPTO ESTERILIZACIÓN Y/O DILATACIÓN Y LEGRADO W/MCC",
"146133 - PH PARTO VAGINAL W/MCC",
"158013 - PH NEONATO CON TRASPLANTE DE ÓRGANO U OXIGENACIÓN POR MEMBRANA EXTRACORPÓREA W/MCC",
"158033 - PH NEONATO, PESO AL NACER <1000 GR SIN PROCEDIMIENTO MAYOR W/MCC",
"158043 - PH NEONATO, PESO AL NACER 1000-1499 GR CON PROCEDIMIENTO MAYOR W/MCC",
"158073 - PH NEONATO, PESO AL NACER >2499 GR CON PROCEDIMIENTO MAYOR W/MCC",
"158083 - PH NEONATO, PESO AL NACER >2499 GR CON DISTRESS RESPIRATORIO W/MCC",
"158103 - MH NEONATO MUERTO O TRANSFERIDO A HOSPITAL DE AGUDOS, CON EDAD <5 DIAS AL ALTA W/MCC",
"158122 - MH NEONATO, PESO AL NACER 1500-1999 GR SIN PROCEDIMIENTO MAYOR W/CC",
"158123 - MH NEONATO, PESO AL NACER 1500-1999 GR SIN PROCEDIMIENTO MAYOR W/MCC",
"158132 - MH NEONATO, PESO AL NACER 2000-2499 GR SIN PROCEDIMIENTO MAYOR W/CC",
"158133 - MH NEONATO, PESO AL NACER 2000-2499 GR SIN PROCEDIMIENTO MAYOR W/MCC",
"158142 - MH NEONATO, PESO AL NACER >2499 GR CON ANOMALÍA MAYOR O PROBLEMAS HEREDITARIOS W/CC",
"158143 - MH NEONATO, PESO AL NACER >2499 GR CON ANOMALÍA MAYOR O PROBLEMAS HEREDITARIOS W/MCC",
"158153 - MH NEONATO, PESO AL NACER >2499 GR CON SÍNDROME DE ASPIRACIÓN W/MCC",
"158172 - MH NEONATO, PESO AL NACER >2499 GR SIN PROCEDIMIENTO MAYOR W/CC",
"158173 - MH NEONATO, PESO AL NACER >2499 GR SIN PROCEDIMIENTO MAYOR W/MCC",
"011103 - PH CRANEOTOMÍA W/MCC",
"024123 - MH OTRAS ENFERMEDADES OCULARES W/MCC",
"031152 - PH PROCEDIMIENTOS SOBRE AMÍGDALAS Y ADENOIDES W/CC",
"031202 - PH OTROS PROCEDIMIENTOS SOBRE OÍDO, NARIZ, BOCA Y GARGANTA W/CC",
"034133 - MH EPIGLOTITIS, OTITIS MEDIA, INFECCIONES TRACTO RESPIRATORIO SUPERIOR Y LARINGOTRAQUEITIS W/MCC",
"041013 - PH ECMO VENTILACIÓN MECÁNICA PROLONGADA CON TRAQUEOSTOMÍA W/MCC",
"041023 - PH VENTILACIÓN MECÁNICA PROLONGADA SIN TRAQUEOSTOMÍA W/MCC",
"041203 - PH PROCEDIMIENTOS NO COMPLEJOS SOBRE APARATO RESPIRATORIO W/MCC",
"044213 - MH OTROS SIGNOS, SÍNTOMAS Y DIAGNÓSTICOS DE APARATO RESPIRATORIO W/MCC",
"051043 - PH PROCEDIMIENTOS SOBRE VÁLVULAS CARDIACAS SIN CATETERISMO CARDIACO W/MCC",
"051123 - PH PROCEDIMIENTOS VASCULARES TORÁCICOS COMPLEJOS W/MCC",
"051133 - PH PROCEDIMIENTOS VASCULARES ABDOMINALES COMPLEJOS W/MCC",
"051152 - PH CATETERISMO CARDIACO W/CC",
"051202 - PH OTROS PROCEDIMIENTOS SOBRE APARATO CIRCULATORIO W/CC",
"051203 - PH OTROS PROCEDIMIENTOS SOBRE APARATO CIRCULATORIO W/MCC",
"051403 - PH PROCEDIMIENTOS CARDIOVASCULARES PERCUTÁNEOS W/MCC",
"064182 - MH OTROS DIAGNÓSTICOS SOBRE APARATO DIGESTIVO W/CC",
"081072 - PH PROCEDIMIENTOS DE FUSIÓN ESPINAL EXCEPTO POR DESVIACIÓN DE COLUMNA W/CC",
"091302 - PH INJERTO DE PIEL SIN QUEMADURA W/CC"
]

# Lista de CONVENIOS
convenios = [
    "GRD UGCC", "GRD-CARDIOPATIAS CONGENITAS", "TRANSP. HEPATICOS (SERVICIOS DE SALUD)", "Transplante Medula Osea Fonasa"
]

# Título de la aplicación
st.title("Evaluador de Traslados C3")
st.write("(Considera convenios GRD-UGCC y niveles de complejidad W/CC y W/MCC)")

# Entrada de datos del usuario
service_input = st.selectbox("Servicio de Ingreso:", services)
diagnosis_input = st.selectbox("GRD:", diagnoses)
convenio_input = st.selectbox("Convenio:", convenios)

# Función para hacer predicciones
def predict_gain_and_stay(service, diagnosis, convenio):
    try:
        # Codificar las entradas categóricas
        diagnosis_encoded = label_encoder_diagnosis.transform([diagnosis])[0]
        service_encoded = label_encoder_service.transform([service])[0]
        convenio_encoded = label_encoder_convenio.transform([convenio])[0]
        
        # Crear matriz de características
        features = pd.DataFrame({
            'IR GRD': [diagnosis_encoded],
            'SERVICIO INGRESO': [service_encoded],
            'CONVENIO': [convenio_encoded]
        })
        features_scaled = scaler.transform(features)
        
        # Hacer predicciones
        predicted_gain = rf_gain_model.predict(features_scaled)
        predicted_stay = rf_stay_model.predict(features_scaled)
        
        return round(predicted_gain[0], 0), round(predicted_stay[0], 2)
    except Exception as e:
        return f"Error: {e}", f"Error: {e}"

# Botón para hacer predicciones
if st.button("Predecir"):
    if service_input and diagnosis_input and convenio_input:
        gain, stay = predict_gain_and_stay(service_input, diagnosis_input, convenio_input)
        st.subheader("Resultados de la Predicción")
        
        # Mostrar Ganancias en formato de pesos chilenos con colores
        if isinstance(gain, str):  # Verifica si hay un error
            st.error(f"Error: {gain}")
        else:
            gain_formatted = f"${gain:,.0f} CLP"
            if gain > 0:
                st.markdown(f"**GANANCIAS:** <span style='color: green;'>{gain_formatted}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"**GANANCIAS:** <span style='color: red;'>{gain_formatted}</span>", unsafe_allow_html=True)
        
        # Mostrar Estancia
        if isinstance(stay, str):  # Verifica si hay un error
            st.error(f"Error: {stay}")
        else:
            st.write(f"**ESTANCIA:** {stay} días")
    else:
        st.warning("Por favor, complete todos los campos antes de predecir.")
