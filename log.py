import os
import shutil
import pandas as pd
from pydub import AudioSegment
from datetime import datetime


def log_received_audio(count, time):
    # Define the constants
    file_name = "received_audio.wav"  # Change this to your desired filename
    saved_folder = "Saved"
    excel_file = "file_records.xlsx"

    # Ensure the "Saved" folder exists
    if not os.path.exists(saved_folder):
        os.makedirs(saved_folder)

    # Check if the Excel file exists, and create it if it doesn't
    if not os.path.exists(excel_file):
        df = pd.DataFrame(columns=["ID", "Filename"])
        df.to_excel(excel_file, index=False)

    # Load the existing records from the Excel file
    df = pd.read_excel(excel_file)

    # Determine the next ID for the new file
    next_id = df["ID"].max() + 1 if not df.empty else 1

    # Construct the new filename with the ID
    new_file_name = f"{next_id}_{file_name}"

    # Save the file to the "Saved" folder
    # os.rename(file_name, os.path.join(saved_folder, new_file_name))

    shutil.copy(file_name, os.path.join(saved_folder, new_file_name))

    
    # Get the duration of the audio file
    audio = AudioSegment.from_file(file_name)
    duration_seconds = len(audio) / 1000  # Convert milliseconds to seconds

    # Get the current system date
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add the record to the Excel table
    new_record = {"ID": next_id, "Filename": new_file_name, "Duration": duration_seconds, "Date": current_date, "Burps": count, "Burp_period": time}
    df = df._append(new_record, ignore_index=True)


    # # Add the record to the Excel table
    # new_record = pd.DataFrame({"ID": [next_id], "Filename": [new_file_name]})
    # df = df._append(new_record, ignore_index=True)

    # # Save the updated table to the Excel file
    df.to_excel(excel_file, index=False)

    print(f"File '{new_file_name}' saved in '{saved_folder}' with ID {next_id}.")


