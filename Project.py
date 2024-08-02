import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import base64  # Import base64 module for encoding

#Displaying Title and description
st.title('Glass Data Analysis 🔍')
st.write('This application performs data cleaning, analysis, and visualization on the Glass_Type dataset.')

# Reading the CSV file
try:
    glass_df = pd.read_csv('Glass_Type.csv')  
    st.success("File loaded successfully!")
except FileNotFoundError:
    st.error("File not found. Please check the file path.")
    st.stop()
except Exception as e:
    st.error(f"error : {e}")
    st.stop()

#Checking if 'Type' column exists
if 'Type' not in glass_df.columns:
    st.error("The 'Type' column is missing from the dataset.")
    st.stop()

# Data Cleaning
# Standardize the 'Type' column (remove extra spaces and standardize format)
try:
    glass_df['Type'] = glass_df['Type'].str.strip().str.replace("'", "").str.replace(" ", "_")
except Exception as e:
    st.error(f"An error occurred while cleaning the 'Type' column: {e}")
    st.stop()

# Filter out rows with zero values in specified columns
try:
    filtered_df = glass_df[(glass_df['Mg'] != 0) &
                           (glass_df['K'] != 0) &
                           (glass_df['Ca'] != 0) &
                           (glass_df['Ba'] != 0) &
                           (glass_df['Fe'] != 0)]
except Exception as e:
    st.error(f"An error occurred while filtering the data: {e}")
    st.stop()

# Calculate additional insights
try:
    element_means = filtered_df.mean(numeric_only=True)
    most_used_element = element_means.idxmax()
    least_used_element = element_means.idxmin()
    glass_type_frequency = filtered_df['Type'].value_counts()
    most_used_glass_type = glass_type_frequency.idxmax()
    least_used_glass_type = glass_type_frequency.idxmin()
except Exception as e:
    st.error(f"An error occurred while calculating insights: {e}")
    st.stop()

# Generate Summary TXT file
summary_text =f"""
Glass Data Analysis Summary:

Most Used Element: {most_used_element} with an average of {element_means[most_used_element]:f}
Least Used Element: {least_used_element} with an average of {element_means[least_used_element]:f}

Element Usage Details:
{element_means}

Most Used Glass Type: {most_used_glass_type} with {glass_type_frequency[most_used_glass_type]} occurrences
Least Used Glass Type: {least_used_glass_type} with {glass_type_frequency[least_used_glass_type]} occurrences
"""

# Sidebar options
st.sidebar.title('Analysis Options')
analysis_options = [
    "Summary Statistics",
    "Element Histograms",
    "Element Scatter Plots",
    "Element Bar Graphs",
    "Element Pie Chart",
    "Glass Type Frequency",
    "Glass Type Pie Chart"
]
analysis_option = st.sidebar.selectbox("Choose Analysis", analysis_options)

# Display selected analysis
if analysis_option == "Summary Statistics":
    st.subheader('Summary Statistics after Filtering')
    st.write(filtered_df.describe())

    # Additional Insights
    st.subheader('Additional Insights')
    try:
        st.write(f"**Most Used Element:** {most_used_element} with an average of {element_means[most_used_element]:.2f}")
        st.write(f"**Least Used Element:** {least_used_element} with an average of {element_means[least_used_element]:.2f}")

        st.write("**Element Usage Details:**")
        st.write(element_means)
    except Exception as e:
        st.error(f"An error occurred while calculating additional insights: {e}")

    # Insights about Glass Types
    try:
        st.write(f"**Most Used Glass Type:** {most_used_glass_type} with {glass_type_frequency[most_used_glass_type]} occurrences")
        st.write(f"**Least Used Glass Type:** {least_used_glass_type} with {glass_type_frequency[least_used_glass_type]} occurrences")
    except Exception as e:
        st.error(f"An error occurred while calculating glass type insights: {e}")

    # Download Summary Text File,took reference from chatgpt 
    if st.button("Download Summary"):
        # Creates a download link for Summary file
        st.markdown("### Download Here")
        href = f"data:text/plain;base64,{base64.b64encode(summary_text.encode()).decode()}"
        st.markdown(f'<a href="{href}" download="glass_data_summary.txt">Click here to download the summary file</a>', unsafe_allow_html=True)

elif analysis_option == "Element Histograms":
    st.subheader('Histograms of Elements')
    elements = ['RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe']
    selected_element = st.selectbox("Select an element for the histogram", elements)
    if selected_element:
        fig,ax = plt.subplots(figsize=(10,12))
        ax.hist(filtered_df[selected_element],bins=30,edgecolor='black', color='skyblue')
        ax.set_title(f'Histogram of {selected_element}')
        ax.set_xlabel(selected_element)
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
elif analysis_option == "Element Scatter Plots":
    st.subheader('Scatter Plots of Elements')
    elements = ['RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe']
    x_element=st.selectbox("Select X-axis element",elements)
    y_element=st.selectbox("Select Y-axis element",elements)
    if x_element and y_element:
        fig,ax = plt.subplots(figsize=(8, 6))
        ax.scatter(filtered_df[x_element], filtered_df[y_element], c='blue')
        ax.set_title(f'Scatter Plot of {x_element} vs {y_element}')
        ax.set_xlabel(x_element)
        ax.set_ylabel(y_element)
        st.pyplot(fig)
elif analysis_option == "Element Bar Graphs":
    st.subheader('Bar Graphs of Elements')
    elements = ['RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe']
    selected_element = st.selectbox("Select an element for the bar graph", elements)
    if selected_element:
        element_values = filtered_df[selected_element].value_counts()
        fig,ax = plt.subplots(figsize=(10, 6))
        ax.bar(element_values.index, element_values.values, color='skyblue',width=0.15)
        ax.set_title(f'Bar Graph of {selected_element}')
        ax.set_xlabel(selected_element)
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
elif analysis_option == "Element Pie Chart":
    st.subheader('Pie Chart of Element Distribution')
    elements = ['RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe']
    selected_element = st.selectbox("Select an element for the pie chart", elements)
    if selected_element:
        element_distribution = filtered_df[selected_element].value_counts()
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(element_distribution.values, labels=element_distribution.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        ax.set_title(f'{selected_element} Distribution')
        st.pyplot(fig)
elif analysis_option == "Glass Type Frequency":
    st.subheader('Frequency of Each Glass Type')
    glass_type_frequency = filtered_df['Type'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(glass_type_frequency.index, glass_type_frequency.values, color='skyblue')
    ax.set_title('Frequency of Each Glass Type after Filtering')
    ax.set_xlabel('Glass Type')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
elif analysis_option == "Glass Type Pie Chart":
    st.subheader('Pie Chart of Glass Type Frequency')
    glass_type_frequency = filtered_df['Type'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(glass_type_frequency.values, labels=glass_type_frequency.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    ax.set_title('Glass Type Frequency Distribution')
    st.pyplot(fig)

