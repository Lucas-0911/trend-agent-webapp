# Trend Pipeline — Hermes Skills

Khi cài Hermes và copy thư mục `skills/` này vào profile, Hermes sẽ đọc các skill và có thể thực hiện toàn bộ luồng:

**Crawl → Score → Analyze**

## Cài đặt

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
hermes profiles create trend
cp -r skills/* ~/.hermes/profiles/trend/skills/
hermes --profile trend
```

Nói: `chạy trend pipeline`
