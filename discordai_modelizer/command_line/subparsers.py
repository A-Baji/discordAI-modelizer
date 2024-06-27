def setup_model_list(model_subcommand):
    model_list = model_subcommand.add_parser(
        "list", description="List your openAi customized models"
    )
    model_list_required_named = model_list.add_argument_group(
        "required named arguments"
    )
    model_list_optional_named = model_list.add_argument_group(
        "optional named arguments"
    )

    model_list_required_named.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key to list the models for. Must either be passed in as an argument or set as an environment variable",
    )
    model_list_optional_named.add_argument(
        "--full",
        action="store_true",
        required=False,
        dest="full",
        help="Return the full details of all the models",
    )


def setup_model_create(model_subcommand):
    model_create = model_subcommand.add_parser(
        "create",
        description="Create a new openAI customized model by downloading the specified chat logs, parsing them into a usable dataset, and then training a customized model using openai",
    )
    model_create_required_named = model_create.add_argument_group(
        "required named arguments"
    )
    model_create_optional_named = model_create.add_argument_group(
        "optional named arguments"
    )

    model_create_required_named.add_argument(
        "-d",
        "--discord-token",
        type=str,
        dest="discord_token",
        help="The discord token for your bot",
    )
    model_create_required_named.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key to use to create the model. Must either be passed in as an argument or set as an environment variable",
    )
    model_create_required_named.add_argument(
        "-c",
        "--channel",
        type=str,
        dest="channel",
        help="The ID of the discord channel you want to use",
    )
    model_create_required_named.add_argument(
        "-u",
        "--user",
        type=str,
        dest="user",
        help="The unique username of the discord user you want to use",
    )

    model_create_optional_named.add_argument(
        "-b",
        "--base-model",
        choices=["davinci", "babbage", "none"],
        default="none",
        required=False,
        dest="base_model",
        help="The base model to use for customization, where `davinci` is the more advanced model and is recommended, while `babbage` is a simpler model and should be reserved for testing since it is cheaper, and `none`, skips the training step: DEFAULT=none",
    )
    model_create_optional_named.add_argument(
        "--ttime",
        "--thought-time",
        type=int,
        default=5,
        required=False,
        dest="thought_time",
        help='The maximum amount of time in seconds to consider two individual messages to be part of the same "thought": DEFAULT=10',
    )
    model_create_optional_named.add_argument(
        "--tmax",
        "--thought-max",
        type=int,
        default=None,
        required=False,
        dest="thought_max",
        help="The maximum length in words of each thought: DEFAULT=None",
    )
    model_create_optional_named.add_argument(
        "--tmin",
        "--thought-min",
        type=int,
        default=6,
        required=False,
        dest="thought_min",
        help="The minimum length in words of each thought: DEFAULT=4",
    )
    model_create_optional_named.add_argument(
        "-m",
        "--max-entries",
        type=int,
        default=1000,
        required=False,
        dest="max_entries",
        help="The max amount of entries (by lines) that may exist in the dataset: DEFAULT=1000",
    )
    model_create_optional_named.add_argument(
        "--os",
        "--offset",
        type=int,
        default=0,
        required=False,
        dest="offset",
        help="The offset by line index starting at 0 for where to start selecting lines for the dataset: DEFAULT=0",
    )
    model_create_optional_named.add_argument(
        "-s",
        "--select-mode",
        choices=["sequential", "distributed"],
        default="sequential",
        required=False,
        dest="select_mode",
        help="The method to select lines for the dataset, where `sequential` mode will select lines in chronological order, while `distributed` mode will select an even distribution of lines: DEFAULT=sequential",
    )
    model_create_optional_named.add_argument(
        "--reverse_lines",
        action="store_true",
        required=False,
        dest="reverse",
        help="Reverse the order in which to select lines for the dataset",
    )
    model_create_optional_named.add_argument(
        "--dirty",
        action="store_false",
        required=False,
        dest="dirty",
        help="Skip the clean up step for outputted files",
    )
    model_create_optional_named.add_argument(
        "--redownload",
        action="store_true",
        required=False,
        dest="redownload",
        help="Redownload the discord chat logs",
    )
    model_create_optional_named.add_argument(
        "--use_existing",
        action="store_true",
        required=False,
        dest="use_existing",
        help="Use an existing dataset that may have been manually revised",
    )


def setup_model_delete(model_subcommand):
    model_delete = model_subcommand.add_parser(
        "delete",
        description="Delete an openAI customized model",
    )
    model_delete_required_named = model_delete.add_argument_group(
        "required named arguments"
    )

    model_delete_required_named.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key associated with the model to delete. Must either be passed in as an argument or set as an environment variable",
    )
    model_delete_required_named.add_argument(
        "-m",
        "--model-id",
        type=str,
        dest="model_id",
        help="Target model id",
    )


def setup_job_list(job_subcommand):
    job_list = job_subcommand.add_parser(
        "list", description="List your openAI customization jobs"
    )
    job_list_required_named = job_list.add_argument_group("required named arguments")
    job_list_optional_named = job_list.add_argument_group("optional named arguments")

    job_list_required_named.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key to list the jobs for. Must either be passed in as an argument or set as an environment variable",
    )
    job_list_optional_named.add_argument(
        "--full",
        action="store_true",
        required=False,
        dest="full",
        help="Return the full details of all the jobs",
    )


def setup_job_info(job_subcommand):
    job_info = job_subcommand.add_parser(
        "info", description="Get an openAI customization job's info"
    )
    job_info_required_named = job_info.add_argument_group("required named arguments")

    job_info_required_named.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key associated with the job to see the info for. Must either be passed in as an argument or set as an environment variable",
    )
    job_info_required_named.add_argument(
        "-j",
        "--job-id",
        type=str,
        dest="job_id",
        help="Target job id",
    )


def setup_job_events(job_subcommand):
    job_events = job_subcommand.add_parser(
        "events", description="Get an openAI customization job's events"
    )
    job_events_required_named = job_events.add_argument_group(
        "required named arguments"
    )

    job_events_required_named.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key associated with the job to see the events for. Must either be passed in as an argument or set as an environment variable",
    )
    job_events_required_named.add_argument(
        "-j",
        "--job-id",
        type=str,
        dest="job_id",
        help="Target job id",
    )


def setup_job_cancel(job_subcommand):
    job_cancel = job_subcommand.add_parser(
        "cancel", description="Cancel an openAI customization job"
    )
    job_cancel_required_named = job_cancel.add_argument_group(
        "required named arguments"
    )

    job_cancel_required_named.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key associated with the job to cancel. Must either be passed in as an argument or set as an environment variable",
    )
    job_cancel_required_named.add_argument(
        "-j",
        "--job-id",
        type=str,
        dest="job_id",
        help="Target job id",
    )