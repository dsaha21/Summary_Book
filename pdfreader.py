import PyPDF2
def pdfread(book):
    txtlist = []

    # creating a pdf file object
    pdfFileObj = open(book, 'rb')

    # creating a pdf reader object
    #pdfr = PyPDF2.PdfFileReader(pdfFileObj)
    pdfr = PyPDF2.PdfReader(pdfFileObj)

    # printing number of pages in pdf file
    #print(pdfRead.numPages)
    print(len(pdfr.pages))

    for i in range(len(pdfr.pages)):

        # creating a page object
        pageObj = pdfr.getPage(i)

        # extracting text from page
        # print(pageObj.extractText())
        print("************** page reading "+str(i)+" done *******************")
        txtlist.append(pageObj.extractText())

    # closing the pdf file object
    pdfFileObj.close()
    return txtlist

# article = " ".join(txtlist)

# print(article)