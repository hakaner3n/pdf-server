from flask import Flask, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import io
import datetime
import base64
import urllib.request
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/zvrwplg9s3e8hk4b85xxvtbm3ml2g4c2"
SMTP_SERVER   = os.environ.get("SMTP_SERVER",   "secure.emailsrvr.com")
SMTP_USER     = os.environ.get("SMTP_USER",     "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

# ── Styles ────────────────────────────────────────────────────
DARK  = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#666666")

def s(name, **kw):
    return ParagraphStyle(name, **kw)

# ── Anmeldebestätigung PDF ────────────────────────────────────
def make_anmeldung(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.5*cm, bottomMargin=3*cm)

    W = A4[0] - 4*cm
    story = []
    heute = datetime.date.today().strftime("%d.%m.%y")

    # Logo
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2*cm, height=2*cm)
    else:
        logo = Paragraph("", s("x", fontSize=10))

    firma_text = [
        Paragraph("<b>Musikschule Hückelhoven e.V.</b>",
                  s("f1", fontSize=16, fontName="Helvetica-Bold", textColor=DARK, leading=20)),
        Paragraph("Kuhlertstr. 98, 52525 Heinsberg",
                  s("f2", fontSize=9, fontName="Helvetica", textColor=MUTED, leading=13)),
        Spacer(1, 4),
        Paragraph("Homepage: www.musikschule-hueckelhoven.de",
                  s("f3", fontSize=9, fontName="Helvetica", textColor=MUTED, leading=13)),
        Paragraph("E-Mail: info@musikschule-hueckelhoven.de",
                  s("f4", fontSize=9, fontName="Helvetica", textColor=MUTED, leading=13)),
    ]

    header_table = Table([[logo, firma_text]], colWidths=[2.5*cm, W - 2.5*cm])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Musikschule Hückelhoven e.V. * Kuhlert Straße 98 * 52525 Heinsberg",
        s("abs", fontSize=7.5, fontName="Helvetica", textColor=MUTED, leading=11)))
    story.append(Spacer(1, 6))

    vorname  = data.get("vorname", "")
    nachname = data.get("nachname", "")
    strasse  = data.get("strasse", "")
    plz      = data.get("plz", "")
    ort      = data.get("ort", "")

    adresse = [
        Paragraph(f"{vorname} {nachname}",
                  s("ad1", fontSize=10, fontName="Helvetica", textColor=DARK, leading=15)),
        Paragraph(strasse,
                  s("ad2", fontSize=10, fontName="Helvetica", textColor=DARK, leading=15)),
        Paragraph(f"{plz} {ort}",
                  s("ad3", fontSize=10, fontName="Helvetica", textColor=DARK, leading=15)),
    ]

    datum_block = [
        Paragraph("Datum",
                  s("db1", fontSize=9, fontName="Helvetica", textColor=MUTED, leading=13, alignment=TA_RIGHT)),
        Spacer(1, 4),
        Paragraph(heute,
                  s("db2", fontSize=10, fontName="Helvetica", textColor=DARK, leading=14, alignment=TA_RIGHT)),
    ]

    addr_table = Table([[adresse, datum_block]], colWidths=[11*cm, 5*cm])
    addr_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(addr_table)
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Betreff: Anmeldebestätigung Saz-Unterricht</b>",
        s("betreff", fontSize=10, fontName="Helvetica-Bold", textColor=DARK, leading=15)))
    story.append(Spacer(1, 16))

    story.append(Paragraph(f"Hallo {vorname},",
        s("anrede", fontSize=10, fontName="Helvetica", textColor=DARK, leading=15)))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "die Anmeldung wurde bestätigt. Anbei erhältst Du die AGB unserer Musikschule und die Widerrufsbelehrung.",
        s("intro", fontSize=10, fontName="Helvetica", textColor=DARK, leading=15)))
    story.append(Spacer(1, 20))

    kurs  = data.get("kurs", "")
    preis = "80€" if "80" in kurs else "68€"

    details = [
        ["Unterrichtsteilnehmer:", Paragraph(f"<b>{vorname} {nachname}</b>",
            s("tv1", fontSize=10, fontName="Helvetica-Bold", textColor=DARK, leading=14))],
        ["Unterrichtsfach:", Paragraph("<b>Musikunterricht - Baglama</b>",
            s("tv2", fontSize=10, fontName="Helvetica-Bold", textColor=DARK, leading=14))],
        ["Unterrichtsart:", Paragraph("<b>Gruppenunterricht</b>",
            s("tv3", fontSize=10, fontName="Helvetica-Bold", textColor=DARK, leading=14))],
        ["Schulgeld monatlich:", Paragraph(
            f"<b>{preis}</b> - Wird per Lastschrift ab 05/26 immer zum 01. eines Monats abgebucht.",
            s("tv4", fontSize=10, fontName="Helvetica", textColor=DARK, leading=14))],
        ["Unterrichtsbeginn:", Paragraph("<b>Sonntag, 03.05.26; 13:50 - 15:10 Uhr</b>",
            s("tv5", fontSize=10, fontName="Helvetica-Bold", textColor=DARK, leading=14))],
        ["Unterrichtsort:", Paragraph("<b>Kirchstr. 20, 40227 Düsseldorf</b>",
            s("tv6", fontSize=10, fontName="Helvetica-Bold", textColor=DARK, leading=14))],
    ]

    detail_table = Table(details, colWidths=[5*cm, 11*cm])
    detail_table.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (0,-1), 0),
        ("FONTNAME",      (0,0), (0,-1), "Helvetica"),
        ("FONTSIZE",      (0,0), (0,-1), 10),
        ("TEXTCOLOR",     (0,0), (0,-1), MUTED),
    ]))
    story.append(detail_table)
    story.append(Spacer(1, 30))

    story.append(Paragraph("Mit freundlichen Grüßen,",
        s("gruss", fontSize=10, fontName="Helvetica", textColor=DARK, leading=15)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Musikschule Hückelhoven",
        s("ms", fontSize=10, fontName="Helvetica", textColor=DARK, leading=15)))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#cccccc"))
        canvas.setLineWidth(0.5)
        canvas.line(2*cm, 2.2*cm, A4[0]-2*cm, 2.2*cm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(2*cm, 1.8*cm, "Bankverbindung der Musikschule Hückelhoven e.V.:")
        canvas.drawRightString(A4[0]-2*cm, 1.8*cm, "Kreissparkasse Heinsberg")
        canvas.drawRightString(A4[0]-2*cm, 1.5*cm, "IBAN: DE96 3125 1220 1401 2544 44")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    buffer.seek(0)
    return buffer.read()


def load_pdf_from_github(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.read()
    except:
        return None


def send_email(to_email, vorname, nachname, anmeldung_pdf, agb_pdf, widerruf_pdf):
    msg = MIMEMultipart()
    msg["From"]    = f"Musikschule Hückelhoven <{SMTP_USER}>"
    msg["To"]      = to_email
    msg["Subject"] = f"Anmeldebestätigung Saz Kurs – {vorname} {nachname}"

    body = f"""<p>Hallo {vorname},</p>
<p>vielen Dank für deine Anmeldung über unsere Webseite. Anbei findest du die Anmeldebestätigung sowie unsere AGB und die Widerrufsbelehrung.</p>
<p><strong>Wichtig:</strong><br>
Bitte bestätige kurz den Erhalt dieser E-Mail, um sicherzustellen, dass sie nicht im Spam-Ordner gelandet ist. Eine kurze Antwort mit "erhalten" genügt.</p>
<p>Bei Fragen stehen wir dir gerne zur Verfügung.</p>
<p>Mit freundlichen Grüßen,<br>Team - Musikschule Hückelhoven</p>"""

    msg.attach(MIMEText(body, "html", "utf-8"))

    def attach_pdf(data, filename):
        if data:
            part = MIMEBase("application", "pdf")
            part.set_payload(data)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
            msg.attach(part)

    attach_pdf(anmeldung_pdf, f"Anmeldebestaetigung_{vorname}_{nachname}.pdf")
    attach_pdf(agb_pdf,       "AGB_Musikschule_Hueckelhoven.pdf")
    attach_pdf(widerruf_pdf,  "Widerrufsbelehrung.pdf")

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)


@app.route("/submit", methods=["POST", "OPTIONS"])
def submit():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Keine Daten"}), 400

        # PDFs erstellen
        anmeldung_pdf = make_anmeldung(data)
        agb_pdf       = load_pdf_from_github(
            "https://raw.githubusercontent.com/hakaner3n/Anmeldung/main/AGB_Musikschule_Hueckelhoven.pdf")
        widerruf_pdf  = load_pdf_from_github(
            "https://raw.githubusercontent.com/hakaner3n/Anmeldung/main/Widerrufsbelehrung.pdf")

        # E-Mail versenden
        send_email(
            to_email     = data.get("email", ""),
            vorname      = data.get("vorname", ""),
            nachname     = data.get("nachname", ""),
            anmeldung_pdf= anmeldung_pdf,
            agb_pdf      = agb_pdf,
            widerruf_pdf = widerruf_pdf
        )

        # Make.com benachrichtigen
        try:
            payload = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                MAKE_WEBHOOK_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            urllib.request.urlopen(req, timeout=10)
        except:
            pass

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Musikschule PDF Generator"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
