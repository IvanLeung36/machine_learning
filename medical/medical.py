import pandas as pd
from urllib.request import urlretrieve
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
import seaborn as sns

pio.renderers.default = "browser"

medical_charges_url = 'https://raw.githubusercontent.com/JovianML/opendatasets/master/data/medical-charges.csv'
urlretrieve(medical_charges_url, 'medical.csv')
medical_df = pd.read_csv('medical.csv')

# Age Distribution Plot
fig_age = px.histogram(medical_df, x='age', marginal='box', nbins=47, title='Distribution of Age')
fig_age.update_layout(bargap=0.1)
fig_age.write_html("age_distribution_plot.html")
print("Age distribution plot saved as 'age_distribution_plot.html'.")

# BMI Distribution Plot
fig_bmi = px.histogram(medical_df, x='bmi', marginal='box', color='smoker', 
                       color_discrete_sequence=['blue', 'red'], title='Distribution of BMI by Smoking Status')
fig_bmi.update_layout(bargap=0.1)
fig_bmi.write_html("bmi_distribution_plot.html")
print("BMI distribution plot saved as 'bmi_distribution_plot.html'.")

# Medical Charges by Smoker/Non-Smoker
fig_charges = px.histogram(medical_df, x='charges', marginal='box', color='smoker', 
                           color_discrete_sequence=['green', 'grey'], title='Annual Medical Charges by Smoking Status')
fig_charges.update_layout(bargap=0.1)
fig_charges.write_html("charges_by_smoker.html")
print("Medical charges plot saved as 'charges_by_smoker.html'.")

# Scatter Plot of Age vs. Charges
fig_scatter = px.scatter(medical_df, x='age', y='charges', color='smoker', 
                         title='Age vs. Medical Charges', trendline='ols')
fig_scatter.write_html("age_vs_charges_scatter.html")
print("Age vs. charges scatter plot saved as 'age_vs_charges_scatter.html'.")

# Scatter Plot of BMI vs. Charges
fig_bmi_charges = px.scatter(medical_df, x='bmi', y='charges', color='smoker', 
                              title='BMI vs. Medical Charges', trendline='ols')
fig_bmi_charges.write_html("bmi_vs_charges_scatter.html")
print("BMI vs. charges scatter plot saved as 'bmi_vs_charges_scatter.html'.")

# Print correlations
print("Correlations:")
print(f"charges-age correlations: {medical_df.charges.corr(medical_df.age)}, charges-bmi: {medical_df.charges.corr(medical_df.bmi)}")

# Scatter Plot for Non-Smokers (Age vs. Charges)
non_smoker_df = medical_df[medical_df.smoker == 'no']
plt.figure(figsize=(10, 6))
plt.title('Age vs. Charges (Non-Smokers)')
sns.scatterplot(data=non_smoker_df, x='age', y='charges', alpha=0.7, s=15)
plt.xlabel('Age')
plt.ylabel('Charges')
plt.show()

# Helper function for estimating charges
def estimate_charges(age, w, b):
    return w * age + b

# Guessed values for w and b
w = 50
b = 100

# Convert ages to numpy array
ages = non_smoker_df.age.to_numpy()

# Estimate charges using the model
estimated_charges = estimate_charges(ages, w, b)

# Plot Estimated Charges vs. Age
plt.plot(ages, estimated_charges, 'r-o')
plt.xlabel('Age')
plt.ylabel('Estimated Charges')
plt.title('Estimated Charges vs. Age')
plt.show()

# Plot Estimated vs Actual Charges for Non-Smokers
target = non_smoker_df.charges

plt.plot(ages, estimated_charges, 'r', alpha=0.9)
plt.scatter(ages, target, s=8,alpha=0.8)
plt.xlabel('Age')
plt.ylabel('Charges')
plt.legend(['Estimate', 'Actual'])
plt.show()

def try_parameters(w, b):
    ages = non_smoker_df.age.to_numpy()
    target = non_smoker_df.charges.to_numpy()
    
    estimated_charges = estimate_charges(ages, w, b)
    
    plt.plot(ages, estimated_charges, 'r', alpha=0.9)
    plt.scatter(ages, target, s=8,alpha=0.8)
    plt.xlabel('Age')
    plt.ylabel('Charges')
    plt.title(f'w = {w}, b = {b}')
    plt.legend(['Estimate', 'Actual'])
    plt.show()
try_parameters(400,2000)
try_parameters(300,-1900)