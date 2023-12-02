"""
Price
Km_driven
No._of_owners
make_year
buyback_price
"""
from datetime import date

weight = [0.048943, 0.142039, 0.221231, 0.278768, 0.309016] #integral value of sin(x) from 0->pi/2 distributed in 5 interval 

price = 2
make_year = 0
km_driven = 1
buy_back_price = 3
no_of_owner = 4
todays_date = date.today() 

def mark_best(data):
    min_km_driven = int(data[0].get('mileage').replace(",", ""))
    total_price = 0
    max_make_year = todays_date.year - data[0].get('make_year')
    # max_buy_back_price = data[0].get('buy_back_price')
    for item in data:
        item['mileage'] = item.get('mileage',"").replace(",", "")
        item['price'] = item.get('price',"").replace(",", "")
        item['buy_back'] = item.get('buy_back_price', "").replace(",", "")
        min_km_driven = int(item.get('mileage')) if min_km_driven>int(item.get('mileage')) else min_km_driven
        total_price += int(item.get('price'))
        max_make_year = todays_date.year - item.get('make_year') if todays_date.year - item.get('make_year') > max_make_year else max_make_year
        # max_buy_back_price = int(item.get('buy_back_price')) if int(item.get('buy_back_price')) > max_buy_back_price else max_buy_back_price
    avg_price = total_price/len(data)
    max_ml_score = 0
    for item in data:
        item["ml_score"] = (((avg_price/int(item.get('price')))*weight[price])+\
                            (((todays_date.year - item.get('make_year'))/max_make_year)*weight[make_year])+\
                                ((min_km_driven/int(item.get('mileage')))*weight[km_driven])+\
                                    ((1)*weight[buy_back_price])+\
                                    # ((int(item.get('buy_back_price'))/max_buy_back_price)*weight[buy_back_price])+\
                                        ((1/int(item.get('no_of_owners')[0]))*weight[no_of_owner]))
        max_ml_score = item["ml_score"] if item["ml_score"] > max_ml_score else max_ml_score
    for item in data:
        item["best"] = True if item.get("ml_score") == max_ml_score else False
    return data

