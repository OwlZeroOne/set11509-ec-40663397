import yfinance as yf
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)


# @app.route("/shares/all-tickers", methods=["GET"])
# def get_all_tickers():
#     try

@app.route("/shares/info/<ticker_code>", methods=["GET"])
def get_share_info(ticker_code):
    try:
        info = yf.Ticker(ticker_code).info
        return jsonify({
            "result": "success",
            "share": {
                "code" : ticker_code,
                "nShares" : info.get("sharesOutstanding"),
                "price" : info.get("regularMarketPrice"),
                "name" : info.get("longName"),
                "marketValue" : info.get("marketCap"),
                "currency" : info.get("currency"),
                "sector" : info.get("sector"),
                "country" : info.get("country")
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/shares/history", methods=["POST"])
def get_history():
    body = request.get_json(force=True, silent=True)
    tickers = body.get("tickers")
    start = body.get("start")
    end = body.get("end")
    interval = body.get("interval")
    data = {}
    for ticker in tickers:
        ticker_df = yf.Ticker(ticker).history(interval=interval, start=start, end=end)
        data[ticker] = ticker_df.to_dict(orient="list")
        data[ticker]["datetime"] = list(ticker_df.index.astype(str))
    return jsonify({"result": "success", "data": data}), 200


@app.route("/shares/holders/<symbol>", methods=["GET"])
def get_holders(symbol):
    try:
        shareholders_df = yf.Ticker(symbol).institutional_holders
        shareholders_list = []
        for row in shareholders_df.itertuples():
            shareholders_list.append({
                "recency" : pd.to_datetime(row[1]).strftime("%d-%m-%Y"),
                "holder" : row[2],
                "pctHeld" : row[3],
                "shares" : row[4],
                "value" : row[5],
                "pctChange" : row[6],
            })

        return jsonify({
            "result": "success",
            "shareholders": shareholders_list
        })
    except Exception as e:
        return jsonify({"error": f"Exception while trying to formulate shareholder data: {e}"}), 500


@app.route("/shares/news/", methods=["GET"])
def get_news():
    tickers: list[str] = request.get_json(force=True, silent=True).get("tickers")
    news_list = []
    for ticker in tickers:
        try:
            articles = yf.Ticker(ticker).news
            news_list += [{
                "ticker": ticker,
                "title": a.get("content",{}).get("title"),
                "summary": a.get("content",{}).get("summary"),
                "date": a.get("content",{}).get("pubDate"),
                "url": a.get("content",{}).get("canonicalUrl").get("url")
                }
                for a in articles
            ]
        except Exception as e:
            return jsonify({"error": f"Failed to extract shareholder news: {e}"}), 500

    return jsonify({
        "result": "success",
        "news": news_list}
    ), 200


@app.route("/shares/activity/<symbol>", methods=["GET"])
def get_holder_activity(symbol):
    try:
        df = yf.Ticker(symbol).insider_transactions
        activities_list = []
        for i in range(len(df)):
            row = df.iloc[i]
            activities_list.append({
                "date" : pd.to_datetime(row["Start Date"]).strftime("%d-%m-%Y"),
                "insider" : row.Insider,
                "shares" : f"{float(row.Shares):,}",
                "value" : f"{float(row.Value):,}",
                "text" : row.Text
            })
            print(activities_list[i])
        return jsonify({
            "result": "success",
            "activities": activities_list
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to extract shareholder activities: {e}"}), 500


@app.route("/shares/recommendations/<symbol>")
def get_recommendations(symbol):
    # ticker.recommendations → DataFrame
    pass



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)