from transformers import pipeline
from pdfreader import txtlist

summarizer = pipeline("summarization",model="facebook/bart-large-cnn",device=0)
article_summary = {}
key = 0
for pageinfo in txtlist:
    # print(summarizer(pageinfo, max_length=100, min_length=30, do_sample=False)[0]['summary_text'])
    # print(summarizer[0])
    # print(summarizer[0]['summary_text'])
    print("**********page "+str(key)+" summerized *************")
    article_summary[key]=(summarizer(pageinfo, max_length=100, min_length=5, do_sample=False)[0]['summary_text'])
    key +=1






























































































# summary = " ".join(article_summary)

print(article_summary)


