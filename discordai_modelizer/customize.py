import os
import subprocess
from pkg_resources import resource_filename

from discordai_modelizer import __name__ as pkg_name
from discordai_modelizer.gen_dataset import parse_logs, get_lines


def create_model(bot_token: str, openai_key: str, channel_id: str, user_id: str, thought_time=10,
                 max_entry_count=1000, reduce_mode="even", base_model="none", clean=False, redownload=False):
    os.environ["OPENAI_API_KEY"] = openai_key
    channel_user = f"{channel_id}_{user_id}"

    # Download logs
    if not os.path.isfile(f"{channel_user}_logs.json") or redownload:
        print("INFO: Exporting chat logs using DiscordChatExporter...")
        print("INFO: This may take a few minutes to hours depending on the message count of the channel")
        print("INFO: Progress will NOT be saved if cancelled")
        print("--------------------------DiscordChatExporter---------------------------")
        DiscordChatExporter = resource_filename(pkg_name, 'DiscordChatExporter/DiscordChatExporter.Cli.exe')
        subprocess.run([
            DiscordChatExporter,
            "export",
            "-c", channel_id,
            "-t", bot_token,
            "-o", f"{channel_user}_logs.json",
            "-f", "Json",
            "--filter", f"from:'{user_id}'"
        ])
        print("--------------------------DiscordChatExporter---------------------------")
    else:
        print("INFO: Chat logs detected locally... Skipping download.")

    # Parse logs
    print("INFO: Parsing chat logs into a openAI compatible dataset...")
    parse_logs(f"{channel_user}_logs.json", user_id, thought_time)

    # Prepare and reduce dataset
    print("INFO: Cleaning up generated dataset...")
    try:
        os.remove(f"{channel_user}_data_set_prepared.jsonl")
    except FileNotFoundError:
        pass
    subprocess.run([
        "openai", "tools", "fine_tunes.prepare_data",
        "-f", f"{channel_user}_data_set.jsonl",
        "-q"
    ])
    if os.path.isfile(f"{channel_user}_data_set_prepared.jsonl"):
        get_lines(f"{channel_user}_data_set_prepared.jsonl", max_entry_count, reduce_mode)
    else:
        get_lines(f"{channel_user}_data_set.jsonl", max_entry_count, reduce_mode)

    # Train customized openAI model
    if base_model in ["davinci", "curie", "babbage", "ada"]:
        print("INFO: Training customized openAI model...")
        print("INFO: This may take a few minutes to hours depending on the size of the dataset and the selected base model")
        if os.path.isfile(f"{channel_user}_data_set_prepared.jsonl"):
            subprocess.run([
                "openai", "api", "fine_tunes.create",
                "-t", f"{channel_user}_data_set_prepared.jsonl",
                "-m", base_model,
                "--suffix", user_id,
                "--no_check_if_files_exist"
            ])
        else:
            subprocess.run([
                "openai", "api", "fine_tunes.create",
                "-t", f"{channel_user}_data_set.jsonl",
                "-m", base_model,
                "--suffix", user_id,
                "--no_check_if_files_exist"
            ])
    elif base_model == "none":
        print("INFO: No base model selected... Skipping training.")

    # Clean up generated files
    if clean:
        try:
            os.remove(f"{channel_user}_data_set.jsonl")
            os.remove(f"{channel_user}_data_set_prepared.jsonl")
        except FileNotFoundError:
            pass