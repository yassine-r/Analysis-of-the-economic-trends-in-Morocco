def start():

    from preprocessing import Cleaner
    from scrapping import scrap_articles
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer
    from creedentials import Database
    import uuid
    from time import strptime
    import datetime
    import sys
    import logging
    logging.basicConfig(level=logging.INFO, filename="log.txt")

    try:
        articles=scrap_articles()
        logging.info("Scrapping at {a}".format(a=datetime.datetime.now()))
    except (Exception) as error:
        logging.error("Error scrapping at {a}, error: {b}".format(a=datetime.datetime.now(),b=error))
        sys.exit(0)

    cleaner=Cleaner()
    cleaned_articles=cleaner.clean_documents(articles)
    cleaned_articles_content=[article["content"] for article in cleaned_articles]

    tfIdfTransformer = TfidfTransformer(use_idf=True)
    countVectorizer = CountVectorizer(ngram_range = (2,2))
    wordCount = countVectorizer.fit_transform(cleaned_articles_content)
    newTfIdf = tfIdfTransformer.fit_transform(wordCount)
    df = pd.DataFrame(newTfIdf.toarray(), columns=countVectorizer.get_feature_names())

    try:
        db=Database()
        for i in range(len(cleaned_articles)):
            
            article=cleaned_articles[i]
            date=article["date"].split()
            bigrams=df.iloc[i].sort_values(ascending=False).head(100).index
            tf_idfs=df.iloc[i].sort_values(ascending=False).head(100).values

            article_id=uuid.uuid1()
            time_id=uuid.uuid1()

            db.insert_into_article_dimension(url=article["url"],author=article["author"],website=article["website"],article_id=article_id)
            db.insert_into_time_dimension(time_id=time_id,day=date[0],year=date[-1],month=strptime(date[1][:3],'%b').tm_mon)
            
            for j in range(len(bigrams)):
                bigram_id=uuid.uuid1()
                
                db.insert_into_bigram_dimension(bigram_name=bigrams[j],bigram_id=bigram_id)
                db.insert_into_fact_bigram(article_id=article_id,time_id=time_id,tf_idf=tf_idfs[j],bigram_id=bigram_id)

        logging.info("Saved to db at {a}".format(a=datetime.datetime.now()))

    except (Exception) as error:
        logging.error("Error Saving to db at {a}, error: {b}".format(a=datetime.datetime.now(),b=error))
        sys.exit(0)


start()