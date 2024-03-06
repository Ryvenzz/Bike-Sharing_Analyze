import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

dsday = pd.read_csv('dashboard/all_data.csv')

def create_daily(dsday):
    daily_rent_ds = dsday.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_rent_ds

def create_season(dsday):
    season_rent = dsday.groupby(by='season')['cnt'].sum().reset_index()
    return season_rent

def create_weekday(dsday):
    weekday_rent = dsday.groupby(by='weekday').agg({
        'cnt': 'sum'
    }).reset_index()
    return weekday_rent

def create_workingday(dsday):
    workingday_rent = dsday.groupby(by='workingday').agg({
        'cnt': 'sum'
    }).reset_index()
    return workingday_rent

def create_holiday(dsday):
    holiday_rent = dsday.groupby(by='holiday').agg({
        'cnt': 'sum'
    }).reset_index()
    return holiday_rent

min_date = pd.to_datetime(dsday['dteday']).dt.date.min()
max_date = pd.to_datetime(dsday['dteday']).dt.date.max()

st.header('Bike Rental Dashboard')

with st.sidebar:
    
    st.text('Filter')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = dsday[(dsday['dteday'] >= str(start_date)) & 
                (dsday['dteday'] <= str(end_date))]

daily_dsday = create_daily(main_df)
weekday_dsday = create_weekday(main_df)
workingday_dsday = create_workingday(main_df)
holiday_dsday = create_holiday(main_df)
season_dsday = create_season(main_df)

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['cnt'].sum()
    st.metric("Total Rides", value=total_all_rides)
with col2:
    total_working_day = main_df[main_df['workingday'] == 1]['cnt'].sum()
    st.metric("Total Workingday", value=total_working_day)
with col3:
    total_holiday = main_df[main_df['holiday'] == 1]['cnt'].sum()
    st.metric("Total Holiday", value=total_holiday)

st.markdown("---")


st.subheader('Seasonly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='cnt',
    data=season_dsday,
    label='1 : Musim semi; 2 : Musim panas; 3 : Musim gugur; 4 : Musim dingin',
    color='tab:green',
    ax=ax
)


for index, row in season_dsday.iterrows():
    ax.text(index, row['cnt'], str(row['cnt']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

st.subheader('Workingday, and Holiday Rentals')

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15,10))

colors1=["tab:blue", "tab:orange"]
colors2=["tab:blue", "tab:orange"]


sns.barplot(
    x='workingday',
    y='cnt',
    data=workingday_dsday,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(workingday_dsday['cnt']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Rents based on Working Day')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)


sns.barplot(
  x='holiday',
  y='cnt',
  data=holiday_dsday,
  palette=colors2,
  ax=axes[1])

for index, row in enumerate(holiday_dsday['cnt']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Rents based on Holiday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)