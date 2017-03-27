import os
import shutil
import pickle
import numpy as np
import cv2

class Data:
    def __init__(self, img_dim):
        self.img_dim = img_dim

    def make_data(self, data, labels, dir_):
        if os.path.exists(dir_):
            shutil.rmtree(dir_)
        os.mkdir(dir_)
        for i, (d, l) in enumerate(zip(data, labels)):
            d = np.array(d).reshape(3, 32, 32).transpose(1, 2, 0)
            img = cv2.resize(d, (self.img_dim, self.img_dim))
            name = "{}_{}.jpg".format("{0:02d}".format(l), "{0:05d}".format(i))
            path = os.path.join(dir_, name)
            cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    def make_label(self, names):
        path = 'class.txt'
        if os.path.exists(path):
            os.remove(path)
        for name in names:
            with open(path, 'a') as f:
                x = '{}\n'.format(name)
                f.write(x)

    def preprocess(self):
        meta, train, test = self.load_pickle('raw')
        self.make_data(train['data'], train['fine_labels'], 'train')
        self.make_data(test['data'], test['fine_labels'], 'test')
        self.make_label(meta['fine_label_names'])

    def load_pickle(self, dir_):
        with open(os.path.join(dir_, 'meta'), 'rb') as f:
            meta = pickle.load(f)
        with open(os.path.join(dir_, 'train'), 'rb') as f:
            train = pickle.load(f, encoding='latin-1')
        with open(os.path.join(dir_, 'test'), 'rb') as f:
            test = pickle.load(f, encoding='latin-1')
        return (meta, train, test)
        
    
if __name__ == '__main__':
    img_dim = 96
    data = Data(img_dim=img_dim)
    data.preprocess()

