from flask import Flask, request, jsonify, Response
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import io
import datetime
import base64
import os
import urllib.request

app = Flask(__name__)

DARK  = colors.HexColor("#2c2c2c")
MUTED = colors.HexColor("#666666")
BLACK = colors.black
BORDER = colors.HexColor("#cccccc")
LIGHT_GRAY = colors.HexColor("#f5f5f5")

LOGO_URL = "https://raw.githubusercontent.com/hakaner3n/pdf-server/main/logo.png"

def s(name, **kw):
    return ParagraphStyle(name, **kw)

def get_logo():
    try:
        tmp = "/tmp/logo_msh.png"
        urllib.request.urlretrieve(LOGO_URL, tmp)
        if os.path.exists(tmp) and os.path.getsize(tmp) > 0:
            return tmp
        return None
    except Exception as e:
        print(f"Logo download failed: {e}")
        return None

def next_sunday(from_date=None):
    if from_date is None:
        from_date = datetime.date.today()
    days_ahead = 6 - from_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return from_date + datetime.timedelta(days=days_ahead)

def format_sunday(d):
    months = ["Januar","Februar","März","April","Mai","Juni",
              "Juli","August","September","Oktober","November","Dezember"]
    return f"Sonntag, {d.day:02d}. {months[d.month-1]} {str(d.year)[2:]}; 13:50 - 15:10 Uhr"

def parse_kurs(kurs, zeitstempel=""):
    kurs_lower = kurs.lower()
    schulgeld = "80&#8364;" if "80" in kurs else "68&#8364;"

    try:
        base_date = datetime.datetime.fromisoformat(zeitstempel[:10]).date() if zeitstempel else datetime.date.today()
    except:
        base_date = datetime.date.today()

    # Laufender Kurs: nächsten Sonntag berechnen
    if "laufend" in kurs_lower or "grundkenntnisse" in kurs_lower:
        naechster_sonntag = next_sunday(base_date)
        beginn = format_sunday(naechster_sonntag)
        abbuchung = f"{schulgeld} - Wird per Lastschrift ab {naechster_sonntag.strftime('%m/%y')} immer zum 01. eines Monats abgebucht."
    else:
        # Datum und Uhrzeit aus dem Kurs-String extrahieren
        # Format: "So. 03/05/26 | 13:50-15:10 Uhr"
        import re
        datum_match = re.search(r'(\d{2}/\d{2}/\d{2})', kurs)
        zeit_match  = re.search(r'(\d{2}:\d{2}[–-]\d{2}:\d{2})', kurs)
        if datum_match and zeit_match:
            d = datum_match.group(1)  # 03/05/26
            z = zeit_match.group(1)   # 13:50-15:10
            try:
                dt = datetime.datetime.strptime(d, '%d/%m/%y')
                wochentage = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
                wochentag = wochentage[dt.weekday()]
                months = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]
                beginn = f"{wochentag}, {dt.day:02d}. {months[dt.month-1]} {str(dt.year)[2:]}; {z} Uhr"
                abbuchung = f"{schulgeld} - Wird per Lastschrift ab {dt.strftime('%m/%y')} immer zum 01. eines Monats abgebucht."
            except:
                beginn = kurs
                abbuchung = f"{schulgeld} - Wird per Lastschrift immer zum 01. eines Monats abgebucht."
        else:
            beginn = kurs
            abbuchung = f"{schulgeld} - Wird per Lastschrift immer zum 01. eines Monats abgebucht."

    return {
        "fach":      "Musikunterricht - Baglama",
        "art":       "Gruppenunterricht",
        "ort":       "Kirchstr. 20, 40227 Düsseldorf",
        "beginn":    beginn,
        "schulgeld": abbuchung,
    }

def make_anmeldung(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        leftMargin=2.0*cm, rightMargin=2.0*cm,
        topMargin=1.5*cm, bottomMargin=3.0*cm)

    W = A4[0] - 4.0*cm

    # Styles – exakt wie in der Original-PDF
    title_style   = s("title",   fontSize=22, leading=28, textColor=BLACK,  fontName="Helvetica-Bold", alignment=TA_CENTER)
    sub_style     = s("sub",     fontSize=10, leading=14, textColor=MUTED,  fontName="Helvetica",      alignment=TA_CENTER)
    contact_style = s("contact", fontSize=9,  leading=13, textColor=MUTED,  fontName="Helvetica",      alignment=TA_CENTER)
    absender_style= s("abs",     fontSize=7,  leading=10, textColor=MUTED,  fontName="Helvetica")
    body_style    = s("body",    fontSize=10, leading=15, textColor=BLACK,  fontName="Helvetica",      spaceAfter=4)
    bold_style    = s("bold",    fontSize=10, leading=15, textColor=BLACK,  fontName="Helvetica-Bold", spaceAfter=4)
    label_style   = s("label",   fontSize=10, leading=14, textColor=MUTED,  fontName="Helvetica")
    value_style   = s("value",   fontSize=10, leading=14, textColor=BLACK,  fontName="Helvetica-Bold")
    date_lbl      = s("dlbl",    fontSize=9,  leading=13, textColor=MUTED,  fontName="Helvetica",      alignment=TA_RIGHT)
    date_val      = s("dval",    fontSize=10, leading=14, textColor=BLACK,  fontName="Helvetica",      alignment=TA_RIGHT)
    betreff_style = s("betreff", fontSize=10, leading=15, textColor=BLACK,  fontName="Helvetica-Bold", spaceAfter=6)
    small_style   = s("small",   fontSize=7,  leading=10, textColor=MUTED,  fontName="Helvetica")

    story = []

    # ── BRIEFKOPF: Logo links, Name+Adresse zentriert ──────────────────────────
    logo_path = get_logo()
    logo_img  = Image(logo_path, width=2.2*cm, height=2.2*cm) if logo_path else Spacer(2.2*cm, 2.2*cm)

    center_block = [
        Paragraph("Musikschule Hückelhoven e.V.", title_style),
        Spacer(1, 2),
        Paragraph("Wassenberger Str. 5b, 52525 Heinsberg", sub_style),
    ]

    header_table = Table([[logo_img, center_block, Spacer(2.6*cm, 1)]], colWidths=[2.6*cm, W - 5.2*cm, 2.6*cm])
    header_table.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "Homepage: www.musikschule-hueckelhoven.de<br/>E-Mail: info@musikschule-hueckelhoven.de",
        contact_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER))
    story.append(Spacer(1, 14))

    # ── ABSENDER-ZEILE ──────────────────────────────────────────────────────────
    story.append(Paragraph(
        "Musikschule Hückelhoven e.V. * Wassenberger Str. 5b * 52525 Heinsberg",
        absender_style))
    story.append(Spacer(1, 8))

    # ── EMPFÄNGER + DATUM ───────────────────────────────────────────────────────
    vorname  = data.get("vorname", "")
    nachname = data.get("nachname", "")
    strasse  = data.get("strasse", "")
    plz      = data.get("plz", "")
    ort_emp  = data.get("ort", "")
    zeitstempel = data.get("zeitstempel", "")

    datum_raw = zeitstempel[:10] if zeitstempel else datetime.date.today().strftime("%Y-%m-%d")
    try:
        datum_fmt = datetime.datetime.strptime(datum_raw, "%Y-%m-%d").strftime("%d.%m.%y")
    except:
        datum_fmt = datum_raw

    empf_block = [
        Paragraph(f"{vorname} {nachname}", body_style),
        Paragraph(strasse, body_style),
        Paragraph(f"{plz} {ort_emp}", body_style),
    ]
    datum_block = [
        Paragraph("Datum", date_lbl),
        Spacer(1, 2),
        Paragraph(datum_fmt, date_val),
    ]

    addr_table = Table([[empf_block, datum_block]], colWidths=[W * 0.65, W * 0.35])
    addr_table.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 0),
    ]))
    story.append(addr_table)
    story.append(Spacer(1, 36))

    # ── BETREFF ─────────────────────────────────────────────────────────────────
    story.append(Paragraph("Betreff: Anmeldebestätigung Saz-Unterricht", betreff_style))
    story.append(Spacer(1, 10))

    # ── ANREDE & TEXT ───────────────────────────────────────────────────────────
    story.append(Paragraph(f"Hallo {vorname},", body_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "die Anmeldung wurde bestätigt. Anbei erhältst Du die AGB unserer Musikschule und die Widerrufsbelehrung.",
        body_style))
    story.append(Spacer(1, 20))

    # ── KURSDETAILS TABELLE ─────────────────────────────────────────────────────
    kurs_info = parse_kurs(data.get("kurs", ""), zeitstempel)
    rows = [
        ("Unterrichtsteilnehmer:", f"{vorname} {nachname}"),
        ("Unterrichtsfach:",       kurs_info["fach"]),
        ("Unterrichtsart:",        kurs_info["art"]),
        ("Schulgeld monatlich:",   kurs_info["schulgeld"]),
        ("Unterrichtsbeginn:",     kurs_info["beginn"]),
        ("Unterrichtsort:",        kurs_info["ort"]),
    ]

    table_data = [[Paragraph(l, label_style), Paragraph(v, value_style)] for l, v in rows]
    details = Table(table_data, colWidths=[4.8*cm, W - 4.8*cm])
    details.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("LINEBELOW",     (0,0), (-1,-1), 0.5, BORDER),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(details)
    story.append(Spacer(1, 30))

    # ── GRUSS ───────────────────────────────────────────────────────────────────
    story.append(Paragraph("Mit freundlichen Grüßen,", body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Musikschule Hückelhoven", body_style))

    # ── FOOTER ──────────────────────────────────────────────────────────────────
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.8)
        canvas.line(2.0*cm, 2.2*cm, A4[0]-2.0*cm, 2.2*cm)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(DARK)
        canvas.drawString(2.0*cm, 1.8*cm, "Bankverbindung der Musikschule Hückelhoven e.V.:")
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(A4[0]-2.0*cm, 1.8*cm, "Kreissparkasse Heinsberg")
        canvas.drawRightString(A4[0]-2.0*cm, 1.2*cm, "IBAN: DE96 3125 1220 1401 2544 44")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    buffer.seek(0)
    return buffer


def make_agb():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        leftMargin=2.0*cm, rightMargin=2.0*cm,
        topMargin=1.5*cm, bottomMargin=2.5*cm)

    title_s = s("at", fontSize=18, leading=24, textColor=BLACK, fontName="Helvetica-Bold", alignment=TA_CENTER)
    sec_s   = s("as", fontSize=11, leading=16, textColor=BLACK, fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4)
    body_s  = s("ab", fontSize=9.5,leading=15, textColor=DARK,  fontName="Helvetica", spaceAfter=4)

    story = [
        Paragraph("Allgemeine Geschäftsbedingungen", title_s),
        Paragraph("Musikschule Hückelhoven e.V.", s("sub", fontSize=11, leading=14, textColor=MUTED, fontName="Helvetica", alignment=TA_CENTER)),
        Spacer(1, 20),
        HRFlowable(width="100%", thickness=1, color=BORDER),
        Spacer(1, 14),
    ]
    paragraphen = [
        ("§ 1 – Geltungsbereich", "Diese AGB gelten für alle Verträge über Musikunterricht zwischen der Musikschule Hückelhoven e.V. und den Kursteilnehmern."),
        ("§ 2 – Vertragsschluss", "Der Vertrag kommt durch die schriftliche oder digitale Anmeldung und Bestätigung durch die Musikschule zustande."),
        ("§ 3 – Leistungsumfang", "Die Musikschule verpflichtet sich, den vereinbarten Unterricht regelmäßig durchzuführen. Bei Ausfall wird ein Ersatztermin angeboten."),
        ("§ 4 – Entgelt und Zahlung", "Das monatliche Unterrichtsentgelt ist zum 01. eines jeden Monats per SEPA-Lastschrift fällig."),
        ("§ 5 – Kündigung", "Der Vertrag kann mit einer Frist von 4 Wochen zum Monatsende schriftlich gekündigt werden."),
        ("§ 6 – Haftung", "Die Musikschule haftet nur für grob fahrlässig oder vorsätzlich verursachte Schäden."),
        ("§ 7 – Datenschutz", "Personenbezogene Daten werden ausschließlich zur Vertragsabwicklung verwendet und nicht an Dritte weitergegeben."),
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
        leftMargin=2.0*cm, rightMargin=2.0*cm,
        topMargin=1.5*cm, bottomMargin=2.5*cm)

    title_s = s("wt", fontSize=18, leading=24, textColor=BLACK, fontName="Helvetica-Bold", alignment=TA_CENTER)
    sec_s   = s("ws", fontSize=11, leading=16, textColor=BLACK, fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4)
    body_s  = s("wb", fontSize=9.5,leading=15, textColor=DARK,  fontName="Helvetica", spaceAfter=4)

    story = [
        Paragraph("Widerrufsbelehrung", title_s),
        Paragraph("Gemäß § 355 BGB", s("wsub", fontSize=11, leading=14, textColor=MUTED, fontName="Helvetica", alignment=TA_CENTER)),
        Spacer(1, 20),
        HRFlowable(width="100%", thickness=1, color=BORDER),
        Spacer(1, 14),
        Paragraph("Widerrufsrecht", sec_s),
        Paragraph("Sie haben das Recht, binnen vierzehn Tagen ohne Angabe von Gründen diesen Vertrag zu widerrufen. Die Widerrufsfrist beträgt vierzehn Tage ab dem Tag des Vertragsschlusses.", body_s),
        Paragraph("Ausübung des Widerrufsrechts", sec_s),
        Paragraph("Um Ihr Widerrufsrecht auszuüben, müssen Sie uns (Musikschule Hückelhoven, info@musikschule-hueckelhoven.de) mittels einer eindeutigen Erklärung informieren.", body_s),
        Paragraph("Folgen des Widerrufs", sec_s),
        Paragraph("Wenn Sie diesen Vertrag widerrufen, haben wir Ihnen alle Zahlungen unverzüglich und spätestens binnen vierzehn Tagen zurückzuzahlen.", body_s),
        Spacer(1, 20),
        Paragraph("Muster-Widerrufsformular", sec_s),
        Paragraph("An: Musikschule Hückelhoven, info@musikschule-hueckelhoven.de<br/><br/>Hiermit widerrufe ich den abgeschlossenen Vertrag.<br/><br/>Name: ______________________________<br/><br/>Datum: ______________________________<br/><br/>Unterschrift: ______________________________", body_s),
    ]

    doc.build(story)
    buffer.seek(0)
    return buffer


@app.route("/anmeldung-pdf", methods=["POST", "GET"])
def anmeldung_pdf():
    try:
        if request.method == "POST":
            data = request.get_json(force=True) or {}
        else:
            data = {k: request.args.get(k, "") for k in
                    ["vorname","nachname","geburtsdatum","strasse","plz","ort",
                     "telefon","email","kurs","kontoinhaber","iban","zeitstempel"]}

        pdf_buf  = make_anmeldung(data)
        vorname  = data.get("vorname", "Anmeldung").replace(" ", "_")
        nachname = data.get("nachname", "").replace(" ", "_")
        filename = f"Anmeldebestaetigung_{vorname}_{nachname}.pdf"

        return Response(
            pdf_buf.read(),
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
            "anmeldung": {"filename": f"Anmeldebestaetigung_{vorname}_{nachname}.pdf", "data": base64.b64encode(anmeldung_buf.read()).decode()},
            "agb":       {"filename": "AGB_Musikschule_Hueckelhoven.pdf",              "data": base64.b64encode(agb_buf.read()).decode()},
            "widerruf":  {"filename": "Widerrufsbelehrung.pdf",                        "data": base64.b64encode(widerruf_buf.read()).decode()},
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Musikschule PDF Generator"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
