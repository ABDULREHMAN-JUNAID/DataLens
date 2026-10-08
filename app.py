import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="DataLens",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    font-size: 3rem !important;
}

.subtitle {
    color: #9ca3af;
    font-size: 1.1rem;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #161b22;
    border: 1px solid #30363d;
    text-align: center;
}

.card-title {
    color: #9ca3af;
    font-size: 0.9rem;
}

.card-value {
    font-size: 2rem;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.title("📊 DataLens")

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Data Analysis Assistant'
    '</div>',
    unsafe_allow_html=True
)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("⚙️ DataLens")

    st.write(
        "Upload your CSV dataset and let DataLens "
        "analyze it automatically."
    )

    uploaded_file = st.file_uploader(
        "📁 Upload CSV",
        type=["csv"]
    )

    st.divider()

    st.markdown("### ✨ Features")

    st.write("📋 Dataset Overview")
    st.write("🔍 Column Analysis")
    st.write("📈 Statistics")
    st.write("🤖 Natural Language Questions")
    st.write("📊 Visualizations")

# ==========================================
# NO FILE
# ==========================================

if uploaded_file is None:

    st.info(
        "👈 Upload a CSV file from the sidebar to begin."
    )

    st.markdown("## 🚀 How DataLens Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="card">'
            '<h2>📁</h2>'
            '<b>1. Upload</b>'
            '<p>Upload your CSV dataset.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="card">'
            '<h2>🤖</h2>'
            '<b>2. Analyze</b>'
            '<p>DataLens analyzes your data.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="card">'
            '<h2>📊</h2>'
            '<b>3. Understand</b>'
            '<p>View charts and insights.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    st.stop()

# ==========================================
# LOAD DATA
# ==========================================

try:

    df = pd.read_csv(uploaded_file)

    st.success("✅ Dataset loaded successfully!")

except Exception as e:

    st.error(f"Unable to read the CSV file: {e}")
    st.stop()

# ==========================================
# BASIC INFORMATION
# ==========================================

numeric_columns = df.select_dtypes(
    include=np.number
).columns

categorical_columns = df.select_dtypes(
    exclude=np.number
).columns

missing_values = int(
    df.isnull().sum().sum()
)

# ==========================================
# DASHBOARD METRICS
# ==========================================

st.header("📋 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📄 Rows",
        df.shape[0]
    )

with col2:

    st.metric(
        "📊 Columns",
        df.shape[1]
    )

with col3:

    st.metric(
        "🔢 Numeric Columns",
        len(numeric_columns)
    )

with col4:

    st.metric(
        "⚠️ Missing Values",
        missing_values
    )

# ==========================================
# DATA PREVIEW
# ==========================================

st.header("👀 Dataset Preview")

st.dataframe(
    df,
    use_container_width=True
)

# ==========================================
# COLUMN INFORMATION
# ==========================================

st.header("🔍 Column Information")

column_info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isnull().sum().values,
    "Unique Values": df.nunique().values
})

st.dataframe(
    column_info,
    use_container_width=True
)

# ==========================================
# STATISTICS
# ==========================================

st.header("📈 Statistical Analysis")

if len(numeric_columns) > 0:

    st.dataframe(
        df[numeric_columns].describe(),
        use_container_width=True
    )

else:

    st.info("No numeric columns were found.")

# ==========================================
# ASK DATALENS
# ==========================================

st.header("🤖 Ask DataLens")

question = st.text_input(
    "Ask a question about your dataset",
    placeholder="Example: What is the average age?"
)

if question:

    q = question.lower()

    # Average
    if "average" in q or "mean" in q:

        found = False

        for column in numeric_columns:

            if column.lower() in q:

                value = df[column].mean()

                st.success(
                    f"📊 The average {column} is **{value:.2f}**."
                )

                found = True
                break

        if not found:

            st.info(
                "Try mentioning a numeric column, "
                "for example: What is the average age?"
            )

    # Highest
    elif (
        "highest" in q
        or "maximum" in q
        or "max" in q
    ):

        found = False

        for column in numeric_columns:

            if column.lower() in q:

                value = df[column].max()

                st.success(
                    f"🏆 The highest {column} is **{value}**."
                )

                found = True
                break

        if not found:

            st.info(
                "Please mention a numeric column."
            )

    # Lowest
    elif (
        "lowest" in q
        or "minimum" in q
        or "min" in q
    ):

        found = False

        for column in numeric_columns:

            if column.lower() in q:

                value = df[column].min()

                st.success(
                    f"📉 The lowest {column} is **{value}**."
                )

                found = True
                break

        if not found:

            st.info(
                "Please mention a numeric column."
            )

    # Count
    elif (
        "how many" in q
        or "count" in q
        or "records" in q
    ):

        st.success(
            f"📋 Your dataset contains "
            f"**{len(df)} records**."
        )

    else:

        st.warning(
            "🤔 I don't understand that question yet."
        )

# ==========================================
# VISUALIZATION
# ==========================================

st.header("📊 Visualization")

if len(numeric_columns) > 0:

    selected_column = st.selectbox(
        "Choose a numeric column",
        numeric_columns
    )

    fig, ax = plt.subplots(
        figsize=(9, 4)
    )

    ax.hist(
        df[selected_column].dropna(),
        bins=10
    )

    ax.set_title(
        f"Distribution of {selected_column}"
    )

    ax.set_xlabel(selected_column)
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

else:

    st.info(
        "A chart requires at least one numeric column."
    )

# ==========================================
# MISSING VALUES
# ==========================================

st.header("⚠️ Data Quality")

missing = df.isnull().sum()

missing = missing[missing > 0]

if len(missing) > 0:

    st.dataframe(missing)

else:

    st.success(
        "🎉 Excellent! No missing values were found."
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "📊 DataLens — AI-Powered Data Analysis Assistant"
)