# UN Enrollment Dashboard

An interactive Streamlit dashboard visualizing female primary‑level enrollment rates worldwide, built for SIADS 521 Module 3.


## Features

- **Global Choropleth Map** of female enrollment % by country  
- **Top N Bar Chart** highlighting highest‑enrollment countries  
- **Trend Line Chart** showing enrollment over time  
- **Slope Chart** illustrating change from first to selected year  
- Interactive filters: year slider & country multiselect


##  Installation and Dependencies

1. **Clone the repo**  
   ```bash
   git clone https://github.com/anitanti77/UN-Enrollment-Dashboard.git
   cd UN-Enrollment-Dashboard
2. **Create Conda Enviroment**  
conda create -n un_dashboard python=3.10 -c conda-forge \
  streamlit pandas plotly xlrd openpyxl -y
conda activate un_dashboard

3. **Dependencies**
   pip install streamlit pandas plotly xlrd openpyxl

##  How to run
streamlit run Module3.py


