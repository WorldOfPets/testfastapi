fake_users = [
    {"id":1, "role":"admin", "name":"bob"},
    {"id":2, "role":"user", "name":"evgen"},
    {"id":3, "role":"user", "name":"ivan"},
    {"id":4, "role":"user", "name":"ivan", "degree":[
        {"id":1, "created_at":"2020-01-01T00:00:00", "type_degree":"expert"}
    ]},
]

fake_trades = [
    {"id":1, "user_id":1, "currency":"BTC", "side":"buy", "price":123, "amount":1.12},
    {"id":2, "user_id":2, "currency":"BTC", "side":"sell", "price":321, "amount":2.42},
    {"id":3, "user_id":3, "currency":"BTC", "side":"buy", "price":231, "amount":3.12},
]