# Util to Download a PDF, Extract the Text Content and then delete the Binary Version (passes text to func as webpage content)
import os
import PyPDF2
import urllib.request




# Get Pdfs from URLs & Delete after extracting Contents
def pdf_extractor(url, file_name):
    # Get Raw PDF Data from Internet -- keep in temporary buffer
    print("Retrieving PDF Text from {}".format(url))
    response = urllib.request.urlopen(url)
    #file = open(file_name + ".pdf", "wb")
    file = open(file_name, "wb") #assuming ".pdf" will be in URL, that is logic for calling this library
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
    pdf_reader = PyPDF2.PdfFileReader(pdf)
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
