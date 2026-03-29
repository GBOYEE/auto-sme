"""WhatsApp webhook router for Twilio integration."""
from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from auto_sme.store import products as _products_db, optout_phones
from auto_sme.routers.orders import process_order

router = APIRouter(prefix="/webhook", tags=["whatsapp"])

def _parse_message(body: str):
    """Parse product name and quantity from message."""
    parts = body.strip().split()
    if len(parts) < 2:
        return None, "Please send product name and quantity, e.g., 'rice 2'."
    try:
        qty = int(parts[-1])
    except ValueError:
        return None, "Quantity must be a number."
    product_name = " ".join(parts[:-1]).lower()
    return product_name, qty

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    from_phone = form.get("From", "")
    body = form.get("Body", "").strip()
    phone = from_phone.replace("whatsapp:", "") if from_phone.startswith("whatsapp:") else from_phone

    # Opt-out handling
    if phone in optout_phones:
        resp = MessagingResponse()
        resp.message("You have been opted out. Text START to re-enable.")
        return Response(content=str(resp), media_type="text/xml")

    if body.upper() == "STOP":
        optout_phones.add(phone)
        resp = MessagingResponse()
        resp.message("You have been opted out. Text START to re-enable.")
        return Response(content=str(resp), media_type="text/xml")

    if body.upper() == "START":
        optout_phones.discard(phone)
        resp = MessagingResponse()
        resp.message("Welcome back! You can now place orders.")
        return Response(content=str(resp), media_type="text/xml")

    # Parse order
    product_name, qty = _parse_message(body)
    if product_name is None:
        resp = MessagingResponse()
        resp.message(qty)
        return Response(content=str(resp), media_type="text/xml")

    # Find product by name (case-insensitive)
    product = next((p for p in _products_db if p["name"].lower() == product_name), None)
    if not product:
        resp = MessagingResponse()
        resp.message(f"Product '{product_name}' not found. Check your inventory list.")
        return Response(content=str(resp), media_type="text/xml")

    # Check stock
    if product["stock"] < qty:
        resp = MessagingResponse()
        resp.message(f"Insufficient stock for {product['name']}. Available: {product['stock']}.")
        return Response(content=str(resp), media_type="text/xml")

    # Create order
    items = [{
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": qty,
        "unit_price": product["price"]
    }]
    order = process_order(customer_phone=phone, items=items, customer_name=None)

    total = order["total_amount"]
    resp = MessagingResponse()
    resp.message(f"Order #{order['id'][:8]} confirmed: {qty} x {product['name']}. Total ${total:.2f}. Thank you!")
    return Response(content=str(resp), media_type="text/xml")