# 1. 영어 워드 임베딩 구축
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_20newsgroups
import nltk
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import skipgrams
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Embedding, Reshape, Activation, Input
from tensorflow.keras.layers import Dot
from tensorflow.keras.utils import plot_model
from IPython.display import SVG
import gensim

# 다운로드한 데이터가 캐시에 저장되어 있는지 확인
from sklearn.datasets import get_data_home
print(get_data_home())


print("데이터 다운로드 중...")
dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))
dataset = dataset.data

news_df = pd.DataFrame({'document':dataset})
news_df

# 1-1. 데이터 전처리
# 결측치 확인
print("데이터 전처리 중...")
news_df.replace("", float("NaN"), inplace=True)
news_df = news_df.dropna().reset_index(drop=True)
print(f"필터링된 데이터셋 총 개수 : {len(news_df)}")
# >> 11096

# 중복제거
print("중복제거 중...")
processed_news_df = news_df.drop_duplicates(['document']).reset_index(drop=True)
processed_news_df

processed_news_df['document'] = processed_news_df['document'].apply(lambda x: x.replace("[^a-zA-Z]", " "))
processed_news_df['document'] = processed_news_df['document'].apply(lambda x: ' '.join([token for token in x.split() if len(token) > 2]))
processed_news_df = processed_news_df[processed_news_df.document.apply(lambda x: len(str(x)) <= 200 and len(str(x).split()) > 5)].reset_index(drop=True)
processed_news_df['document'] = processed_news_df['document'].apply(lambda x: x.lower())
processed_news_df


nltk.download('stopwords')

stop_words = stopwords.words('english')

tokenized_doc = processed_news_df['document'].apply(lambda x: x.split())
tokenized_doc = tokenized_doc.apply(lambda x: [s_word for s_word in x if s_word not in stop_words])
tokenized_doc

# 1-2. 단어 토큰화
print("단어 토큰화 중...")
drop_train = [index for index, sentence in enumerate(tokenized_doc) if len(sentence) <= 1]
tokenized_doc = np.delete(tokenized_doc, drop_train, axis=0)

print(len(tokenized_doc))
# >> 2235

tokenizer = Tokenizer()
tokenizer.fit_on_texts(tokenized_doc)

word2idx = tokenizer.word_index
idx2word = {value : key for key, value in word2idx.items()}
encoded = tokenizer.texts_to_sequences(tokenized_doc)

vocab_size = len(word2idx) + 1
print("어휘 사전 크기:", vocab_size)

# 1-3. negative sampling
print("negative sampling 중...")

training_dataset = [skipgrams(sample, vocabulary_size=vocab_size, window_size=10) 
                    for sample in encoded[:1000]]

# ✅ 첫 번째 샘플에서 couples, labels 꺼내오기
couples, labels = training_dataset[0]

# ✅ 예시 출력 5개
for i in range(5):
    print("({:s} ({:d}), {:s} ({:d})) -> {:d}".format(
        idx2word[couples[i][0]], couples[i][0],
        idx2word[couples[i][1]], couples[i][1],
        labels[i]
    ))


# 1-4. Skip-gram with Negative Sampling
print("Skip-gram 중...")

embedding_dim = 100

# 중심 단어를 위한 임베딩 테이블
w_inputs = Input(shape=(1, ), dtype='int32')
word_embedding = Embedding(vocab_size, embedding_dim)(w_inputs)

# 주변 단어를 위한 임베딩 테이블
c_inputs = Input(shape=(1, ), dtype='int32')
context_embedding  = Embedding(vocab_size, embedding_dim)(c_inputs)

dot_product = Dot(axes=2)([word_embedding, context_embedding])
dot_product = Reshape((1,), input_shape=(1, 1))(dot_product)
output = Activation('sigmoid')(dot_product)

model = Model(inputs=[w_inputs, c_inputs], outputs=output)
model.summary()
model.compile(loss='binary_crossentropy', optimizer='adam')
plot_model(model, to_file='model3.png', show_shapes=True, show_layer_names=True, rankdir='TB')

for epoch in range(10):
    loss = 0
    for _, elem in enumerate(training_dataset):
        first_elem = np.array(list(zip(*elem[0]))[0], dtype='int32')
        second_elem = np.array(list(zip(*elem[0]))[1], dtype='int32')
        labels = np.array(elem[1], dtype='int32')
        X = [first_elem, second_elem]
        Y = labels
        loss += model.train_on_batch(X,Y)  
    print('Epoch :', epoch + 1, 'Loss :', loss)

# 1-5. 임베딩 품질 확인
print("임베딩 품질 확인 중...")

f = open('practice/vectors.txt' ,'w')
f.write('{} {}\n'.format(vocab_size-1, embedding_dim))
vectors = model.get_weights()[0]
for word, i in tokenizer.word_index.items():
  f.write('{} {}\n'.format(word, ' '.join(map(str, list(vectors[i, :])))))
f.close()

# 모델 로드
w2v = gensim.models.KeyedVectors.load_word2vec_format('./practice/vectors.txt', binary=False)

w2v.most_similar(positive=['apple'])
