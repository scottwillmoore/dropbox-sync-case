import core
import click


CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-t",
    "--token",
    "access_token",
    required=True,
    help="The Dropbox OAuth 2 access token.",
)
@click.option(
    "-d",
    "--dropbox",
    "dropbox_path",
    required=True,
    type=click.Path(),
    help="The path to the local Dropbox directory.",
)
@click.option(
    "-s",
    "--scope",
    "scope_path",
    type=click.Path(),
    default="",
    help="Restrict the sync of capitalisations to a specific directory within your Dropbox.",
)
@click.option(
    "-m",
    "--mode",
    required=True,
    type=click.Choice(["push", "pull"]),
    help="Choose whether to 'push' or 'pull' the capitalisations to your Dropbox.",
)
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    help="Do not modify any local or cloud files or directories. Instead show what would've been changed.",
)
@click.pass_context
def cli(ctx, access_token, dropbox_path, scope_path, mode, dry_run):
    core.run(ctx, access_token, dropbox_path, scope_path, mode, dry_run)
