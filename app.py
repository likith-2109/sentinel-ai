import streamlit as st
import joblib
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Sentinel AI | Cybersecurity",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================
# LOAD TRAINED MODEL
# ==========================================

@st.cache_resource
def load_models():
    model = joblib.load("saved_models/random_forest.pkl")
    vectorizer = joblib.load("saved_models/tfidf_vectorizer.pkl")
    return model, vectorizer


model, tfidf = load_models()


# ==========================================
# SESSION STATE
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []


# ==========================================
# TEXT PREPROCESSING
# ==========================================

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ==========================================
# WARNING SIGN DETECTION
# ==========================================

def find_warning_signs(message):

    text = message.lower()

    warning_patterns = {
        "Urgent or pressure-based language": {
            "phrases": [
                "act now", "urgent", "immediately",
                "limited time", "hurry", "last chance"
            ],
            "explanation": (
                "This message pressures you to act quickly. "
                "Scam messages often use urgency to stop people "
                "from checking whether an offer is genuine."
            )
        },

        "Prize or reward claims": {
            "phrases": [
                "you have won", "winner", "free prize",
                "claim your reward", "congratulations"
            ],
            "explanation": (
                "This message mentions a prize or reward. "
                "Unexpected prize claims can be used to trick "
                "people into clicking links or sharing information."
            )
        },

        "Sensitive information requests": {
            "phrases": [
                "password", "otp", "bank details",
                "credit card", "pin number"
            ],
            "explanation": (
                "This message mentions sensitive personal or "
                "financial information. Never share your OTP, "
                "password or banking PIN with an unknown sender."
            )
        },

        "Suspicious links or contact requests": {
            "phrases": [
                "click here", "call now", "verify your account",
                "http://", "https://", "bit.ly"
            ],
            "explanation": (
                "This message contains a link or asks you to "
                "make contact. Check the website or sender "
                "independently before responding."
            )
        }
    }

    found_signs = []

    for category, details in warning_patterns.items():

        if any(phrase in text for phrase in details["phrases"]):

            found_signs.append({
                "category": category,
                "explanation": details["explanation"]
            })

    return found_signs


# ==========================================
# CUSTOM CSS - DARK NAVY THEME
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #080f1f;
    color: #e2e8f0;
}

header[data-testid="stHeader"] {
    background-color: #080f1f;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #60a5fa;
}

.subtitle {
    font-size: 16px;
    color: #94a3b8;
}

h1, h2, h3, h4, p, label {
    color: #e2e8f0;
}

[data-testid="stSidebar"] {
    background-color: #0f1b31;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

.info-card {
    background-color: #14233d;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #263c5d;
    min-height: 115px;
}

.info-card h4 {
    color: #60a5fa !important;
}

.info-card p {
    color: #e2e8f0 !important;
}

.stTextArea textarea {
    background-color: #14233d !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid #334e75 !important;
    border-radius: 10px !important;
}

.stTextArea textarea::placeholder {
    color: #94a3b8 !important;
}

div.stButton > button {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 9px;
    height: 45px;
    border: none;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #1d4ed8 !important;
}

[data-testid="stMetric"] {
    background-color: #14233d;
    padding: 18px;
    border: 1px solid #263c5d;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

[data-testid="stMetricValue"] {
    color: #60a5fa !important;
}

[data-testid="stDataFrame"] {
    background-color: #14233d;
}

.stSelectbox div {
    color: #e2e8f0;
}

hr {
    border-color: #263c5d;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:

    st.title("🛡️ SENTINEL AI")

    st.caption("INTELLIGENT MESSAGE SECURITY")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Message Detection",
            "Detection History"
        ]
    )

    st.divider()

    st.write("### AI TECHNOLOGIES")

    st.write("🤖 Random Forest")

    st.write("📝 TF-IDF")

    st.write("🧠 Natural Language Processing")

    st.divider()

    st.caption("AI-Based Scam Detection System")

    st.caption("Academic Project")


# ==========================================
# APPLICATION HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🛡️ SENTINEL AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Message Security and Threat Detection</div>',
    unsafe_allow_html=True
)

st.write("")


# ==========================================
# DASHBOARD PAGE
# ==========================================

if page == "Dashboard":

    st.subheader("📊 Security Dashboard")

    st.write(
        "Monitor your message security and view your detection activity."
    )

    history_df = pd.DataFrame(st.session_state.history)

    total = len(history_df)

    if total > 0:

        spam_count = (
            history_df["Prediction"] == "SPAM"
        ).sum()

        genuine_count = (
            history_df["Prediction"] == "GENUINE"
        ).sum()

        high_count = (
            history_df["Risk Level"] == "HIGH"
        ).sum()

        medium_count = (
            history_df["Risk Level"] == "MEDIUM"
        ).sum()

        low_count = (
            history_df["Risk Level"] == "LOW"
        ).sum()

    else:

        spam_count = 0
        genuine_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0

    # STATISTICS CARDS

    st.write("### Security Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Scanned",
            total
        )

    with col2:
        st.metric(
            "Spam Detected",
            spam_count
        )

    with col3:
        st.metric(
            "Genuine Messages",
            genuine_count
        )

    with col4:
        st.metric(
            "High Risk",
            high_count
        )

    st.write("")

    # CHARTS

    st.write("### Threat Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.markdown("#### Message Classification")

        if total > 0:

            fig, ax = plt.subplots(figsize=(5, 4))

            fig.patch.set_facecolor("#14233d")
            ax.set_facecolor("#14233d")

            values = [spam_count, genuine_count]
            labels = ["Spam", "Genuine"]

            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                textprops={"color": "white"},
                colors=["#ef4444", "#22c55e"]
            )

            ax.set_title(
                "Spam vs Genuine",
                color="white"
            )

            st.pyplot(fig)

            plt.close(fig)

        else:

            st.info(
                "No messages scanned yet. Start by analysing a message."
            )

    with chart_col2:

        st.markdown("#### Risk Distribution")

        if total > 0:

            fig2, ax2 = plt.subplots(figsize=(5, 4))

            fig2.patch.set_facecolor("#14233d")
            ax2.set_facecolor("#14233d")

            risk_labels = ["High", "Medium", "Low"]

            risk_values = [
                high_count,
                medium_count,
                low_count
            ]

            ax2.bar(
                risk_labels,
                risk_values,
                color=["#ef4444", "#f59e0b", "#22c55e"]
            )

            ax2.set_ylabel(
                "Number of Messages",
                color="white"
            )

            ax2.set_title(
                "Risk Level Distribution",
                color="white"
            )

            ax2.tick_params(colors="white")

            ax2.spines["bottom"].set_color("white")
            ax2.spines["left"].set_color("white")

            st.pyplot(fig2)

            plt.close(fig2)

        else:

            st.info(
                "Risk statistics will appear after your first scan."
            )

    st.divider()

    # RECENT ACTIVITY

    st.write("### 🕒 Recent Detection Activity")

    if total > 0:

        recent_history = history_df.tail(5).iloc[::-1]

        st.dataframe(
            recent_history[
                [
                    "Date and Time",
                    "Prediction",
                    "Spam Score",
                    "Risk Level"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No recent activity. Go to Message Detection to scan your first message."
        )

    st.divider()

    st.caption(
        "Dashboard statistics are based on messages analysed during this session. "
        "They reset when the Streamlit session is restarted."
    )


# ==========================================
# MESSAGE DETECTION PAGE
# ==========================================

elif page == "Message Detection":

    st.subheader("🔍 Message Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="info-card">
        <h4>🤖 AI Engine</h4>
        <p>Random Forest Classifier</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="info-card">
        <h4>📝 Text Processing</h4>
        <p>TF-IDF Vectorization</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="info-card">
        <h4>🛡️ Classification</h4>
        <p>Spam / Genuine</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    message = st.text_area(
        "Enter your SMS or message",
        height=160,
        placeholder="Paste your message here..."
    )

    if st.button("🔍 Analyze Message", use_container_width=True):

        if not message.strip():

            st.warning("Please enter a message.")

        else:

            cleaned_message = clean_text(message)

            message_vector = tfidf.transform([cleaned_message])

            prediction = model.predict(message_vector)[0]

            probabilities = model.predict_proba(message_vector)[0]

            spam_index = list(model.classes_).index(1)

            spam_probability = probabilities[spam_index] * 100

            result = "SPAM" if prediction == 1 else "GENUINE"

            if spam_probability >= 70:

                risk = "HIGH"

            elif spam_probability >= 40:

                risk = "MEDIUM"

            else:

                risk = "LOW"

            st.divider()

            st.subheader("📋 Analysis Result")

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                if prediction == 1:

                    st.error("⚠️ SPAM DETECTED")

                    st.write(
                        "The model classified this message as spam."
                    )

                else:

                    st.success("✅ GENUINE MESSAGE")

                    st.write(
                        "The model classified this message as genuine."
                    )

            with result_col2:

                st.metric(
                    "Model Spam Score",
                    f"{spam_probability:.2f}%"
                )

                st.progress(float(spam_probability / 100))

                st.metric("Display Risk Level", risk)

            # WARNING SIGNS

            st.divider()

            st.subheader("🔎 Message Warning Signs")

            warning_signs = find_warning_signs(message)

            if warning_signs:

                for sign in warning_signs:

                    st.warning(
                        "⚠️ " + sign["category"]
                    )

                    st.write(
                        sign["explanation"]
                    )

            else:

                st.success(
                    "No common warning signs detected in this message."
                )

            # SAFETY RECOMMENDATIONS

            st.divider()

            st.subheader("🛡️ Safety Recommendations")

            if prediction == 1:

                st.warning(
                    "Do not click suspicious links or call unknown numbers."
                )

                st.write(
                    "- Never share your OTP, password, or bank details."
                )

                st.write(
                    "- Do not make payments to claim unexpected prizes."
                )

                st.write(
                    "- Verify the sender through an official source."
                )

            else:

                st.info(
                    "The message appears genuine according to the model, "
                    "but always verify unexpected requests."
                )

                st.write(
                    "- Avoid sharing sensitive information unnecessarily."
                )

                st.write(
                    "- Check links before opening them."
                )

            st.caption(
                "The risk level is based on the model's spam score. "
                "It is not a separate trained risk classifier. "
                "Warning signs are identified using simple text patterns."
            )

            # SAVE HISTORY

            st.session_state.history.append({

                "Date and Time": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),

                "Message": message,

                "Prediction": result,

                "Spam Score": f"{spam_probability:.2f}%",

                "Risk Level": risk

            })


# ==========================================
# DETECTION HISTORY PAGE
# ==========================================

elif page == "Detection History":

    st.subheader("📜 Message Detection History")

    if st.session_state.history:

        history_df = pd.DataFrame(st.session_state.history)

        total = len(history_df)

        spam_count = (
            history_df["Prediction"] == "SPAM"
        ).sum()

        genuine_count = (
            history_df["Prediction"] == "GENUINE"
        ).sum()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Messages", total)

        col2.metric("Spam Detected", spam_count)

        col3.metric("Genuine Messages", genuine_count)

        st.write("### Previous Analyses")

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        csv = history_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download History CSV",
            data=csv,
            file_name="scam_detection_history.csv",
            mime="text/csv"
        )

        if st.button("🗑️ Clear History"):

            st.session_state.history = []

            st.rerun()


        st.info("No messages have been analyzed yet.")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "© 2026 Sentinel AI | AI-Based Scam Detection System | "
    "Machine Learning and Natural Language Processing"
)

st.caption(
    "This system is an academic prototype trained on an SMS spam dataset. "
    "It cannot guarantee that a message is safe or fraudulent."
)