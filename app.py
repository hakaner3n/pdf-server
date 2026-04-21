<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Verbindliche Anmeldung – Musikschule Hückelhoven</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:#f7fafb;font-family:'Source Sans 3',sans-serif;font-size:16px;color:#2c2c2c;line-height:1.6;padding:0 0 60px}

.form-wrap{max-width:640px;margin:0 auto;padding:0 20px}

.form-header{text-align:center;padding:36px 0 28px;border-bottom:1px solid #ccd8da;margin-bottom:28px}
.form-header .icon{width:56px;height:56px;border-radius:50%;background:#e8f4f6;display:flex;align-items:center;justify-content:center;margin:0 auto 16px}
.form-header .school{font-size:12px;font-weight:600;color:#1a5f6a;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:6px}
.form-header h1{font-family:'Playfair Display',serif;font-size:1.7rem;color:#144d57;margin-bottom:6px}
.form-header .sub{font-size:14px;color:#888;margin-bottom:20px}
.trust-row{display:flex;justify-content:center;gap:28px;flex-wrap:wrap}
.trust-item{display:flex;align-items:center;gap:6px;font-size:13px;color:#666}
.trust-item svg{flex-shrink:0}

.section{background:#fff;border:1px solid #ccd8da;border-radius:10px;padding:22px 24px;margin-bottom:16px}
.section-label{font-size:11px;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:14px}

.kurs-option{border:1.5px solid #ccd8da;border-radius:8px;padding:14px 16px;margin-bottom:8px;cursor:pointer;background:#fff;transition:all 0.15s;display:flex;align-items:center;gap:14px;user-select:none}
.kurs-option:last-child{margin-bottom:0}
.kurs-option.selected{border-color:#1a5f6a;background:#e8f4f6}
.kurs-option.fixed{cursor:default}
.radio-dot{width:18px;height:18px;border-radius:50%;border:2px solid #ccd8da;flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:all 0.15s}
.kurs-option.selected .radio-dot{border-color:#1a5f6a;background:#1a5f6a}
.radio-inner{width:6px;height:6px;border-radius:50%;background:white;display:none}
.kurs-option.selected .radio-inner{display:block}
.kurs-info{flex:1}
.kurs-title{font-size:15px;font-weight:600;color:#2c2c2c}
.kurs-option.selected .kurs-title{color:#085041}
.kurs-sub{font-size:13px;color:#888;margin-top:2px}
.kurs-option.selected .kurs-sub{color:#0F6E56}
.kurs-badge{background:#e8f4f6;color:#144d57;font-size:12px;font-weight:600;padding:3px 10px;border-radius:20px;white-space:nowrap;flex-shrink:0}
.kurs-option.selected .kurs-badge{background:#1a5f6a;color:#fff}
.kurs-err{display:none;color:#c0392b;font-size:13px;margin-top:6px}

.field-grid{display:grid;gap:12px;margin-bottom:12px}
.field-grid.cols2{grid-template-columns:1fr 1fr}
.field-grid.cols3{grid-template-columns:2fr 1fr 1fr}
.field-grid.cols1{grid-template-columns:1fr}
.field-grid:last-child{margin-bottom:0}
.field{display:flex;flex-direction:column;gap:4px}
.field label{font-size:12px;font-weight:600;color:#666;text-transform:uppercase;letter-spacing:0.04em}
.field .star{color:#c0392b}
.field input,.field textarea{width:100%;padding:10px 13px;border:1.5px solid #ccd8da;border-radius:6px;font-family:'Source Sans 3',sans-serif;font-size:15px;color:#2c2c2c;background:#fff;outline:none;transition:border-color 0.15s}
.field input:focus,.field textarea:focus{border-color:#1a5f6a;box-shadow:0 0 0 3px rgba(26,95,106,0.1)}
.field input.err,.field textarea.err{border-color:#c0392b}
.field textarea{min-height:70px;resize:vertical}
.field-err{display:none;color:#c0392b;font-size:12px}

.check-wrap{display:flex;align-items:flex-start;gap:12px;padding:13px 15px;border:1.5px solid #ccd8da;border-radius:8px;cursor:pointer;margin-bottom:8px;background:#fff;transition:all 0.15s}
.check-wrap:last-of-type{margin-bottom:0}
.check-wrap:hover{border-color:#1a5f6a;background:#f0f9fa}
.check-wrap.checked{border-color:#1a5f6a;background:#e8f4f6}
.checkmark{width:22px;height:22px;min-width:22px;border:2px solid #ccd8da;border-radius:5px;background:#fff;display:flex;align-items:center;justify-content:center;margin-top:1px;transition:all 0.15s;flex-shrink:0}
.check-wrap.checked .checkmark{border-color:#1a5f6a;background:#1a5f6a}
.checkmark svg{display:none}
.check-wrap.checked .checkmark svg{display:block}
.check-wrap input[type=checkbox]{display:none}
.check-text{font-size:14px;color:#2c2c2c;line-height:1.5}
.check-text a{color:#1a5f6a;font-weight:600}
.check-err{display:none;color:#c0392b;font-size:12px;margin-top:4px}

.quelle-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px}
.quelle-opt{display:flex;align-items:center;gap:8px;padding:9px 12px;border:1.5px solid #ccd8da;border-radius:6px;cursor:pointer;font-size:14px;background:#fff;transition:all 0.15s;user-select:none}
.quelle-opt:hover{border-color:#1a5f6a;background:#f0f9fa}
.quelle-opt.selected{border-color:#1a5f6a;background:#e8f4f6;color:#085041;font-weight:600}
.quelle-dot{width:16px;height:16px;border-radius:50%;border:2px solid #ccd8da;flex-shrink:0;display:flex;align-items:center;justify-content:center}
.quelle-opt.selected .quelle-dot{border-color:#1a5f6a;background:#1a5f6a}
.quelle-inner{width:5px;height:5px;border-radius:50%;background:white;display:none}
.quelle-opt.selected .quelle-inner{display:block}
.quelle-err{display:none;color:#c0392b;font-size:12px;margin-top:6px}

.submit-wrap{text-align:center;margin-top:8px}
.submit-btn{display:inline-block;background:#1a5f6a;color:#fff;border:none;padding:15px 48px;font-family:'Source Sans 3',sans-serif;font-size:16px;font-weight:600;border-radius:7px;cursor:pointer;width:100%;max-width:360px;transition:background 0.15s}
.submit-btn:hover{background:#144d57}
.submit-btn:disabled{background:#aaa;cursor:not-allowed}
.submit-note{font-size:12px;color:#aaa;margin-top:10px}
.spinner{display:none;width:20px;height:20px;border:2px solid rgba(255,255,255,0.4);border-top-color:#fff;border-radius:50%;animation:spin 0.7s linear infinite;margin:0 auto}
@keyframes spin{to{transform:rotate(360deg)}}

.success{display:none;text-align:center;padding:48px 24px;background:#e8f4f6;border-radius:12px;margin-top:24px}
.success h2{font-family:'Playfair Display',serif;color:#144d57;margin-bottom:10px;font-size:1.4rem}
.tick{font-size:3rem;margin-bottom:12px;display:block}

@media(max-width:580px){
  .field-grid.cols2,.field-grid.cols3{grid-template-columns:1fr}
  .trust-row{gap:16px}
  .form-header h1{font-size:1.4rem}
}
</style>
</head>
<body>

<div class="form-wrap">

  <div class="form-header">
    <div class="icon">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1a5f6a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
    </div>
    <p class="school">Musikschule Hückelhoven</p>
    <h1>Verbindliche Anmeldung</h1>
    <p class="sub">Bağlama-Unterricht · Düsseldorf</p>
    <div class="trust-row">
      <span class="trust-item">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#1a5f6a" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
        14 Tage Widerrufsrecht
      </span>
      <span class="trust-item">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#1a5f6a" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
        Kein Vorwissen nötig
      </span>
    </div>
  </div>

  <form id="msfForm" novalidate>

    <div class="section">
      <p class="section-label">1 · Kursstart</p>
      <div class="kurs-option fixed selected" id="kursstart">
        <div class="radio-dot"><div class="radio-inner"></div></div>
        <div class="kurs-info">
          <div class="kurs-title">Sonntag, 03. Mai 2026</div>
          <div class="kurs-sub">13:50–15:10 Uhr · Kirchstr. 20, 40227 Düsseldorf</div>
        </div>
      </div>
    </div>

    <div class="section">
      <p class="section-label">2 · Leihinstrument</p>
      <div class="kurs-option selected" onclick="selectLeih(this,'D\'dorf | 03/05/26 | 13:50-15:10 | ohne Leih | 68')" id="leih1">
        <div class="radio-dot"><div class="radio-inner"></div></div>
        <div class="kurs-info">
          <div class="kurs-title">Ohne Leihinstrument</div>
          <div class="kurs-sub">Du bringst deine eigene Bağlama mit</div>
        </div>
        <div class="kurs-badge">68 € / mtl.</div>
      </div>
      <div class="kurs-option" onclick="selectLeih(this,'D\'dorf | 03/05/26 | 13:50-15:10 | mit Leih | 80')" id="leih2">
        <div class="radio-dot"><div class="radio-inner"></div></div>
        <div class="kurs-info">
          <div class="kurs-title">Mit Leihinstrument</div>
          <div class="kurs-sub">Wir stellen dir eine Bağlama für den Unterricht</div>
        </div>
        <div class="kurs-badge">80 € / mtl.</div>
      </div>
      <span class="kurs-err" id="leihErr">Bitte eine Option auswählen.</span>
      <input type="hidden" name="kurs" id="msfKurs" value="D'dorf | 03/05/26 | 13:50-15:10 | ohne Leih | 68">
    </div>

    <div class="section">
      <p class="section-label">3 · Angaben zur Person</p>
      <div class="field-grid cols2">
        <div class="field">
          <label>Vorname des Schülers <span class="star">*</span></label>
          <input type="text" name="vorname" id="msfVorname" placeholder="Vorname">
          <span class="field-err" id="msfVornameErr">Bitte Vorname eingeben.</span>
        </div>
        <div class="field">
          <label>Familienname <span class="star">*</span></label>
          <input type="text" name="nachname" id="msfNachname" placeholder="Nachname">
          <span class="field-err" id="msfNachnameErr">Bitte Nachname eingeben.</span>
        </div>
      </div>
      <div class="field-grid cols2">
        <div class="field">
          <label>Geburtsdatum <span class="star">*</span></label>
          <input type="date" name="geburtsdatum" id="msfGeburt">
          <span class="field-err" id="msfGeburtErr">Bitte Geburtsdatum eingeben.</span>
        </div>
        <div class="field">
          <label>Telefon <span class="star">*</span></label>
          <input type="text" name="telefon" id="msfTelefon" placeholder="01234 56789">
          <span class="field-err" id="msfTelefonErr">Bitte Telefonnummer eingeben.</span>
        </div>
      </div>
      <div class="field-grid cols1">
        <div class="field">
          <label>E-Mail <span class="star">*</span></label>
          <input type="email" name="email" id="msfEmail" placeholder="deine@email.de">
          <span class="field-err" id="msfEmailErr">Bitte gültige E-Mail eingeben.</span>
        </div>
      </div>
      <div class="field-grid cols1">
        <div class="field">
          <label>E-Mail wiederholen <span class="star">*</span></label>
          <input type="email" name="email2" id="msfEmail2" placeholder="deine@email.de">
          <span class="field-err" id="msfEmail2Err">E-Mail-Adressen stimmen nicht überein.</span>
        </div>
      </div>
      <div class="field-grid cols3">
        <div class="field">
          <label>Straße & Hausnummer <span class="star">*</span></label>
          <input type="text" name="strasse" id="msfStrasse" placeholder="Musterstraße 1">
          <span class="field-err" id="msfStrasseErr">Bitte Adresse eingeben.</span>
        </div>
        <div class="field">
          <label>PLZ <span class="star">*</span></label>
          <input type="text" name="plz" id="msfPlz" placeholder="12345">
          <span class="field-err" id="msfPlzErr">Bitte PLZ eingeben.</span>
        </div>
        <div class="field">
          <label>Ort <span class="star">*</span></label>
          <input type="text" name="ort" id="msfOrt" placeholder="Musterstadt">
          <span class="field-err" id="msfOrtErr">Bitte Ort eingeben.</span>
        </div>
      </div>
      <div class="field-grid cols1" style="margin-top:12px">
        <div class="field">
          <label>Erziehungsberechtigter (falls unter 18)</label>
          <textarea name="erziehungsber" placeholder="Vor- und Nachname eines Erziehungsberechtigten"></textarea>
        </div>
      </div>
    </div>

    <div class="section">
      <p class="section-label">4 · SEPA-Lastschriftmandat</p>
      <div class="field-grid cols2">
        <div class="field">
          <label>Kontoinhaber <span class="star">*</span></label>
          <input type="text" name="kontoinhaber" id="msfKonto" placeholder="Vor- und Nachname">
          <span class="field-err" id="msfKontoErr">Bitte Kontoinhaber eingeben.</span>
        </div>
        <div class="field">
          <label>IBAN <span class="star">*</span></label>
          <input type="text" name="iban" id="msfIban" placeholder="DE00 0000 0000 0000 0000 00">
          <span class="field-err" id="msfIbanErr">Bitte IBAN eingeben.</span>
        </div>
      </div>
      <div style="margin-top:14px">
        <label class="check-wrap" onclick="msfToggleCheck(this)">
          <input type="checkbox" name="sepa" id="msfSepa">
          <div class="checkmark"><svg width="13" height="13" viewBox="0 0 14 14" fill="none"><polyline points="2,7 5.5,10.5 12,3" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <span class="check-text">Hiermit ermächtige ich die Musikschule Hückelhoven, den monatlich fälligen Betrag per SEPA-Lastschrift einzuziehen. Gläubiger-ID: <strong>DE64ZZZ00002060164</strong></span>
        </label>
        <span class="check-err" id="msfSepaErr">Bitte SEPA-Mandat bestätigen.</span>
        <label class="check-wrap" onclick="msfToggleCheck(this)" style="margin-top:8px">
          <input type="checkbox" name="agb" id="msfAgb">
          <div class="checkmark"><svg width="13" height="13" viewBox="0 0 14 14" fill="none"><polyline points="2,7 5.5,10.5 12,3" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <span class="check-text">Ich akzeptiere die <a href="https://www.musikschule-hueckelhoven.de/j/shop/terms" target="_blank">AGB</a> sowie die <a href="https://www.musikschule-hueckelhoven.de/j/shop/withdrawal" target="_blank">Widerrufsbelehrung</a> der Musikschule.</span>
        </label>
        <span class="check-err" id="msfAgbErr">Bitte AGB & Widerrufsbelehrung akzeptieren.</span>
      </div>
    </div>

    <div class="section">
      <p class="section-label">5 · Wie bist Du auf uns aufmerksam geworden? <span class="star">*</span></p>
      <div class="quelle-grid">
        <div class="quelle-opt" onclick="selectQuelle(this,'YouTube')"><div class="quelle-dot"><div class="quelle-inner"></div></div>YouTube</div>
        <div class="quelle-opt" onclick="selectQuelle(this,'Google')"><div class="quelle-dot"><div class="quelle-inner"></div></div>Google</div>
        <div class="quelle-opt" onclick="selectQuelle(this,'TikTok')"><div class="quelle-dot"><div class="quelle-inner"></div></div>TikTok</div>
        <div class="quelle-opt" onclick="selectQuelle(this,'Facebook')"><div class="quelle-dot"><div class="quelle-inner"></div></div>Facebook</div>
        <div class="quelle-opt" onclick="selectQuelle(this,'Instagram')"><div class="quelle-dot"><div class="quelle-inner"></div></div>Instagram</div>
        <div class="quelle-opt" onclick="selectQuelle(this,'Ebay Kleinanzeigen')"><div class="quelle-dot"><div class="quelle-inner"></div></div>Ebay Kleinanzeigen</div>
        <div class="quelle-opt" onclick="selectQuelle(this,'Sonstige')"><div class="quelle-dot"><div class="quelle-inner"></div></div>Sonstige</div>
      </div>
      <span class="quelle-err" id="msfQuelleErr">Bitte eine Option auswählen.</span>
      <input type="hidden" name="quelle" id="msfQuelle" value="">
    </div>

    <div class="submit-wrap">
      <p style="font-size:12px;color:#aaa;margin-bottom:12px">Es gilt unsere <a href="#" style="color:#1a5f6a">Datenschutzerklärung</a> · SSL-verschlüsselt</p>
      <button type="submit" class="submit-btn" id="msfBtn">
        <span id="msfBtnTxt">Anmeldung absenden</span>
        <div class="spinner" id="msfSpinner"></div>
      </button>
    </div>

  </form>

  <div class="success" id="msfSuccess">
    <span class="tick">&#10003;</span>
    <h2>Vielen Dank für Deine Anmeldung!</h2>
    <p>Du erhältst in Kürze eine Bestätigungs-E-Mail mit allen Unterlagen.</p>
  </div>

</div>

<script>
var WEBHOOK = 'https://hook.eu1.make.com/ncu8n26ptg7oq3a7hy82hfah68r828zd';

function selectLeih(el, val) {
  document.querySelectorAll('#leih1,#leih2').forEach(function(o){ o.classList.remove('selected'); });
  el.classList.add('selected');
  document.getElementById('msfKurs').value = val;
}

function selectQuelle(el, val) {
  document.querySelectorAll('.quelle-opt').forEach(function(o){ o.classList.remove('selected'); });
  el.classList.add('selected');
  document.getElementById('msfQuelle').value = val;
}

function msfToggleCheck(label) {
  var cb = label.querySelector('input[type=checkbox]');
  cb.checked = !cb.checked;
  label.classList.toggle('checked', cb.checked);
}

function showErr(id, show) {
  var el = document.getElementById(id);
  if(el) el.style.display = show ? 'block' : 'none';
}

function fieldErr(id, errId, show) {
  var inp = document.getElementById(id);
  if(inp){ if(show) inp.classList.add('err'); else inp.classList.remove('err'); }
  showErr(errId, show);
}

function validate() {
  var ok = true;

  var fields = [
    ['msfVorname','msfVornameErr'],
    ['msfNachname','msfNachnameErr'],
    ['msfGeburt','msfGeburtErr'],
    ['msfTelefon','msfTelefonErr'],
    ['msfStrasse','msfStrasseErr'],
    ['msfPlz','msfPlzErr'],
    ['msfOrt','msfOrtErr'],
    ['msfKonto','msfKontoErr'],
    ['msfIban','msfIbanErr'],
  ];
  fields.forEach(function(f){
    var empty = !document.getElementById(f[0]).value.trim();
    fieldErr(f[0], f[1], empty);
    if(empty) ok = false;
  });

  var em = document.getElementById('msfEmail').value.trim();
  var em2 = document.getElementById('msfEmail2').value.trim();
  var emOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em);
  fieldErr('msfEmail','msfEmailErr',!emOk); if(!emOk) ok=false;
  fieldErr('msfEmail2','msfEmail2Err',em!==em2); if(em!==em2) ok=false;

  var sepa = document.getElementById('msfSepa').checked;
  showErr('msfSepaErr',!sepa); if(!sepa) ok=false;

  var agb = document.getElementById('msfAgb').checked;
  showErr('msfAgbErr',!agb); if(!agb) ok=false;

  var quelle = document.getElementById('msfQuelle').value;
  showErr('msfQuelleErr',!quelle); if(!quelle) ok=false;

  return ok;
}

document.getElementById('msfForm').addEventListener('submit', async function(e){
  e.preventDefault();
  if(!validate()) return;

  var btn  = document.getElementById('msfBtn');
  var txt  = document.getElementById('msfBtnTxt');
  var spin = document.getElementById('msfSpinner');
  btn.disabled=true; txt.style.display='none'; spin.style.display='block';

  var data = {
    kurs:          document.getElementById('msfKurs').value,
    vorname:       document.getElementById('msfVorname').value.trim(),
    nachname:      document.getElementById('msfNachname').value.trim(),
    geburtsdatum:  document.getElementById('msfGeburt').value,
    strasse:       document.getElementById('msfStrasse').value.trim(),
    plz:           document.getElementById('msfPlz').value.trim(),
    ort:           document.getElementById('msfOrt').value.trim(),
    erziehungsber: document.querySelector('textarea[name="erziehungsber"]').value.trim(),
    telefon:       document.getElementById('msfTelefon').value.trim(),
    email:         document.getElementById('msfEmail').value.trim(),
    kontoinhaber:  document.getElementById('msfKonto').value.trim(),
    iban:          document.getElementById('msfIban').value.trim(),
    quelle:        document.getElementById('msfQuelle').value,
    zeitstempel:   new Date().toISOString()
  };

  try {
    await fetch(WEBHOOK, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data), mode:'no-cors'});
    document.getElementById('msfForm').style.display='none';
    document.getElementById('msfSuccess').style.display='block';
  } catch(err) {
    btn.disabled=false; txt.style.display='block'; spin.style.display='none';
    alert('Fehler beim Absenden. Bitte versuche es erneut oder kontaktiere uns direkt.');
  }
});
</script>

</body>
</html>
