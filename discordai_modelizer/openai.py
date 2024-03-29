import openai
import json
import os
import subprocess


def list_jobs(openai_key: str, simple=False):
    finetunes = openai.FineTune.list(openai_key)
    if not simple:
        print(finetunes)
    else:
        simplified = []
        for ft in finetunes["data"]:
            entry = {}
            entry["fine_tuned_model"] = ft["fine_tuned_model"]
            entry["id"] = ft["id"]
            entry["status"] = ft["status"]
            simplified.append(entry)
        print(json.dumps(simplified, indent=4))


def list_models(openai_key: str, simple=False):
    finetunes = openai.Model.list(openai_key)
    if not simple:
        print(finetunes)
    else:
        simplified = []
        for ft in finetunes["data"]:
            entry = {}
            entry["id"] = ft["id"]
            simplified.append(entry)
        print(json.dumps(simplified, indent=4))


def follow_job(openai_key: str, job_id: str):
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    try:
        subprocess.run([
            "openai", "api", "fine_tunes.follow",
            "-i", job_id
        ])
    except FileNotFoundError:
        print("ERROR: You must have the `openai` python package installed to use this command.")


def get_status(openai_key: str, job_id: str, events: bool):
    status = openai.FineTune.retrieve(job_id, openai_key)
    if events:
        print(status["events"])
    else:
        print(status)


def cancel_job(openai_key: str, job_id: str):
    print(openai.FineTune.cancel(job_id, openai_key))


def delete_model(openai_key: str, model_name: str):
    confirm = input("Are you sure you want to delete this model? This action is not reversable. Y/N: ")
    if confirm not in ["Y", "y", "yes", "Yes", "YES"]:
        print("Cancelling model deletion...")
        return
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    print(openai.Model.delete(model_name))
