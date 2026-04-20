from flask import Flask, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import io
import datetime
import base64
import urllib.request
import json

app = Flask(__name__)

MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/zvrwplg9s3e8hk4b85xxvtbm3ml2g4c2"

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/submit", methods=["POST", "OPTIONS"])
def submit():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Keine Daten"}), 400
        payload = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            MAKE_WEBHOOK_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=10)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



TEAL      = colors.HexColor("#1a5f6a")
TEAL_DARK = colors.HexColor("#144d57")
ACCENT    = colors.HexColor("#c0392b")
BORDER    = colors.HexColor("#ccd8da")
GRAY      = colors.HexColor("#f7fafb")
WHITE     = colors.white
DARK      = colors.HexColor("#2c2c2c")
MUTED     = colors.HexColor("#666666")

def s(name, **kw):
    return ParagraphStyle(name, **kw)

def make_anmeldung(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.5*cm, bottomMargin=2.5*cm)

    title_style = s("title", fontSize=20, leading=26, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_LEFT)
    body_style  = s("body",  fontSize=9.5, leading=15, textColor=DARK, fontName="Helvetica", spaceAfter=4)
    bold_style  = s("bold",  fontSize=9.5, leading=15, textColor=DARK, fontName="Helvetica-Bold", spaceAfter=2)
    label_style = s("label", fontSize=8,   leading=11, textColor=MUTED, fontName="Helvetica-Bold")
    value_style = s("value", fontSize=10,  leading=14, textColor=DARK,  fontName="Helvetica-Bold")
    small_style = s("small", fontSize=8,   leading=12, textColor=MUTED, fontName="Helvetica")

    story = []
    W = A4[0] - 4*cm

    datum = data.get("zeitstempel", "")[:10] if data.get("zeitstempel") else datetime.date.today().strftime("%Y-%m-%d")
    try:
        datum_fmt = datetime.datetime.strptime(datum, "%Y-%m-%d").strftime("%d.%m.%Y")
    except:
        datum_fmt = datum

    anmelde_nr = f"ANM-{datetime.date.today().strftime('%Y')}-{abs(hash(data.get('email',''))) % 9000 + 1000}"

    header = Table([[
        Paragraph("Anmeldebestaetigung", title_style),
        [Paragraph("Nr.", small_style),
         Paragraph(f"<b><font color='white'>{anmelde_nr}</font></b>",
                   ParagraphStyle("nr", fontSize=11, fontName="Helvetica-Bold", textColor=WHITE, leading=14)),
         Spacer(1,4),
         Paragraph("Datum", small_style),
         Paragraph(f"<b><font color='white'>{datum_fmt}</font></b>",
                   ParagraphStyle("dt", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, leading=14))]
    ]], colWidths=[11*cm, 5*cm])
    header.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), TEAL_DARK),
        ("TOPPADDING",    (0,0), (-1,-1), 16),
        ("BOTTOMPADDING", (0,0), (-1,-1), 16),
        ("LEFTPADDING",   (0,0), (0,0),  14),
        ("RIGHTPADDING",  (1,0), (1,0),  14),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("LINEBELOW",     (0,0), (-1,-1), 3, ACCENT),
    ]))
    story.append(header)
    story.append(Spacer(1, 14))

    vorname  = data.get("vorname", "")
    nachname = data.get("nachname", "")
    story.append(Paragraph(f"Sehr geehrte/r {vorname} {nachname},", bold_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "wir freuen uns ueber Ihre Anmeldung und bestaetigen hiermit Ihre Aufnahme in unsere Musikschule.",
        body_style))
    story.append(Spacer(1, 10))

    def accent_bar(text):
        t = Table([[Paragraph(text, ParagraphStyle("ab", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, leading=14))]],
                  colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), ACCENT),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ]))
        return t

    def info_grid(rows):
        cells = [[Paragraph(l, label_style), Paragraph(str(v), value_style)] for l, v in rows]
        t = Table(cells, colWidths=[4.5*cm, 11.5*cm])
        t.setStyle(TableStyle([
            ("ROWBACKGROUNDS", (0,0), (-1,-1), [GRAY, WHITE]),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ("LINEBELOW",     (0,0), (-1,-2), 0.5, BORDER),
            ("BOX",           (0,0), (-1,-1), 1, BORDER),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ]))
        return t

    story.append(accent_bar("Angaben zur/zum Schueler/in"))
    story.append(Spacer(1, 4))
    story.append(info_grid([
        ("Vorname",      data.get("vorname", "")),
        ("Nachname",     data.get("nachname", "")),
        ("Geburtsdatum", data.get("geburtsdatum", "")),
        ("Strasse / Nr.",data.get("strasse", "")),
        ("PLZ / Ort",    f'{data.get("plz","")}  {data.get("ort","")}'),
        ("Telefon",      data.get("telefon", "")),
        ("E-Mail",       data.get("email", "")),
    ]))
    story.append(Spacer(1, 12))

    story.append(accent_bar("Gebuchter Kurs"))
    story.append(Spacer(1, 4))
    story.append(info_grid([("Kurs", data.get("kurs", ""))]))
    story.append(Spacer(1, 12))

    story.append(accent_bar("Bankdaten / SEPA-Lastschriftmandat"))
    story.append(Spacer(1, 4))
    story.append(info_grid([
        ("Kontoinhaber", data.get("kontoinhaber", "")),
        ("IBAN",         data.get("iban", "")),
        ("Faelligkeit",  "Monatlich zum 01. des Monats"),
    ]))
    story.append(Spacer(1, 16))

    story.append(HRFlowable(width="100%", thickness=1, color=BORDER))
    story.append(Spacer(1, 8))
    for titel, text in [
        ("Probezeit",  "Die ersten zwei Unterrichtseinheiten gelten als unverbindliche Probestunden."),
        ("Kuendigung", "Kuendigungen sind mit einer Frist von 4 Wochen zum Monatsende schriftlich einzureichen."),
        ("Kontakt",    "Bei Fragen: info@musikschule-hueckelhoven.de"),
    ]:
        story.append(Paragraph(f"<b>{titel}:</b>  {text}", body_style))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7.5)
        y = 1.2*cm
        canvas.drawCentredString(A4[0]/2, y,
            "Musikschule Hueckelhoven · info@musikschule-hueckelhoven.de · www.musikschule-hueckelhoven.de")
        canvas.setStrokeColor(ACCENT)
        canvas.setLineWidth(2)
        canvas.line(2*cm, y+12, A4[0]-2*cm, y+12)
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    buffer.seek(0)
    return buffer


def make_agb():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.5*cm, bottomMargin=2.5*cm)

    title_s = s("at", fontSize=18, leading=24, textColor=TEAL_DARK, fontName="Helvetica-Bold", alignment=TA_CENTER)
    sec_s   = s("as", fontSize=11, leading=16, textColor=ACCENT,    fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4)
    body_s  = s("ab", fontSize=9.5,leading=15, textColor=DARK,      fontName="Helvetica", spaceAfter=4)

    story = [
        Paragraph("Allgemeine Geschaeftsbedingungen", title_s),
        Paragraph("Musikschule Hueckelhoven e.V.", s("sub", fontSize=11, leading=14, textColor=MUTED, fontName="Helvetica", alignment=TA_CENTER)),
        Spacer(1, 20),
        HRFlowable(width="100%", thickness=2, color=ACCENT),
        Spacer(1, 14),
    ]

    paragraphen = [
        ("SS 1 - Geltungsbereich",
         "Diese AGB gelten fuer alle Vertraege ueber Musikunterricht zwischen der Musikschule Hueckelhoven e.V. und den Kursteilnehmern."),
        ("SS 2 - Vertragsschluss",
         "Der Vertrag kommt durch die schriftliche oder digitale Anmeldung und Bestaetigung durch die Musikschule zustande."),
        ("SS 3 - Leistungsumfang",
         "Die Musikschule verpflichtet sich, den vereinbarten Unterricht regelmaessig durchzufuehren. Bei Ausfall wird ein Ersatztermin angeboten."),
        ("SS 4 - Entgelt und Zahlung",
         "Das monatliche Unterrichtsentgelt ist zum 01. eines jeden Monats per SEPA-Lastschrift faellig."),
        ("SS 5 - Kuendigung",
         "Der Vertrag kann mit einer Frist von 4 Wochen zum Monatsende schriftlich gekuendigt werden."),
        ("SS 6 - Haftung",
         "Die Musikschule haftet nur fuer grob fahrlaessig oder vorsaetzlich verursachte Schaeden."),
        ("SS 7 - Datenschutz",
         "Personenbezogene Daten werden ausschliesslich zur Vertragsabwicklung verwendet und nicht an Dritte weitergegeben."),
    ]

    for titel, text in paragraphen:
        story.append(Paragraph(titel, sec_s))
        story.append(Paragraph(text, body_s))

    doc.build(story)
    buffer.seek(0)
    return buffer


def make_widerruf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.5*cm, bottomMargin=2.5*cm)

    title_s = s("wt", fontSize=18, leading=24, textColor=TEAL_DARK, fontName="Helvetica-Bold", alignment=TA_CENTER)
    sec_s   = s("ws", fontSize=11, leading=16, textColor=ACCENT,    fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4)
    body_s  = s("wb", fontSize=9.5,leading=15, textColor=DARK,      fontName="Helvetica", spaceAfter=4)

    story = [
        Paragraph("Widerrufsbelehrung", title_s),
        Paragraph("Gemaess SS 355 BGB", s("wsub", fontSize=11, leading=14, textColor=MUTED, fontName="Helvetica", alignment=TA_CENTER)),
        Spacer(1, 20),
        HRFlowable(width="100%", thickness=2, color=ACCENT),
        Spacer(1, 14),
        Paragraph("Widerrufsrecht", sec_s),
        Paragraph(
            "Sie haben das Recht, binnen vierzehn Tagen ohne Angabe von Gruenden diesen Vertrag zu widerrufen. "
            "Die Widerrufsfrist betraegt vierzehn Tage ab dem Tag des Vertragsschlusses.",
            body_s),
        Paragraph("Ausuebung des Widerrufsrechts", sec_s),
        Paragraph(
            "Um Ihr Widerrufsrecht auszuueben, muessen Sie uns (Musikschule Hueckelhoven, "
            "info@musikschule-hueckelhoven.de) mittels einer eindeutigen Erklaerung informieren.",
            body_s),
        Paragraph("Folgen des Widerrufs", sec_s),
        Paragraph(
            "Wenn Sie diesen Vertrag widerrufen, haben wir Ihnen alle Zahlungen unverzueglich "
            "und spaetestens binnen vierzehn Tagen zurueckzuzahlen.",
            body_s),
        Spacer(1, 20),
        Paragraph("Muster-Widerrufsformular", sec_s),
        Paragraph(
            "An: Musikschule Hueckelhoven, info@musikschule-hueckelhoven.de\n\n"
            "Hiermit widerrufe ich den abgeschlossenen Vertrag.\n\n"
            "Name: ______________________________\n\n"
            "Datum: ______________________________\n\n"
            "Unterschrift: ______________________________",
            body_s),
    ]

    doc.build(story)
    buffer.seek(0)
    return buffer


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Keine Daten empfangen"}), 400

        anmeldung_buf = make_anmeldung(data)
        agb_buf       = make_agb()
        widerruf_buf  = make_widerruf()

        vorname  = data.get("vorname", "Anmeldung").replace(" ", "_")
        nachname = data.get("nachname", "").replace(" ", "_")

        return jsonify({
            "anmeldung": {
                "filename": f"Anmeldebestaetigung_{vorname}_{nachname}.pdf",
                "data": base64.b64encode(anmeldung_buf.read()).decode("utf-8")
            },
            "agb": {
                "filename": "AGB_Musikschule_Hueckelhoven.pdf",
                "data": base64.b64encode(agb_buf.read()).decode("utf-8")
            },
            "widerruf": {
                "filename": "Widerrufsbelehrung.pdf",
                "data": base64.b64encode(widerruf_buf.read()).decode("utf-8")
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Musikschule PDF Generator"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
