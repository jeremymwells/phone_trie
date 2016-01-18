import urllib3
import yaml

def get():
	# maybe handle multiple word sources? -->
	with open("config.yaml", 'r') as stream: src = yaml.load(stream)['word-sources'][0]
	return urllib3.PoolManager().request(src['verb'], src['url']).data.split("\r\n")

