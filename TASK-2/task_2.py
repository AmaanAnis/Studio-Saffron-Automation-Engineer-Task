import gspread
from trello import TrelloClient
import logging
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

logging.basicConfig(
    filename="task_automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

gc = gspread.service_account(filename="google_creds.json")
sh = gc.open_by_key(os.getenv("SHEET_ID"))
worksheet = sh.sheet1

trello = TrelloClient(
    api_key=os.getenv("TRELLO_API_KEY"),
    api_secret=os.getenv("TRELLO_API_SECRET"),
    token=os.getenv("TRELLO_TOKEN"),
)
board = trello.get_board(os.getenv("TRELLO_BOARD_ID"))
target_list = board.get_list(os.getenv("TRELLO_LIST_ID"))


def process_new_tasks():
    try:
        records = worksheet.get_all_records()
        last_row = int(worksheet.acell("LAST_ROW").value)  

        new_rows = records[last_row:]
        for row in new_rows:
            task_name = row["Task Name"]
            due_date = row["Due Date"]

            if not task_name or task_exists_in_trello(task_name):
                continue

            card = target_list.add_card(name=task_name, due=due_date)
            logging.info(f"Task '{task_name}' added at {datetime.now()}")

            last_row += 1
            worksheet.update("A1", last_row)

    except Exception as e:
        logging.error(f"Error: {str(e)}")


def task_exists_in_trello(task_name):
    existing_cards = target_list.list_cards()
    return any(card.name == task_name for card in existing_cards)


if __name__ == "__main__":
    process_new_tasks()
