# 🚀 Guide de Déploiement Gratuit

## Option 1 : Render.com (Recommandé - Tout-en-un)

### ✅ Avantages
- **100% Gratuit** pour les petits projets
- Backend + Frontend sur la même plateforme
- Déploiement automatique depuis GitHub
- Support natif de Python/FastAPI

### 📝 Étapes

#### 1. Préparer le code
```bash
# Créer un compte GitHub si vous n'en avez pas
# Pusher votre code sur GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
git push -u origin main
```

#### 2. Déployer le Backend sur Render

1. Allez sur [render.com](https://render.com)
2. Créez un compte (gratuit)
3. Cliquez sur **"New +"** → **"Web Service"**
4. Connectez votre repo GitHub
5. Configuration :
   - **Name** : `smartresume-backend`
   - **Region** : Frankfurt (Europe)
   - **Branch** : `main`
   - **Root Directory** : `backend`
   - **Runtime** : Python 3
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type** : Free

6. Variables d'environnement :
   - Cliquez sur **"Advanced"**
   - Ajoutez :
     ```
     AI_PROVIDER=gemini
     AI_API_KEY=AIzaSyAmv1ESjsIAJ8_Nbi2hPhZJIZ4fE7wm3mU
     AI_MODEL=gemini-2.5-flash
     CORS_ORIGINS=https://VOTRE-FRONTEND.vercel.app
     ```

7. Cliquez sur **"Create Web Service"**
8. Notez l'URL : `https://smartresume-backend.onrender.com`

#### 3. Déployer le Frontend sur Vercel

1. Allez sur [vercel.com](https://vercel.com)
2. Connectez-vous avec GitHub
3. Cliquez sur **"Add New"** → **"Project"**
4. Sélectionnez votre repo
5. Configuration :
   - **Framework Preset** : Vite
   - **Root Directory** : `frontend`
   - **Build Command** : `npm run build`
   - **Output Directory** : `dist`

6. Variables d'environnement :
   - Ajoutez : `VITE_API_URL=https://smartresume-backend.onrender.com`

7. Cliquez sur **"Deploy"**
8. Votre app sera sur : `https://VOTRE-APP.vercel.app`

---

## Option 2 : Railway.app (Alternative)

### Backend + Frontend
1. Allez sur [railway.app](https://railway.app)
2. **"New Project"** → **"Deploy from GitHub repo"**
3. Sélectionnez votre repo
4. Railway détectera automatiquement Python et Node.js
5. Configurez les variables d'environnement
6. Déployé automatiquement !

**Crédits gratuits** : $5/mois (suffisant pour petits projets)

---

## Option 3 : Fly.io (Backend) + Vercel (Frontend)

### Backend sur Fly.io
```bash
# Installer Fly CLI
curl -L https://fly.io/install.sh | sh

# Dans le dossier backend
cd backend
fly launch
fly secrets set AI_API_KEY=AIzaSyAmv1ESjsIAJ8_Nbi2hPhZJIZ4fE7wm3mU
fly deploy
```

**Gratuit** : 3 VMs partagées + 3GB stockage

---

## Option 4 : PythonAnywhere (Backend seulement)

### Limitations
- ⚠️ Pas de WebSockets
- ⚠️ Limité à 100k requêtes/jour
- ✅ Gratuit à vie

### Configuration
1. [pythonanywhere.com](https://www.pythonanywhere.com)
2. Créer un compte gratuit
3. Upload votre code
4. Configurer WSGI

---

## 📊 Comparaison

| Plateforme | Backend | Frontend | Gratuit | Recommandé |
|------------|---------|----------|---------|------------|
| **Render** | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **Vercel** | ❌ | ✅ | ✅ | ⭐⭐⭐⭐ |
| **Railway** | ✅ | ✅ | $5/mois | ⭐⭐⭐⭐ |
| **Fly.io** | ✅ | ❌ | ✅ | ⭐⭐⭐ |
| **PythonAnywhere** | ✅ | ❌ | ✅ | ⭐⭐ |

---

## 🎯 Ma Recommandation

**Pour votre projet** :
1. **Backend** → Render.com (gratuit, facile)
2. **Frontend** → Vercel (gratuit, ultra-rapide)

**Temps total** : 15-20 minutes

---

## ⚡ Déploiement rapide avec les fichiers de configuration

J'ai créé les fichiers nécessaires :
- `render.yaml` - Configuration Render
- `vercel.json` - Configuration Vercel
- `.dockerignore` - Pour optimiser

Suivez simplement les étapes ci-dessus !
