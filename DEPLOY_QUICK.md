# 🚀 Déploiement Rapide - 5 Minutes

## Méthode la plus simple : Render + Vercel

### Étape 1 : Pousser sur GitHub (2 min)

```bash
# Dans le dossier principal
git init
git add .
git commit -m "Ready for deployment"
git branch -M main

# Créer un repo sur github.com puis :
git remote add origin https://github.com/VOTRE_USERNAME/smartresume-analyzer.git
git push -u origin main
```

### Étape 2 : Backend sur Render (2 min)

1. **[render.com](https://render.com)** → Sign Up (gratuit)
2. **New +** → **Web Service**
3. Connecter GitHub → Sélectionner votre repo
4. Configuration :
   ```
   Name: smartresume-backend
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
5. **Environment Variables** :
   ```
   AI_PROVIDER=gemini
   AI_API_KEY=AIzaSyAmv1ESjsIAJ8_Nbi2hPhZJIZ4fE7wm3mU
   AI_MODEL=gemini-2.5-flash
   CORS_ORIGINS=https://votre-app.vercel.app
   ```
6. **Create Web Service**
7. ✅ Backend déployé : `https://smartresume-backend.onrender.com`

### Étape 3 : Frontend sur Vercel (1 min)

1. **[vercel.com](https://vercel.com)** → Sign Up avec GitHub
2. **New Project** → Importer votre repo
3. Configuration :
   ```
   Framework: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```
4. **Environment Variable** :
   ```
   VITE_API_URL=https://smartresume-backend.onrender.com
   ```
5. **Deploy**
6. ✅ Frontend déployé : `https://smartresume-analyzer.vercel.app`

### Étape 4 : Mettre à jour CORS

1. Retournez sur Render
2. Allez dans votre backend → Environment
3. Modifiez `CORS_ORIGINS` avec l'URL Vercel
4. Sauvegardez (redémarrage automatique)

## ✅ C'est fait !

Votre application est maintenant en ligne, gratuite, et accessible mondialement !

---

## Alternative : Railway (Encore plus simple)

1. **[railway.app](https://railway.app)** → Login avec GitHub
2. **New Project** → **Deploy from GitHub**
3. Sélectionner le repo
4. Ajouter les variables d'environnement
5. ✅ Tout est déployé automatiquement !

**Gratuit** : $5 de crédit/mois (suffisant pour petits projets)

---

## 📝 Checklist

- [ ] Code sur GitHub
- [ ] Backend sur Render
- [ ] Frontend sur Vercel
- [ ] Variables d'environnement configurées
- [ ] CORS mis à jour
- [ ] Test de l'application en ligne

**Temps total : ~5-10 minutes**
