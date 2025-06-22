import logging 
import os
from datetime import datetime
LOG_FILE=f"{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log"
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)
Log_file_path=os.path.join(logs_path,LOG_FILE)
logging.basicConfig(
    filename=Log_file_path,
    level=logging.INFO,
    format="[%(asctime)s] %(lineno)d %(levelname)s - %(message)s",
   )
if __name__=="__main__":
    logging.info("logging has entered")