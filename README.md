# scrapebin

>**IMPORTANT**: This is under active development (aka "I'm tinkering around
>constantly") and most likely won't work. Do not rely on this. There are plenty
>of actually good pastebin-scraping tools out there!

This is a simple scraper for [Pastebin](https://pastebin.com), powered by their
Scraping API. It's designed to provide basic functionality without configuration effort.

Per default it ..

* .. downloads the metadata for each new paste and stores it into an
  SQlite-database
* .. fetches the content for each new paste and stores it as a textfile on your
  local disk

There is support for ..

* .. providing a list of regular expressions against which the title and content of all new pastes will be checked
* .. alerting via mail if there is a match

#### Usage

**Important**: If you don't have a [PRO account](https://pastebin.com/pro)
*and* have your IP-address whitelisted scrapebin won't work.

Make sure that the modules listed in `requirements.txt` are installed,
otherwise install them:

```
pip3 install -r requirements.txt
```

You can run it with the following command:

```
./scrapebin.py $storage_path
```

`$storage_path` is a local path the the user running scrapebin has r/w-access
to - this is a mandatory argument. For more information use `-h` for the
built-in help.

#### License

```
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar
  14 rue de Plaisance, 75014 Paris, France
 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
```
