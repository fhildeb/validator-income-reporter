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

    ### YEARLY INCOME TABLE

    # Prepare styling and title
    pdf.ln(10)
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, f"Monthly Incomes of {YEAR}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    # Prepare columns
    col_width = pdf.w / 4
    row_height = pdf.font_size
    spacing = 1.2

    # Create monthly income table headers

    # Center the table horizontally
    pdf.set_x((pdf.w - col_width * 3) / 2)
    
    # Set bold font for headers
    pdf.set_font("Arial", size=12, style='B')  
    
    pdf.cell(col_width, row_height * spacing, "Month", border=1, align="R")
    pdf.cell(col_width, row_height * spacing, "Crypto Currency", border=1, align="R")
    pdf.cell(col_width, row_height * spacing, "Income", border=1, align="R")

    # Reset font to regular
    pdf.set_font("Arial", size=12)  
    pdf.ln(row_height * spacing)

    # Fill table with monthly income data
    for month in range(1, 13):

        # Center the table horizontally
        pdf.set_x((pdf.w - col_width * 3) / 2)  
        month_name_str = month_name[month]
        income = monthly_incomes.get(month, 0.0)
        coins = monthly_coins.get(month, 0.0)
        pdf.cell(col_width, row_height * spacing, month_name_str, border=1, align="R")
        pdf.cell(col_width, row_height * spacing, f"{coins:.8f} {COIN_NAME}", border=1, align="R")
        pdf.cell(col_width, row_height * spacing, f"{income:.2f} {FIAT_CURRENCY}", border=1, align="R")
        pdf.ln(row_height * spacing)

    # Calculate yearly income
    pdf.ln(10)
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, f"Total received crypto currency: {total_coins:.8f} {COIN_NAME}", ln=True, align="C")
    pdf.cell(200, 10, f"Total price-adjusted income: {total_income:.2f} {FIAT_CURRENCY}", ln=True, align="C")

    pdf.set_font("Arial", size=12)