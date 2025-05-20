```bash
npm i -g vercel;
```

```json
{
	"buildCommand": "next build",
	"outputDirectory": ".next",
	"framework": "nextjs"
}
```

```bash
vercel login;
```

```bash
vercel init;
vercel link; ## Associate local folder with vercel project (or create new one)
```

```bash
varcel dev;
vercel; # prompt-based deploy
vercel --prod --confirm; # non-interactive deploy
```