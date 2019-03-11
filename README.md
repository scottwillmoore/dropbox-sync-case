# Dropbox Sync Case

Use this project to synchronise the capitalisation of your folders between the cloud and local files. You can *push* the capitalisation from your local files to your cloud files, or *pull* the capitalisation from your cloud files to your local files.

*Why would I ever want to do that?*

Dropbox treats all files as case-insensitive, which means that the file `hello.txt` and `HELLO.txt` are exactly the same. When you rename a file to the same name (e.g. `hello.txt` to `HELLO.txt`), the Dropbox client will not push this change to the cloud. This means that all other devices that you sync your files onto will pull the file down as `hello.txt`, even though you've renamed your file to `HELLO.txt`. This tool aims to solve that problem. It works by identifying differences in capitalisation between your local files and cloud files and then attempts to correct them.


## Warning!

As always, it is very possible that bugs (or edge cases that I haven't discovered) exist in this script. I would recommend taking a backup before executing the script. In addition, you should carefully examine the output of the script with the `--dry-run` to double check that everything looks okay.

While in theory this has been designed so that it should work on all platforms, so far I have only been able to test on Windows. I have been careful to ensure it should work on non-Windows platforms, but it is still very possible that bugs exist (or edge-cases that I haven't discovered). Again, I would carefully examine the ouput of the script with `--dry-run` to double check that every looks okay.

## Requirements

Make sure that you have Python 3 installed, along with the `pip` (required) and `venv` (optional) packages.

## Usage

If you do not care about creating a `venv`, then simply run `pip install .`. Otherwise, create a `venv` then run `pip install .`.

The package exposes the CLI `dropbox-sync-case` which can be controlled with the following options.

````
dropbox-sync-case -h

Usage: dropbox-sync-case [OPTIONS]

Options:
  -t, --token TEXT        The Dropbox OAuth 2 access token.  [required]
  -d, --dropbox PATH      The path to the local Dropbox directory.  [required]
  -s, --scope PATH        Restrict the sync of capitalisations to a specific
                          directory within your Dropbox.
  -m, --mode [push|pull]  Choose whether to 'push' or 'pull' the
                          capitalisations to your Dropbox.  [required]
  -n, --dry-run           Do not modify any local or cloud files or
                          directories. Instead show what would've been
                          changed.
  -h, --help              Show this message and exit.

````

You should always run the tool with `-n` (perform a dry run), until you are happy that the tool will modify the correct files. Once you are ready, then remove the `-n`.

````
dropbox-sync-case -m push -d C:\Users\Scott\Dropbox -t <access_token> -n

PUSH: C:\Users\Scott\Dropbox\hello.txt -> Hello.txt
...
````

## Contributions

If you see any issues and would like to fix them, feel free to create a pull request or raise an issue.


## Todo

Fix the many TODOs still littered throughout script.