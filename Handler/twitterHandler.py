import json

class TwitterHandler:

    def __init__(self):
        pass

    @staticmethod
    def match_tweet_data (data):
        KEYWORD = ['차단중', '차단 중', '작업중', '진행중', '작업 중', '정체', '지연']
        PATTERN = r"[가-힣]+[A-Z가-힣\s]+[\s→\s]+[가-힣]+"

        for keyword in KEYWORD:
            if keyword in data['message']:
                return True

        return False

    @staticmethod
    def parse_promising_data(promsing_data):
        TwitterHandler.seoul_data(promsing_data)
        TwitterHandler.need_Data()

    @staticmethod
    def seoul_data(jsonData):
        import csv

        outfile = open("/Users/heesu.lee/PycharmProjects/Server/seoultopis_output.csv", "w")

        count = 0

        csvwriter = csv.writer(outfile)
        for data in jsonData:
            # 문자열
            if count == 0:
                header = data.keys()
                csvwriter.writerow(header)
                count += 1
            csvwriter.writerow(data.values())
            json_time = jsonData[count]["created_time"]
            # print(json_time)
            json_message = jsonData[count]["message"]
            # print(json_message)

    @staticmethod
    def dnn(xdata, ydata):
        import tensorflow as tf
        x_data = xdata
        y_data = ydata

        X = tf.placeholder(tf.float32)
        Y = tf.placeholder(tf.float32)

        W1 = tf.Variable(tf.random_uniform([1, 10], -1., 1.))
        W2 = tf.Variable(tf.random_uniform([10, 3], -1., 1.))

        b1 = tf.Variable(tf.zeros([10]))
        b2 = tf.Variable(tf.zeros([3]))

        L1 = tf.add(tf.matmul(X, W1), b1)
        L1 = tf.nn.relu(L1)

        model = tf.add(tf.matmul(L1, W2), b2)
        cost = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits_v2(labels=Y, logits=model))

        optimizer = tf.train.AdamOptimizer(learning_rate=0.01)
        train_op = optimizer.minimize(cost)

        init = tf.global_variables_initializer()
        sess = tf.Session()
        sess.run(init)

        for step in range(1000):
            sess.run(train_op, feed_dict={X: x_data, Y: y_data})

            if (step + 1) % 10 == 0:
                print(step + 1, sess.run(cost, feed_dict={X: x_data, Y: y_data}))

        # todo: 결과 확인
        # todo: 0: 정체 1: 보통 2: 원활
        prediction = tf.argmax(model, 1)
        target = tf.argmax(Y, 1)
        print('예측값:', sess.run(prediction, feed_dict={X: x_data}))
        print('실제값:', sess.run(target, feed_dict={Y: y_data}))

        is_correct = tf.equal(prediction, target)
        accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
        print('정확도: %.2f' % sess.run(accuracy * 100, feed_dict={X: x_data, Y: y_data}))

        #accuracy_list = list(accuracy)

        # import matplotlib.pyplot as plt
        # plt.plot(x_data, 'o')
        # plt.show()

    @staticmethod
    def need_Data():
        from random import randint
        import csv
        import pandas as pd
        import re
        origin_data = pd.read_csv("/Users/heesu.lee/PycharmProjects/Server/seoultopis_output.csv")
        origin_data.drop(['hashtags', 'link', 'name', 'num_angrys', 'num_comments', 'num_hahas'
                             , 'num_likes', 'num_loves', 'num_reactions', 'num_sads', 'num_shares',
                          'num_wows', 'post_id'],
                         axis=1,
                         inplace=True)
        dp = origin_data.to_csv("/Users/heesu.lee/PycharmProjects/Server/seoultopis_output.csv",
                                mode='w')
        dp = pd.read_csv("/Users/heesu.lee/PycharmProjects/Server/seoultopis_output.csv",
                         index_col=0)

        file = open("/Users/heesu.lee/PycharmProjects/Server/seoultopis_output.csv", 'r')
        lines = csv.reader(file)
        cnt = 0
        situation_list = list()
        pattern_event = ["정체", "서행", "원활"]
        pattern_remove = ["이 시각"]
        for line in lines:
            if cnt > 0:
                situation_list.append(line)
            cnt += 1
        cnt_total = -1
        cnt_fast = 1
        cnt_nor = 2
        cnt_slow = 3
        PATTERN = r"[가-힣\s가-힣0-9]+[A-Z가-힣\s]+[\s→\s|\s↔\s]+[0-9.0-90-9가-힣0-9가-]+[A-Z\s]+"
        normal_PATTERN = ["주의운전", "참고운전", "공사로 차단", "공사중", "공사 진행중"]
        good_PATTERN = ["공사 완료", "처리 완료"]
        pattern = re.compile(PATTERN)
        loads = list()
        loads_situation = list()
        for frq in situation_list:
            print(str(frq[2]))
            # print(frq, "fksdoijfoasdjfoa")
            if "이 시각 서울시 소통상황입니다." in (str(frq[2])):
                continue
            if "[집회안내]" in (str(frq[2])):
                continue
            load = pattern.search(str(frq))
            loads.append(str(load.group()))
            tmp = len(loads)
            for word in frq:
                if "정체" in word:
                    # print("----------", cnt_slow)
                    cnt_slow += 1
                    loads_situation.append("100")
                    break
                elif "원활" in word:
                    # print("----------", cnt_fast)
                    cnt_fast += 1
                    loads_situation.append("1")
                    break
                elif "서행" in word:
                    # print("----------", cnt_nor)
                    cnt_nor += 1
                    loads_situation.append("10")
                    break
                elif "주의" in word:
                    # print("----------", cnt_nor)
                    cnt_nor += 1
                    loads_situation.append("10")
                    break
                else:
                    continue

        import numpy as np
        situation_list = list()
        prediction_list = list()
        for k in loads_situation:
            if k is "100":
                prediction_list.append([1, 0, 0])
                situation_list.append([randint(1, 19)])
            elif k is "10":
                prediction_list.append([0, 1, 0])
                situation_list.append([randint(20, 39)])
            elif k is "100":
                prediction_list.append([0, 0, 1])
                situation_list.append([40, 120])
        print(prediction_list)
        xdata = np.array(situation_list)
        print(xdata)
        ydata = np.array(prediction_list)
        print(ydata)
        TwitterHandler.dnn(xdata, ydata)

    @staticmethod
    def extract_promising_data(tweet_data):
        promising_data = []

        for tweet in tweet_data:
            if TwitterHandler.match_tweet_data(tweet) is True:
                promising_data.append(tweet)

        TwitterHandler.parse_promising_data(promising_data)

        with open('promising_twitter.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(promising_data,
                            indent=4, sort_keys=True,
                            ensure_ascii=False)
            outfile.write(str_)

        print(promising_data)