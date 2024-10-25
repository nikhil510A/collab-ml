import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import preprocessor,helper

st.sidebar.title("Whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    #st.dataframe(df)

    #fetch unique user
    user_list =df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    #user_list.append("Overall")
    #user_list.index(0,"Overall")
    user_list.insert(0, "Overall")

    selected_user =st.sidebar.selectbox("show analysis wrt user",user_list)

    if st.sidebar.button("show analysis"):
        num_messages, words ,num_media_msg , num_links  =helper.fetch_stat(selected_user,df)

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("total messages")
            st.title(num_messages)
        with col2:
            st.header("total words")
            st.title(words)
        with col3:
            st.header("total media")
            st.title(num_media_msg)
        with col4:
            st.header("total links")
            st.title(num_links)

        if selected_user == 'Overall':
            st.title('most busy user')
            x,new_df = helper.most_busy_user(df)
            fig , ax = plt.subplots()
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #worcCloud
        st.title("wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("most common words")
        df_most_cmn =helper.most_cmn_word(selected_user, df)
        fig,ax = plt.subplots()
        ax.barh(df_most_cmn[0],df_most_cmn[1])
        #plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #st.dataframe(df_most_cmn)

        #monthly timeline

        st.title("monthly timeline")
        timeline = helper.timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("daily timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'],color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)












