__version__ = "1.0.0"

import argparse
import os
# import re
# from click import confirm
import sqlite3
import requests
import json
from pathlib import Path
from tqdm import tqdm 
import sys
import wget 

def main(cwd=None):

	my_parser = argparse.ArgumentParser(description="download and install deb packages from github")

	my_parser.add_argument('-i',"-install",
							metavar="package", 
							nargs=1,
							help="install package")

	my_parser.add_argument('-l','-list',
							action="store_true",
							dest="list",
							help='check list of upgradable packages from your list')

	my_parser.add_argument('-show',
							metavar="package",
							nargs=1,
							help='show the detaile of package')


	my_parser.add_argument('-ud',"-update",
							action="store_true",
							dest="update",
							help="update your full packages list")

	my_parser.add_argument('-v',"-version",
							action="store_true",
							dest="version",
							help="check version of sachet")

	my_parser.add_argument('-n',"-new",
						action="store_true",
						dest="new",
						help="update deb to latest version")


	args = my_parser.parse_args()

	install = bool(args.i)
	list = bool(args.list)
	show = bool(args.show)
	update = bool(args.update)
	# upgrade = bool(args.upgrade)
	version = bool(args.version)
	new = bool(args.new)

	conn  = sqlite3.connect("deb.db")
	cursor = conn.cursor()


	if (list):
		pkgs = cursor.execute("SELECT name,version,architecture FROM pkgs ORDER BY name").fetchall()
		conn.close()
		# print(pkgs)

		for i in pkgs:
			list_pks = []
			sep = " "
			c = sep.join(i)
			print(c)
	
		print("")

	elif (show):
		for i in args.show:
			pkgs = cursor.execute("SELECT name,version,architecture,description,section,maintainer,homePage FROM pkgs WHERE name = ?", (i,),).fetchall()
			conn.close()
		# print(pkgs)
		# print(type(pkgs))

		for pkg in pkgs:
			# print(pkg)
			# print(type(pkg))
			print(f"Package: {pkg[0]}")
			print(f"Version: {pkg[1]}")
			print(f"Architecture: {pkg[2]}")
			print(f"Section: {pkg[4]}")
			print(f"Maintainer: {pkg[5]}")
			print(f"Homepage: {pkg[6]}")
			print(f"Description: {pkg[3]}")

		print("")

	elif (install):
		print(args.i)
		for i in args.i:
			pkgs = cursor.execute("SELECT url FROM pkgs WHERE name = ?", (i,),).fetchall()
			conn.close()
		# print(pkgs)

		for j in pkgs:
			# r = requests.get(j[0])
			print(j[0])
			url = j[0]

			def bar_custom(current, total, width=80):
				print("Downloading : %d%% [%d / %d] bytes" % (current / total * 100, current, total))

			# wget.download(url, bar=bar_custom)
			wget.download(url)

			# home_path = Path.home()
			# sub_path = "tmp"

			# filesize = int(requests.head(url).headers["Content-Length"])
			# filename = os.path.basename(url)

			# os.makedirs(os.path.join(home_path, sub_path), exist_ok=True)

			# dl_path = os.path.join(home_path, sub_path, filename)
			# chunk_size = 1024


			# with requests.get(url, stream=True) as r, open(dl_path, "wb") as f, tqdm(
			#         unit="B",  # unit string to be displayed.
			#         unit_scale=True,  # let tqdm to determine the scale in kilo, mega..etc.
			#         unit_divisor=1024,  # is used when unit_scale is true
			#         total=filesize,  # the total iteration.
			#         file=sys.stdout,  # default goes to stderr, this is the display on console.
			#         desc=filename  # prefix to be displayed on progress bar.
			# ) as progress:
			#     for chunk in r.iter_content(chunk_size=chunk_size):
			#         datasize = f.write(chunk)
			#         progress.update(datasize)

		# resp = json.loads(r.text)
		# print(resp['browser_download_url'])

	elif version:
		print(__version__)

	elif new:
		os.system("pip3 install deb --upgrade")

	else:
		print("run sachet -h for help")

if __name__ == "__main__":
    main()
