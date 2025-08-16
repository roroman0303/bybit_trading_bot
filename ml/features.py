import numpy as np, pandas as pd
def ema(x, span): return x.ewm(span=span, adjust=False).mean()
def rsi(x, period=14):
    d=x.diff(); gain=(d.where(d>0,0)).rolling(period).mean(); loss=(-d.where(d<0,0)).rolling(period).mean()
    rs=gain/(loss+1e-12); return 100-(100/(1+rs))
def stoch(h,l,c,kp=14,dp=3):
    ll=l.rolling(kp).min(); hh=h.rolling(kp).max(); k=100*(c-ll)/(hh-ll+1e-12); return k, k.rolling(dp).mean()
def macd(c, f=12, s=26, sig=9):
    ef=ema(c,f); es=ema(c,s); line=ef-es; sigl=ema(line,sig); return line, sigl, line-sigl
def bb_pct_b(c, p=20, m=2.0):
    ma=c.rolling(p).mean(); std=c.rolling(p).std(); up=ma+m*std; lo=ma-m*std; return (c-lo)/(up-lo+1e-12)
def atr(h,l,c,p=14):
    pc=c.shift(1); tr=pd.concat([(h-l),(h-pc).abs(),(l-pc).abs()],axis=1).max(axis=1); return tr.rolling(p).mean()
def adx(h,l,c,p=14):
    up=h.diff(); dn=-l.diff()
    plus_dm=(up.where((up>dn)&(up>0),0.0)).rolling(p).mean(); minus_dm=(dn.where((dn>up)&(dn>0),0.0)).rolling(p).mean()
    tr=atr(h,l,c,p); plus_di=100*(plus_dm/(tr+1e-12)); minus_di=100*(minus_dm/(tr+1e-12))
    dx=100*((plus_di-minus_di).abs()/((plus_di+minus_di)+1e-12)); return dx.rolling(p).mean(), plus_di, minus_di
def cci(h,l,c,p=20):
    tp=(h+l+c)/3.0; ma=tp.rolling(p).mean(); md=(tp-ma).abs().rolling(p).mean(); return (tp-ma)/(0.015*(md+1e-12))
def mfi(h,l,c,v,p=14):
    tp=(h+l+c)/3.0; rmf=tp*v; pos=rmf.where(tp.diff()>0,0.0).rolling(p).sum(); neg=rmf.where(tp.diff()<0,0.0).rolling(p).sum()
    mr=pos/(neg+1e-12); return 100-(100/(1+mr))
def obv(c,v): return (np.sign(c.diff().fillna(0))*v).fillna(0).cumsum()
def williams_r(h,l,c,p=14):
    hh=h.rolling(p).max(); ll=l.rolling(p).min(); return -100*(hh-c)/(hh-ll+1e-12)
def donchian_pos(c,h,l,p=20):
    hh=h.rolling(p).max(); ll=l.rolling(p).min(); return (c-ll)/(hh-ll+1e-12)
FEATURES=['ema_9','ema_21','ema_50','ema_200','rsi_14','stoch_k_14','stoch_d_3','macd','macd_signal','macd_hist','bb_pct_b','atr_14','adx_14','di_plus_14','di_minus_14','cci_20','mfi_14','obv_slope_5','williams_r_14','donchian_pos_20']
def add_features(df: pd.DataFrame)->pd.DataFrame:
    df['ema_9']=ema(df['close'],9); df['ema_21']=ema(df['close'],21); df['ema_50']=ema(df['close'],50); df['ema_200']=ema(df['close'],200)
    df['rsi_14']=rsi(df['close'],14); k,d=stoch(df['high'],df['low'],df['close'],14,3); df['stoch_k_14']=k; df['stoch_d_3']=d
    line,sigl,hist=macd(df['close'],12,26,9); df['macd']=line; df['macd_signal']=sigl; df['macd_hist']=hist
    df['bb_pct_b']=bb_pct_b(df['close'],20,2.0); df['atr_14']=atr(df['high'],df['low'],df['close'],14)
    adxv,plus,minus=adx(df['high'],df['low'],df['close'],14); df['adx_14']=adxv; df['di_plus_14']=plus; df['di_minus_14']=minus
    df['cci_20']=cci(df['high'],df['low'],df['close'],20); df['mfi_14']=mfi(df['high'],df['low'],df['close'],df['volume'],14)
    df['obv']=obv(df['close'],df['volume']); df['obv_slope_5']=df['obv'].diff(5); df['williams_r_14']=williams_r(df['high'],df['low'],df['close'],14)
    df['donchian_pos_20']=donchian_pos(df['close'],df['high'],df['low'],20); return df
