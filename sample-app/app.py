def calculate_delivery_fee(order_amount, region_code, is_member):
    if order_amount >= 50000:
        return 0
    if region_code == "JJ":
        return 5000
    return 3000