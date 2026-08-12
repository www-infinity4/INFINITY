# INFINITY
A complete workup on the ideology behind infinite eternal life.

## Local AI runtime

Start the standard-library runtime with:

```bash
python ai-runtime/server.py
```

Browser access to the loopback runtime is deliberately opt-in. Configure one exact HTTPS
application origin; the wildcard default will never receive a private-network grant:

```bash
INFINITY_AI_ALLOW_ORIGIN=https://your-app.example \
INFINITY_AI_ALLOW_PRIVATE_NETWORK=1 \
python ai-runtime/server.py
```

Modern browsers may also ask the user for local-network permission. The response header is only
one part of that browser security flow; it does not bypass the user's permission choice. Keep the
service bound to loopback unless remote access is intentionally secured.

Run the header contract tests with:

```bash
python ai-runtime/test_server.py
```
