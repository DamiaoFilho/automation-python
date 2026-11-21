from pathlib import Path
import pandas as pd
from datetime import datetime
from openpyxl.styles import Font

BASE_DIR = Path(__file__).parent
SELLS_DIR = BASE_DIR / "vendas"

sells = SELLS_DIR.glob("*.csv")

#Read everything as str to full data type control
merged_sells = pd.concat(
    (pd.read_csv(sell, dtype=str) for sell in sells),
    ignore_index=True
)
#Remove extra whitespaces for all values
#Applies first upper case letter to words for all values
for col in merged_sells.columns:
    merged_sells[col] = merged_sells[col].str.strip().str.title()


#Transform numbers column to numeric
merged_sells["valor"] = pd.to_numeric(
    merged_sells["valor"].str.replace(",", ".", regex=False),
    errors="coerce"
)

#Convert date to valid br formats with iso as fallback
date_iso = pd.to_datetime(
    merged_sells["data"],
    format="%Y-%m-%d",
    errors="coerce"
)
date_br = pd.to_datetime(
    merged_sells["data"],
    format="%d/%m/%Y",
    errors="coerce"
)
merged_sells["data"] = date_iso.fillna(date_br)


#Remove duplicates
merged_sells = merged_sells.drop_duplicates()
#Remove duplicated id rows
merged_sells = merged_sells.drop_duplicates(subset=["id_venda"])

#See duplicated ids
# duplicated_ids = merged_sells[merged_sells.duplicated(subset=["id_venda"], keep=False)]
# print("ids duplicados", duplicated_ids)

valid_values = (
    merged_sells["id_venda"].notna() & merged_sells["produto"].notna()
    & (merged_sells["produto"] != "") & merged_sells["valor"].notna()
    & (merged_sells["valor"] > 0) & merged_sells["data"].notna()
)
invalid = (~valid_values).sum()
merged_sells = merged_sells[valid_values].reset_index(drop=True)






now = datetime.now().strftime("%H_%M_%S")
# export = merged_sells.assign(data=merged_sells["data"].dt.date)
# export.to_excel(f"result_{now}.xlsx", sheet_name=f"result_{now}", index=False)


#Sells by month
sells_by_month = (
    merged_sells.groupby(merged_sells["data"].dt.strftime("%Y-%m"))["valor"]
    .sum()
    .reset_index()
    .rename(columns={"data":"mes"})

)


now = datetime.now().strftime("%H_%M_%S")
with pd.ExcelWriter(f"result_{now}.xlsx", engine="openpyxl") as writer:
    # Remove time from data since is always 0
    by_product = merged_sells.assign(data=merged_sells["data"].dt.date)
    by_product.to_excel(writer, sheet_name=f"by_product", index=False)

    ws = writer.sheets["by_product"]
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for (cell,) in ws.iter_rows(min_row=2, min_col=4, max_col=4):
            cell.number_format = '"R$" #,##0.00'

    sells_by_month.to_excel(writer, sheet_name=f"sells_by_month", index=False)

    ws = writer.sheets["sells_by_month"]
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for (cell,) in ws.iter_rows(min_row=2, min_col=2, max_col=2):
            cell.number_format = '"R$" #,##0.00'
