# 🎹 Keyboard & Switch Finder

Sistema di raccomandazione intelligente e trasparente per tastiere meccaniche, switch e keycaps.

## 🎯 Caratteristiche

### Tre modalità di ricerca:
- **⚙️ Switch Meccanici**: Trova gli switch perfetti in base a feel, suono, peso e caratteristiche
- **🔤 Keycaps**: Scegli il set ideale per layout, materiale, profilo e stile
- **⌨️ Tastiera Completa**: Trova la tastiera meccanica con tutte le caratteristiche desiderate

### Funzionalità principali:
- ✅ **Questionario guidato step-by-step** - Una domanda per volta con spiegazioni chiare
- 🎯 **Motore di scoring con cosine similarity** - Matching preciso tra preferenze e prodotti
- 📊 **Trasparenza totale** - Ogni punteggio è spiegato con breakdown dettagliato
- 🔍 **Verifica compatibilità** - Controlla pin, layout, PCB orientation e coverage
- 💰 **Gestione budget** - Filtra per budget hard e soft con suggerimenti
- 🌍 **Disponibilità regionale** - Filtra per EU, US, UK, ASIA
- 📥 **Export build sheet** - Esporta i risultati in JSON

### Sistema di scoring avanzato:
- Algoritmo basato su **cosine similarity** tra vettore preferenze e caratteristiche prodotto
- **Pesi personalizzabili** con preset (gaming, typing, silent, premium, budget)
- **Vincoli hard** per requisiti obbligatori (layout ISO-IT, hot-swap 5-pin, silent, etc.)
- **Diversity filtering** per evitare risultati troppo simili
- **Bonus/penalità** per match/mismatch su criteri importanti

## 🚀 Quick Start

### Prerequisiti
- Python 3.8+
- pip

### Installazione

```bash
# Clona il repository
git clone <repository-url>
cd Keyboard-And-Switch-Finder

# Installa le dipendenze
pip install -r requirements.txt

# Avvia l'applicazione
python run.py
```

L'applicazione sarà disponibile su `http://localhost:5000`

### Installazione con virtual environment (consigliato)

```bash
# Crea virtual environment
python -m venv venv

# Attiva virtual environment
# Su Linux/Mac:
source venv/bin/activate
# Su Windows:
venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt

# Avvia
python run.py
```

## 📖 Come funziona

### 1. Selezione modalità
Scegli tra Switch, Keycaps o Tastiera completa in base a cosa stai cercando.

### 2. Questionario dinamico
Rispondi a domande mirate sul tipo di feel, suono, budget, layout, e altre preferenze.
Il sistema salta automaticamente domande irrilevanti in base alle risposte precedenti.

### 3. Analisi e scoring
Il motore:
1. Costruisce un **vettore di preferenze** dalle tue risposte
2. Applica **pesi** per dare priorità a criteri importanti
3. Calcola **cosine similarity** tra le tue preferenze e ogni prodotto
4. Aggiunge **bonus** per match su vincoli hard
5. Applica **penalità** per mismatch forti
6. Filtra per **diversità** per evitare risultati quasi identici

### 4. Risultati con spiegazioni
Visualizzi:
- **Scelta principale** con punteggio e breakdown dettagliato
- **Alternative** con focus differenti (budget, premium, disponibilità)
- **Spiegazione riga-per-riga** di cosa ha contribuito al punteggio
- **Riepilogo trasparente** con tutte le tue risposte e vincoli

### 5. Verifica compatibilità
Controlla la compatibilità tra:
- Board ↔ Switch (pin count, hot-swap)
- Board ↔ Keycaps (layout, ISO enter, bottom row, numpad)
- Keycaps ↔ Switch (north-facing interference, stem fit)

## 🗂️ Struttura del progetto

```
Keyboard-And-Switch-Finder/
├── app/
│   ├── models/           # Modelli dati (Switch, Keycap, Board, Session)
│   ├── engine/           # Motore di scoring e compatibilità
│   ├── questionnaires/   # Questionari dinamici per ogni modalità
│   ├── api/              # API REST con Flask
│   ├── data/             # Database JSON con prodotti
│   ├── templates/        # Template HTML
│   ├── static/           # CSS, JS, audio samples
│   └── main.py           # Entry point Flask
├── config.py             # Configurazione globale
├── requirements.txt      # Dipendenze Python
├── run.py                # Script di avvio
└── README.md
```

## 🔧 Configurazione

Modifica `config.py` per personalizzare:
- Porta e host del server
- Numero di risultati top-N
- Soglia di diversità
- Regioni e lingue supportate
- Percorsi dei dati

### Variabili d'ambiente (opzionali)

```bash
export DEBUG=True
export PORT=5000
export HOST=0.0.0.0
export SECRET_KEY=your-secret-key
```

## 📊 Database prodotti

I prodotti sono in file JSON in `app/data/`:
- `switches.json` - Switch meccanici
- `keycaps.json` - Set di keycaps
- `boards.json` - Tastiere complete

### Aggiungere nuovi prodotti

Modifica i file JSON seguendo lo schema Pydantic nei modelli. Ogni prodotto ha:
- **Identificazione**: id, name, brand
- **Caratteristiche tecniche**: specifiche del tipo di prodotto
- **Availability**: region, stock_status, pricing
- **Metadati**: verified, last_updated, notes

Esempio switch:
```json
{
  "id": "gateron-milky-yellow",
  "name": "Gateron Milky Yellow Pro",
  "brand": "Gateron",
  "feel": "linear",
  "actuation_force": 50,
  "sound_profile": ["thock", "creamy"],
  "factory_lubed": true,
  "price_90": 32.0,
  ...
}
```

## 🎨 Personalizzazione UI

Modifica `app/static/css/style.css` per cambiare:
- Colori (variabili CSS in `:root`)
- Layout e spacing
- Stili dei componenti
- Responsive breakpoints

## 🔬 Algoritmo di scoring

### Formula base:
```
score = cosine_similarity(preferences, product_features) + hard_constraints_bonus
```

### Cosine Similarity:
```
similarity = (A · B) / (||A|| × ||B||)
```
dove A è il vettore preferenze e B il vettore caratteristiche prodotto.

### Hard Constraints:
- **Match esatto**: +0.15
- **Mismatch**: -0.20
- **Range numerico**: bonus/penalità proporzionale alla distanza

### Diversity Filtering:
Prodotti con similarity > (1 - threshold) tra loro vengono filtrati per garantire varietà.

## 🧪 Testing

Per testare l'API:

```bash
# Health check
curl http://localhost:5000/api/health

# Lista switch
curl http://localhost:5000/api/products/switches?limit=5

# Avvia sessione
curl -X POST http://localhost:5000/api/session/start \
  -H "Content-Type: application/json" \
  -d '{"mode": "switch"}'
```

## 🚧 Roadmap

- [ ] Profili utente salvabili
- [ ] Comparatore tra due prodotti
- [ ] Simulatore sonoro con IR convolution
- [ ] Community notes e feedback
- [ ] Integrazione con vendor API per prezzi real-time
- [ ] Supporto per layout custom (40%, ortho, split)
- [ ] Machine learning per migliorare i pesi

## 🤝 Contribuire

1. Fork del repository
2. Crea branch per feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📝 License

Questo progetto è open source per uso educativo e personale.

## 🙏 Credits

Sviluppato con ❤️ per la community delle tastiere meccaniche.

### Fonti e ispirazione:
- [r/MechanicalKeyboards](https://reddit.com/r/MechanicalKeyboards)
- [Geekhack](https://geekhack.org)
- [ThocStock](https://thocstock.com)
- [Keycap Designers](https://keycaplendar.firebaseapp.com)

### Tecnologie utilizzate:
- Flask - Web framework
- Pydantic - Data validation
- NumPy - Calcoli vettoriali
- Vanilla JS - Frontend interattivo

---

**Nota**: I dati dei prodotti sono esempi. Per un'applicazione in produzione, integra API di vendor reali e mantieni i dati aggiornati.
