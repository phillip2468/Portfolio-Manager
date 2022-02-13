# This file should contain records you want created when you run flask db seed.
from sqlalchemy import func

from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio
from money_maker.models.ticker_prices import TickerPrice
from money_maker.models.user import User
from money_maker.models.watchlist import Watchlist
from money_maker.tasks.task import update_yh_stocks
from money_maker.ticker.routes import refresh_au_symbols, get_american_yh_stocks

initial_user = User(email="testemail1234@email.com", hashed_password="Password12345")

# Create a sample user
if len(db.session.query(User).all()) == 0:
    db.session.add(initial_user)
    db.session.commit()
    print("New user table added!")


# Creates all the necessary stocks in the database, with their respective prices/ information
if len(db.session.query(TickerPrice).filter(TickerPrice.symbol.contains(".AX")).all()) == 0 \
        or len(db.session.query(TickerPrice).filter(~TickerPrice.symbol.contains(".AX")).all()) == 0:
    refresh_au_symbols()
    get_american_yh_stocks()
    update_yh_stocks()

    find_user = db.session.query(User).filter(User.email == "testemail1234@email.com").one()
    random_stocks: TickerPrice = db.session.query(TickerPrice).order_by(func.random()).limit(3).all()
    sample_portfolio = Portfolio(portfolio_name="My portfolio", stock_id=random_stocks[0].stock_id, units_purchased=10
                                 , units_price=100, user_id=find_user.user_id)
    sample_portfolio_2 = Portfolio(portfolio_name="My portfolio", stock_id=random_stocks[1].stock_id, units_purchased=10
                                   , units_price=100, user_id=find_user.user_id)

    sample_watchlist = Watchlist(watchlist_name="My watchlist", stock_id=random_stocks[2].stock_id, user_id=find_user.user_id)
    db.session.add_all([sample_portfolio, sample_portfolio_2, sample_watchlist])

    db.session.commit()
