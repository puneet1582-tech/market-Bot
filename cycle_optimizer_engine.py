# CYCLE OPTIMIZER ENGINE
# Dynamically adjusts scanning interval based on universe size

def optimized_cycle_interval(stock_count, base_interval=300):
    try:
        if stock_count < 50:
            return base_interval
        elif stock_count < 200:
            return base_interval + 60
        elif stock_count < 500:
            return base_interval + 180
        else:
            return base_interval + 300
    except:
        return base_interval
