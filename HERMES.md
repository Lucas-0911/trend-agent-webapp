# Trend Agent — Hướng dẫn cho Hermes

## Cài đặt

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
hermes profiles create trend
cp skills/AGENT.md ~/.hermes/profiles/trend/
cp -r skills/trend-pipeline ~/.hermes/profiles/trend/skills/
hermes --profile trend
```

## Sử dụng
Nói: `chạy trend pipeline` hoặc `soi sản phẩm hot hôm nay`

Agent sẽ tự thu thập → chấm điểm → gợi ý video.

## File quan trọng
- skills/AGENT.md — vai trò agent
- skills/trend-pipeline/SKILL.md — quy trình đầy đủ
