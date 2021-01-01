#!/usr/bin/env python3

import yaml
from dataclasses import dataclass, field
from typing import List, Dict
import json
from tabulate import tabulate
import argparse
from pathlib import Path
import musicbrainzngs

id_file="brainz.yaml"
cache_dir=".cache"

@dataclass
class Series:
	series_id: str = ""
	series_key: str = ""
	data: Dict[str, str] = field(default_factory = lambda: ({}))
	table: List[List[str]] = field(default_factory = lambda: ([]))
	headers: List[str] = field(default_factory = lambda: ([]))

	def __post_init__(self):
		musicbrainzngs.set_useragent("tastybrainz", "0.1", "https://github.com/a74nh/")
		self.__get_series_data()

	def __get_series_data(self):
		Path(cache_dir).mkdir(parents=True, exist_ok=True)
		cache_file=f'{cache_dir}/{self.series_id}.json'
		try:
			with open(cache_file) as f:
				self.data = json.load(f)
			self.relations = self.data["release_group-relation-list"]
		except FileNotFoundError:
			print('Reading series from musicbrainz:',self.series_id)
			self.data = musicbrainzngs.get_series_by_id(self.series_key, includes=["release-group-rels"])["series"]
			self.relations = self.data["release_group-relation-list"]
			self.__get_artist_credits()
			with open(cache_file, 'w') as f:
				json.dump(self.data, f)

	def __get_artist_credits(self):
		datarel=self.relations
		for rel in datarel:
			i=rel["release-group"]["id"]
			cache_file=f'{cache_dir}/release-group-{i}.json'
			try:
				with open(cache_file) as f:
					credit = json.load(f)
			except FileNotFoundError:
				print('Reading artists from musicbrainz:',rel["release-group"]["title"])
				credit=musicbrainzngs.get_release_group_by_id(i, includes=["artist-credits"])
				with open(cache_file, 'w') as f:
					json.dump(credit, f)
			rel["release-group"]["artist-credit"] = credit["release-group"]["artist-credit"]
			rel["release-group"]["artist-credit-phrase"] = credit["release-group"]["artist-credit-phrase"]

	def __repr__(self):
		return f'{self.data["name"]}'

	def __generate_row_headers(self,other_lists):
		self.headers=["num", "title", "artist", "year"]
		for other in other_lists:
			self.headers.append(other.series_id)

	def generate_table(self,other_lists,max_len):
		self.__generate_row_headers(other_lists)
		ret=[]
		self.table = [None]*len(self.relations)
		self.counts = [0]*len(other_lists)

		for rel in self.relations:
			key=int(rel['ordering-key'])
			g=rel["release-group"]
			title=g['title'][0:max_len]
			artist=g["artist-credit-phrase"][0:max_len]
			yr=g['first-release-date'].split("-")[0]
			row = [key,title,artist,yr]

			c=0
			for other in other_lists:
				other_rel=other.__find_relation(g["id"])
				try:
					other_key=int(other_rel['ordering-key'])
					diff=other_key-key
					if diff==0:
						diff="-"
					elif diff<0:
						diff="v"+str(-diff)
					else:
						diff="^"+str(diff)
					self.counts[c]=self.counts[c]+1
				except TypeError:
					diff="x"
				row.append(diff)
				c=c+1

			self.table[key-1] = row

	def __find_relation(self,fid):
		for r in self.relations:
			if r["release-group"]["id"]==fid:
				return r
		return None

	def sort_by_column(self,col):
		colval=self.headers.index(col)
		if colval<4:
			self.table.sort(key=lambda x: x[colval])
		else:
			def difftonum(x):
				if x=="x":
					return 9999999
				elif x=="-":
					return 0
				elif x[0]=="^":
					return int(x[1:])
				elif x[0]=="v":
					return -int(x[1:])
				raise ValueError
			self.table.sort(key=lambda x: difftonum(x[colval]))


	def tabulate(self,tablefmt):
		t=self.table
		if self.counts:
			t=t+[["totals","","",""]+self.counts]
		return f'{self.data["name"]}\n{tabulate(t,tablefmt=tablefmt,headers=self.headers)}'

def load_config():
	with open(id_file, 'r') as f:
		return yaml.safe_load(f)

def generate_table(series_id, compare_ids=[], truncate=None, id_config=None):
	if not id_config:
		id_config = load_config()
	base_list=Series(series_id,id_config[series_id])
	other_list=[Series(i,id_config[i]) for i in compare_ids]
	base_list.generate_table(other_list,truncate)
	return base_list

def main():
	id_config=load_config()

	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--sort", help="sort by column", type=str)
	parser.add_argument("--style", help="tabulate style", type=str, default="orgtbl")
	parser.add_argument("-t", "--truncate", help="truncate entries", type=int, default=None)
	parser.add_argument('id', nargs="?", help="id of series to show", choices=[x for x in id_config], default="rs2020")
	parser.add_argument('compare_ids', nargs='*', help="ids of series to compare against")
	args = parser.parse_args()

	base_list = generate_table(args.id,args.compare_ids,args.truncate,id_config)
	if args.sort:
		base_list.sort_by_column(args.sort)

	try:
		print(base_list.tabulate(args.style))
	except (BrokenPipeError, IOError):
		pass

if __name__ == "__main__":
    main()
