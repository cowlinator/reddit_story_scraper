Download multi-post stories from Reddit (such as those found on HFY) into one document.

= Installation = 

You will need to install the python modules in requirements.txt

python -m pip install -r requirements.txt

= Usage=
usage: scrape.py [-h] [-u URL] [-n NEXT] [-m MAX] [-f {plaintext,html}] [-o OUTPUT] [-s SLEEP]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     the root (first) url to start from
  -n NEXT, --next NEXT  the link to the next page
  -m MAX, --max MAX     the max number of pages to scrape
  -f {plaintext,html}, --format {plaintext,html}
                        output format
  -o OUTPUT, --output OUTPUT
                        the output file
  -s SLEEP, --sleep SLEEP
                        how many seconds to sleep between each request

= Example usage =

python scrape.py --url https://www.reddit.com/r/HFY/comments/u19xpa/the_nature_of_predators/ --next Next --max 200 --format plaintext --output The_Nature_Of_Predators.txt --sleep 1
