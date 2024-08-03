# GENERATES PDF REPORT

# External libraries
import pandas as pd
from fpdf import FPDF
from calendar import month_name

# Internal library imports
from utility.terminal_outputs import printLine

# Internal config data
from config import YEAR, ETH1_ADDRESS
from config import COIN_NAME, FIAT_CURRENCY, REPORT_TITLE, EXPLORER_LINK

def csv_to_pdf(csv_file, pdf_file, miner_count, withdrawal_count):
    """
    Generates a PDF report from a CSV file.

    - Builds a cover page with global report metadata
    - Creates a table with monthly and yearly incomes
    - Adds detailed monthly income pages from daily data

    :param csv_file (str): The path to the input CSV file containing daily income data.
    :param pdf_file (str): The path where the generated PDF report will be saved.
    """
    
    # Read CSV file
    df = pd.read_csv(csv_file)
    
    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Create instance of FPDF class
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    total_income = 0.0
    total_coins = 0.0
    monthly_incomes = {}
    monthly_coins = {}

    # Calculate yearly and monthly incomes
    for month, month_df in df.groupby(df['Date'].dt.month):
        monthly_total_income = 0.0
        monthly_total_coins = 0.0
        for row in month_df.itertuples():
            monthly_total_income += float(row[4]) if row[4] != 'None' else 0.0
            monthly_total_coins += float(row[2])
        monthly_incomes[month] = monthly_total_income
        monthly_coins[month] = monthly_total_coins
        total_income += monthly_total_income
        total_coins += monthly_total_coins

    ### COVER PAGE

    # New page with title
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, f"Validator Income Report {YEAR}", ln=True, align="C")
    pdf.ln(20)

    # Draw info box for global report metadata
    frame_width = 160
    frame_height = 40 
    x_start = (pdf.w - frame_width) / 2
    y_start_1 = 35
    y_start_2 = 80

    pdf.rect(x_start, y_start_1, frame_width, frame_height)
    pdf.rect(x_start, y_start_2, frame_width, frame_height)

    total_validations = miner_count + withdrawal_count

    # Write global report metadata
    inset = 30 
    pdf.set_x(inset)
    pdf.cell(0, 10, f"Job: {REPORT_TITLE}", ln=True, align="L")
    pdf.set_x(inset)
    pdf.cell(0, 10, f"Explorer: {EXPLORER_LINK}", ln=True, align="L")
    pdf.set_x(inset)
    pdf.cell(0, 10, f"Coin: {COIN_NAME}", ln=True, align="L")
    pdf.ln(15)
    pdf.set_x(inset)
    pdf.cell(0, 10, f"{ETH1_ADDRESS}", ln=True, align="L")
    pdf.set_x(inset)
    pdf.cell(0, 10, f"received a total of {total_validations} validator payments from", ln=True, align="L")
    pdf.set_x(inset)
    pdf.cell(0, 10, f"{withdrawal_count} withdrawal listings and {miner_count} miner records.", ln=True, align="L")

    pdf.ln(10)