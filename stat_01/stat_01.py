"""Main module."""
import datetime

def calculate_investment_value(symbol, purchase_date, purchase_amount):
    try:
        today = datetime.datetime.now().date()
        
        if purchase_date.date() > today:
            return "Error: Purchase date cannot be in the future."
        
        days_since_purchase = (today - purchase_date.date()).days
        
        sample_price_data = {
            '2024-03-24': 150.00,  # Sample adjusted closing price for the given purchase date
            '2024-03-25': 155.00   # Sample adjusted closing price for today (assumed)
        }
        
        latest_close = sample_price_data[str(today)]
        
        current_value = latest_close * purchase_amount
        
        return current_value
    
    except Exception as e:
        return f"Error: {e}"

investment_value = calculate_investment_value(symbol, purchase_date, purchase_amount)
print(f"The current value of your investment in {symbol} is: ${investment_value:.2f}")
