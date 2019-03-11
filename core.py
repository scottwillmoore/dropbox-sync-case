import click
from os import walk
from pathlib import Path, PurePosixPath
from dropbox import Dropbox
from dropbox.exceptions import AuthError, BadInputError


def validate_dropbox_path(ctx, dropbox_path, scope_path):
    dropbox_path = Path(dropbox_path)
    if not dropbox_path.is_dir():
        ctx.fail("The dropbox path must be a valid directory.")

    return dropbox_path


def validate_scope_path(ctx, dropbox_path, scope_path):
    scope_path = PurePosixPath(scope_path)
    if not scope_path.is_absolute():
        scope_path = "/" / scope_path

    target_path = dropbox_path / scope_path.relative_to("/")
    if not target_path.is_dir():
        ctx.fail("The scope must be a valid directory inside the dropbox directory.")

    return scope_path, target_path


def validate_access_token(ctx, access_token):
    try:
        db = Dropbox(access_token)
        db.users_get_current_account()
    except AuthError:
        ctx.fail("The OAuth2 access token is invalid.")
    except BadInputError:
        ctx.fail("The OAuth2 access token token is malformed.")

    return db


def os_files_and_folders(dropbox_path, target_path):
    for path, folders, files in walk(target_path):
        entries = folders + files
        for entry in entries:
            yield Path(path, entry).relative_to(dropbox_path)


# TODO: Handle scope_path doesn't exist and other errors.
# TODO: Could show the progress of how many pages have been retrieved.
def db_files_and_folders(db, scope_path):
    entries = []

    result = db.files_list_folder(scope_path, recursive=True)
    entries.extend(result.entries)

    while result.has_more:
        result = db.files_list_folder_continue(result.cursor)
        entries.extend(result.entries)

    entries = list(map(lambda entry: PurePosixPath(entry.path_display), entries))

    return entries


# TODO: Handle collision and other errors.
def db_rename(db, old_path, new_path, temporary_suffix="_"):
    intermediate_path = old_path + temporary_suffix
    db.files_move(old_path, intermediate_path)
    db.files_move(intermediate_path, new_path)


def create_path_lookup(paths):
    lookup = {}

    for path in paths:
        lookup[path.as_posix().lower()] = path

    return lookup


# TODO: Could create a progress bar.
# TODO: Could rename using the batch API call. Make the script faster.
def run(ctx, access_token, dropbox_path, scope_path, mode, dry_run):
    dropbox_path = validate_dropbox_path(ctx, dropbox_path, scope_path)
    scope_path, target_path = validate_scope_path(ctx, dropbox_path, scope_path)
    db = validate_access_token(ctx, access_token)

    db_paths = db_files_and_folders(db, scope_path.as_posix())
    db_lookup = create_path_lookup(db_paths)

    for os_path in os_files_and_folders(dropbox_path, target_path):

        lookup_path = ("/" / os_path).as_posix().lower()
        if lookup_path in db_lookup:
            db_path = db_lookup[lookup_path]

            if os_path.name != db_path.name:
                if mode == "push":
                    new_db_path = "/" / os_path

                    click.echo("PUSH: " + str(db_path) + " -> " + os_path.name)

                    if not dry_run:
                        db_rename(db, db_path.as_posix(), new_db_path.as_posix())

                if mode == "pull":

                    click.echo("PULL: " + str(os_path) + " -> " + db_path.name)

                    if not dry_run:
                        old_os_path = dropbox_path / os_path
                        new_os_path = old_os_path.with_name(db_path.name)
                        old_os_path.rename(new_os_path)
