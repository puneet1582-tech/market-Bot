# SCANNER BATCH ENGINE
# Processes large stock universe in batches

def create_batches(stock_list, batch_size=25):
    for i in range(0, len(stock_list), batch_size):
        yield stock_list[i:i + batch_size]
