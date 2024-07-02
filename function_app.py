import logging
import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from bloombergapa import get_file_data, get_file_list


app = func.FunctionApp()

connection_str = os.environ["CONNECTION_STRING"]
logging.info(f"Connection String: {connection_str}")

service = BlobServiceClient.from_connection_string(connection_str)
container = service.get_container_client("bloombergapa")


@app.timer_trigger(
    schedule="0 58 20 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def timer_trigger1(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    for filename, download_link in get_file_list():
        data = get_file_data(download_link)
        logging.info("uploading {filename} to blob storage")
        container.upload_blob(filename, data, overwrite=True)
