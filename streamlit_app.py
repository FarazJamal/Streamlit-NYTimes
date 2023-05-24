import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
import json
import numpy as np
import pandas as pd
from collections import Counter
import seaborn as sns

def get_top_words(data, max_words):
    titles = ' '.join([article['title'] for article in data['results']])
    wordcloud = WordCloud(width=800, height=800, max_words=max_words, colormap=colormap, background_color=background_color).generate(titles)
    fig, ax = plt.subplots(figsize=(6, 6), facecolor=None)
    ax.imshow(wordcloud)
    ax.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(fig)

def get_data(endpoint):
    NYTIMES_API_KEY = 'VGGGQzc6XcfNBGRHzNue51F736ypPOAA'
    url = f'https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={NYTIMES_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

st.set_page_config(page_title='NYTimes Word Cloud', layout='wide')
endpoints = ['topstories', 'mostpopular']
sections = ['Arts', 'Business', 'Health', 'Science', 'Sports', 'Technology', 'World']
max_words_options = list(range(10, 101, 10))
colormap_options = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
default_endpoint = 'topstories'
default_topic = 'Arts'
default_max_words = 50
default_colormap = 'viridis'
default_background_color = '#00FFAA'

with st.sidebar:
    endpoint = st.selectbox('Select API:', endpoints, index=0)

############################################################    TOP STORIES     #########################################################################


if endpoint == "topstories":
    st.title('The Stories API') 
    st.title('I - NYTimes Word Cloud')    
    section = st.selectbox('Select a topic of your interest', sections)
    max_words = st.slider('Select maximum number of words to be displayed:', 1, 200)
    colormap = st.selectbox('Choose a colormap:', colormap_options, index=0)
    background_color = st.color_picker('Select a background color:', default_background_color)
    data = get_data(endpoint)
    data = {'results': [article for article in data['results'] if section.lower() in article['section'].lower()]}
    get_top_words(data, max_words)
    st.title('II - Frequency Distribution')
    freq = st.checkbox("Click here to display the Frequency Distribution plot")
    if freq:
        num_words = st.slider("Select number of words to be displayed", 1, 20, 2)

        if data.get('fault'):
            st.write('Error:', data['fault']['faultstring'])
        else:
            text = ""
            for article in data['results']:
                text += article['abstract'] + " "
            text = text.lower().split()
            stopwords = ["the", "to", "of", "and", "in", "a", "that", "for", "with", "on", "is", "as", "an", "be", "by", "at", "it", "this", "that", "from", "or", "are", "which", "if", "can", "all", "but", "not"]
            filtered_text = [word for word in text if word not in stopwords and word.isalpha()]
            word_freq = Counter(filtered_text)
            common_words = word_freq.most_common(num_words)
            words = [word[0] for word in common_words]
            freq = [word[1] for word in common_words]
            y_pos = np.arange(len(words))
            fig, ax = plt.subplots(figsize=(6, 4))
            ax = sns.barplot(x=freq, y=words, palette=sns.color_palette("Blues_d", len(freq)))
            for i, v in enumerate(freq):
                ax.text(v + 3, i + .25, "", color='blue')    
            plt.xlabel('Frequency')
            plt.title('Word Frequency Distribution')
            plt.tight_layout()
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels)
            st.pyplot(fig)

############################################################    MOST POPULAR     #########################################################################

elif endpoint == "mostpopular":
    import streamlit as st
    import requests
    from collections import Counter
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    api_key = 'bX0w4ppA6R7mwrwfyAVucIlt6NZT2m73'
    def get_nytimes_data(section, days):
        url = f'https://api.nytimes.com/svc/mostpopular/v2/{section}/{days}.json?api-key={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error('Error retrieving data')

    def get_word_freq_dist(data, max_words):
        max_words = st.slider("Select number of words to be displayed", 1, 50, 10)
        text = ""
        for article in data['results']:
            text += article['abstract'] + " "
        text = text.lower().split()
        stopwords = ["the", "to", "of", "and", "in", "a", "that", "for", "with", "on", "is", "as", "an", "be", "by", "at", "it", "this", "that", "from", "or", "are", "which", "if", "can", "all", "but", "not"]
        filtered_text = [word for word in text if word not in stopwords and word.isalpha()]
        word_freq = Counter(filtered_text)
        common_words = word_freq.most_common(max_words)
        words = [word[0] for word in common_words]
        freq = [word[1] for word in common_words]
        y_pos = np.arange(len(words))
        fig, ax = plt.subplots(figsize=(10, 8))
        cmap = sns.color_palette(colormap_options, len(freq)).as_cmap()
        sns.barplot(x=freq, y=words, palette=cmap, ax=ax)
        for i, v in enumerate(freq):
            ax.text(v + 3, i + .25, "", color='black', fontweight='bold')      
        ax.set_xlabel('Frequency')
        ax.set_title('Word Frequency Distribution')
        st.pyplot(fig)

    def plot_wordcloud(data, background_color, max_words):
        text = ""
        for article in data['results']:
            text += article['abstract'] + " "
        wordcloud = WordCloud(background_color=background_color, max_words=max_words).generate(text)
        fig, ax = plt.subplots(figsize=(6,4))
        handles, labels = ax.get_legend_handles_labels()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud')
        ax.legend(handles, labels)
        st.pyplot(fig)

    def get_frequency_distribution(data, num_words):  
        text = ""
        for article in data['results']:
            text += article['abstract'] + " "
        text = text.lower().split()
        stopwords = ["the", "to", "of", "and", "in", "a", "that", "for", "with", "on", "is", "as", "an", "be", "by", "at", "it", "this", "that", "from", "or", "are", "which", "if", "can", "all", "but", "not"]
        filtered_text = [word for word in text if word not in stopwords and word.isalpha()]
        word_freq = Counter(filtered_text)
        common_words = word_freq.most_common(num_words)
        words = [word[0] for word in common_words]
        freq = [word[1] for word in common_words]
        y_pos = np.arange(len(words))
        plt.figure(figsize=(10, 8))
        ax = sns.barplot(x=freq, y=words, palette=sns.color_palette("Blues_d", len(freq)))
        for i, v in enumerate(freq):
            ax.text(v + 3, i + .25, "", color='blue')      
        plt.xlabel('Frequency')
        plt.title('Word Frequency Distribution')
        plt.tight_layout()
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        st.pyplot(plt)

    def main():
        st.title('Most Popular Articles')
        st.title('I - Comparing Most Shared, Viewed and Email Articles')
        section = st.selectbox('Select your preferred set of articles', ['emailed', 'shared', 'viewed'], key='section_selectbox')
        days = st.selectbox('Select the age of your articles (in days)', ['1', '7', '30'], key='days_selectbox')
        num_words = st.slider('Choose a maximum number of words to be displayed', 1, 200, 10, key='num_words_slider')
        colormap = st.selectbox('Chhose a colormap:', colormap_options, index=0, key='colormap_selectbox')
        background_color = st.color_picker('Choose a background color:', default_background_color, key='background_color_picker')
        data = get_nytimes_data(section, days)
        plot_wordcloud(data, background_color, num_words)
        st.title('II - Frequency Distribution')
        freq = st.checkbox("Click here to display the Frequency Distribution plot",  key='frequency_checkbox')
        if freq:
            total_words = st.slider('Choose a maximum number of words to be displayed', 1, 20, 2, key='total_words_slider')
            get_frequency_distribution(data, total_words)

    if __name__ == '__main__':
        main()