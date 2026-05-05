def calculate_delivery_fee(order_amount, region_code, is_member):
    free_shipping = is_member and order_amount >= 50000
    if region_code == "JJ":
        return 3000 if free_shipping else 5000
    return 0 if free_shipping else 3000