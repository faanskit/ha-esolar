# SAJ eSolar Custom Integration - Basic Test
### Basic Test
To perform a basic test of the SAJ eSolar Data Downloader, edit the `basic_test.py` file and update your credentials
```
USER = "NAME"
PASSWORD = "PASSWORD"
```

Copy the file `esolar.py` to the same directory and run the script
```
python basic_test.py
```

This will create a file `output.txt` which contains the JSON output from your system.

### Simulated system
The data in `output.txt` can be used in the integration as a simulated environment.
Some tweaks of the output can be required depending on your JSON decoder.
E.g. `null` values may have to be changed to `None` and `true`/`false` may have to be changed to `True`/`False`

1. Edit the file `esolar_static_test.py` to include your data. Both `web_get_plant_static_h1_r5` and `get_esolar_data_static_h1_r5` needs to be updated.
2. Edit the file `esolar.py` from `BASIC_TEST = False` to `BASIC_TEST = True`

