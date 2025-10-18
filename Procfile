# web process type for platform-agnostic runners (Heroku-style, Dokku, Railway, etc.)
web: uvicorn cs_fundamentals.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers ${WEB_CONCURRENCY:-2} --timeout-keep-alive 5
