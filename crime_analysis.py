import pandas as pd  # For data handling
import matplotlib.pyplot as plt  # For plotting graphs
import seaborn as sns  # For better visualizations
import folium  # For interactive maps
import calendar
from folium.plugins import HeatMap  # For crime heatmaps


# Load the crime data
crime_df = pd.read_csv("calgary_crime_data.csv")

# Preview data
print(crime_df.head())

# Remove first few rows if they contain invalid data
crime_df = crime_df.iloc[610:]

# Reset the index
crime_df.reset_index(drop=True, inplace=True)

# Convert Year and Month to integers
crime_df["Year"] = crime_df["Year"].astype(int)
crime_df["Month"] = crime_df["Month"].astype(int)

# Convert 'Crime Count' to integer
crime_df["Crime Count"] = crime_df["Crime Count"].astype(int)

# Convert month numbers to month names
crime_df["Month Name"] = crime_df["Month"].apply(lambda x: calendar.month_name[x])

# Standardize community names (lowercase & strip spaces)
crime_df["Community"] = crime_df["Community"].str.lower().str.strip()

# Check for missing values and fill them
crime_df.fillna({"Community": "Unknown", "Category": "Unknown", "Crime Count": 0}, inplace=True)

# Remove duplicates
crime_df.drop_duplicates(inplace=True)

# Save the cleaned dataset
crime_df.to_csv("calgary_crime_cleaned.csv", index=False)

print("Cleaned dataset saved as calgary_crime_cleaned.csv")


#Identifying most common crimes in calgary



# Count occurrences of each crime type
crime_counts = crime_df["Category"].value_counts().head(8)  # Get top 10

# Adjust figure size and plot
plt.figure(figsize=(10,5))  
sns.barplot(x=crime_counts.index, y=crime_counts.values, color="red")

# Titles and labels
plt.title("Top 8 Most Common Crimes in Calgary", fontsize=14)
plt.xlabel("Crime Category", fontsize=10)
plt.ylabel("Crime Count", fontsize=10)

# Rotate labels with proper alignment
plt.xticks(rotation=20, ha="right", fontsize=8)

# Show plot
plt.show()



#Identifying crime trends over year


crime_by_month = crime_df.groupby("Month")["Crime Count"].sum()

# Sort by actual month order (not alphabetically)
crime_by_month = crime_by_month.reindex(range(1, 13))  

# Plot crime trends
plt.figure(figsize=(10, 5))
#crime_by_month.plot(kind="line", color="lightgreen")
plt.plot(crime_by_month.index, crime_by_month.values, marker="o", linestyle="-", color="green")


# Formatting
plt.title("Monthly Crime Trends in Calgary (2021-2024)", fontsize=14)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Number of Crimes", fontsize=12)
plt.xticks(range(12), calendar.month_name[1:13], rotation=20, fontsize=8)

# Show plot
plt.show()


#crime distribution by community

crime_df["Community"] = crime_df["Community"].replace("downtown commercial core", "downtown core")


# Count crimes by community (Top 8)
crime_by_community = crime_df.groupby("Community")["Crime Count"].sum().sort_values(ascending=False).head(8)

# Plot horizontal bar chart
plt.figure(figsize=(30, 12))
sns.barplot(y=crime_by_community.index, x=crime_by_community.values, color="yellow")

# Formatting
plt.title("Top 8 High-Crime Communities in Calgary", fontsize=14)
plt.xlabel("Crime Count", fontsize=12)
plt.ylabel("Community", fontsize=12)

# Show plot
plt.show()


