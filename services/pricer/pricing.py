def get_price(data): 
    pricing_parameters = data["pricing-parameters"]
    data["results"]
    for result in data["results"]:
        price_result = get_price_result(pricing_parameters, result)
        result["price"] = price_result
    return data    

def get_price_result(pricing_parameters, result):
    fare = result["price-components"]["flight"]["fare"]["total"]
    tax = result["price-components"]["flight"]["tax"]["total"]
    fee = None
    if pricing_parameters["price_type"] == "NORMAL":
        fee = 0
        fee = pricing_parameters["fee_flat"]
        fee = pricing_parameters["fee"] * (fare + tax)
        if pricing_parameters["user_type"] == "PREMIUM":
            fee += 0
        elif pricing_parameters["user_type"] == "MEMBER":
            fee += 5
        elif pricing_parameters["user_type"] == "GUEST":
            fee += 10
        
        elif pricing_parameters["device"] == "DESKTOP":
            fee += 0
        elif pricing_parameters["device"] == "IOS":
            fee += 20
        elif pricing_parameters["device"] == "ANDROID":
            fee += 10

    return {
        "currency": "EUR",
        "fare": fare,
        "tax": tax,
        "fee": fee,
        "total": fare + tax + fee
    }