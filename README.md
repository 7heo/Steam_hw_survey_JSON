Steam_hw_survey_JSON
====================

A simple python script to turn VALVe's Steam Hardware Survey data into JSON

Beware, however, that this is only tested with/for the video card data.

Usage
-----

To use this repository, you need to either know how to parse JSON, or have `curl` and `jq` installed on a POSIX compliant (for [`bc`](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/bc.html), [`sed`](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/sed.html) and [`tr`](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/tr.html)) Operating System, and run:

```sh
curl -SsL https://github.com/7heo/Steam_hw_survey_JSON/releases/download/$_CURRENT_MONTH/steam_hw_survey_videocards.json \
| jq '."ALL VIDEO CARDS"|with_entries(select(.key | startswith("$_BRAND")))|.[]|.$_MONTH' \
| tr '\n' '+' | sed 's/+$/\n/' | bc -l
```

Where `_BRAND` is set to either "NVIDIA", "AMD" or "Intel" (or something else entirely), `_CURRENT_MONTH` is set to the month (in [`date`](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/date.html)'s `%b` format) you want to download the information from, and `_MONTH` is set to the month (same format as for `_CURRENT_MONTH`, but all in UPPER CASE) you want the data for (which has to be, at the time of writing, 1 to 5 months prior to the `_CURRENT_MONTH` value).
> [!TIP]
> Note that you can also replace the [`startswith`](https://jqlang.github.io/jq/manual/#startswith) `jq` function with the [`contains`](https://jqlang.github.io/jq/manual/#contains) one.
