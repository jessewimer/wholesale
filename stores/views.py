from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import Store
from products.models import Product
import json
from orders.models import Order, OrderIncludes
# from orders.auto_email import send_email
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum
import pytz

class CustomLogoutView(LogoutView):
    next_page = 'login'

class CustomLoginView(LoginView):
    def get_success_url(self):
        store_name = self.request.user.store.username
        return reverse('dashboard', kwargs={'store_name': store_name})

@login_required
def dashboard(request, store_name):
    user = request.user
    store = Store.objects.get(store_user=user)
    current_year = settings.CURRENT_ORDER_YEAR
    year_suffix = f"{current_year % 100:02d}"
    pkt_price = settings.PACKET_PRICE

    if request.method == 'POST':
        # Process the form submission
        order_data = json.loads(request.body)
        invalid_products = []
        # print("ORDER DATA: ", order_data)

        # Check for invalid products
        for product_number in order_data.keys():
            try:
                # Convert product_number to integer since it comes as string from JSON
                product_number_int = int(product_number)
                # Check if the product exists in the store's available products
                if not store.available_products.filter(item_number=product_number_int).exists():
                    invalid_products.append(product_number)
            except (ValueError, TypeError):
                # Handle cases where product_number can't be converted to int
                invalid_products.append(product_number)

        if invalid_products:
            # print("NEW inside invalid_products")
            return JsonResponse({'invalid_products': invalid_products}, status=400)

        existing_orders = Order.objects.filter(store=store, order_number__endswith=f"-{year_suffix}")
        this_year_order_count = existing_orders.count() + 1

        pacific_tz = pytz.timezone('US/Pacific')
        pacific_now = timezone.now().astimezone(pacific_tz).date()

        order = Order.objects.create(
            store=store,
            order_number = f"W{store.store_number:02d}{this_year_order_count:02d}-{year_suffix}",
            order_date=pacific_now,
        )

        # Create OrderIncludes entries for each product in the order
        for item_number, quantity in order_data.items():
            try:
                product = Product.objects.get(item_number=item_number)
                OrderIncludes.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=pkt_price,
                )
            except Product.DoesNotExist:
                print(f"Product with item_number {item_number} does not exist")
                continue
        # send_email(order)
        # Return success response for AJAX
        return JsonResponse({'status': 'success'}, status=200)

    # Get all orders for the current year for this store
    current_year_orders = Order.objects.filter(
        store=store,
        order_number__endswith=f"-{year_suffix}"
    ).select_related('store').prefetch_related('orderincludes_set__product').order_by('-order_date')

    # Get previous items with total quantity per product
    previous_orders = (
        OrderIncludes.objects
        .filter(order__store=store)
        .values('product__item_number')
        .annotate(total_qty=Sum('quantity'))
    )
    # Convert to dictionary: { 'item_number': quantity }
    previous_items_dict = {
        entry['product__item_number']: entry['total_qty']
        for entry in previous_orders
    }

    # Get all available products for the store
    products = Product.objects.filter(
        available_in_stores=store,
        storeproduct__is_available=True
    )
    # Attach `.previously_ordered_count` to each product
    for product in products:
        product.previously_ordered_count = previous_items_dict.get(product.item_number, 0)

    # Prepare orders data for JavaScript (if needed)
    orders_data = []
    for order in current_year_orders:
        order_items = []
        for order_include in order.orderincludes_set.all():
            order_items.append({
                'item_number': order_include.product.item_number,
                'variety': order_include.product.variety,
                'quantity': order_include.quantity,
                'price': float(pkt_price)
            })

        orders_data.append({
            'id': order.id,
            'order_number': order.order_number,
            'order_date': order.order_date.strftime('%Y-%m-%d'),
            'items': order_items,
            'total_items': sum(item['quantity'] for item in order_items),
            'total_cost': sum(item['quantity'] for item in order_items) * pkt_price
        })

    # for order in orders_data:
    #     print(f"Order ID: {order['id']}, Order Num: {order['order_number']}, Total Cost: {order['total_cost']}")

    # product_dict = {101: ['Calypso', 'BEAN'], 102: ['Cocaigne', 'BEAN'], 103: ['Flageolet Vert', 'BEAN'], 104: ['Hungarian Rice Bean', 'BEAN'], 105: ['Hutterite', 'BEAN'], 106: ['Ireland Creek Annie', 'BEAN'],
    #                 107: ['Jacob’s Cattle', 'BEAN'], 108: ['Jacob’s Gold', 'BEAN'], 109: ['Kenearly Yellow Eye', 'BEAN'], 110: ['Lina Sisco’s Bird Egg', 'BEAN'], 111: ['Marfax', 'BEAN'], 112: ['Purgatorio', 'BEAN'],
    #                 113: ['Rockwell', 'BEAN'], 114: ['Rosso di Lucca', 'BEAN'], 115: ['Tiger’s Eye', 'BEAN'], 116: ['Zolfino', 'BEAN'], 117: ['Alaric (Tarbais)', 'BEAN'], 118: ['Annie Jackson', 'BEAN'],
    #                 119: ['Pellegrini', 'BEAN'], 120: ['Sorana', 'BEAN'], 121: ['Tolosa', 'BEAN'], 122: ['Karmazyn', 'BEAN'], 123: ['Blooming Prairie', 'BEAN'], 124: ['Dragon Langerie', 'BEAN'], 125: ['Empress', 'BEAN'],
    #                 126: ['Provider', 'BEAN'], 127: ['Marvel of Venice', 'BEAN'], 128: ['Trionfo Violetto', 'BEAN'], 129: ['Touchstone', 'BEET'], 130: ['Crapaudine', 'BEET'], 131: ['Feuer Kugel', 'BEET'],
    #                 132: ['Lutz Green Leaf', 'BEET'], 133: ['Shiraz', 'BEET'], 134: ['Chioggia', 'BEET'], 385: ['3 Beet Mix', 'BEET'], 135: ['Novantina', 'BROCCOLI'], 136: ['Solstice', 'BROCCOLI'],
    #                 137: ['Umpqua', 'BROCCOLI'], 138: ['Takinogawa', 'BURDOCK'], 139: ['Dowinda', 'CABBAGE'], 140: ['Filderkraut', 'CABBAGE'], 141: ['January King', 'CABBAGE'], 142: ['Columbia', 'CABBAGE'],
    #                 143: ['Marner', 'CABBAGE'], 144: ['Gobbo di Nizza', 'CARDOON'], 145: ['Rainbow Carrot Mix', 'CARROT'], 146: ['Dragon', 'CARROT'], 147: ['Scarlet Nantes', 'CARROT'], 148: ['Tonda di Parigi', 'CARROT'],
    #                 149: ['Prestige', 'CAULIFLOWER'], 150: ['Monarch', 'CELERIAC'], 151: ['Rainbow Chard', 'CHARD'], 152: ['Cascade Glaze', 'COLLARDS'], 153: ['Champion', 'COLLARDS'], 154: ['Floriani Red Flint', 'CORN'],
    #                 155: ['Painted Mountain', 'CORN'], 156: ['Amish Butter', 'CORN'], 157: ['Dakota Black', 'CORN'], 158: ['Tuxana', 'CORN'], 159: ['Vorgebirgstrauben', 'CUCUMBER'], 160: ['Çengelköy', 'CUCUMBER'],
    #                 161: ['Lemon', 'CUCUMBER'], 162: ['Sandita', 'CUCUMBER'], 163: ['Shintokiwa', 'CUCUMBER'], 164: ['Silver Slicer', 'CUCUMBER'], 165: ['Sweet Marketmore', 'CUCUMBER'], 166: ['Diamond', 'EGGPLANT'],
    #                 378: ['Violetta di Firenze', 'EGGPLANT'], 167: ['Finale', 'FENNEL'], 168: ['Suriname', 'GREENS'], 169: ['Astro', 'GREENS'], 170: ['Rucola', 'GREENS'], 383: ['Wasabi Arugula', 'GREENS'],
    #                 171: ['Early Mizuna', 'GREENS'], 172: ['Golden Frills', 'GREENS'], 173: ['Ruby Streaks', 'GREENS'], 174: ['Tatsoi', 'GREENS'], 175: ['Uprising Braising Mix', 'GREENS'],
    #                 176: ['Wrinkled Crinkled Crumpled', 'GREENS'], 178: ['Uprising Mild Mix', 'GREENS'], 179: ['Uprising Spicy Mix', 'GREENS'], 180: ['Green Wave', 'GREENS'], 177: ['Broadleaf', 'GREENS'],
    #                 181: ['Blood Sorrel', 'GREENS'], 182: ['Erba Stella (Minutina)', 'GREENS'], 183: ['A Tale of Three Kales', 'KALE'], 184: ['Black Tuscan', 'KALE'], 185: ['Dazzling Blue', 'KALE'],
    #                 186: ['Dwarf Blue Scotch', 'KALE'], 187: ['Red Russian', 'KALE'], 188: ['Russian Frills', 'KALE'], 189: ['Lincoln', 'LEEK'], 190: ['Neptune', 'LEEK'], 191: ['Winter Density', 'LETTUCE'],
    #                 192: ['Divina', 'LETTUCE'], 193: ['Scarlet Butter', 'LETTUCE'], 194: ['Tennis Ball', 'LETTUCE'], 195: ['Emerald Fan', 'LETTUCE'], 196: ['Hyper Red Rumpled Waved', 'LETTUCE'],
    #                 197: ['La Brillante', 'LETTUCE'], 198: ['Merlot', 'LETTUCE'], 199: ['Royal Red', 'LETTUCE'], 200: ['Bijella', 'LETTUCE'], 201: ['Flashy Butter Oak', 'LETTUCE'], 202: ['Italienischer', 'LETTUCE'],
    #                 203: ['Mascara', 'LETTUCE'], 204: ['Barnwood Gem', 'LETTUCE'], 205: ['Cimarron', 'LETTUCE'], 206: ['Eruption', 'LETTUCE'], 207: ['Flashy Trout’s Back', 'LETTUCE'], 208: ['Jericho', 'LETTUCE'],
    #                 375: ['Little Gem', 'LETTUCE'], 209: ['Uprising Lettuce Mix', 'LETTUCE'], 210: ['Blacktail Mountain', 'MELON'], 211: ['Janosik', 'MELON'], 212: ['Eel River', 'MELON'],
    #                 213: ['Giallo D’Inverno', 'MELON'], 214: ['Prescott Fond Blanc', 'MELON'], 215: ['Sakata Sweet', 'MELON'], 216: ['Ishikura Long Winter', 'ONION'], 217: ["Ed's Red", 'ONION'],
    #                 376: ['Rijnsburg 5', 'ONION'], 218: ['Rossa di Milano', 'ONION'], 219: ['Ailsa Craig', 'ONION'], 220: ['Red Long of Tropea', 'ONION'], 221: ['Lancer', 'PARSNIP'], 222: ['Roveja', 'PEA'],
    #                 223: ['Maestro', 'PEA'], 224: ['Cascadia', 'PEA'], 225: ['Sugar Snap', 'PEA'], 226: ['Sugar Ann', 'PEA'], 227: ['Golden Sweet', 'PEA'], 228: ['Ho Lan Dow', 'PEA'], 229: ['Schweizer Riesen', 'PEA'],
    #                 230: ['Basque', 'PEPPER'], 231: ['Pimiento di Padron', 'PEPPER'], 232: ['Sarit Gat', 'PEPPER'], 377: ['Biquinho Red', 'PEPPER'], 233: ['Elephant Ears', 'PEPPER'], 234: ['Jimmy Nardello', 'PEPPER'],
    #                 235: ['Marta Polka', 'PEPPER'], 236: ['Petit Marseillais', 'PEPPER'], 237: ['Long Pie', 'PUMPKIN'], 238: ['Winter Luxury', 'PUMPKIN'], 239: ['French Breakfast', 'RADISH'], 240: ['Sora', 'RADISH'],
    #                 241: ['Beaujolais', 'SPINACH'], 242: ['Winter Bloomsdale', 'SPINACH'], 243: ['Winter Giant', 'SPINACH'], 244: ['Odesa', 'SQUASH'], 245: ['Yellow Crookneck', 'SQUASH'],
    #                 246: ['Costata Romanesco', 'SQUASH'], 247: ['Dark Star', 'SQUASH'], 248: ['Bitterroot Buttercup', 'SQUASH'], 249: ['Black Forest Kabocha', 'SQUASH'], 250: ['Black Futsu', 'SQUASH'],
    #                 251: ['Burpee’s Butterbush', 'SQUASH'], 252: ['Sweet Meat', 'SQUASH'], 253: ['Zeppelin Delicata', 'SQUASH'], 379: ['Zucca Mantovana', 'SQUASH'], 254: ['De Milpa', 'TOMATILLO'],
    #                 255: ['Black Cherry', 'TOMATO'], 256: ['Blush', 'TOMATO'], 257: ['Pinky', 'TOMATO'], 258: ['Sweet Orange II', 'TOMATO'], 259: ['Afghan', 'TOMATO'], 260: ['Jaune Flamme', 'TOMATO'],
    #                 261: ['Latah', 'TOMATO'], 262: ['Matina', 'TOMATO'], 263: ['Stupice', 'TOMATO'], 264: ['Black Prince', 'TOMATO'], 265: ['Nepal', 'TOMATO'], 266: ['Cuor di Bue Albenga', 'TOMATO'],
    #                 283: ['Anise Hyssop', 'ANISE HYSSOP'], 267: ['Italian Large Leaf', 'BASIL'], 382: ['German Chamomile', 'CHAMOMILE'], 268: ['Pokey Joe', 'CILANTRO'], 269: ['Goldkrone', 'DILL'],
    #                 303: ['Echinacea purpurea', 'ECHINACEA'], 270: ['Hyssop', 'HYSSOP'], 321: ['Mexican Tarragon', 'MARIGOLD'], 271: ['Mentuccia Romana', 'NEPITELLA'], 272: ['Mersin', 'PARSLEY'],
    #                 273: ['Sculpit (Stridolo)', 'SCULPIT'], 274: ['Blue Fenugreek', 'TRIGONELLA'], 275: ['Tulsi (Sacred Basil)', 'TULSI'], 276: ['Common Mullein', 'VERBASCUM'], 278: ['Coral Fountains', 'AMARANTH'],
    #                 279: ['Elephant Head', 'AMARANTH'], 280: ['Hot Biscuits', 'AMARANTH'], 281: ['Love Lies Bleeding', 'AMARANTH'], 282: ['Opopeo', 'AMARANTH'], 284: ['Hot Pants', 'ASTER'],
    #                 285: ['Tower Chamois', 'ASTER'], 380: ['Tower Silver', 'ASTER'], 286: ['Black Ball', 'BACHELOR’S BUTTON'], 287: ['Florist Blue Boy', 'BACHELOR’S BUTTON'], 288: ['Aloha Blanca', 'BASKET FLOWER'],
    #                 289: ['Borage', 'BORAGE'], 291: ['Calendula Mix', 'CALENDULA'], 290: ['Zeolights', 'CALENDULA'], 292: ['Ruby Parfait', 'CELOSIA'], 293: ['Supercrest and Friends', 'CELOSIA'],
    #                 294: ['Pride of Gibraltar', 'CERINTHE'], 295: ['Violet Queen', 'CLEOME'], 296: ['Black Barlow', 'COLUMBINE'], 297: ['Bordeaux Barlow', 'COLUMBINE'], 298: ['Roulette', 'COREOPSIS'],
    #                 299: ['Diablo', 'COSMOS'], 300: ['Snow Puff', 'COSMOS'], 301: ['Velouette', 'COSMOS'], 302: ['Xsenia', 'COSMOS'], 381: ['Pink Butterfly', 'DELPHINIUM'], 386: ['Blue Lace Flower', 'DIDISCUS'],
    #                 304: ['Edible Flower Mix', 'EDIBLE'], 305: ['Blue Glitter', 'ERYNGIUM'], 306: ['Full Moon', 'FOUR O’CLOCK'], 307: ['Strega', 'FOUR O’CLOCK'], 308: ['Apricot Beauty', 'FOXGLOVE'],
    #                 309: ['Café Creme', 'FOXGLOVE'], 310: ['Giant Yellow Herold', 'FOXGLOVE'], 311: ['Wild Cascades', 'FOXGLOVE'], 312: ['Frosted Explosion', 'GRASS'], 313: ['Covent Garden', 'GYPSOPHILA'],
    #                 314: ['Blue Pearl', "JACOB'S LADDER"], 315: ['Blue Cloud', 'LARKSPUR'], 316: ['Earl Grey', 'LARKSPUR'], 317: ['Salmon Beauty', 'LARKSPUR'], 318: ['White Cloud', 'LARKSPUR'],
    #                 319: ['French Brocade', 'MARIGOLD'], 320: ['Gems', 'MARIGOLD'], 322: ['Pinwheel', 'MARIGOLD'], 323: ['Lemon Bergamot', 'MONARDA'], 324: ['Grandpa Ott’s', 'MORNING GLORY'],
    #                 325: ['Trailing Mix', 'NASTURTIUM'], 326: ['Alaska', 'NASTURTIUM'], 327: ['Langsdorff’s Tobacco', 'NICOTIANA'], 328: ['Lime Green', 'NICOTIANA'], 329: ['Only The Lonely', 'NICOTIANA'],
    #                 330: ['Peach Screamer', 'NICOTIANA'], 331: ['Bridal Veil', 'NIGELLA'], 332: ['Delft Blue', 'NIGELLA'], 333: ['Exotica', 'NIGELLA'], 334: ["Bee's Friend", 'PHACELIA'],
    #                 335: ['California Poppy Mix', 'POPPY'], 336: ['Pastel Meadows', 'POPPY'], 337: ['Amazing Grey', 'POPPY'], 338: ['Cornfield', 'POPPY'], 339: ['Mother of Pearl', 'POPPY'], 340: ['Pandora', 'POPPY'],
    #                 341: ['Black Swan', 'POPPY'], 342: ['Danish Flag', 'POPPY'], 343: ['Flemish Antique', 'POPPY'], 344: ['Frilled White', 'POPPY'], 345: ['Ziar Breadseed', 'POPPY'], 346: ['Autumn Sunset', 'RUDBECKIA'],
    #                 347: ['Prairie Glow', 'RUDBECKIA'], 348: ['Prairie Sun', 'RUDBECKIA'], 349: ['Sahara', 'RUDBECKIA'], 350: ['Texas Hummingbird Sage', 'SALVIA'], 351: ['Transylvanian Sage', 'SALVIA'],
    #                 352: ['White Swan', 'SALVIA'], 353: ['White Beauty', 'SAPONARIA'], 354: ['Fama Deep Blue', 'SCABIOSA'], 355: ['Fata Morgana', 'SCABIOSA'], 356: ['Giant Yellow', 'SCABIOSA'],
    #                 357: ['Salmon Queen', 'SCABIOSA'], 358: ['Snowmaiden', 'SCABIOSA'], 359: ['Apricot Peach Mix', 'STRAWFLOWER'], 360: ['Monstrosum Fireball', 'STRAWFLOWER'], 361: ['Garden Anarchy', 'SUNFLOWER'],
    #                 362: ['Giant Sungold', 'SUNFLOWER'], 363: ['Reds', 'SUNFLOWER'], 364: ['Soraya', 'SUNFLOWER'], 365: ['Tarahumara', 'SUNFLOWER'], 366: ['Transylvanian Giant', 'SUNFLOWER'],
    #                 367: ['April in Paris', 'SWEET PEA'], 384: ['Azureus', 'SWEET PEA'], 387: ['Lathyrus Chloranthus', 'SWEET PEA'], 368: ['Arctic Summer', 'VERBASCUM'], 369: ['Phoenician Mullein', 'VERBASCUM'],
    #                 370: ['Benary’s Giant Mix', 'ZINNIA'], 371: ['Queen Red Lime', 'ZINNIA'], 372: ['Salmon Rose', 'ZINNIA'], 373: ['Zinderella Lilac', 'ZINNIA'], 374: ['Zinderella Peach', 'ZINNIA'],
    #                 388: ['Borlotto Gaston', 'BEAN'], 389: ["Aunt Molly's", 'GROUNDCHERRY'], 390: ['Goldrush', 'LETTUCE'], 391: ['Prize Choi', 'GREENS'], 393: ['Ҫekirdeği Oyali', 'MELON'],
    #                 394: ['Yellow Nardello', 'PEPPER'], 395: ['Double Diamond', 'YARROW'], 396: ['Love Parade', 'YARROW'], 397: ['Green Gold', 'BUPLEURUM'], 398: ['Silvery Rose', 'STRAWFLOWER'],
    #                 400: ['Speckled', 'LETTUCE'], 401: ["Grandpa Admire's", 'LETTUCE'], 402: ['Australian Yellowleaf', 'LETTUCE'], 403: ['Cracoviensis', 'LETTUCE'], 404: ['Les Orielles du Diable', 'LETTUCE'],
    #                 405: ['Reine de Glaces', 'LETTUCE'], 406: ['Howden', 'PUMPKIN'], 407: ['Koralik', 'TOMATO'], 408: ['Galina', 'TOMATO'], 409: ['Gold Rush', 'BEAN'], 410: ['Yellowstone', 'CARROT'],
    #                 411: ["Gardener's Sweetheart", 'TOMATO'], 412: ['Carbon', 'TOMATO'], 413: ['Fairy Trumpets', 'FOUR O’CLOCK'], 414: ['Bronze Queen', 'NICOTIANA'], 415: ['Kingfisher', 'SWEET PEA'],
    #                 416: ['Mollie Rilstone', 'SWEET PEA'], 417: ['Windsor', 'SWEET PEA'], 392: ['Matsushima', 'CABBAGE'], 418: ['Vertissimo', 'CHERVIL'], 399: ['Torch', 'SUNFLOWER'], 419: ['Flora Norton', 'SWEET PEA'],
    #                 420: ['Bristol', 'Sweet Pea'], 421: ['Suzy Z', 'Sweet Pea'], 422: ['Just Jenny', 'Sweet Pea'], 423: ['Mystery Rose', 'FORGET-ME-NOT'], 424: ['Coral', 'CARROT'], 441: ['Merveille des Quatre Saisons', 'LETTUCE'],
    #                 442: ['Stocky Red Roaster', 'PEPPER'], 433: ['Manyel', 'TOMATO'], 432: ['Moldovan Green', 'TOMATO'], 434: ['Northern Ruby', 'TOMATO'], 435: ['Red Fig', 'TOMATO'], 440: ['Lilac Pompom', 'POPPY']};


    product_qs = Product.objects.all().values('item_number', 'variety', 'veg_type')
    product_dict = {}

    for p in product_qs:
        item_num = p['item_number']
        # Skip if item_number is None or missing variety/veg_type to avoid bad entries
        if item_num is not None and p['variety'] and p['veg_type']:
            product_dict[item_num] = [p['variety'], p['veg_type']]


    product_dict_json = json.dumps(product_dict)

    context = {
        'store': store,
        'products': products,
        'slots': store.slots,
        'previous_items': json.dumps(previous_items_dict),  # still useful for JS
        'current_year_orders': orders_data,
        'orders_data': json.dumps(orders_data),  # JSON data for JavaScript
        'current_year': current_year,
        'year_suffix': year_suffix,
        'pkt_price': pkt_price,
        'product_dict_json': product_dict_json,
    }
    return render(request, 'stores/dashboard.html', context)
