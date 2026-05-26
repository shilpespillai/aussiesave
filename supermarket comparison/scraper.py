import urllib.request
import urllib.parse
import json
import ssl
import time
import random
import re
import os
import sys
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Firestore connection
db = None
try:
    cred_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'firebase-credentials.json')
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'projectId': 'pantrybloom'
        })
        db = firestore.client()
        print("Successfully initialized Firebase Admin SDK (Project ID: pantrybloom).")
    else:
        # Fallback if credentials file is not present
        print("Warning: firebase-credentials.json not found. Running in OFFLINE mode (updating local JSON cache).")
except Exception as e:
    print("Error initializing Firebase Admin SDK:", e)
    print("Running in OFFLINE mode.")

# Categories to scrape
CATEGORIES = ["laundry", "dishwashing", "milk", "bread", "chips", "chocolate"]

def save_product_to_firestore(product_id, product_data, store_name, price_data):
    """
    Saves product data and price information to Firebase Firestore.
    Logic:
    - If price has not changed for this store, overwrite the product info & update last_updated in price.
    - Else, overwrite product info, update price, and add a new row to the price_history collection.
    """
    if db is None:
        print(f"[OFFLINE] Store product: {product_id} | Name: {product_data['name']}")
        print(f"[OFFLINE] Store price: {store_name} | Price: ${price_data['price']} (Promo: {price_data['is_promo']})")
        return

    try:
        # 1. Product Document reference in 'scraped_products' collection
        product_ref = db.collection('scraped_products').document(product_id)
        
        # 2. Store price Document reference in 'prices' subcollection
        price_ref = product_ref.collection('prices').document(store_name)
        
        # Check if the price has changed
        price_changed = True
        price_snapshot = price_ref.get()
        if price_snapshot.exists:
            existing_data = price_snapshot.to_dict()
            existing_price = existing_data.get('price')
            existing_promo = existing_data.get('is_promo', False)
            # If price and promo status are identical, price has not changed
            if existing_price == price_data['price'] and existing_promo == price_data['is_promo']:
                price_changed = False
                
        # Always overwrite/update the product information
        product_ref.set(product_data, merge=True)
        
        # Update current price representation with Server Timestamp
        price_data['last_updated'] = firestore.SERVER_TIMESTAMP
        price_ref.set(price_data)
        
        # If price changed or is brand new, create a new history record to track patterns
        if price_changed:
            history_ref = product_ref.collection('price_history').document()
            history_data = {
                'store_name': store_name,
                'price': price_data['price'],
                'original_price': price_data.get('original_price'),
                'is_promo': price_data.get('is_promo', False),
                'promo_desc': price_data.get('promo_desc', ''),
                'timestamp': firestore.SERVER_TIMESTAMP
            }
            history_ref.set(history_data)
            print(f"Firestore Update: Product {product_id} details written. PRICE CHANGED for {store_name} to ${price_data['price']}. Added history row.")
        else:
            print(f"Firestore Update: Product {product_id} details written. PRICE UNCHANGED for {store_name} (${price_data['price']}). Skipped history row.")
            
    except Exception as e:
        print(f"Error saving product {product_id} to Firestore: {e}")

def scrape_woolworths(category):
    print(f"\n--- Scraping Woolworths for: {category} ---")
    url = "https://www.woolworths.com.au/apis/v3/product/search"
    body = json.dumps({
        "SearchTerm": category,
        "PageSize": 40,
        "PageNumber": 1,
        "SortType": "TraderRelevance"
    }).encode('utf-8')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, data=body, headers=headers)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    scraped_items = []
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            for p in data.get('Products', []):
                prod_info = p.get('Products', [])
                prod = prod_info[0] if prod_info else p
                
                name = prod.get('Name')
                stockcode = prod.get('Stockcode')
                if not name or not stockcode:
                    continue
                
                brand = prod.get('Brand', '').strip()
                if not brand:
                    brand = "Woolworths" if "woolworths" in name.lower() or "everyday" in name.lower() else "Generic"
                
                size = prod.get('PackageSize', '').strip()
                if not size:
                    match = re.search(r'\b(\d+(?:\.\d+)?\s*(?:L|mL|g|kg|pk|pack|sheets))\b', name, re.IGNORECASE)
                    size = match.group(1) if match else "Each"
                
                price = prod.get('Price')
                if price is None:
                    continue
                
                was_price = prod.get('WasPrice')
                is_promo = prod.get('IsOnSpecial', False)
                promo_desc = ""
                if is_promo:
                    promo_desc = prod.get('PromoOrgPriceDetail', '')
                    if not promo_desc and was_price:
                        promo_desc = f"Save ${round(was_price - price, 2)}"
                else:
                    was_price = price
                    
                image_url = prod.get('MediumImageFile', '')
                if image_url and not image_url.startswith('http'):
                    image_url = f"https://www.woolworths.com.au{image_url}"
                
                barcode = prod.get('Barcode', '')
                
                product_id = f"ww_{stockcode}"
                product_data = {
                    'barcode': barcode,
                    'name': name,
                    'brand': brand,
                    'size': size,
                    'category': category,
                    'image_url': image_url
                }
                
                price_data = {
                    'price': float(price),
                    'original_price': float(was_price),
                    'is_promo': bool(is_promo),
                    'promo_desc': promo_desc
                }
                
                scraped_items.append((product_id, product_data, "Woolworths", price_data))
    except Exception as e:
        print(f"Error scraping Woolworths for {category}: {e}")
        
    return scraped_items

def scrape_coles(category):
    print(f"\n--- Scraping Coles for: {category} ---")
    url = f"https://www.coles.com.au/api/searches/products?q={urllib.parse.quote(category)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    scraped_items = []
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('results', [])
            for p in results:
                if not isinstance(p, dict) or p.get('_type') != 'PRODUCT':
                    continue
                    
                name = p.get('name')
                prod_id = p.get('id')
                if not name or not prod_id:
                    continue
                    
                brand = p.get('brand', '').strip()
                if not brand:
                    brand = "Coles" if "coles" in name.lower() or "smart buy" in name.lower() else "Generic"
                    
                size = p.get('size', '').strip()
                if not size:
                    match = re.search(r'\b(\d+(?:\.\d+)?\s*(?:L|mL|g|kg|pk|pack|sheets))\b', name, re.IGNORECASE)
                    size = match.group(1) if match else "Each"
                    
                pricing = p.get('pricing', {})
                if not pricing:
                    continue
                    
                price = pricing.get('now')
                if price is None:
                    continue
                    
                was_price = pricing.get('was')
                is_promo = was_price is not None and was_price > price
                if was_price is None:
                    was_price = price
                    
                promo_desc = ""
                if is_promo:
                    promo_desc = f"Save ${round(was_price - price, 2)}"
                    
                image_url = ""
                image_uris = p.get('imageUris', [])
                if image_uris:
                    img_uri = image_uris[0].get('uri')
                    if img_uri:
                        if not img_uri.startswith('http'):
                            image_url = f"https://productimages.coles.com.au/productimages{img_uri}"
                        else:
                            image_url = img_uri
                            
                barcode = ""
                
                product_id = f"coles_{prod_id}"
                product_data = {
                    'barcode': barcode,
                    'name': name,
                    'brand': brand,
                    'size': size,
                    'category': category,
                    'image_url': image_url
                }
                
                price_data = {
                    'price': float(price),
                    'original_price': float(was_price),
                    'is_promo': bool(is_promo),
                    'promo_desc': promo_desc
                }
                
                scraped_items.append((product_id, product_data, "Coles", price_data))
    except Exception as e:
        print(f"Error scraping Coles for {category}: {e}")
        
    return scraped_items

def scrape_aldi():
    print(f"\n--- Scraping ALDI (Specials & Everyday) ---")
    urls = [
        ("https://www.aldi.com.au/en/groceries/super-savers/", "super-savers"),
        ("https://www.aldi.com.au/en/groceries/laundry-household/", "laundry"),
        ("https://www.aldi.com.au/en/groceries/baby/", "baby")
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    scraped_items = []
    for url, default_cat in urls:
        print(f"Fetching ALDI URL: {url}")
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
                html = response.read().decode('utf-8')
                
                # Regex match for product tiles
                tiles = re.findall(r'class="product-tile"(.*?)</a>', html, re.DOTALL)
                print(f"Found {len(tiles)} product tiles on ALDI page.")
                
                for tile in tiles:
                    # Extract title/name
                    title_match = re.search(r'title="([^"]+)"', tile)
                    if not title_match:
                        name_match = re.search(r'class="product-tile__name"[^>]*><p[^>]*>(.*?)</p>', tile, re.DOTALL)
                        name = name_match.group(1).strip() if name_match else ""
                    else:
                        name = title_match.group(1).strip()
                        
                    if not name:
                        continue
                        
                    # Clean up HTML tags if any in name
                    name = re.sub('<[^<]+?>', '', name).strip()
                    
                    # Extract brand
                    brand_match = re.search(r'class="product-tile__brandname"[^>]*><p[^>]*>(.*?)</p>', tile, re.DOTALL)
                    brand = brand_match.group(1).strip() if brand_match else "ALDI"
                    brand = re.sub('<[^<]+?>', '', brand).strip()
                    
                    # Extract ID from a href link
                    id_match = re.search(r'href="/product/[^"-]+-([^"/]+)"', tile)
                    if id_match:
                        aldi_id = id_match.group(1)
                    else:
                        # Fallback unique id
                        aldi_id = str(abs(hash(name)))
                        
                    # Extract size
                    size_match = re.search(r'class="product-tile__unit-of-measurement"[^>]*><p>(.*?)</p>', tile, re.DOTALL)
                    size = size_match.group(1).strip() if size_match else ""
                    if not size:
                        match = re.search(r'\b(\d+(?:\.\d+)?\s*(?:L|mL|g|kg|pk|pack|sheets))\b', name, re.IGNORECASE)
                        size = match.group(1) if match else "Each"
                        
                    # Extract price
                    price_match = re.search(r'class="base-price[^"]*"[^>]*>.*?<span>\$(\d+\.\d+)</span>', tile, re.DOTALL)
                    if not price_match:
                        # Fallback simple price
                        price_match = re.search(r'\$(\d+\.\d+)', tile)
                        
                    if not price_match:
                        continue
                    price = float(price_match.group(1))
                    
                    # Extract image URL
                    img_match = re.search(r'srcset="([^ ]+)', tile)
                    if not img_match:
                        img_match = re.search(r'src="([^"]+)"', tile)
                    
                    image_url = img_match.group(1).strip() if img_match else ""
                    
                    category = default_cat
                    for keyword in CATEGORIES:
                        if keyword in name.lower() or keyword in category.lower():
                            category = keyword
                            break
                            
                    product_id = f"aldi_{aldi_id}"
                    product_data = {
                        'barcode': "",
                        'name': name,
                        'brand': brand,
                        'size': size,
                        'category': category,
                        'image_url': image_url
                    }
                    
                    price_data = {
                        'price': price,
                        'original_price': price,
                        'is_promo': False,
                        'promo_desc': ""
                    }
                    
                    scraped_items.append((product_id, product_data, "ALDI", price_data))
        except Exception as e:
            print(f"Error scraping ALDI URL {url}: {e}")
            
    return scraped_items

def run_scraper():
    print("==================================================")
    print("          STARTING SUPERMARKET SCRAPER            ")
    print("==================================================")
    
    all_results = []
    
    # 1. Scrape Woolworths & Coles
    for category in CATEGORIES:
        # Woolworths
        ww_results = scrape_woolworths(category)
        all_results.extend(ww_results)
        time.sleep(random.uniform(1.0, 3.0)) # Be polite, avoid blocks
        
        # Coles
        coles_results = scrape_coles(category)
        all_results.extend(coles_results)
        time.sleep(random.uniform(1.0, 3.0)) # Be polite, avoid blocks

    # 2. Scrape ALDI
    aldi_results = scrape_aldi()
    all_results.extend(aldi_results)
    
    print("\n==================================================")
    print(f"Scraped {len(all_results)} total items. Uploading to DB...")
    print("==================================================")
    
    upload_count = 0
    dry_run_dict = {}
    
    for pid, pdata, store, price in all_results:
        try:
            save_product_to_firestore(pid, pdata, store, price)
            upload_count += 1
            
            # For offline cache update, collect into a dictionary to output as local JSON file
            if db is None:
                if pid not in dry_run_dict:
                    dry_run_dict[pid] = {**pdata, 'prices': {}, 'price_history': []}
                dry_run_dict[pid]['prices'][store] = price
        except Exception as e:
            print(f"Failed uploading {pid} to Firestore: {e}")
            
    # Write fallback JSON if in offline cache mode
    if db is None and dry_run_dict:
        fallback_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scraped_products_fallback.json')
        with open(fallback_path, 'w', encoding='utf-8') as f:
            json.dump(dry_run_dict, f, indent=4)
        print(f"\n[OFFLINE] Wrote {len(dry_run_dict)} products to fallback JSON file at {fallback_path}")
        
    print(f"\nScraper run finished. Uploaded/Processed {upload_count} records.")

if __name__ == "__main__":
    run_scraper()
