import os
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.services.base_service import BaseService
from app.services.preference_service import PreferenceService

logger = logging.getLogger(__name__)

class PDFService(BaseService):
    """
    Handles PDF generation for invoices/bills.
    """

    def __init__(self, db: Session):
        super().__init__(db)
        self.pref_service = PreferenceService(db)

    def generate_invoice_pdf(self, bill) -> str:
        """
        Generates a beautiful HTML invoice and compiles it to PDF using WeasyPrint.
        Returns the absolute filepath to the generated file (either PDF or HTML fallback).
        """
        store_name = self.pref_service.get_store_name()
        currency = self.pref_service.get_currency()
        
        # Ensure directories exist
        output_dir = os.path.abspath(os.path.join("data", "invoices"))
        os.makedirs(output_dir, exist_ok=True)
        
        created_at_str = bill.created_at.strftime("%Y-%m-%d %H:%M:%S") if bill.created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        customer_name = bill.customer.name if bill.customer else "Walk-in Customer"
        customer_phone = bill.customer.phone if bill.customer else "N/A"
        
        # Calculate item line totals
        items_html = ""
        for index, item in enumerate(bill.bill_items, start=1):
            product_name = item.product.name if item.product else f"Product ID: {item.product_id}"
            line_total = item.quantity * item.unit_price
            items_html += f"""
            <tr class="item">
                <td class="text-center">{index}</td>
                <td>{product_name}</td>
                <td class="text-right">{item.quantity}</td>
                <td class="text-right">{currency} {item.unit_price:.2f}</td>
                <td class="text-right">{item.gst_rate}%</td>
                <td class="text-right">{currency} {item.gst_amount:.2f}</td>
                <td class="text-right">{currency} {item.line_total:.2f}</td>
            </tr>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Invoice {bill.invoice_number}</title>
            <style>
                body {{
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                    color: #333;
                    margin: 0;
                    padding: 10px;
                    background-color: #f9f9f9;
                }}
                .invoice-box {{
                    max-width: 800px;
                    margin: auto;
                    padding: 30px;
                    border: 1px solid #e2e8f0;
                    background-color: #ffffff;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    border-radius: 8px;
                }}
                .header-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 30px;
                }}
                .header-table td {{
                    vertical-align: top;
                }}
                .store-title {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #2563eb;
                    margin: 0 0 5px 0;
                }}
                .store-sub {{
                    font-size: 14px;
                    color: #64748b;
                }}
                .invoice-title {{
                    font-size: 26px;
                    font-weight: bold;
                    color: #1e293b;
                    text-align: right;
                    margin: 0;
                }}
                .invoice-meta {{
                    text-align: right;
                    font-size: 14px;
                    color: #475569;
                    margin-top: 5px;
                }}
                .details-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 30px;
                }}
                .details-table td {{
                    padding: 8px;
                    border: 1px solid #e2e8f0;
                    font-size: 14px;
                }}
                .details-table th {{
                    background-color: #f8fafc;
                    padding: 8px;
                    border: 1px solid #e2e8f0;
                    text-align: left;
                    font-size: 14px;
                    color: #475569;
                }}
                .items-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 30px;
                }}
                .items-table th {{
                    background-color: #2563eb;
                    color: white;
                    padding: 10px;
                    font-size: 14px;
                    text-align: left;
                    font-weight: 600;
                }}
                .items-table td {{
                    padding: 10px;
                    border-bottom: 1px solid #e2e8f0;
                    font-size: 14px;
                }}
                .text-right {{
                    text-align: right !important;
                }}
                .text-center {{
                    text-align: center !important;
                }}
                .summary-table {{
                    width: 40%;
                    margin-left: auto;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                .summary-table td {{
                    padding: 8px;
                    font-size: 14px;
                }}
                .summary-table .label {{
                    text-align: right;
                    color: #475569;
                }}
                .summary-table .value {{
                    text-align: right;
                    font-weight: 600;
                    color: #1e293b;
                }}
                .summary-table .grand-total-row td {{
                    border-top: 2px solid #2563eb;
                    font-size: 18px;
                    font-weight: bold;
                    color: #2563eb;
                    padding-top: 12px;
                }}
                .footer {{
                    margin-top: 50px;
                    text-align: center;
                    font-size: 12px;
                    color: #94a3b8;
                    border-top: 1px solid #e2e8f0;
                    padding-top: 20px;
                }}
                .badge {{
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: 600;
                    text-transform: uppercase;
                }}
                .badge-paid {{
                    background-color: #dcfce7;
                    color: #166534;
                }}
                .badge-pending {{
                    background-color: #fef9c3;
                    color: #854d0e;
                }}
                .badge-cancelled {{
                    background-color: #fee2e2;
                    color: #991b1b;
                }}
            </style>
        </head>
        <body>
            <div class="invoice-box">
                <table class="header-table">
                    <tr>
                        <td>
                            <div class="store-title">{store_name}</div>
                            <div class="store-sub">Your Neighborhood Supermarket</div>
                        </td>
                        <td>
                            <div class="invoice-title">TAX INVOICE</div>
                            <div class="invoice-meta">
                                <strong>Invoice No:</strong> {bill.invoice_number}<br>
                                <strong>Date:</strong> {created_at_str}
                            </div>
                        </td>
                    </tr>
                </table>

                <table class="details-table">
                    <tr>
                        <th width="50%">Billed To (Customer Details)</th>
                        <th width="50%">Payment Details</th>
                    </tr>
                    <tr>
                        <td>
                            <strong>Name:</strong> {customer_name}<br>
                            <strong>Phone:</strong> {customer_phone}
                        </td>
                        <td>
                            <strong>Payment Method:</strong> {bill.payment_method.value}<br>
                            <strong>Status:</strong> 
                            <span class="badge badge-{bill.payment_status.value.lower()}">{bill.payment_status.value}</span>
                        </td>
                    </tr>
                </table>

                <table class="items-table">
                    <thead>
                        <tr>
                            <th width="5%" class="text-center">#</th>
                            <th width="40%">Item Name</th>
                            <th width="10%" class="text-right">Qty</th>
                            <th width="15%" class="text-right">Unit Price</th>
                            <th width="10%" class="text-right">GST Rate</th>
                            <th width="10%" class="text-right">GST Amt</th>
                            <th width="15%" class="text-right">Line Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_html}
                    </tbody>
                </table>

                <table class="summary-table">
                    <tr>
                        <td class="label">Subtotal:</td>
                        <td class="value">{currency} {bill.subtotal:.2f}</td>
                    </tr>
                    <tr>
                        <td class="label">GST Total:</td>
                        <td class="value">{currency} {bill.gst_amount:.2f}</td>
                    </tr>
                    <tr>
                        <td class="label">Discount:</td>
                        <td class="value">- {currency} {bill.discount:.2f}</td>
                    </tr>
                    <tr class="grand-total-row">
                        <td class="label">Grand Total:</td>
                        <td class="value">{currency} {bill.grand_total:.2f}</td>
                    </tr>
                </table>

                <div class="footer">
                    Thank you for shopping with {store_name}!<br>
                    For any queries, please contact support.
                </div>
            </div>
        </body>
        </html>
        """
        
        pdf_path = os.path.join(output_dir, f"{bill.invoice_number}.pdf")
        html_path = os.path.join(output_dir, f"{bill.invoice_number}.html")
        
        # Save HTML version first (both as output and fallback)
        try:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            logger.error(f"Failed to save HTML invoice: {e}")
            
        # Try compiling to PDF via WeasyPrint
        try:
            from weasyprint import HTML
            HTML(string=html_content).write_pdf(pdf_path)
            logger.info(f"PDF invoice successfully generated: {pdf_path}")
            return pdf_path
        except Exception as e:
            logger.warning(f"WeasyPrint PDF compilation failed, falling back to HTML file. Error: {e}")
            # If WeasyPrint fails (e.g. missing GTK on Windows), return the HTML file path
            return html_path
