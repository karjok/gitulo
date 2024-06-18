from requests import get
from bs4 import BeautifulSoup as BS
from user_agent import generate_user_agent
from concurrent.futures import ThreadPoolExecutor
import time
import sys

## initializing

# colors
cl_grey = "\033[90m"
cl_red = "\033[91m"
cl_green = "\033[92m"
cl_yellow = "\033[93m"
cl_cyan  = "\033[96m"
cl_normal = "\033[0m"

# utils functions
def get_headers():
	headers = {"User-Agent": generate_user_agent()}
	return headers
def read_list(file):
	lines = [i.strip() for i in open(file,"r").readlines()]
	return lines
def now_time():
	return time.strftime("%H:%M:%S")

# main functions
def check_for_git(domain):
	# domain format fixing
	domain = domain[:-1] if domain.endswith("/") else domain
	domain = domain.replace("https://").replace("http://") if domain.startswith("http") else domain

	url = "/".join([domain,".git/"])
	try:
		try:
			resp = get("http://"+url, headers=get_headers(), timeout=10)
		except SSLError:
			resp = get("https://"+url, headers=get_headers(), timeout=10)

		bs = BS(resp.text,"html.parser")
		try:
			title = f"{cl_green}|{cl_normal} {cl_grey}{bs.title.text}{cl_normal}"
		except:
			title = ""
		try:
			content_length =  f"{cl_green}|{cl_normal} {cl_grey}{resp.headers['Content-Length']}{cl_normal}"
		except:
			content_length = ""

		code = resp.status_code
		if code == 200:
			if "403" in resp.text:
				color = cl_yellow
				code = 403
			elif "Index Of" in resp.text:
				color = cl_green
			else:
				if resp.history:
					code = resp.history[0].status_code
					color = cl_cyan
				else:
					code = "???"
					color = cl_grey
		elif code == 403:
			color = cl_yellow
		elif code == 500:
			color = cl_red
		else:
			color = cl_grey

		print(f"[{now_time()}] {cl_green}[{color}{code}{cl_green}]{cl_normal} {resp.url} {content_length} {title}")
	except Exception as E:
		color = cl_red
		print(f"[{now_time()}] {cl_green}[{color}ERR{cl_normal}{cl_green}]{cl_normal} {resp.url} {cl_green}|{cl_normal} {cl_grey}{type(E).__name__}{cl_normal}")



def main():
	try:
		domain_list = read_list(input(f"[{now_time()}] {cl_green}[{cl_normal}!{cl_normal}{cl_green}]{cl_normal} Input domain list path: "))
		domain_list_filtered = list(set(domain_list))
	except:
		exit()

	print(f"[{now_time()}] {cl_green}[{cl_normal}!{cl_green}]{cl_normal} {cl_green}{len(domain_list)} {cl_normal} url(s) loaded, reduced to {len(domain_list_filtered)} Starting threads..")
	print("\n")
	threads = ThreadPoolExecutor(max_workers=50)
	futures = []
	for domain in domain_list_filtered:
		if not "panel" in domain:
			try:
				# check_for_git(domain)
				futures.append(threads.submit(check_for_git,domain))
			except KeyboardInterrupt:
				break


if __name__ == "__main__":
	main()


