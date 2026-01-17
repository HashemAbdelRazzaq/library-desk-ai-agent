from langchain.tools import tool
from server.db import get_connection


@tool
def find_books(q: str, by: str):
    """
    Search books by title or author
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        f"SELECT isbn, title, author, stock, price FROM books WHERE {by} LIKE ?",
        (f"%{q}%",)
    )

    return cur.fetchall()


@tool
def create_order(customer_id: int, items: list):
    """
    Create order and reduce stock
    """
    conn = get_connection()
    cur = conn.cursor()

    # create order
    cur.execute(
        "INSERT INTO orders (customer_id) VALUES (?)",
        (customer_id,)
    )
    order_id = cur.lastrowid

    # process items
    for item in items:
        isbn = item["isbn"]
        qty = item["qty"]

        cur.execute("SELECT stock FROM books WHERE isbn = ?", (isbn,))
        stock = cur.fetchone()[0]

        if stock < qty:
            raise Exception("Not enough stock")

        cur.execute(
            "UPDATE books SET stock = stock - ? WHERE isbn = ?",
            (qty, isbn)
        )

        cur.execute(
            "INSERT INTO order_items VALUES (?, ?, ?)",
            (order_id, isbn, qty)
        )

    conn.commit()
    return {"order_id": order_id}


@tool
def restock_book(isbn: str, qty: int):
    """
    Increase book stock
    """
    conn = get_connection()
    conn.execute(
        "UPDATE books SET stock = stock + ? WHERE isbn = ?",
        (qty, isbn)
    )
    conn.commit()
    return "Stock updated"


@tool
def update_price(isbn: str, price: float):
    """
    Update book price
    """
    conn = get_connection()
    conn.execute(
        "UPDATE books SET price = ? WHERE isbn = ?",
        (price, isbn)
    )
    conn.commit()
    return "Price updated"


@tool
def order_status(order_id: int):
    """
    Get order details
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cur.fetchone()

    cur.execute(
        "SELECT isbn, qty FROM order_items WHERE order_id = ?",
        (order_id,)
    )
    items = cur.fetchall()

    return {
        "order": order,
        "items": items
    }


@tool
def inventory_summary():
    """
    List all books and stock
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT title, stock FROM books")
    return cur.fetchall()
