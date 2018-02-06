
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.utils.np_utils import to_categorical

import numpy as np
import pandas as pd


# X:[収束] => Y:0
# X:[発散] => Y:1

syuusoku_data  = pd.read_csv('syuusoku.csv', header=None)
hassan_data  = pd.read_csv('hassan.csv', header=None)

syuusoku_array = syuusoku_data.as_matrix()
hassan_array = hassan_data.as_matrix()

syuusoku_array = syuusoku_array.transpose()
hassan_array = hassan_array.transpose()

syuusoku_array = np.array(syuusoku_array)
hassan_array = np.array(hassan_array)

X_list = np.concatenate([syuusoku_array, hassan_array],axis=0)

syuusoku_label = np.zeros(260)
hassan_label = np.ones(20)

Y_list = np.concatenate([syuusoku_label, hassan_label],axis=0)


# kerasのmodelに渡す前にXをnumpyのarrayに変換する。
X = np.array(X_list)
Y = to_categorical(Y_list) #one-hot化

# 学習のためのモデルを作る
model = Sequential()
# 全結合層(100層->400層)
model.add(Dense(input_dim=100, output_dim=400))
# 活性化関数(ReLu関数)
model.add(Activation("relu"))
# 全結合層(400層->2層)
model.add(Dense(output_dim=2))
# 活性化関数(softmax関数)
model.add(Activation("softmax"))
# モデルをコンパイル
#model.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])
model.compile(loss="binary_crossentropy", optimizer="sgd", metrics=["accuracy"])
# 学習を実行
model.fit(X, Y, nb_epoch=1000, batch_size=100)

# 学習したモデルで予測する。
# [発散]=> 1([0,1]) 1番目のビットが立っている
# [収束]=> 0([1,0]) 0番目のビットが立っている
# という予測になるはず...


# 発散ケースのテスト
hassan_test_data  = pd.read_csv('hassan_test.csv', header=None)
hassan_test_array = hassan_test_data.as_matrix()
hassan_test_array = hassan_test_array.transpose()
hassan_test_array = np.array(hassan_test_array)
#print(hassan_test_data)

results = model.predict_proba(hassan_test_array)
print("Predict(発散):\n", results)

# 収束ケースのテスト
syuusoku_test_data  = pd.read_csv('syuusoku_test.csv', header=None)
syuusoku_test_array = syuusoku_test_data.as_matrix()
syuusoku_test_array = syuusoku_test_array.transpose()
syuusoku_test_array = np.array(syuusoku_test_array)

results1 = model.predict_proba(syuusoku_test_array)
print("Predict(収束):\n", results1)
