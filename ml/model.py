import os, joblib, numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler

class ProbModel:
    def __init__(self):
        self.scaler = StandardScaler(with_mean=False)
        self.clf = SGDClassifier(loss='log_loss', max_iter=200, tol=1e-3, random_state=42)
        self.classes_ = np.array([-1,0,1])
    def fit_partial(self, X, y):
        Xs = self.scaler.partial_fit(X).transform(X)
        self.clf.partial_fit(Xs, y, classes=self.classes_)
        return self
    def predict_proba_row(self, x_row):
        Xs = self.scaler.transform(x_row.reshape(1,-1))
        p = self.clf.predict_proba(Xs)[0]
        return {int(self.clf.classes_[i]): float(p[i]) for i in range(len(self.clf.classes_))}
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({'scaler': self.scaler, 'clf': self.clf}, path)
    def load(self, path):
        obj = joblib.load(path); self.scaler=obj['scaler']; self.clf=obj['clf']; 
        self.classes_ = getattr(self.clf,'classes_', self.classes_); return self
