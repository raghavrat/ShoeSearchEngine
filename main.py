import os
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import requests
import webbrowser
from PIL import Image, ImageTk
import io
from dotenv import load_dotenv
import threading
import validators

load_dotenv(dotenv_path='token.env')
API_KEY = os.environ.get('API_KEY')

url = f'https://api.sneakersapi.dev/api/v2/products'
headers = {"Authorization": f"{API_KEY}"}
response = requests.request("GET", url, headers=headers)

root = tk.Tk()
root.title("Shoe Suggestion Program")
root.state('zoomed')

style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 16))
style.configure("TButton", font=("Helvetica", 14))

label = ttk.Label(root, text="Shoe Suggestion Program")
label.pack(pady=20)

def get_shoes(search, size=None, min_price=None, max_price=None, sort_by=None, brands=None):
    url = f'https://api.sneakersapi.dev/api/v2/products'
    querystring = {"search": search, "category": "sneakers"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json().get("data")
    if data is None:
        return []

    shoes = []
    for item in data:
        if size:
            price = next((variant["price"] for variant in item["variants"] if variant["size"] == size), None)
            if price is None:
                continue
        else:
            price = min(variant["price"] for variant in item["variants"])

        if min_price:
            try:
                min_price = float(min_price)
                if price < min_price:
                    continue
            except ValueError:
                pass

        if max_price:
            try:
                max_price = float(max_price)
                if price > max_price:
                    continue
            except ValueError:
                pass

        brand = item.get('brand', '').lower()
        if brands and brand not in brands:
            continue

        shoes.append({
            "title": item['title'],
            "price": price,
            "brand": brand,
            "image": item.get('image', ''),
            "stockx_link": item.get('stockx_link', '')
        })
        if len(shoes) == 4:
            break

    if sort_by == "Price: Low to High":
        shoes.sort(key=lambda x: x['price'])
    elif sort_by == "Price: High to Low":
        shoes.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == "Most Relevant":
        shoes.sort(key=lambda x: x['title'])  # Assuming relevance is based on title
    elif sort_by == "Brand":
        shoes.sort(key=lambda x: x['brand'])  # Sort by brand

    return shoes

def on_search():
    search_term = searchbar.get()
    size = size_var.get()
    min_price = min_price_var.get()
    max_price = max_price_var.get()
    sort_by = sort_var.get()
    brands = [brand.strip().lower() for brand in brand_var.get().split(',')]

    for widget in result_inner_frame.winfo_children():
        widget.destroy()
    loading_label.pack(pady=10)
    threading.Thread(target=load_shoes, args=(search_term, size, min_price, max_price, sort_by, brands)).start()

    # Increase size and show recommended shoes box
    recommended_frame.config(width=1200, height=800)
    recommended_frame.pack(pady=20, fill='both', expand=True)

def load_shoes(search_term, size, min_price, max_price, sort_by, brands):
    results = get_shoes(search_term, size, min_price, max_price, sort_by, brands)
    root.after(0, lambda: display_results(results))

def display_results(results):
    loading_label.pack_forget()
    for widget in result_inner_frame.winfo_children():
        widget.destroy()
    for result in results:
        if result['image']:
            image_response = requests.get(result['image'])
            image_data = image_response.content
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((600, 600), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            frame = ttk.Frame(result_inner_frame, padding=10, height=900, width=900, borderwidth=2, relief="solid")
            frame.pack_propagate(False)
            frame.pack(pady=5)

            def open_url(url):
                if validators.url(url):
                    webbrowser.open(url)
                else:
                    print(f"Invalid URL: {url}")

            button = ttk.Button(frame, text=f"{result['title']} - ${result['price']}", image=photo, compound='top', command=lambda url=result['stockx_link']: open_url(url))
            button.image = photo
            button.pack()

def update_filter_menu():
    filter_menu.delete(0, 'end')
    filter_menu.add_command(label=f"Size ({size_var.get()})" if size_var.get() else "Size", command=lambda: size_var.set(simpledialog.askstring("Size", "Enter size:")))
    filter_menu.add_command(label=f"Min Price ({min_price_var.get()})" if min_price_var.get() else "Min Price", command=lambda: min_price_var.set(simpledialog.askstring("Min Price", "Enter minimum price:")))
    filter_menu.add_command(label=f"Max Price ({max_price_var.get()})" if max_price_var.get() else "Max Price", command=lambda: max_price_var.set(simpledialog.askstring("Max Price", "Enter maximum price:")))
    filter_menu.add_command(label=f"Sort by Price: Low to High" if sort_var.get() == "Price: Low to High" else "Sort by Price: Low to High", command=lambda: sort_var.set("Price: Low to High"))
    filter_menu.add_command(label=f"Sort by Price: High to Low" if sort_var.get() == "Price: High to Low" else "Sort by Price: High to Low", command=lambda: sort_var.set("Price: High to Low"))
    filter_menu.add_command(label=f"Sort by Most Relevant" if sort_var.get() == "Most Relevant" else "Sort by Most Relevant", command=lambda: sort_var.set("Most Relevant"))

searchbar = ttk.Entry(root, width=50)
searchbar.pack(pady=20)

# Add a new entry for brand input
brand_var = tk.StringVar()
brand_entry = ttk.Entry(root, textvariable=brand_var, width=50)
brand_entry.pack(pady=10)
brand_entry.insert(0, "Enter brands separated by commas (e.g., nike, adidas, reebok)")

search_button = ttk.Button(root, text="Search", command=on_search)
search_button.pack(pady=10)

filter_button = ttk.Menubutton(root, text="Filters", direction='below')
filter_menu = tk.Menu(filter_button, tearoff=0)
filter_button["menu"] = filter_menu

size_var = tk.StringVar()
min_price_var = tk.StringVar()
max_price_var = tk.StringVar()
sort_var = tk.StringVar()

update_filter_menu()
filter_button.pack(pady=20)

canvas = tk.Canvas(root)
canvas.pack(side='left', fill='both', expand=True)

scrollbar = ttk.Scrollbar(root, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')

canvas.configure(yscrollcommand=scrollbar.set)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
frame_width = int(screen_width * 0.8)
frame_height = int(screen_height * 0.5)

recommended_frame = ttk.Frame(canvas, width=frame_width, height=frame_height, borderwidth=2, relief="solid")
canvas.create_window((screen_width // 2, screen_height // 2), window=recommended_frame, anchor='center')

recommended_label = ttk.Label(recommended_frame, text="Recommended Shoes", font=("Helvetica", 16))
recommended_label.pack(pady=10)

loading_label = ttk.Label(recommended_frame, text="Loading...", font=("Helvetica", 14))

result_frame = ttk.Frame(recommended_frame)  # Remove fixed width and height for result_frame
result_frame.pack(pady=10, fill='both', expand=True)

result_canvas = tk.Canvas(result_frame)
result_canvas.pack(side='left', fill='both', expand=True)

result_scrollbar = ttk.Scrollbar(result_frame, orient='vertical', command=result_canvas.yview)
result_scrollbar.pack(side='right', fill='y')

result_canvas.configure(yscrollcommand=result_scrollbar.set)

result_inner_frame = ttk.Frame(result_canvas)
result_canvas.create_window((0, 0), window=result_inner_frame, anchor='nw')

def on_result_frame_configure(event):
    result_canvas.configure(scrollregion=result_canvas.bbox('all'))

result_inner_frame.bind('<Configure>', on_result_frame_configure)

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))

recommended_frame.bind('<Configure>', on_frame_configure)

def _on_mouse_wheel(event):
    if result_canvas.winfo_exists():
        result_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

result_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

# Hide recommended_frame initially
recommended_frame.pack_forget()

root.mainloop()