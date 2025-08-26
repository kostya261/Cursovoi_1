from config import (file_path, save_line_transactions, save_main_page, save_names_transactions,
                    save_phone_numbers_transactions)
from src.loader import excel_loader
from src.reports import spending_by_category
from src.saver import save_json
from src.services import search_line, search_name, search_phone
from src.utils import convert_data
from src.views import main_page

excel_file = excel_loader(file_path)
data = convert_data(excel_file, "25-11-2019 12:50:00")

# Views.py
main_pg = main_page("15-07-2019 00:00:00")


# services.py
phone_number_transactions = search_phone(excel_file)
search_name_transactions = search_name(excel_file)
search_line_transactions = search_line(excel_file, "Магнит")

# reports.py
reports = spending_by_category(excel_file, "Перевод", "03-11-2019 00:50:00", filename="C:\\temp\\test.xlsx")

# Всё сохраняем в json файлы
save_json(save_main_page, main_pg)
save_json(save_phone_numbers_transactions, phone_number_transactions)
save_json(save_names_transactions, search_name_transactions)
save_json(save_line_transactions, search_line_transactions)


print(main_pg)
print(phone_number_transactions)
print(search_name_transactions)
print(search_line_transactions)
print(reports)
