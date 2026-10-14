from dataclasses import dataclass
@dataclass
class Product:
    name: str
    price: float      
    rating: float     
    sold: int         

    def __str__(self):
        return f"{self.name:<22} Rs.{self.price:>9,.2f}   {self.rating:>3.1f} stars   {self.sold:>5} sold"


def merge(left, right, key, reverse):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        a, b = key(left[i]), key(right[j])
        take_left = (a >= b) if reverse else (a <= b)
        if take_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
def merge_sort(products, key, reverse=False):
    if len(products) <= 1:                      
        return products

    mid = len(products) // 2
    left = merge_sort(products[:mid], key, reverse)    
    right = merge_sort(products[mid:], key, reverse)   
    return merge(left, right, key, reverse)           
SORT_OPTIONS = {
    "1": ("Price: Low to High",   lambda p: p.price,          False),
    "2": ("Price: High to Low",   lambda p: p.price,          True),
    "3": ("Customer Rating",      lambda p: p.rating,         True),
    "4": ("Best Sellers",         lambda p: p.sold,           True),
    "5": ("Name: A to Z",         lambda p: p.name.lower(),   False),
}


def show(products, title):
    print(f"\n--- {title} ---")
    for p in products:
        print(p)


def main():
    catalog = [
        Product("Wireless Mouse",      599.00, 4.3, 1520),
        Product("Mechanical Keyboard", 2499.00, 4.6, 830),
        Product("USB-C Hub",           1299.00, 4.1, 410),
        Product("Laptop Stand",         899.00, 4.4, 975),
        Product("Webcam HD",           1799.00, 3.9, 260),
        Product("Bluetooth Speaker",   1999.00, 4.5, 1210),
        Product("Phone Tripod",         349.00, 4.0, 1890),
        Product("Noise Cancel Headset", 3499.00, 4.7, 640),
    ]

    show(catalog, "Original Catalog")

    while True:
        print("\nSort products by:")
        for k, (label, _, _) in SORT_OPTIONS.items():
            print(f"  {k}. {label}")
        print("  0. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        if choice not in SORT_OPTIONS:
            print("Invalid choice, try again.")
            continue

        label, key, reverse = SORT_OPTIONS[choice]
        show(merge_sort(catalog, key, reverse), label)

if __name__ == "__main__":
    main()