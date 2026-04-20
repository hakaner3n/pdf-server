from flask import Flask, request, jsonify, send_file
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import io
import datetime

app = Flask(__name__)

TEAL      = colors.HexColor("#1a5f6a")
TEAL_DARK = colors.HexColor("#144d57")
LIGHT     = colors.HexColor("#e8f4f6")
ACCENT    = colors.HexColor("#c0392b")
BORDER    = colors.HexColor("#ccd8da")
GRAY      = colors.HexColor("#f7fafb")
WHITE     = colors.white
DARK      = colors.HexColor("#2c2c2c")
MUTED     = colors.HexColor("#666666")

def make_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.5*cm, bottomMargin=2.5*cm
    )

    def s(name, **kw):
        return ParagraphStyle(name, **kw)

    title_style  = s("title",  fontSize=20, leading=26, textColor=WHITE,      fontName="Helvetica-Bold", alignment=TA_LEFT)
    sub_style    = s("sub",    fontSize=10, leading=14, textColor=colors.HexColor("#c8d8da"), fontName="Helvetica", alignment=TA_LEFT)
    section_style= s("sec",    fontSize=11, leading=16, textColor=ACCENT,      fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4)
    body_style   = s("body",   fontSize=9.5,leading=15, textColor=DARK,        fontName="Helvetica", spaceAfter=4)
    bold_style   = s("bold",   fontSize=9.5,leading=15, textColor=DARK,        fontName="Helvetica-Bold", spaceAfter=2)
    label_style  = s("label",  fontSize=8,  leading=11, textColor=MUTED,       fontName="Helvetica-Bold")
    value_style  = s("value",  fontSize=10, leading=14, textColor=DARK,        fontName="Helvetica-Bold")
    footer_style = s("footer", fontSize=7.5,leading=11, textColor=MUTED,       fontName="Helvetica", alignment=TA_CENTER)
    small_style  = s("small",  fontSize=8,  leading=12, textColor=MUTED,       fontName="Helvetica")

    story = []
    W = A4[0] - 4*cm

    # ── Header ──────────────────────────────────────────────────
    datum = data.get("zeitstempel", "")[:10] if data.get("zeitstempel") else datetime.date.today().strftime("%Y-%m-%d")
    try:
        datum_fmt = datetime.datetime.strptime(datum, "%Y-%m-%d").strftime("%d.%m.%Y")
    except:
        datum_fmt = datum

    anmelde_nr = f"ANM-{datetime.date.today().strftime('%Y')}-{abs(hash(data.get('email',''))  ) % 9000 + 1000}"

    header = Table([[
        Paragraph("Anmeldebestätigung", title_style),
        [Paragraph("Nr.", small_style),
         Paragraph(f"<b><font color='white'>{anmelde_nr}</font></b>", ParagraphStyle("nr", fontSize=11, fontName="Helvetica-Bold", textColor=WHITE, leading=14)),
         Spacer(1,4),
         Paragraph("Datum", small_style),
         Paragraph(f"<b><font color='white'>{datum_fmt}</font></b>", ParagraphStyle("dt", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, leading=14))]
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

    # ── Greeting ─────────────────────────────────────────────────
    vorname  = data.get("vorname", "")
    nachname = data.get("nachname", "")
    story.append(Paragraph(f"Sehr geehrte/r {vorname} {nachname},", bold_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "wir freuen uns über Ihre Anmeldung und bestätigen hiermit Ihre Aufnahme in unsere Musikschule. "
        "Nachfolgend finden Sie eine Übersicht Ihrer Anmeldedaten.",
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

    # ── Schüler ───────────────────────────────────────────────────
    story.append(accent_bar("Angaben zur/zum Schüler/in"))
    story.append(Spacer(1, 4))
    story.append(info_grid([
        ("Vorname",      data.get("vorname", "")),
        ("Nachname",     data.get("nachname", "")),
        ("Geburtsdatum", data.get("geburtsdatum", "")),
        ("Straße / Nr.", data.get("strasse", "")),
        ("PLZ / Ort",    f'{data.get("plz","")}  {data.get("ort","")}'),
        ("Telefon",      data.get("telefon", "")),
        ("E-Mail",       data.get("email", "")),
    ]))
    story.append(Spacer(1, 12))

    # ── Kurs ──────────────────────────────────────────────────────
    story.append(accent_bar("Gebuchter Kurs"))
    story.append(Spacer(1, 4))
    story.append(info_grid([
        ("Kurs", data.get("kurs", "")),
    ]))
    story.append(Spacer(1, 12))

    # ── Bankdaten ─────────────────────────────────────────────────
    story.append(accent_bar("Bankdaten / SEPA-Lastschriftmandat"))
    story.append(Spacer(1, 4))
    story.append(info_grid([
        ("Kontoinhaber", data.get("kontoinhaber", "")),
        ("IBAN",         data.get("iban", "")),
        ("Fälligkeit",   "Monatlich zum 01. des Monats"),
    ]))
    story.append(Spacer(1, 16))

    # ── Hinweise ──────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER))
    story.append(Spacer(1, 8))
    hinweise = [
        ("Probezeit",  "Die ersten zwei Unterrichtseinheiten gelten als unverbindliche Probestunden."),
        ("Kündigung",  "Kündigungen sind mit einer Frist von 4 Wochen zum Monatsende schriftlich einzureichen."),
        ("Kontakt",    "Bei Fragen: info@musikschule-hueckelhoven.de | Tel: 01234 56789"),
    ]
    for titel, text in hinweise:
        story.append(Paragraph(f"<b>{titel}:</b>  {text}", body_style))

    story.append(Spacer(1, 20))

    # ── Unterschrift ──────────────────────────────────────────────
    sig = Table(
        [["____________________________", "____________________________"],
         ["Ort, Datum", "Unterschrift Sorgeberechtigte/r"]],
        colWidths=[8*cm, 8*cm]
    )
    sig.setStyle(TableStyle([
        ("FONTNAME",  (0,1), (-1,1), "Helvetica"),
        ("FONTSIZE",  (0,1), (-1,1), 8),
        ("TEXTCOLOR", (0,1), (-1,1), MUTED),
        ("TOPPADDING",(0,0), (-1,-1), 4),
        ("ALIGN",     (0,0), (-1,-1), "CENTER"),
    ]))
    story.append(sig)

    # ── Footer ────────────────────────────────────────────────────
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7.5)
        y = 1.2*cm
        canvas.drawCentredString(A4[0]/2, y,
            "Musikschule Hückelhoven · info@musikschule-hueckelhoven.de · www.musikschule-hueckelhoven.de")
        canvas.setStrokeColor(ACCENT)
        canvas.setLineWidth(2)
        canvas.line(2*cm, y+12, A4[0]-2*cm, y+12)
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    buffer.seek(0)
    return buffer


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Keine Daten empfangen"}), 400

        pdf_buffer = make_pdf(data)
        vorname  = data.get("vorname", "Anmeldung").replace(" ", "_")
        nachname = data.get("nachname", "").replace(" ", "_")
        filename = f"Anmeldebestaetigung_{vorname}_{nachname}.pdf"

        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Musikschule PDF Generator"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
