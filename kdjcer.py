import os.path
# hlwhoeayrjpydfbh
# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header
import pandas as pd
from pandas import DataFrame
import time


def kdj(df: DataFrame):
    low_list = df['low'].rolling(9, min_periods=9).min()
    low_list.fillna(value=df['low'].expanding().min(), inplace=True)
    high_list = df['high'].rolling(9, min_periods=9).max()
    high_list.fillna(value=df['high'].expanding().max(), inplace=True)
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100
    # 计算kdj
    df['K'] = pd.Series.ewm(rsv, com=2).mean()
    df['D'] = pd.Series.ewm(df['K'], com=2).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    return df


def signal(df: DataFrame):
    df['SIGNAL'] = 'N'
    df['J_1'] = df['J'].shift()
    # 1，要求j值小于k，d值
    # 2，要求近两日的j值递增
    # 3，要求当前已有数据的j值和d值的差值小于30
    df.loc[(df['J'] < df['K']) & (df['J'] < df['D']) & (df['D'] - df['J'] < 28) & (df['D'] - df['J'] > 10) & (df['J'] > df['J_1']), 'SIGNAL'] = 'Y'
    return df


def save(df: DataFrame, output):
    res = df.copy()
    res = res.rename(columns={'date': '日期'})
    res = res.round(2)
    res.to_csv(output, sep=',', index=False, header=True)


def process_dir(input: str, output: str):
    stock = []
    if not os.path.exists(output):
        os.mkdir(output)
    for filename in os.listdir(input):
        name, suffix = os.path.splitext(os.path.basename(filename))
        if suffix in [".csv"]:
            f = os.path.join(input, filename)
            t = f"{output}/{name}-kdj{suffix}"
            # 依次是'交易日期,开盘价,收盘价,*,涨幅,最低价,最高价,*,成交额,换手率'
            df = pd.read_csv(f, sep=',')
            df = df.rename(columns={'0': 'date', '1': 'open', '2': 'close', '5': 'low', '6': 'high'})
            df = df[['date', 'open', 'close', 'high', 'low']]
            # 按照时间从小到大进行排序
            df = df.sort_values(by="date", ascending=True)
            # 计算kdj
            df = kdj(df)
            df = signal(df)
            # 只有最后一天命中的才需要输出
            if len(df) > 0 and df.iloc[-1].at["SIGNAL"] == "Y":
                df = df[['date', 'K', 'D', 'J', "SIGNAL"]]
                st = os.path.splitext(os.path.basename(filename))
                print(st)
                send = f"{st}"
                stock.append(send)
                save(df, t)
    stock = ''.join(stock)
    stock = stock.replace("('","流入比:")
    stock = stock.replace("', '.csv')", "\n")
    stock = stock.replace("-", "股票代码:")
    print("ex")
    fileName = 'C://Users//Administrator//Desktop//web//www//root//127.0.0.1//kdjm.txt'
    today = time.strftime("%Y-%m-%d")
    with open(fileName, 'a+') as file:
        file.write("<h2>" + today + '号推荐股票:' + stock + "</h2>")
        print("pr")
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = 'wrsxz@qq.com'
    password = 'renxfezznhgidfdf'
    # 收信方邮箱
    to_addr = 'wrsxz@qq.com'# '3560342102@qq.com','479793860@qq.com','380491807@qq.com'
    # 发信服务器
    smtp_server = 'smtp.qq.com'
    massage = f"本策略基于技术指标:KDJ。\n 复权因子:大盘涨跌，资金流入。\n 本策略仅供参考，不对用户行为负任何责任。\n 股市有风险，投资需谨慎。\n 今日命中策略的股票有:\n{stock}\n我的网站 http://106.52.121.183/\n 本策略还未成熟，目前还在跑模拟盘。请自行斟酌损益，自负盈亏。"
    # 邮件头信息
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(massage, 'plain', 'utf-8')
    msg['From'] = Header('模拟盘战神—GKR')  # 发送者
    msg['To'] = Header('白鼠1号')  # 接收者
    subject = 'KDJ基线交易策略输出(买入信号)'
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
    try:
        smtpobj = smtplib.SMTP_SSL(smtp_server)
        # 建立连接--qq邮箱服务和端口号（可百度查询
        print("1")
        smtpobj.connect(smtp_server, 465)
        # 登录--发送者账号和口令
        print("2")
        smtpobj.login(from_addr, password)
        # 发送邮件
        print("3")
        smtpobj.sendmail(from_addr, to_addr, msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")
    finally:
        # 关闭服务器
        smtpobj.quit()


if __name__ == '__main__':
    process_dir("C:\\Users\\Administrator\\Desktop\\kdj基线策略组\\date\\", "C:\\Users\\Administrator\\Desktop\\kdj基线策略组\\kdj\\")
