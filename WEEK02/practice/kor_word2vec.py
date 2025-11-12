# 2. 한국어 워드 임베딩 구축 및 시각화
# JDK 11 필요

import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jpype
from konlpy.tag import Okt
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from matplotlib import rc
import matplotlib.font_manager as fm
import os

# 설치된 폰트 확인
for f in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
    if "Nanum" in f or "NotoSans" in f:
        rc('font', family='NanumBarunGothic')
        break


# 2-1. 데이터 수집
print("데이터 수집 중...")

urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt", filename="practice/ratings_train.txt")
urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt", filename="practice/ratings_test.txt")

# ✅ 데이터 로드
train_dataset = pd.read_table("ratings_train.txt")
test_dataset = pd.read_table("ratings_test.txt")

# 2-2. 데이터 전처리
print("데이터 전처리 중...")

# 결측치 처리
train_dataset.replace("", float("NaN"), inplace=True)
train_dataset = train_dataset.dropna().reset_index(drop=True)

# 중복 제거
train_dataset = train_dataset.drop_duplicates(['document']).reset_index(drop=True)

# 한글이 아닌 문자 제거
train_dataset['document'] = train_dataset['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","", regex=True)

# 길이가 짧은 데이터 제거
train_dataset['document'] = train_dataset['document'].apply(
    lambda x: ' '.join([token for token in x.split() if len(token) > 2])
)

# 전체 길이가 10 이하이거나 전체 단어 개수가 5개 이하인 데이터 제거
train_dataset = train_dataset[train_dataset.document.apply(
    lambda x: len(str(x)) > 10 and len(str(x).split()) > 5
)].reset_index(drop=True)

# 불용어 정의
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를',
             '으로','자','에','와','한','하다']

# 2-2. 토큰화
print("형태소 분석기 토큰화 중...")

okt = Okt()
tokenized_data = []

for sentence in train_dataset['document']:
    tokenized_sentence = okt.morphs(sentence, stem=True)   # 토큰화
    stopwords_removed = [word for word in tokenized_sentence if word not in stopwords]  # 불용어 제거
    tokenized_data.append(stopwords_removed)

# 2-3. 데이터 분포 확인
print("데이터 분포 확인 중...")

print('리뷰의 최대 길이 :', max(len(review) for review in tokenized_data))
print('리뷰의 평균 길이 :', sum(map(len, tokenized_data))/len(tokenized_data))

plt.hist([len(review) for review in tokenized_data], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()

# 2-4. 워드 임베딩 구축
print("워드 임베딩 구축 중...")

embedding_dim = 100

model = Word2Vec(
    sentences=tokenized_data,
    vector_size=embedding_dim,
    window=5,
    min_count=5,
    workers=4,
    sg=0  # CBOW
)

word_vectors = model.wv
vocabs = list(word_vectors.key_to_index.keys())

# 유사도 확인
print("👉 '마블'과 유사한 단어:")
for sim_word in model.wv.most_similar("마블"):
    print(sim_word)

print("👉 '슬픔' vs '눈물' 유사도:", model.wv.similarity('슬픔', '눈물'))

# 2-5. PCA를 이용한 시각화
print("PCA 시각화 중...")

word_vector_list = [word_vectors[word] for word in vocabs]

pca = PCA(n_components=2)
xys = pca.fit_transform(word_vector_list)

x_axis = xys[:, 0]
y_axis = xys[:, 1]

def plot_pca_graph(vocabs, x_axis, y_axis):
    plt.figure(figsize=(25, 15))
    plt.scatter(x_axis, y_axis, marker='o')
    for i, v in enumerate(vocabs):
        plt.annotate(v, xy=(x_axis[i], y_axis[i]))
    plt.show()

plot_pca_graph(vocabs, x_axis, y_axis)

# 2-6. t-SNE를 이용한 시각화
print("t-SNE 시각화 중...")

tsne = TSNE(learning_rate=100, n_iter=1000, perplexity=30)
word_vector_list = np.array(word_vector_list)
transformed = tsne.fit_transform(word_vector_list)

x_axis_tsne = transformed[:, 0]
y_axis_tsne = transformed[:, 1]

def plot_tsne_graph(vocabs, x_axis, y_axis):
    plt.figure(figsize=(30, 30))
    plt.scatter(x_axis, y_axis, marker='o')
    for i, v in enumerate(vocabs):
        plt.annotate(v, xy=(x_axis[i], y_axis[i]))
    plt.show()

plot_tsne_graph(vocabs, x_axis_tsne, y_axis_tsne)

# 2-7. 임베딩 프로젝터용 저장

print("임베딩 프로젝터용 파일 저장 중...")

model.wv.save_word2vec_format('sample_word2vec_embedding')

# gensim 내장 스크립트 실행하면 텐서보드에서 Embedding Projector로 확인 가능
# !python -m gensim.scripts.word2vec2tensor --input sample_word2vec_embedding --output sample_word2vec_embedding
