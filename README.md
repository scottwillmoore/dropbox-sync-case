# Dropbox Sync Case

Use this project to synchronise the capitalisation of your folders between the cloud and local files. You can *push* the capitalisation from your local files to your cloud files, or *pull* the capitalisation from your cloud files to your local files.

***Why would I ever want to do that?***

Dropbox treats all files as case-insensitive, which means that the file `hello.txt` and `HELLO.txt` are exactly the same. When you rename a file to the same name (e.g. `hello.txt` to `HELLO.txt`), the Dropbox client will not push this change to the cloud. This means that all other devices that you sync your files onto will pull the file down as `hello.txt`, even though you've renamed your file to `HELLO.txt`. This tool aims to solve that problem. It works by identifying differences in capitalisation between your local files and cloud files and then attempts to correct them.


## Warning!

For now, turn off all instances of Dropbox clients that are connected to your account. I have had the Dropbox client delete the directory with the old name, only to have to download all the data from this directory to put it into the directory with the new name.

As always, it is very possible that bugs (or edge cases that I haven't discovered) exist in this script. I would recommend taking a backup before executing the script. In addition, you should carefully examine the output of the script with the `--dry-run` to double check that everything looks okay.

While in theory this has been designed so that it should work on all platforms, so far I have only been able to test on Windows. I have been careful to ensure it should work on non-Windows platforms, but it is still very possible that bugs exist (or edge-cases that I haven't discovered). Again, I would carefully examine the ouput of the script with `--dry-run` to double check that every looks okay.

## Requirements

Make sure that you have Python 3 installed, along with the `pip` (required) and `venv` (optional) packages.

You must also generate an OAuth 2 access token for your account. This is easy to do. Simply go to the [Dropbox API Explorer](https://dropbox.github.io/dropbox-api-v2-explorer/#users_get_current_account), authenticate with your Dropbox account and then click 'Get Token'.

## Usage

To use `dropbox-sync-case` in a virtual environment you must run the following commands.

````bash
# Ensure you are in the directory of the script.
cd sync-dropbox-case

# Create a virutal environment.
python -m venv venv

# Enter the virutal environment.
./venv/Scripts/activate

# Install dropbox-sync-case and required packages.
pip install .

# Run dropbox-sync-case commands.
dropbox-sync-case -h

# Exit the virtual environment.
deactivate
````

The `dropbox-sync-case` CLU can be controlled with the following options.

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

You should always run the tool with `--dry-run`, until you are happy that the tool will modify the correct files. Once you are ready, then remove the `--dry-run`.

## Contributions

If you see any issues and would like to fix them, feel free to create a pull request or raise an issue.


## Todo

Fix the many TODOs still littered throughout script.

I believe the script crashes if you call the Dropbox API too many times due to rate limitting. This could be fixed by checking this error message and exponentially backing off. In addition, the script should be able to handle when the API returns an error.

Moving to operations instead of repeating the same API call many, many times should also improve the reliability of the script.

There also appears to be an issue, whereby Dropbox clients will resync every file in a folder after a name change. This will require further investigation. This is extremely annoying as it will redownload all the files.