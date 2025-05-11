from requests_html import HTMLSession

base_url = 'https://www.beerwulf.com/en-gb/c/beers?segment-Beers&catalogCode=Beer_1'

session = HTMLSession()
r = session.get(base_url)
path='C:\\webdrivers\\chromedriver'
r.html.render(sleep=1, executablepath=path)

print(r.status_code)
