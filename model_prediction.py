import pandas as pd 
import numpy as np
import tensorflow
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

# Make Code and URL Dictionary for different Emotions
emo_code_url = {
    "empty": [0, "./static/assets/emoticons/Empty.png"],
    "sadness": [1, "./static/assets/emoticons/Sadness.png"],
    "enthusiasm": [2, "./static/assets/emoticons/Enthusiasm.png"],
    "neutral": [3, "./static/assets/emoticons/Neutral.png"],
    "worry": [4, "./static/assets/emoticons/Worry.png"],
    "surprise": [5, "./static/assets/emoticons/Surprise.png"],
    "love": [6, "./static/assets/emoticons/Love.png"],
    "fun": [7, "./static/assets/emoticons/Fun.png"],
    "hate": [8, "./static/assets/emoticons/Hate.png"],
    "happiness": [9, "./static/assets/emoticons/Happiness.png"],
    "boredom": [10, "./static/assets/emoticons/Boredom.png"],
    "relief": [11, "./static/assets/emoticons/Relief.png"],
    "anger": [12, "./static/assets/emoticons/Anger.png"],
}

def predict(text):
    train_data = pd.read_csv("./static/assets/data_files/tweet_emotions.csv")    
    training_sentences = []

    for i in range(len(train_data)):
        sentence = train_data.loc[i, "content"]
        training_sentences.append(sentence)

    model = load_model("./static/assets/model_file/Tweets_Text_Emotion.h5")

    vocab_size = 40000
    max_length = 100
    trunc_type = "post"
    padding_type = "post"
    oov_tok = "<OOV>"

    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
    tokenizer.fit_on_texts(training_sentences)

    predicted_emotion_img_url=""
    predicted_emotion=""

    if  text!="":
        sentence = []
        sentence.append(text)
        print("sentence list",sentence)

        sequences = tokenizer.texts_to_sequences(sentence)
        print("sequence", sequences)

        padded = pad_sequences(
            sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type
        )
        testing_padded = np.array(padded)

        predicted_class_label = np.argmax(model.predict(testing_padded), axis=-1)
        print(predicted_class_label)
        
            
        for key, value in emo_code_url.items():
            if value[0]==predicted_class_label:
                predicted_emotion_img_url=value[1]
                predicted_emotion=key
        return predicted_emotion, predicted_emotion_img_url

def show_entry():
    # Read Data Entry CSV File as Pandas DataFrame
    day_entry_list = pd.read_csv("./static/assets/data_files/data_entry.csv")

    day_entry_list = day_entry_list.iloc[::-1]
    # print(day_entry_list)
    
    # Get Top 3 dates, text entries and emotion from the dataframe
    date1, date2, date3 =  pd.to_datetime(day_entry_list['date'].values[0]), pd.to_datetime(day_entry_list['date'].values[1]), pd.to_datetime(day_entry_list['date'].values[2])
    entry1, entry2, entry3 = day_entry_list['text'].values[0], day_entry_list['text'].values[1], day_entry_list['text'].values[2]

    emotion1, emotion2, emotion3 = day_entry_list["emotion"].values[0], day_entry_list["emotion"].values[1], day_entry_list["emotion"].values[2]

    emotion_url_1=""
    emotion_url_2=""
    emotion_url_3=""

    for key, value in emo_code_url.items():
        if key==emotion1:
            emotion_url_1 = value[1]
        if key==emotion2:
            emotion_url_2 = value[1]
        if key==emotion3:
            emotion_url_3 = value[1]

    return date1, date2, date3, entry1, entry2, entry3, emotion1, emotion2, emotion3, emotion_url_1, emotion_url_2, emotion_url_3
