# WIK
WIK is a command-line tool to view Wikipedia pages from your terminal.
It also lets you search Wikipedia articles with a single query.

<div align="center">

  ### \[[Installation](#installation)] \[[Options](#options)] \[[Examples](#example)] \[[Contribution](#contribution)]

</div>

## Requirements
- Python3
- beautifulsoup4

## Installation

#### Linux

##### From Source
```bash
sudo pip3 install beautifulsoup4 flit_core
git clone https://github.com/yashsinghcodes/wik.git
cd wik
sudo pip3 install .
```

##### PYPI
```bash
sudo pip3 install wik
```

#### Windows

##### From Source

```
pip install beautifulsoup4 flit_core
git clone https://github.com/yashsinghcodes/wik.git
cd wik
pip install .
```
>Note: Windows users should add Python to their environment variables.

##### PYPI
```
pip install wik
```

## Options
Using WIK is simple.

```
usage: wik [-h] [-s SEARCH] [-i INFO] [-q QUICK] [-l LANG] [-x] [--no-cache]
           [--clear-cache]

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH, --search SEARCH
                        Search any topic
  -i INFO, --info INFO  Get info on any topic
  -q QUICK, --quick QUICK
                        Get the summary on any topic
  -l LANG, --lang LANG  Get info in your native language (default english)
  -x, --rand            Get random Wikipedia article
  --no-cache            Disable on-disk cache for this run
  --clear-cache         Clear cached pages and exit
```

## Example

```bash
$ wik -i Linux
```
![carbon (6)](https://user-images.githubusercontent.com/32360914/155836508-63c7424f-b7d6-4871-a170-e2f0fdd6617d.png)

```bash
$ wik -q Linux
```
![carbon (7)](https://user-images.githubusercontent.com/32360914/155836565-281eb678-9605-4131-a6c9-9a6c871bdc77.png)

```
$ wik -i Linux -l br
```
![lang](https://user-images.githubusercontent.com/32360914/155878486-e46c909d-4373-4cae-8ada-3d6df8545a96.png)

### Cache
WIK stores pages on disk so repeated queries are instant and can work offline. You can
disable caching per run or clear the cache:

```
wik --no-cache -i Linux
wik --clear-cache
```


## Contribution
You can contribute by opening an issue or making a pull request. If you have ideas or
feedback, you can [contact me](mailto:yash9vardhan@gmail.com).
