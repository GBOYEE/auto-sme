"""WhatsApp webhook router for Twilio integration."""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy.orm import Session
from auto_sme.crud import get_products, is_opted_out, opt_out, create_order, adjust_stock
from auto_sme.database import get_db

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
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    from_phone = form.get("From", "")
    body = form.get("Body", "").strip()
    phone = from_phone.replace("whatsapp:", "") if from_phone.startswith("whatsapp:") else from_phone

    # Opt-out handling
    if is_opted_out(db=db, phone=phone):
        resp = MessagingResponse()
        resp.message("You have been opted out. Text START to re-enable.")
        return Response(content=str(resp), media_type="text/xml")

    if body.upper() == "STOP":
        opt_out(db=db, phone=phone)
        resp = MessagingResponse()
        resp.message("You have been opted out. Text START to re-enable.")
        return Response(content=str(resp), media_type="text/xml")

    if body.upper() == "START":
        # No direct un-opt-out function; simply allow through (we don't store explicit opt-in)
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
    products = get_products(db)
    product = next((p for p in products if p.name.lower() == product_name), None)
    if not product:
        resp = MessagingResponse()
        resp.message(f"Product '{product_name}' not found. Check your inventory list.")
        return Response(content=str(resp), media_type="text/xml")

    # Check stock
    if product.stock < qty:
        resp = MessagingResponse()
        resp.message(f"Insufficient stock for {product.name}. Available: {product.stock}.")
        return Response(content=str(resp), media_type="text/xml")

    # Create order and deduct stock
    total = product.price * qty
    order = create_order(
        db=db,
        customer_phone=phone,
        items=[{
            "product_id": product.id,
            "product_name": product.name,
            "quantity": qty,
            "unit_price": product.price
        }],
        customer_name=None
    )
    # Deduct stock
    adjust_stock(db=db, product_id=product.id, delta=-qty)

    resp = MessagingResponse()
    resp.message(f"Order #{order.id[:8]} confirmed: {qty} x {product.name}. Total ${total:.2f}. Thank you!")
    return Response(content=str(resp), media_type="text/xml")
