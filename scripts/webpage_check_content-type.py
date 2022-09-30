# Simple Request to check what a webpage's Application type is 

import requests

url = "https://stackoverflow.com/questions/38690586/determine-if-url-is-a-pdf-or-html-file"
url = "https://dl.acm.org/doi/pdf/10.5555/2627435.2670313"

response = requests.get(url)
content_type = response.headers.get("content-type")
print("type:", content_type)
content_type = content_type.split(";")[0]
print("type:", type(content_type))
print(content_type)


# Logic to Map the Webpage
if content_type == "text/html":
    print("HTML DOCUMENT")
elif content_type == "application/pdf":
    print("PDF DOCUMENT")

