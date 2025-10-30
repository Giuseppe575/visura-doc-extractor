# 🐳 Deploy con Docker - Guida Completa

## Perché Docker?

Docker ti permette di deployare l'applicazione su **qualsiasi server** con:
- ✅ Privacy totale (dati sul tuo server)
- ✅ Nessun limite di risorse
- ✅ Controllo completo
- ✅ Isolamento e sicurezza
- ✅ Facile scalabilità

---

## 📋 Requisiti

1. **Docker** installato sul server
2. **Docker Compose** (opzionale ma consigliato)
3. Server Linux/Windows/macOS
4. Almeno 1GB RAM, 2GB consigliati

---

## 🚀 OPZIONE 1: Docker Compose (FACILE)

### Passo 1: Installa Docker

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
```bash
brew install docker docker-compose
```

**Windows:**
Scarica [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Passo 2: Clona il Repository

```bash
git clone https://github.com/tuousername/document-extractor.git
cd document-extractor
```

### Passo 3: Build e Avvio

```bash
# Build dell'immagine
docker-compose build

# Avvio del container
docker-compose up -d

# Verifica lo stato
docker-compose ps
```

### Passo 4: Accedi all'App

Apri il browser su:
```
http://localhost:8501
```

O se su server remoto:
```
http://TUO_IP_SERVER:8501
```

**L'app è online! 🎉**

---

## 🔧 OPZIONE 2: Docker Manuale

### Build dell'Immagine

```bash
docker build -t document-extractor .
```

### Run del Container

```bash
docker run -d \
  --name document-extractor \
  -p 8501:8501 \
  --restart unless-stopped \
  document-extractor
```

### Verifica

```bash
# Controlla i container attivi
docker ps

# Vedi i logs
docker logs document-extractor

# Ferma il container
docker stop document-extractor

# Riavvia il container
docker start document-extractor
```

---

## 🌐 Deploy su Server Cloud

### DigitalOcean (Droplet)

1. **Crea Droplet** ($6/mese):
   - Ubuntu 22.04
   - 1GB RAM minimo
   - Datacenter vicino a te

2. **Connetti via SSH:**
```bash
ssh root@TUO_IP
```

3. **Installa Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

4. **Clona e Avvia:**
```bash
git clone https://github.com/tuousername/document-extractor.git
cd document-extractor
docker-compose up -d
```

5. **Configura Firewall:**
```bash
ufw allow 8501/tcp
ufw enable
```

6. **Accedi:** `http://TUO_IP:8501`

### AWS EC2

1. **Lancia EC2 Instance** (t2.micro free tier):
   - Ubuntu Server 22.04
   - Security Group: porta 8501

2. **Connetti e installa Docker:**
```bash
ssh -i chiave.pem ubuntu@TUO_IP
sudo apt update && sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
```

3. **Deploy come sopra**

### Google Cloud Platform

1. **Crea VM Instance** (e2-micro free tier)
2. **Firewall:** Consenti porta 8501
3. **Deploy come DigitalOcean**

---

## 🔒 Configurazione HTTPS (Nginx + Let's Encrypt)

Per produzione, usa HTTPS!

### Passo 1: Installa Nginx

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

### Passo 2: Configura Nginx

Crea `/etc/nginx/sites-available/document-extractor`:

```nginx
server {
    listen 80;
    server_name tuodominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Passo 3: Abilita e Ottieni Certificato

```bash
sudo ln -s /etc/nginx/sites-available/document-extractor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d tuodominio.com
```

Ora l'app è disponibile su: `https://tuodominio.com` 🔒

---

## 📊 Monitoraggio

### Logs in Tempo Reale

```bash
# Segui i logs
docker-compose logs -f

# Solo errori
docker-compose logs -f | grep ERROR

# Ultimi 100 righe
docker-compose logs --tail=100
```

### Uso Risorse

```bash
# Statistiche container
docker stats document-extractor

# Uso disco
docker system df

# Pulizia immagini inutilizzate
docker system prune -a
```

---

## 🔄 Aggiornamenti

### Metodo 1: Pull e Rebuild

```bash
# Ferma il container
docker-compose down

# Pull nuove modifiche
git pull

# Rebuild e riavvia
docker-compose up -d --build
```

### Metodo 2: Script Automatico

Crea `update.sh`:

```bash
#!/bin/bash
echo "Aggiornamento Document Extractor..."
docker-compose down
git pull
docker-compose build
docker-compose up -d
echo "Aggiornamento completato!"
```

Rendi eseguibile:
```bash
chmod +x update.sh
./update.sh
```

---

## 💾 Backup e Persistenza

### Volume per Dati

Modifica `docker-compose.yml`:

```yaml
volumes:
  - ./data:/app/data
  - ./logs:/app/logs
```

### Backup Automatico

Crea script `backup.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz data/ logs/
echo "Backup creato: backup_$DATE.tar.gz"
```

### Cronjob per Backup Giornaliero

```bash
crontab -e
# Aggiungi:
0 2 * * * /path/to/backup.sh
```

---

## 🔐 Sicurezza

### Limitare Accesso per IP

In `docker-compose.yml`:

```yaml
ports:
  - "127.0.0.1:8501:8501"  # Solo localhost
```

Poi usa Nginx come reverse proxy con autenticazione.

### Autenticazione Base con Nginx

```nginx
location / {
    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://localhost:8501;
}
```

Crea password:
```bash
sudo htpasswd -c /etc/nginx/.htpasswd admin
```

---

## 📈 Scalabilità

### Docker Swarm (Multi-container)

```bash
# Inizializza Swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml doc-extractor

# Scala a 3 istanze
docker service scale doc-extractor_document-extractor=3
```

### Kubernetes

Per ambienti enterprise, considera Kubernetes:
- Helm charts
- Auto-scaling
- Load balancing
- Rolling updates

---

## 🐛 Risoluzione Problemi

### Container non si avvia

```bash
# Controlla i logs
docker-compose logs

# Verifica porte
sudo netstat -tulpn | grep 8501

# Rebuild da zero
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Errore Tesseract

Verifica che sia installato nel container:
```bash
docker exec document-extractor tesseract --version
```

### Out of Memory

Aumenta memoria del container in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      memory: 2G
    reservations:
      memory: 1G
```

---

## 💰 Costi Hosting

| Provider | Piano | Costo/Mese | RAM | Note |
|----------|-------|------------|-----|------|
| DigitalOcean | Basic Droplet | $6 | 1GB | Consigliato |
| AWS EC2 | t2.micro | Gratis (1 anno) | 1GB | Free tier |
| Linode | Nanode | $5 | 1GB | Ottimo rapporto qualità/prezzo |
| Hetzner | CX11 | €3.79 | 2GB | Più economico |
| Contabo | VPS S | €4.99 | 8GB | Più potente |

---

## ✅ Checklist Deploy Produzione

- [ ] Docker installato e funzionante
- [ ] App testata in locale
- [ ] Firewall configurato (porta 8501)
- [ ] Nginx installato e configurato
- [ ] HTTPS attivo con Let's Encrypt
- [ ] Backup automatici configurati
- [ ] Monitoring attivo
- [ ] Autenticazione (se necessaria)
- [ ] Log rotation configurata
- [ ] Alert per downtime

---

## 📱 Test Post-Deploy

```bash
# Test disponibilità
curl http://localhost:8501

# Test con file
curl -F "file=@test.pdf" http://localhost:8501

# Load test (opzionale)
ab -n 100 -c 10 http://localhost:8501/
```

---

## 🎯 Confronto: Streamlit Cloud vs Docker

| Feature | Streamlit Cloud | Docker VPS |
|---------|-----------------|------------|
| Costo | Gratis | $5-10/mese |
| Setup | 5 minuti | 30 minuti |
| Privacy | Pubblica | Privata |
| Controllo | Limitato | Totale |
| Risorse | 1GB RAM | Configurabile |
| HTTPS | Incluso | Da configurare |
| Dominio | .streamlit.app | Custom |
| Backup | No | Manuale |

**Usa Streamlit Cloud per**: Demo, test, progetti personali
**Usa Docker per**: Produzione, dati sensibili, custom requirements

---

## 📚 Risorse

- **Docker Docs**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **DigitalOcean Tutorials**: https://www.digitalocean.com/community/tutorials
- **Nginx Config**: https://www.nginx.com/resources/wiki/
- **Let's Encrypt**: https://letsencrypt.org/getting-started/

---

## 🎊 Conclusione

Con Docker hai il **controllo completo** della tua applicazione!

Scegli la soluzione più adatta:
- 🚀 **Veloce e gratis**: Streamlit Cloud
- 🏢 **Professionale**: Docker su VPS
- 🎯 **Entrambe**: Demo su Streamlit, produzione su Docker

**Buon Deploy! 🐳**
