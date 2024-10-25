from wordcloud import WordCloud
from urlextract import URLExtract
import pandas as pd
from collections import Counter
extract = URLExtract()
def fetch_stat(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    # extract url links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words) ,num_media_msg , len(links)

def most_busy_user(df):
    x = df['user'].value_counts().head()
    # calculate the number of msg per user and round off them
    #rename cols
    df=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percentage'})
    return x,df

#wordcloud
def create_wordcloud(selected_user ,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc= WordCloud(width=400,height=400,min_font_size=10,background_color='white')
    temp['message']= temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_cmn_word(selected_user , df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']



    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df =pd.DataFrame(Counter(words).most_common(20))
    return return_df

#timeline
def timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline







 #  if selected_user== 'Overall':
        #1 fetch the num of mgs
#        num_messages = df.shape[0]
        #2 number of words
#        words = []
 #       for message in df['message']:
 #           words.extend(message.split())
  #      return num_messages, len(words)
   # else:
    #    new_df = df[df['user'] == selected_user]
    #    num_messages = new_df.shape[0]
     #   words =[]
     #   for message in df['message']:
      #      words.extend(message.split())

       # return num_messages, len(words)



