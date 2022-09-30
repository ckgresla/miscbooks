# Util to Download a PDF, Extract the Text Content and then delete the Binary Version (passes text to func as webpage content)
import os
import PyPDF2
import urllib.request


# Issue w SSL Certs (popped up in UDE, not in alexandria)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Create a Header
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/pdf;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


# Get Pdfs from URLs & Delete after extracting Contents
def pdf_extractor(url, file_name):
    # Get Raw PDF Data from Internet -- keep in temporary buffer
    print("Retrieving PDF Text from {}".format(url))

    request = urllib.request.Request(url, None, headers=header)
    # response = urllib.request.urlopen(url) #directly w URL
    response = urllib.request.urlopen(request) #request w Custom Header

    file = open(file_name, "wb") #assuming ".pdf" will be in URL, that is logic for calling this library
    #file = open(file_name + ".pdf", "wb")
    file.write(response.read())
    file.close()

    # Get Text Content & Title (if possible)
    doc_text, doc_title = extract_text(file_name)

    # Remove PDF from Dir after extracting Text
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        print("No file to remove...\nWas looking for file–'{}'".format(file_name))

    if doc_title == None:
        return doc_text, "NA"
    else:
        return doc_text, doc_title


# Calls PyPDF2 to get Text from Local PDF
def extract_text(file_path):
    """Util to get text from PDF files in local dir, need request the file content from Web first"""
    pdf = open(file_path, "rb")
    try:
        pdf_reader = PyPDF2.PdfFileReader(pdf)
    except Exception as E:
        print(f"Error in PDF Parsing: {E} -- trying again without Strict Mode")
        try:
            pdf_reader = PyPDF2.PdfFileReader(pdf, strict=False) #try again
        except Exception as E:
            print(f"2nd Error in PDF Parsing: {E} -- Exiting Text Extraction")
            return None, None

    count_pages = pdf_reader.numPages
    doc_string = ""

    if count_pages > 3:
        # Truncate docs that are very long, assuming first few pages are most relevant
        for i in range(3):
            page = pdf_reader.getPage(i)
            doc_string += page.extractText() #text from current page
    else:
        # Extract all Text from PDF
        for i in range(count_pages):
            page = pdf_reader.getPage(i)
            # print(f"Page {i}")
            # print(page.extractText())
            doc_string += page.extractText() #text from current page

    # Parse out Title of PDF if Possible- https://pypdf2.readthedocs.io/en/latest/user/metadata.html
    doc_title = pdf_reader.metadata.title

    print("PDF Text Extracted -- {} Characters".format(len(doc_string)))
    return doc_string, doc_title



# Example Usage
if __name__ == "__main__":
    url = "https://www.cs.princeton.edu/courses/archive/fall13/cos597E/papers/howtoread.pdf"
    content, title = pdf_extractor(url, "tmp.pdf")
    print("title: ", title, "\n") #will return "NA" if there is no title in metadata of pdf (could still be a reasonable title though)
    print("content: ", content, "\n")

