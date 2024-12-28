# Shoe Search Engine

A Python-based desktop application that allows users to search and browse shoes from StockX, with various filtering options and direct links to purchase pages.

## Description

The Shoe Search Engine provides a user-friendly interface for searching and discovering shoes available on StockX. The application features real-time price updates, high-quality product images, and seamless integration with StockX's marketplace.

### Key Features

- Interactive search functionality
- Real-time price information
- High-quality product images
- Direct StockX purchase links
- Comprehensive filtering system
- Brand-specific searches
- Size availability checking
- Price range filtering

## Usage

### Basic Search

Simply enter your search term in the main search bar and click "Search":

```python
def on_search():
    search_term = searchbar.get()
    size = size_var.get()
    min_price = min_price_var.get()
    max_price = max_price_var.get()
    sort_by = sort_var.get()
    brands = [brand.strip().lower() for brand in brand_var.get().split(',')]
```

### Brand Filtering

Enter brands in the brand entry field, separated by commas:

```
nike, adidas, reebok
```

### Size and Price Filtering

The application supports various filtering options:

```python
def get_shoes(search, size=None, min_price=None, max_price=None, sort_by=None, brands=None):
    # Filter by size
    if size:
        price = next((variant["price"] for variant in item["variants"] if variant["size"] == size), None)
        
    # Filter by price range
    if min_price:
        if price < min_price:
            continue
            
    if max_price:
        if price > max_price:
            continue
```

### Sorting Options

The following sorting methods are available:
- Price: Low to High
- Price: High to Low
- Most Relevant
- Brand

## Features

### Search Results Display

Each search result includes:
- Product image
- Product name
- Price
- Clickable link to StockX

### Price Filtering

Users can set:
- Minimum price threshold
- Maximum price threshold
- Sort by price (ascending or descending)

### Size Availability

- Filter products by specific sizes
- Only shows products available in selected size
- Displays accurate pricing for selected size

### Brand Filtering

- Search for specific brands
- Multiple brand selection supported
- Case-insensitive brand matching

## Future Enhancements

1. Additional Filters
   - Color options
   - Release date
   - Condition rating
   
2. Extended Options
   - Saved searches
   - Price alerts
   - Wishlist functionality
   
3. Expanded Product Coverage
   - More StockX categories
   - Additional marketplace integrations
   - Historical price data

## Technical Implementation

The application uses threading for smooth performance:

```python
def on_search():
    # ... search parameter setup ...
    threading.Thread(target=load_shoes, args=(search_term, size, min_price, max_price, sort_by, brands)).start()
```

Image handling is optimized for performance:

```python
def display_results(results):
    for result in results:
        if result['image']:
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((600, 600), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
```

## Security

The application implements secure API key handling using environment variables:

```python
load_dotenv(dotenv_path='token.env')
API_KEY = os.environ.get('API_KEY')
```

## API Integration

The application integrates with the SneakersAPI:

- API Endpoint: `https://api.sneakersapi.dev/api/v2/products`
- Authentication: Bearer token
- Response format: JSON
- Rate limiting: Implemented through threading

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/raghavrat/shoe-search-engine.git
cd shoe-search-engine
```

### 2. Install Required Libraries

```bash
pip install tkinter pillow requests python-dotenv validators
```

### 3. API Key Setup

1. Visit [SneakersAPI](https://sneakersapi.dev) and create an account
2. Generate an API key from your dashboard
3. Create a file named `token.env` in the project root directory
4. Add your API key to the file:

```env
API_KEY=your_api_key_here
```

### 4. Run the Application

```bash
python main.py
```
