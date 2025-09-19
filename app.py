import streamlit as st
import pandas as pd
import joblib

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- LOAD SAVED MODEL ---
# The model is loaded once and cached to improve performance
@st.cache_resource
def load_model(model_path):
    """Loads the pre-trained model from the specified path."""
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        st.error(f"Model file not found at {model_path}. Please ensure the file exists.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")
        return None

model = load_model('final_model.joblib')

# --- CUSTOM CSS FOR MODERN UI ---
st.markdown("""
    <style>
        /* General body styling */
        .main {
            background-color: #f0f2f6;
        }

        /* Main container styling */
        [data-testid="stAppViewContainer"] > .main {
            background-color: #f0f2f6;
            padding: 2rem;
        }

        /* Title and header styling */
        h1 {
            color: #1e3a8a; /* Dark Blue */
            text-align: center;
            font-weight: bold;
        }
        
        .st-emotion-cache-10trblm {
            text-align: center;
            color: #4b5563; /* Gray */
        }

        /* Form container styling */
        [data-testid="stForm"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        /* Button styling */
        div.stButton > button {
            background-image: linear-gradient(to right, #3b82f6, #1e3a8a);
            color: white;
            font-size: 1.1rem;
            font-weight: bold;
            padding: 0.75rem 2rem;
            border-radius: 0.5rem;
            border: none;
            width: 100%;
            transition: all 0.2s ease-in-out;
        }

        div.stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3), 0 4px 6px -2px rgba(59, 130, 246, 0.2);
        }
        
        /* Input and select box styling */
        div[data-testid="stNumberInput"] input, 
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            border-radius: 0.5rem;
            border: 2px solid #d1d5db;
        }
        div[data-testid="stNumberInput"] input:focus, 
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }
        
        /* Success message (prediction result) styling */
        [data-testid="stSuccess"] {
            background-color: #dbeafe; /* Light Blue */
            border-radius: 0.75rem;
            border-left: 5px solid #1e3a8a;
            text-align: center;
        }
        [data-testid="stSuccess"] p {
            font-size: 1.5rem;
            font-weight: bold;
            color: #1e3a8a;
        }
    </style>
""", unsafe_allow_html=True)


# --- APP LAYOUT ---

# Main Title and Subheader
st.title("🏠 House Price Predictor")
st.markdown("Enter the details of the house to get a price prediction.")

# Only proceed if the model loaded successfully
if model is not None:
    # Use a form to group inputs for a cleaner UX
    with st.form(key='prediction_form'):
        st.write("### Property Details")
        
        # Create a 3x2 grid for inputs
        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            area = st.number_input("Area (sqft)", min_value=100, max_value=100000, value=1500, step=100)
            mainroad = st.selectbox("Mainroad Access", options=[(1, 'Yes'), (0, 'No')], format_func=lambda x: x[1])[0]

        with col2:
            bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3, step=1)
            basement = st.selectbox("Basement", options=[(1, 'Yes'), (0, 'No')], format_func=lambda x: x[1])[0]

        with col3:
            bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=2, step=1)
            parking = st.number_input("Parking Spots", min_value=0, max_value=10, value=2, step=1)

        # Submit button for the form
        submit_button = st.form_submit_button(label="Predict Price")

    # --- PREDICTION LOGIC ---
    if submit_button:
        # Collect inputs into a DataFrame
        input_data = {
            'area': area,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'mainroad': mainroad,
            'basement': basement,
            'parking': parking
        }
        input_df = pd.DataFrame([input_data])
        
        # Make a prediction
        try:
            with st.spinner('Calculating...'):
                price = model.predict(input_df)[0]
                # Display the result
                st.success(f"💰 Predicted Price: ₹ {price:,.0f}")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
