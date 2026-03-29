"""Reports router — sales PDF generation."""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from typing import List
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from auto_sme.dependencies import verify_api_key
from auto_sme.store import orders as _orders_db, products as _products_db

router = APIRouter(prefix="/reports", dependencies=[Depends(verify_api_key)])

@router.get("/sales")
async def sales_report(
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str = Query(..., description="YYYY-MM-DD")
):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    period_orders = [
        o for o in _orders_db
        if start <= o["created_at"] <= end
    ]
    total_orders = len(period_orders)
    total_revenue = sum(o["total_amount"] for o in period_orders)

    # Top products aggregation
    product_quantities = {}
    product_revenue = {}
    for o in period_orders:
        for item in o["items"]:
            pid = item["product_id"]
            product_quantities[pid] = product_quantities.get(pid, 0) + item["quantity"]
            product_revenue[pid] = product_revenue.get(pid, 0) + item["quantity"] * item["unit_price"]

    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AutoSME Sales Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Period: {start_date} to {end_date}", styles["Normal"]))
    story.append(Spacer(1, 12))

    data = [
        ["Metric", "Value"],
        ["Total Orders", str(total_orders)],
        ["Total Revenue", f"${total_revenue:,.2f}"],
    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,0), 14),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ]))
    story.append(table)
    story.append(Spacer(1, 24))

    # Top products table
    if product_quantities:
        story.append(Paragraph("Top Products", styles["Heading2"]))
        story.append(Spacer(1, 12))
        prod_data = [["Product", "Quantity", "Revenue"]]
        for pid, qty in sorted(product_quantities.items(), key=lambda x: x[1], reverse=True)[:10]:
            name = next((p["name"] for p in _products_db if p["id"] == pid), "Unknown")
            rev = product_revenue.get(pid, 0)
            prod_data.append([name, str(qty), f"${rev:,.2f}"])
        prod_table = Table(prod_data)
        prod_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1,0), 12),
        ]))
        story.append(prod_table)

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return Response(content=pdf, media_type="application/pdf")