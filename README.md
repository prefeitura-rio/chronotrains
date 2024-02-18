# Chronobus

Chronobus is an interactive map that allows comparing how far you can travel by bus before and after subsidizing system in Rio de Janeiro.

![Screen Shot 2022-08-30 at 3 39 18 PM](https://user-images.githubusercontent.com/11202803/187453751-816f9f2b-8cb5-4586-ae40-4bc3b5da2087.png)

## Technology

This is a Next.js application deployed on Vercel. This allows using the Vercel Edge cache to serve the isochrones fast enough to have a smooth experience.

The mapping library is mapbox-gl.

The data is stored on a Postgres database hosted at Supabase.

The pre-processing is a mix between Node.js scripts and SQL queries. It is currenly triggered by hand and processed locally.

## Internationalization

We use `next-i18next` to translate the app into various languages. If you'd like to contribute a language, you can do so by submitting a Pull Request with a new file in `public/locales/[your language]/common.json`, and editing `next-i18next.config.js` to add your locale name.


## How to run 

Spin up the database
```bash
source .env.sample
dc up
```

Setup env vars and migrate database
```bash
npx prisma migrate dev 
```

Serve website
```bash
npm run dev
```


Build isochrones by running `add-geoms.ipynb` notebook and createing a env file with the following packages:
```bash
pip install -r requirements.txt
```
